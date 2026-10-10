"""Importing this package registers every model on `Base.metadata`.

Models must import `Base` from `app.core.db` only, and reference other tables by
name in `ForeignKey("table.id")` strings — never import sibling model modules —
so there are no circular imports.
"""
from app.models.asset_book import AssetBook
from app.models.audit_log import AuditLog
from app.models.gap_snapshot import GapSnapshot
from app.models.historical_log import HistoricalLog
from app.models.ingestion_error import IngestionError
from app.models.ingestion_run import IngestionRun
from app.models.liability_book import LiabilityBook
from app.models.ml_model import MLModel
from app.models.prediction import Prediction
from app.models.recommendation import Recommendation
from app.models.user import User

__all__ = [
    "AssetBook", "AuditLog", "GapSnapshot", "HistoricalLog", "IngestionError",
    "IngestionRun", "LiabilityBook", "MLModel", "Prediction", "Recommendation", "User",
]
