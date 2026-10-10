"""Authentication schemas. Owner: Dev 6. Full login flow arrives in G2."""
from enum import Enum

from pydantic import BaseModel, Field

from app.schemas.common import Location


class Role(str, Enum):
    # ASSUMPTION (docs/assumptions.md): two roles. Location-scoped users and a
    # Support role that may access every location.
    USER = "user"
    SUPPORT = "support"


class LoginRequest(BaseModel):
    username: str = Field(min_length=1, max_length=150)
    password: str = Field(min_length=1, max_length=256)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserOut(BaseModel):
    id: int
    username: str
    role: Role
    location: Location | None = Field(default=None, description="null for Support users")
