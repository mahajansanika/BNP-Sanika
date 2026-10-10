"""Auth dependencies for feature routers. Owner: Dev 6.

Feature developers can already depend on these; the signatures are the G2
contract. Until G2 they FAIL CLOSED (HTTP 501) — there is no development
bypass and nothing ever grants Support access implicitly.

    from app.auth.deps import get_current_user
    @router.get("/ladder")
    def ladder(user = Depends(get_current_user)): ...
"""
from app.core.errors import NotImplementedFeatureError
from app.schemas.auth import UserOut


class AuthNotAvailableError(NotImplementedFeatureError):
    code = "AUTH_NOT_IMPLEMENTED"
    message = "Authentication is not available until G2."


def get_current_user() -> UserOut:
    raise AuthNotAvailableError()


def require_location_access(location: str, user: UserOut) -> None:
    """G2: raise ForbiddenError unless user.role is support or user.location == location."""
    raise AuthNotAvailableError()
