"""G1 auth guarantees: placeholders fail closed; no Support bypass."""
import pytest

from app.auth.deps import AuthNotAvailableError, get_current_user, require_location_access
from app.core.config import get_settings


def test_get_current_user_fails_closed():
    with pytest.raises(AuthNotAvailableError) as exc:
        get_current_user()
    assert exc.value.status_code == 501


def test_location_check_fails_closed():
    with pytest.raises(AuthNotAvailableError):
        require_location_access("Singapore", None)  # type: ignore[arg-type]


def test_secrets_are_not_exposed_in_repr():
    s = get_settings()
    assert s.jwt_secret.get_secret_value() not in repr(s)
    assert s.database_url.get_secret_value() not in repr(s)


def test_redact_url_hides_password():
    from app.core.logging import redact_url
    out = redact_url("postgresql+psycopg://u:supersecret@db:5432/x")
    assert "supersecret" not in out and "db:5432" in out
