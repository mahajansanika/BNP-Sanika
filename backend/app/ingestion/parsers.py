# parsers.py

from pathlib import Path
import pandas as pd

from .rules import SHEETS


class HeaderError(Exception):
    """Raised when expected columns are missing (rule R0: reject whole file)."""
    def __init__(self, missing, extra):
        self.missing, self.extra = missing, extra
        super().__init__(f"Missing columns: {missing}; unexpected columns: {extra}")


def _clean(v: str) -> str:
    v = v.strip()
    # Excel often turns dates into '2026-01-05 00:00:00'
    if len(v) == 19 and v.endswith(" 00:00:00"):
        v = v[:10]
    return v


def read_sheet(path, sheet: str) -> list[tuple[int, dict]]:
    path = Path(path)
    if path.suffix.lower() == ".csv":
        df = pd.read_csv(path, dtype=str, keep_default_na=False)
    elif path.suffix.lower() in (".xlsx", ".xls"):
        df = pd.read_excel(path, dtype=str, keep_default_na=False)
    else:
        raise ValueError(f"Unsupported file type: {path.suffix}")

    df.columns = [c.strip() for c in df.columns]
    expected = SHEETS[sheet]["headers"]
    missing = [c for c in expected if c not in df.columns]
    extra = [c for c in df.columns if c not in expected]
    if missing or extra:
        raise HeaderError(missing, extra)

    rows = []
    for i, rec in enumerate(df[expected].to_dict("records")):
        # spreadsheet row number: header is row 1, first data row is 2
        rows.append((i + 2, {k: _clean(str(v)) for k, v in rec.items()}))
    return rows