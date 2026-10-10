# validator.py
import math
import re
from datetime import datetime

from .rules import (
    SHEETS, ENTITY_LOCATION, ENTITIES, LOCATIONS, CURRENCIES, SEGMENTS,
    CUSTOMER_ID_RE, ID_RE, DATE_FMT,
)

DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def _date(v):
    if not DATE_RE.match(v):
        return None
    try:
        return datetime.strptime(v, DATE_FMT).date()
    except ValueError:
        return None


def _num(v):
    try:
        x = float(v)
    except ValueError:
        return None
    return x if math.isfinite(x) else None


def validate_rows(sheet, rows):
    cfg = SHEETS[sheet]
    optional = cfg.get("optional", set())
    amt_col, mat_col, prod_col = cfg["amount"], cfg["maturity"], cfg["product"]
    seen_ids, seen_rows = set(), set()
    valid, errors = [], []

    for rownum, r in rows:
        errs = []

        def add(col, rule, msg):
            errs.append({"row": rownum, "column": col, "value": r.get(col, ""),
                         "rule": rule, "message": msg})

        # R1: mandatory fields
        blank = {c for c in cfg["headers"] if c not in optional and r[c] == ""}
        for c in blank:
            add(c, "R1", "Mandatory field is empty")

        def ok(c):  # only run further checks on non-blank fields
            return c not in blank

        # R2: transaction id format + uniqueness
        tid = r["Transaction_ID"]
        if ok("Transaction_ID"):
            if not ID_RE[sheet].match(tid):
                add("Transaction_ID", "R2", "Invalid ID format")
            elif tid in seen_ids:
                add("Transaction_ID", "R2", "Duplicate Transaction_ID")
            else:
                seen_ids.add(tid)

        # R3: customer id
        if ok("Customer_ID") and not CUSTOMER_ID_RE.match(r["Customer_ID"]):
            add("Customer_ID", "R3", "Invalid Customer_ID format")

        # R4-R6: entity, location, pair
        ent_ok = ok("Entity") and r["Entity"] in ENTITIES
        loc_ok = ok("Location") and r["Location"] in LOCATIONS
        if ok("Entity") and not ent_ok:
            add("Entity", "R4", "Unknown entity")
        if ok("Location") and not loc_ok:
            add("Location", "R5", "Unknown location")
        if ent_ok and loc_ok and ENTITY_LOCATION[r["Entity"]] != r["Location"]:
            add("Location", "R6", f"Entity {r['Entity']} does not belong in {r['Location']}")

        # R7: amount
        if ok(amt_col):
            a = _num(r[amt_col])
            if a is None or a <= 0:
                add(amt_col, "R7", "Amount must be a number > 0")

        # R8: currency
        if ok("Currency") and r["Currency"] not in CURRENCIES:
            add("Currency", "R8", "Unsupported currency")

        # R9 / R10: dates
        tdate = mdate = None
        if ok("Transaction_Date"):
            tdate = _date(r["Transaction_Date"])
            if tdate is None:
                add("Transaction_Date", "R9", "Not a valid YYYY-MM-DD date")
        if ok(mat_col):
            mdate = _date(r[mat_col])
            if mdate is None:
                add(mat_col, "R9", "Not a valid YYYY-MM-DD date")
        if tdate and mdate and mdate < tdate:
            add(mat_col, "R10", "Maturity is before transaction date")
        if "Actual_Closure_Date" in optional and r["Actual_Closure_Date"] != "":
            cdate = _date(r["Actual_Closure_Date"])
            if cdate is None:
                add("Actual_Closure_Date", "R9", "Not a valid YYYY-MM-DD date")
            elif tdate and cdate < tdate:
                add("Actual_Closure_Date", "R10", "Closure is before transaction date")

        # R11: rates
        for c in ("Interest_Rate_Pct", "Market_Interest_Rate_Pct"):
            if ok(c):
                x = _num(r[c])
                if x is None or not (0 <= x <= 100):
                    add(c, "R11", "Rate must be a number between 0 and 100")

        # R12-R14: product, segment, rating
        if ok(prod_col) and r[prod_col] not in cfg["product_set"]:
            add(prod_col, "R12", "Unknown product type")
        if ok("Customer_Segment") and r["Customer_Segment"] not in SEGMENTS:
            add("Customer_Segment", "R13", "Unknown segment")
        if ok("Client_Rating") and not (r["Client_Rating"].isdigit() and 1 <= int(r["Client_Rating"]) <= 5):
            add("Client_Rating", "R14", "Rating must be an integer 1-5")

        # R16: historical Type, and ID prefix must agree with it
        if sheet == "historical" and ok("Type"):
            t = r["Type"].lower()
            if t not in cfg["types"]:
                add("Type", "R16", "Type must be Asset or Liability")
            elif tid and not tid.startswith("AST-" if t == "asset" else "LIA-"):
                add("Type", "R16", "Type does not match Transaction_ID prefix")

        # R15: exact duplicate row
        key = tuple(r[c] for c in cfg["headers"])
        if key in seen_rows:
            add("Transaction_ID", "R15", "Exact duplicate of an earlier row")
        seen_rows.add(key)

        if errs:
            errors.extend(errs)
        else:
            valid.append((rownum, r))

    return valid, errors