# Assumptions and open decisions (G1)

Items here are **not** specified by the source documents. Each one should be confirmed or changed by the team.

1. **`run_id` is a string** in the API contract, so it can carry either an integer ID or a UUID from `ingestion_runs`. The fixture uses `fixture-sg-sgd-20260930`.
2. **Roles are `user` and `support`.** Location-scoped users have exactly one location; Support has none and can access all. Whether a user may have several locations is open.
3. **Money on the wire is a JSON number.** JSON cannot keep trailing zeros, so `1250000.00` arrives as `1250000.0`; the frontend formats to 2 dp. Rounding is half-up to 2 dp at serialisation only; calculations stay in `Decimal`.
4. **Validation errors return 422** (`VALIDATION_ERROR`), FastAPI's standard, and 400 is reserved for business-rule failures raised by feature code.
5. **Feature routers are empty at G1.** No placeholder 501 endpoints were invented, because their contracts are not agreed.
6. **URL sub-prefixes** (`/scenarios`, `/exports`, etc.) were chosen by Dev 6 at G1; owners may rename them in their own `router.py` before G2, after telling Dev 1.
7. **Feature model stubs contain only a primary key.** No business columns, day-count conventions or gap calculations are defined at G1.
8. **The fixture is fully synthetic** (Singapore, SGD, `calc_date` 2026-09-30). It is not real customer data and contains no PII.
9. **`/api/v1/fixtures/ladder` is temporary and unauthenticated.** It will be put behind auth in G2 or removed once the real ladder endpoint exists.
10. **Docker image uses Python 3.12** (`python:3.12-slim`) and PostgreSQL 16.
