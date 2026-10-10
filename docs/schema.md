# Database schema (G1)

All models inherit `app.core.db.Base`. Models reference other tables only by `ForeignKey("table.id")` strings and never import sibling model modules, so there are no circular imports. Money columns must use `Numeric`, never `Float`.

| Table | Model file | Owner | G1 status |
|---|---|---|---|
| `users` | `models/user.py` | Dev 6 | Defined |
| `audit_log` | `models/audit_log.py` | Dev 6 | Defined |
| `ingestion_runs` | `models/ingestion_run.py` | Dev 2 | Stub (PK only) |
| `ingestion_errors` | `models/ingestion_error.py` | Dev 2 | Stub (PK only) |
| `asset_book` | `models/asset_book.py` | Dev 2 | Stub (PK only) |
| `liability_book` | `models/liability_book.py` | Dev 2 | Stub (PK only) |
| `historical_log` | `models/historical_log.py` | Dev 2 | Stub (PK only) |
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
