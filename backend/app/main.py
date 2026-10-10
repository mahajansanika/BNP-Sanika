"""Liquid+ FastAPI application entry point. Owner: Dev 6.

Every feature router is registered exactly once below. Feature developers add
endpoints to their own `router.py`; they should never need to edit this file.
"""
import logging

from fastapi import FastAPI

from app.analytics.router import router as analytics_router
from app.auth.router import router as auth_router
from app.behavioural.router import router as behavioural_router
from app.core.config import API_V1_PREFIX, get_settings
from app.core.errors import register_error_handlers
from app.core.logging import configure_logging
from app.export.router import router as export_router
from app.fixtures.router import router as fixtures_router
from app.gap.router import router as gap_router
from app.health.router import router as health_router
from app.ingestion.router import router as ingestion_router
from app.ml.router import router as ml_router
from app.recommendations.router import router as recommendations_router
from app.scenario.router import router as scenario_router

API_VERSION = "0.1.0"

settings = get_settings()
configure_logging(settings.log_level)
logger = logging.getLogger("app")

if settings.is_insecure_jwt_secret and settings.environment == "production":
    raise RuntimeError("JWT_SECRET must be set to a strong value in production.")

app = FastAPI(
    title=settings.app_name,
    description=(
        "Liquid+: Intelligent Long Term Liquidity Gap Forecasting. "
        "Deterministic and AI-adjusted liquidity ladders by maturity bucket, "
        "currency and location."
    ),
    version=API_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

@app.get("/", tags=["Platform"])
def root():
    """Provide a welcome message and API documentation links."""
    return {
        "message": "Welcome to Liquid+ API",
        "version": API_VERSION,
        "docs": "/docs",
        "health": "/health",
    }

register_error_handlers(app)

# Unversioned
app.include_router(health_router)

# /api/v1
app.include_router(auth_router, prefix=API_V1_PREFIX)
app.include_router(fixtures_router, prefix=API_V1_PREFIX)
app.include_router(ingestion_router, prefix=API_V1_PREFIX)
app.include_router(gap_router, prefix=API_V1_PREFIX)
app.include_router(scenario_router, prefix=API_V1_PREFIX)
app.include_router(export_router, prefix=API_V1_PREFIX)
app.include_router(ml_router, prefix=API_V1_PREFIX)
app.include_router(analytics_router, prefix=API_V1_PREFIX)
app.include_router(behavioural_router, prefix=API_V1_PREFIX)
app.include_router(recommendations_router, prefix=API_V1_PREFIX)

logger.info("%s %s started (environment=%s)", settings.app_name, API_VERSION, settings.environment)
