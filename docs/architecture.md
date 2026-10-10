# Liquid+ architecture (G1)

## Overview

```
React + Vite + TS (Dev 1)  ──HTTP/JSON──▶  FastAPI app (single process)  ──SQLAlchemy 2.0──▶  PostgreSQL 16
                                            ├─ core/      config, db, logging, errors   (Dev 6)
                                            ├─ auth/      JWT + bcrypt, location scope  (Dev 6, G2)
                                            ├─ health/    GET /health                   (Dev 6)
                                            ├─ fixtures/  GET /api/v1/fixtures/ladder   (Dev 6, temporary)
                                            ├─ ingestion/                               (Dev 2)
                                            ├─ gap/ scenario/ export/                   (Dev 3)
                                            ├─ ml/ analytics/                           (Dev 4, scikit-learn in-process)
                                            └─ behavioural/ recommendations/            (Dev 5)
```

There is one FastAPI application. ML runs inside it; there is no separate ML service.

## Routing

| Router | Mounted at |
|---|---|
| health | `/health` (unversioned) |
| auth | `/api/v1/auth` |
| fixtures | `/api/v1/fixtures` |
| ingestion | `/api/v1/ingestion` |
| gap | `/api/v1/gap` |
| scenario | `/api/v1/scenarios` |
| export | `/api/v1/exports` |
| ml | `/api/v1/ml` |
| analytics | `/api/v1/analytics` |
| behavioural | `/api/v1/behavioural` |
| recommendations | `/api/v1/recommendations` |

Each module's `router.py` owns its sub-prefix (`APIRouter(prefix="/gap")`); `main.py` adds `/api/v1` and registers each router exactly once. **Feature developers add endpoints to their own `router.py` and never edit `main.py`.** A test (`tests/e2e/test_app_contract.py`) fails if a router is missing or registered twice.

## API conventions (frozen at G1)

Defined in `backend/app/schemas/common.py`:

- Prefix `/api/v1`, `snake_case` JSON, dates `YYYY-MM-DD`.
- Currencies: `USD EUR GBP SGD HKD`. Locations: `Hong Kong, New York, London, Singapore, Paris`.
- Buckets, in this order: `0-1M, 1-3M, 3-12M, 1-5Y, >5Y`.
- Approach: `deterministic | ai | whatif`.
- Money: `Decimal` / PostgreSQL `NUMERIC` in the backend; JSON number rounded to 2 dp on the wire (`Money` type).
- Ladder/drill-down query parameters: `calc_date, currency, location, run_id` (`LadderQueryParams`).

### Errors

Every non-2xx response is `{"code": "ERROR_CODE", "message": "..."}` (`core/errors.py`).
Raise `BadRequestError` (400), `UnauthorizedError` (401), `ForbiddenError` (403), `NotFoundError` (404) or a custom `AppError`. Request validation failures return 422 `VALIDATION_ERROR`; unhandled exceptions return 500 `INTERNAL_ERROR` with no stack trace.

### Ladder contract

`LadderResponse` in `schemas/ladder.py`: `calc_date, currency, location, approach, run_id, buckets[5]`; each bucket has `bucket, assets, liabilities, net_gap, transaction_count`. The schema itself enforces bucket order and `net_gap = assets − liabilities`.

## Database

`core/db.py` provides `Base`, a pooled `engine` (`pool_pre_ping`), `SessionLocal`, the `get_db` request dependency, and `create_all()`. The engine does not connect at import, so the API starts even if PostgreSQL is down. No Alembic: tables are created with `create_all()` plus a seed script (G2).

## Authentication (G2)

JWT bearer tokens; bcrypt password hashes. Location-scoped users see only their location; Support sees all. `auth/deps.py` already exposes `get_current_user` and `require_location_access`; until G2 they fail closed with 501.
