"""Application configuration loaded from environment variables and `.env`.

Owner: Dev 6. Values here are development defaults only; real secrets must be
supplied through the environment (see `.env.example`).
"""
from functools import lru_cache
from pathlib import Path

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

# backend/ directory (…/backend/app/core/config.py -> parents[2]).
BACKEND_DIR = Path(__file__).resolve().parents[2]
REPO_ROOT = BACKEND_DIR.parent

API_V1_PREFIX = "/api/v1"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        # Read `.env` from the repo root or backend/, whichever exists.
        # Real environment variables always take precedence.
        env_file=(REPO_ROOT / ".env", BACKEND_DIR / ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    app_name: str = "Liquid+ API"
    environment: str = Field(default="development", description="development | test | production")
    log_level: str = "INFO"

    # SQLAlchemy URL using the psycopg (v3) driver.
    database_url: SecretStr = SecretStr(
        "postgresql+psycopg://liquidplus:change-me@localhost:5432/liquidplus"
    )

    # Used from G2 onwards for signing JWTs. The default is deliberately
    # unusable outside development; see `is_insecure_jwt_secret`.
    jwt_secret: SecretStr = SecretStr("dev-only-change-me")
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    @property
    def is_insecure_jwt_secret(self) -> bool:
        return self.jwt_secret.get_secret_value() in {"", "dev-only-change-me", "change-me"}


@lru_cache
def get_settings() -> Settings:
    return Settings()
