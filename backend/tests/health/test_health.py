def test_health_returns_200(client):
    assert client.get("/health").status_code == 200


def test_health_body_is_ok(client):
    assert client.get("/health").json() == {"status": "ok"}


def test_health_needs_no_auth_header(client):
    r = client.get("/health", headers={})
    assert r.status_code == 200
