from app.ingestion.validator import validate_rows
import pytest
from app.ingestion.validator import validate_rows

BASE = {
    "asset": {
        "Transaction_ID": "AST-000001", "Entity": "IBC UK", "Location": "London",
        "Customer_ID": "CUS-00001", "Loan_Amount": "1000000", "Currency": "GBP",
        "Transaction_Date": "2024-01-01", "Maturity_Date": "2026-01-01",
        "Interest_Rate_Pct": "5", "Market_Interest_Rate_Pct": "4.5",
        "Loan_Type": "Loan-Type-A", "Customer_Segment": "Corporate", "Client_Rating": "3",
    },
    "liability": {
        "Transaction_ID": "LIA-000001", "Entity": "IBC USA", "Location": "New York",
        "Customer_ID": "CUS-00001", "Amount": "500000", "Currency": "USD",
        "Transaction_Date": "2024-01-01", "Maturity_Date": "2026-01-01",
        "Interest_Rate_Pct": "2", "Market_Interest_Rate_Pct": "3",
        "Product_Type": "Product-A", "Customer_Segment": "Retail", "Client_Rating": "2",
    },
    "historical": {
        "Transaction_ID": "LIA-000001", "Entity": "IBC USA", "Type": "Liability",
        "Location": "New York", "Transaction_Date": "2024-09-17",
        "Customer_ID": "CUS-00001", "Customer_Segment": "Institutional",
        "Client_Rating": "2", "Amount": "3408000", "Currency": "EUR",
        "Interest_Rate_Pct": "2.35", "Market_Interest_Rate_Pct": "3.5",
        "Product_Type": "Product-B", "Contractual_Maturity_Date": "2027-02-05",
        "Actual_Closure_Date": "2025-09-15",
    },
}


def run(sheet, **changes):
    row = {**BASE[sheet], **changes}
    valid, errors = validate_rows(sheet, [(2, row)])
    return valid, {e["rule"] for e in errors}


@pytest.mark.parametrize("sheet", BASE)
def test_base_row_is_valid(sheet):
    valid, rules = run(sheet)
    assert len(valid) == 1 and not rules


BAD = [
    ("asset", "Transaction_ID", "LIA-000001", "R2"),
    ("asset", "Transaction_ID", "AST-1x", "R2"),
    ("asset", "Customer_ID", "C-1", "R3"),
    ("asset", "Entity", "HBC HK", "R4"),
    ("asset", "Location", "Mumbai", "R5"),
    ("asset", "Location", "Paris", "R6"),
    ("asset", "Loan_Amount", "0", "R7"),
    ("asset", "Loan_Amount", "-5", "R7"),
    ("asset", "Loan_Amount", "abc", "R7"),
    ("asset", "Currency", "US", "R8"),
    ("asset", "Currency", "", "R1"),
    ("asset", "Transaction_Date", "32/13/2026", "R9"),
    ("asset", "Transaction_Date", "2024-1-1", "R9"),
    ("asset", "Maturity_Date", "2023-01-01", "R10"),
    ("asset", "Interest_Rate_Pct", "101", "R11"),
    ("asset", "Market_Interest_Rate_Pct", "-1", "R11"),
    ("asset", "Loan_Type", "Product-A", "R12"),
    ("asset", "Customer_Segment", "VIP", "R13"),
    ("asset", "Client_Rating", "6", "R14"),
    ("asset", "Client_Rating", "2.5", "R14"),
    ("liability", "Transaction_ID", "AST-000001", "R2"),
    ("liability", "Product_Type", "Loan-Type-A", "R12"),
    ("historical", "Type", "Deposit", "R16"),
    ("historical", "Type", "Asset", "R16"),            # LIA- id but Type=Asset
    ("historical", "Actual_Closure_Date", "bad", "R9"),
    ("historical", "Actual_Closure_Date", "2020-01-01", "R10"),
]


@pytest.mark.parametrize("sheet,col,val,rule", BAD)
def test_bad_value_is_rejected(sheet, col, val, rule):
    valid, rules = run(sheet, **{col: val})
    assert rule in rules
    assert not valid


def test_blank_closure_date_means_open_loan():
    valid, rules = run("historical", Actual_Closure_Date="")
    assert valid and not rules


def test_type_is_case_insensitive():
    valid, _ = run("historical", Type="liability")
    assert valid


def test_whole_row_duplicate_and_duplicate_id():
    row = BASE["asset"]
    valid, errors = validate_rows("asset", [(2, row), (3, dict(row))])
    assert len(valid) == 1
    assert {e["rule"] for e in errors if e["row"] == 3} == {"R2", "R15"}


def test_all_failures_on_a_row_are_collected():
    _, rules = run("asset", Currency="US", Client_Rating="9", Entity="HBC HK")
    assert {"R8", "R14", "R4"} <= rules