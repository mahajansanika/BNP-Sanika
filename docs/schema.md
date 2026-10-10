# Database schema (G1)

All models inherit `app.core.db.Base`. Models reference other tables only by `ForeignKey("table.id")` strings and never import sibling model modules, so there are no circular imports. Money columns must use `Numeric`, never `Float`.

| Table | Model file | Owner | G1 status |
|---|---|---|---|
| `users` | `models/user.py` | Dev 6 | Defined |
| `audit_log` | `models/audit_log.py` | Dev 6 | Defined |
| `ingestion_runs` | `models/ingestion_run.py` | Dev 2 | Defined |
| `ingestion_errors` | `models/ingestion_error.py` | Dev 2 | Defined |
| `asset_book` | `models/asset_book.py` | Dev 2 | Defined |
| `liability_book` | `models/liability_book.py` | Dev 2 | Defined |
| `historical_log` | `models/historical_log.py` | Dev 2 | Defined |
| `gap_snapshots` | `models/gap_snapshot.py` | Dev 3 | Stub (PK only) |
| `ml_models` | `models/ml_model.py` | Dev 4 | Stub (PK only) |
| `predictions` | `models/prediction.py` | Dev 4 | Stub (PK only) |
| `recommendations` | `models/recommendation.py` | Dev 5 | Stub (PK only) |

Stubs define only `id` so the table name is reserved and metadata is consistent. Columns were deliberately **not** invented; each owner adds them once agreed and updates this file.

## `users`

| Column | Type | Notes |
|---|---|---|
| id | integer PK | |
| username | varchar(150) | unique, indexed |
| password_hash | varchar(255) | bcrypt hash only |
| role | varchar(20) | `user` or `support` (check constraint) |
| location | varchar(50), nullable | required unless role is `support` (check constraint) |
| is_active | boolean | default true |
| created_at | timestamptz | server default `now()` |

## `audit_log`

| Column | Type | Notes |
|---|---|---|
| id | integer PK | |
| user_id | integer FK → users.id, nullable | `ON DELETE SET NULL` |
| action | varchar(100) | e.g. `login`, `ingestion.upload` |
| resource | varchar(255), nullable | |
| location | varchar(50), nullable | |
| detail | JSON, nullable | never secrets or tokens |
| created_at | timestamptz | indexed |

## `ingestion_runs` (Dev 2)

One row per upload attempt. History is kept; book tables are replaced on each accepted upload.

| Column | Type | Notes |
|---|---|---|
| id | integer PK | |
| sheet | varchar(20) | `asset`, `liability` or `historical` |
| filename | varchar(255) | |
| status | varchar(10) | `success`, `partial` or `failed` |
| rows_read / rows_accepted / rows_rejected | integer | default 0 |
| errors_total | integer | default 0 |
| file_error | text, nullable | set when the whole file is rejected (rule R0 or unreadable file) |
| created_at | timestamptz | server default `now()` |

## `ingestion_errors` (Dev 2)

One row per failed rule on a row; `ON DELETE CASCADE` from the run.

| Column | Type | Notes |
|---|---|---|
| id | integer PK | |
| run_id | integer FK → ingestion_runs.id | indexed |
| row_number | integer | spreadsheet row, header = row 1 |
| column_name | varchar(60) | |
| value | text | offending value |
| rule | varchar(5) | `R1`..`R16` |
| message | varchar(200) | |

## `asset_book`, `liability_book`, `historical_log` (Dev 2)

The three tables share the columns below (`BookColumns` mixin in `models/book_common.py`). Rows come only from accepted uploads. `cashflow` = principal + simple interest at maturity (actual/365), in the original currency, no FX conversion.

| Column | Type | Notes |
|---|---|---|
| id | integer PK | |
| run_id | integer FK → ingestion_runs.id | indexed |
| transaction_id | varchar(20) | indexed; `AST-` / `LIA-` prefix |
| entity | varchar(30) | |
| location | varchar(30) | indexed |
| customer_id | varchar(20) | |
| amount | numeric(20,2) | principal (`Loan_Amount` in the asset sheet) |
| currency | varchar(3) | indexed |
| transaction_date | date | |
| maturity_date | date | indexed (`Contractual_Maturity_Date` in historical) |
| interest_rate_pct | numeric(7,4) | |
| market_interest_rate_pct | numeric(7,4) | |
| product_type | varchar(20) | `Loan_Type` in the asset sheet |
| customer_segment | varchar(20) | |
| client_rating | integer | |
| tenor_days | integer | maturity - transaction date |
| interest_amount | numeric(20,2) | |
| cashflow | numeric(20,2) | amount + interest_amount |

`historical_log` adds:

| Column | Type | Notes |
|---|---|---|
| type | varchar(10) | `Asset` or `Liability` |
| actual_closure_date | date, nullable | NULL = still open |
