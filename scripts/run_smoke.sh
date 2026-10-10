#!/usr/bin/env bash
# Smoke test against a running API (e.g. after `docker compose up --build`).
# Usage: scripts/run_smoke.sh [BASE_URL]    default: http://localhost:8000
# Windows PowerShell alternative: see README.md ("Smoke test").
set -euo pipefail

BASE_URL="${1:-${BASE_URL:-http://localhost:8000}}"
PY="$(command -v python3 || command -v python)"
fail() { echo "FAIL: $*" >&2; exit 1; }

echo "Smoke testing ${BASE_URL}"

health="$(curl -fsS --max-time 5 "${BASE_URL}/health")" || fail "/health did not return 2xx"
echo "$health" | "$PY" -c 'import json,sys; assert json.load(sys.stdin)=={"status":"ok"}' \
  || fail "/health body was: $health"
echo "PASS /health"

ladder="$(curl -fsS --max-time 5 "${BASE_URL}/api/v1/fixtures/ladder")" \
  || fail "/api/v1/fixtures/ladder did not return 2xx"
echo "$ladder" | "$PY" -c '
import json, sys
from decimal import Decimal
d = json.load(sys.stdin, parse_float=Decimal)
assert {"calc_date","currency","location","approach","run_id","buckets"} <= d.keys(), "missing top-level fields"
assert [b["bucket"] for b in d["buckets"]] == ["0-1M","1-3M","3-12M","1-5Y",">5Y"], "bucket order"
for b in d["buckets"]:
    assert abs(Decimal(b["assets"]) - Decimal(b["liabilities"]) - Decimal(b["net_gap"])) <= Decimal("0.005"), b["bucket"]
    assert isinstance(b["transaction_count"], int) and b["transaction_count"] >= 0, b["bucket"]
' || fail "ladder fixture failed validation"
echo "PASS /api/v1/fixtures/ladder"

code="$(curl -s -o /dev/null -w '%{http_code}' --max-time 5 "${BASE_URL}/openapi.json")"
[ "$code" = "200" ] || fail "/openapi.json returned $code"
echo "PASS /openapi.json"

echo "Smoke test passed."
