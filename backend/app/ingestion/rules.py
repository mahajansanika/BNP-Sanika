# rules.py — single source of truth for ingestion validation constants.
import re

ENTITY_LOCATION = {
    "IBC HongKong": "Hong Kong",
    "IBC USA": "New York",
    "IBC UK": "London",
    "IBC Singapore": "Singapore",
    "IBC SA": "Paris",
}
ENTITIES = set(ENTITY_LOCATION)
LOCATIONS = set(ENTITY_LOCATION.values())
CURRENCIES = {"USD", "EUR", "GBP", "SGD", "HKD"}
SEGMENTS = {"Retail", "Corporate", "SME", "Institutional"}
RATINGS = {1, 2, 3, 4, 5}

LOAN_TYPES = {f"Loan-Type-{c}" for c in "ABCDE"}
PRODUCT_TYPES = {f"Product-{c}" for c in "ABCDE"}

CUSTOMER_ID_RE = re.compile(r"^CUS-\d+$")
ID_RE = {
    "asset": re.compile(r"^AST-\d+$"),
    "liability": re.compile(r"^LIA-\d+$"),
    "historical": re.compile(r"^(AST|LIA)-\d+$"),
}
DATE_FMT = "%Y-%m-%d"

# Per-sheet config: expected headers + the column map for the 3 differing concepts.
SHEETS = {
    "asset": {
        "headers": [
            "Transaction_ID", "Entity", "Location", "Customer_ID", "Loan_Amount",
            "Currency", "Transaction_Date", "Maturity_Date", "Interest_Rate_Pct",
            "Market_Interest_Rate_Pct", "Loan_Type", "Customer_Segment", "Client_Rating",
        ],
        "amount": "Loan_Amount",
        "maturity": "Maturity_Date",
        "product": "Loan_Type",
        "product_set": LOAN_TYPES,
    },
    "liability": {
        "headers": [
            "Transaction_ID", "Entity", "Location", "Customer_ID", "Amount",
            "Currency", "Transaction_Date", "Maturity_Date", "Interest_Rate_Pct",
            "Market_Interest_Rate_Pct", "Product_Type", "Customer_Segment", "Client_Rating",
        ],
        "amount": "Amount",
        "maturity": "Maturity_Date",
        "product": "Product_Type",
        "product_set": PRODUCT_TYPES,
    },
    "historical": {
        "headers": [
            "Transaction_ID", "Entity", "Type", "Location", "Transaction_Date",
            "Customer_ID", "Customer_Segment", "Client_Rating", "Amount", "Currency",
            "Interest_Rate_Pct", "Market_Interest_Rate_Pct", "Product_Type",
            "Contractual_Maturity_Date", "Actual_Closure_Date",
        ],
        "amount": "Amount",
        "maturity": "Contractual_Maturity_Date",
        "product": "Product_Type",
        "product_set": LOAN_TYPES | PRODUCT_TYPES,
        "optional": {"Actual_Closure_Date"},
        "types": {"asset", "liability"},  # compare after .lower()
    },
}