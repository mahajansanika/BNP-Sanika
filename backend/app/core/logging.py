"""Logging setup. Owner: Dev 6.

Never log passwords, tokens, the JWT secret or full database URLs.
Use `redact_url` when a connection target must be logged.
"""
import logging

from sqlalchemy.engine import make_url

_FORMAT = "%(asctime)s %(levelname)s [%(name)s] %(message)s"


def configure_logging(level: str = "INFO") -> None:
    logging.basicConfig(level=level.upper(), format=_FORMAT)


def redact_url(url: str) -> str:
    """Return a URL with the password removed, e.g. for startup logs."""
    try:
        return make_url(url).render_as_string(hide_password=True)
    except Exception:  # noqa: BLE001 - never leak the raw value on parse failure
        return "<unparseable database url>"
