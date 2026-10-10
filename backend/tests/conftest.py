"""Shared pytest fixtures. Owner: Dev 6.

Tests must not need a live PostgreSQL server or any external service.
"""
import os

# Deterministic settings for the test run (set before the app is imported).
os.environ.setdefault("ENVIRONMENT", "test")
os.environ.setdefault("DATABASE_URL", "postgresql+psycopg://test:test@localhost:5432/test")
os.environ.setdefault("JWT_SECRET", "test-only-secret")

import pytest  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402

from app.main import app  # noqa: E402


@pytest.fixture(scope="session")
def client() -> TestClient:
    # raise_server_exceptions=False so we can assert on the 500 error *body*.
    with TestClient(app, raise_server_exceptions=False) as c:
        yield c
