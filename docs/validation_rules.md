# Ingestion validation rules (Dev 2)

Three input sheets are validated row by row. A row that fails any rule is
rejected and reported; valid rows continue to the cash-flow step. R0 rejects the
whole file.

## Sheets and column map

| Concept | Asset book | Liability book | Historical log |
| --- | --- | --- | --- |
| Amount | `Loan_Amount` | `Amount` | `Amount` |
| Maturity | `Maturity_Date` | `Maturity_Date` | `Contractual_Maturity_Date` |
| Product | `Loan_Type` (Loan-Type-A..E) | `Product_Type` (Product-A..E) | `Product_Type` (either set) |
| ID prefix | `AST-` | `LIA-` | `AST-` or `LIA-` |
| Extra columns | none | none | `Type`, `Actual_Closure_Date` (blank = still open) |

## Rules

| # | Check | Column(s) |
| --- | --- | --- |
| R0 | All expected headers present and no extra columns, else reject the whole file | all |
| R1 | Not blank (after trimming), except `Actual_Closure_Date` | all |
| R2 | Matches the sheet's ID pattern and is unique in the file | `Transaction_ID` |
| R3 | Matches `CUS-<n>` | `Customer_ID` |
| R4 | One of IBC HongKong, IBC USA, IBC UK, IBC Singapore, IBC SA | `Entity` |
| R5 | One of Hong Kong, New York, London, Singapore, Paris | `Location` |
| R6 | Entity and location pair valid (HongKong-Hong Kong, USA-New York, UK-London, Singapore-Singapore, SA-Paris) | `Entity` + `Location` |
| R7 | Number greater than 0 | amount column |
| R8 | One of USD, EUR, GBP, SGD, HKD | `Currency` |
| R9 | Real date in YYYY-MM-DD | `Transaction_Date`, maturity, `Actual_Closure_Date` if present |
| R10 | Maturity on or after transaction date. Closure on or after transaction date | dates |
| R11 | Number from 0 to 100 | `Interest_Rate_Pct`, `Market_Interest_Rate_Pct` |
| R12 | In the sheet's product set | product column |
| R13 | One of Retail, Corporate, SME, Institutional | `Customer_Segment` |
| R14 | Integer from 1 to 5 | `Client_Rating` |
| R15 | Row is not an exact duplicate of an earlier row | whole row |
| R16 | `Type` is Asset or Liability (case-insensitive) and matches the ID prefix (historical only) | `Type` |

All failures on a row are collected. Each error reports row number, column,
value, rule and message. Row numbers match the spreadsheet (header is row 1).

## Frozen conventions

- Whitespace is trimmed on every cell before checking.
- Interest is simple, paid at maturity, actual/365:
  `interest_amount = principal x rate / 100 x tenor_days / 365`
- `cashflow = principal + interest_amount`, in the original currency (no FX).
- Rate used is `Interest_Rate_Pct`.

## Columns added after validation

`principal` (the amount column, same name on every sheet), `tenor_days`,
`interest_amount`, `cashflow`, `row` (source row number).

## Known bad rows in the supplied files

| Sheet | Row | Problem | Rule |
| --- | --- | --- | --- |
| Asset | 755 | Currency `US` | R8 |
| Asset | 756 | Maturity before transaction date | R10 |
| Liability | 1105 | Currency `EURO` | R8 |
| Historical | 2389 | Currency `US` | R8 |
| Historical | 4778 | Type `Deposit` | R16 |
| Historical | 7166 | Amount `0` | R7 |
| Historical | 9554 | Entity `HBC HK` | R4 |
| Historical | 11943 | Maturity `32/13/2026` | R9 |

Three more historical rows are rejected (two on currency, one on date order).
Totals: asset 753 of 755 accepted, liability 1103 of 1104, historical 16178 of 16186.