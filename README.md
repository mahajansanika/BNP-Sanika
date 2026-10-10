# Liquid+: Intelligent Long Term Liquidity Gap Forecasting

Liquid+ forecasts liquidity gaps for financial institutions. It ingests asset, liability and historical transaction data; builds deterministic liquidity ladders by maturity bucket (`0-1M`, `1-3M`, `3-12M`, `1-5Y`, `>5Y`), currency and location; adjusts expected maturities with a behavioural ML model; and compares deterministic vs AI-adjusted results, with recommendations and what-if scenarios. Access is location-scoped, with a Support role that sees every location.

**Current gate: G1** — backend skeleton and frozen API contract.

## Stack

FastAPI · SQLAlchemy 2.0 · PostgreSQL 16 · Pydantic v2 / pydantic-settings · scikit-learn (in-process, later gate) · pytest · Docker Compose · React + Vite + TypeScript frontend (Dev 1).

See [docs/architecture.md](docs/architecture.md), [docs/schema.md](docs/schema.md) and [docs/assumptions.md](docs/assumptions.md).

## Prerequisites

- Docker Desktop (with Compose v2)
- Python 3.12 for running the API or tests outside Docker
- Git configured with `core.autocrlf` default; `.gitattributes` keeps shell scripts and Dockerfiles LF

## Configure

```powershell
Copy-Item .env.example .env
```

Edit `.env` and replace `POSTGRES_PASSWORD`, the password inside `DATABASE_URL`, and `JWT_SECRET`. Never commit `.env`.

## Run with Docker (PostgreSQL + API)

```powershell
docker compose up --build
```

- API: http://localhost:8000 · Swagger UI: http://localhost:8000/docs · OpenAPI: http://localhost:8000/openapi.json
- PostgreSQL: `localhost:5432` (data persists in the `pgdata` volume; `docker compose down -v` wipes it)

## Run the API locally (no Docker for the API)

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

The API starts even if PostgreSQL is not running; only database-backed endpoints need it. To use the Compose database, run `docker compose up db` and keep `DATABASE_URL` pointing at `localhost`.

## Tests

```powershell
cd backend
python -m pytest -q
```

Tests need no database or network.

## Smoke test (against a running API)

Bash / Git Bash / WSL:

```bash
scripts/run_smoke.sh http://localhost:8000
```

PowerShell:

```powershell
$base = "http://localhost:8000"
(Invoke-RestMethod "$base/health").status            # -> ok
$l = Invoke-RestMethod "$base/api/v1/fixtures/ladder"
$l.buckets.bucket -join ","                            # -> 0-1M,1-3M,3-12M,1-5Y,>5Y
$l.buckets | ForEach-Object { [math]::Abs($_.assets - $_.liabilities - $_.net_gap) -lt 0.005 }  # -> all True
```

## For feature developers

- Add endpoints to **your own** `backend/app/<module>/router.py`. It is already registered in `main.py` under `/api/v1`; do not edit `main.py`.
- Use the shared types in `app/schemas/common.py` and raise errors from `app/core/errors.py`.
- Add your table columns to your model stub in `app/models/` (keep the table name) and update `docs/schema.md`.
- Use `Depends(get_current_user)` from `app/auth/deps.py` for protected routes; it fails closed until G2.

## G1 status and limitations

- Working: `/health`, `/api/v1/fixtures/ladder` (synthetic SGD/Singapore ladder), OpenAPI and Swagger, shared error shape, config, DB engine/session, all 11 tables importable, Docker Compose, CI.
- **Temporary:** `/api/v1/fixtures/ladder` is unauthenticated.
- Feature routers are registered but empty; feature tables are primary-key-only stubs.
- No authentication yet.

## Next (G2)

JWT login (`POST /api/v1/auth/login`, `GET /api/v1/auth/me`), bcrypt hashing, `seed_users`, location-scoped access checks with Support override, and protecting the fixture endpoint. `/health/db` follows in G3.
