# cashflow.py
from datetime import datetime
from .rules import SHEETS, DATE_FMT

DAY_COUNT = 365


def _d(s):
    return datetime.strptime(s, DATE_FMT).date()


def add_cashflows(sheet, rows):
    """rows: valid (row_number, dict) pairs from the validator.
    Returns dicts with the original columns plus normalized principal/tenor/interest/cashflow."""
    cfg = SHEETS[sheet]
    out = []
    for rownum, r in rows:
        principal = float(r[cfg["amount"]])
        rate = float(r["Interest_Rate_Pct"])
        tenor_days = (_d(r[cfg["maturity"]]) - _d(r["Transaction_Date"])).days
        interest = principal * rate / 100 * tenor_days / DAY_COUNT
        out.append({
            **r,
            "row": rownum,
            "principal": principal,            # one name, regardless of sheet
            "tenor_days": tenor_days,
            "interest_amount": round(interest, 2),
            "cashflow": round(principal + interest, 2),
        })
    return out