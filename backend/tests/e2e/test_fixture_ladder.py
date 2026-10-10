import json
from decimal import Decimal

import pytest

from app.fixtures import router as fixtures_module
from app.schemas.ladder import LadderResponse

URL = "/api/v1/fixtures/ladder"
TOP_LEVEL = {"calc_date", "currency", "location", "approach", "run_id", "buckets"}
BUCKET_KEYS = {"bucket", "assets", "liabilities", "net_gap", "transaction_count"}
ORDER = ["0-1M", "1-3M", "3-12M", "1-5Y", ">5Y"]


@pytest.fixture(scope="module")
def body(client):
    r = client.get(URL)
    assert r.status_code == 200, r.text
    return r.json()


def test_status_200(client):
    assert client.get(URL).status_code == 200


def test_top_level_fields(body):
    assert set(body) == TOP_LEVEL


def test_five_buckets_in_order(body):
    assert [b["bucket"] for b in body["buckets"]] == ORDER


def test_bucket_keys(body):
    for b in body["buckets"]:
        assert set(b) == BUCKET_KEYS


def test_net_gap_equals_assets_minus_liabilities(body):
    for b in body["buckets"]:
        diff = Decimal(str(b["assets"])) - Decimal(str(b["liabilities"])) - Decimal(str(b["net_gap"]))
        assert abs(diff) <= Decimal("0.005"), b


def test_money_is_json_number_with_two_dp(body):
    for b in body["buckets"]:
        for k in ("assets", "liabilities", "net_gap"):
            assert isinstance(b[k], (int, float)) and not isinstance(b[k], bool)
            assert Decimal(str(b[k])) == Decimal(str(b[k])).quantize(Decimal("0.01"))


def test_transaction_count_non_negative_int(body):
    for b in body["buckets"]:
        assert isinstance(b["transaction_count"], int) and not isinstance(b["transaction_count"], bool)
        assert b["transaction_count"] >= 0


def test_contract_values(body):
    assert body["approach"] in {"deterministic", "ai", "whatif"}
    assert body["currency"] in {"USD", "EUR", "GBP", "SGD", "HKD"}
    assert body["location"] in {"Hong Kong", "New York", "London", "Singapore", "Paris"}
    assert len(body["calc_date"]) == 10 and body["calc_date"][4] == "-"


def test_response_validates_against_schema(body):
    LadderResponse.model_validate(body)


def test_route_uses_ladder_response_model(client):
    from app.main import app
    route = next(r for r in app.routes if getattr(r, "path", None) == URL)
    assert route.response_model is LadderResponse
    schema = client.get("/openapi.json").json()
    ref = schema["paths"][URL]["get"]["responses"]["200"]["content"]["application/json"]["schema"]["$ref"]
    assert ref.endswith("/LadderResponse")


def test_api_returns_the_file_not_hardcoded_values(body):
    on_disk = json.loads(fixtures_module.LADDER_FIXTURE_PATH.read_text(encoding="utf-8"))
    assert body == on_disk


def test_missing_fixture_gives_500_error_shape(client, monkeypatch, tmp_path):
    monkeypatch.setattr(fixtures_module, "LADDER_FIXTURE_PATH", tmp_path / "nope.json")
    r = client.get(URL)
    assert r.status_code == 500
    assert r.json() == {"code": "FIXTURE_UNAVAILABLE",
                        "message": "The ladder fixture is not available on the server."}


def test_invalid_fixture_gives_500_error_shape(client, monkeypatch, tmp_path):
    bad = tmp_path / "bad.json"
    data = json.loads(fixtures_module.LADDER_FIXTURE_PATH.read_text(encoding="utf-8"))
    data["buckets"][0]["net_gap"] = 1.00  # breaks assets - liabilities
    bad.write_text(json.dumps(data), encoding="utf-8")
    monkeypatch.setattr(fixtures_module, "LADDER_FIXTURE_PATH", bad)
    r = client.get(URL)
    assert r.status_code == 500
    assert r.json()["code"] == "FIXTURE_INVALID"
    assert "Traceback" not in r.text


def test_fixture_path_is_not_request_controlled(client):
    r = client.get(URL, params={"path": "../../etc/passwd", "file": "x"})
    assert r.status_code == 200
    assert r.json()["location"] == "Singapore"
