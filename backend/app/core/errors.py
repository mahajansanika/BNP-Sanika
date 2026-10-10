"""Shared API error structure. Owner: Dev 6.

Every error response has the shape::

    {"code": "ERROR_CODE", "message": "Human-readable description"}

Raise an `AppError` subclass from any feature module; never return errors with
HTTP 200, and never put stack traces, credentials or config in `message`.
"""
import logging

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

logger = logging.getLogger("app.errors")


class AppError(Exception):
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    code: str = "INTERNAL_ERROR"
    message: str = "An unexpected error occurred."

    def __init__(self, message: str | None = None, *, code: str | None = None,
                 status_code: int | None = None) -> None:
        if message is not None:
            self.message = message
        if code is not None:
            self.code = code
        if status_code is not None:
            self.status_code = status_code
        super().__init__(self.message)


class BadRequestError(AppError):
    status_code = status.HTTP_400_BAD_REQUEST
    code = "BAD_REQUEST"
    message = "The request is invalid."


class UnauthorizedError(AppError):
    status_code = status.HTTP_401_UNAUTHORIZED
    code = "UNAUTHENTICATED"
    message = "Authentication is required."


class ForbiddenError(AppError):
    status_code = status.HTTP_403_FORBIDDEN
    code = "FORBIDDEN"
    message = "You do not have access to this resource."


class NotFoundError(AppError):
    status_code = status.HTTP_404_NOT_FOUND
    code = "NOT_FOUND"
    message = "The requested resource was not found."


class NotImplementedFeatureError(AppError):
    status_code = status.HTTP_501_NOT_IMPLEMENTED
    code = "NOT_IMPLEMENTED"
    message = "This feature is not implemented yet."


_HTTP_STATUS_CODES = {
    400: "BAD_REQUEST",
    401: "UNAUTHENTICATED",
    403: "FORBIDDEN",
    404: "NOT_FOUND",
    405: "METHOD_NOT_ALLOWED",
    409: "CONFLICT",
    422: "VALIDATION_ERROR",
    501: "NOT_IMPLEMENTED",
}


def _body(code: str, message: str) -> dict[str, str]:
    return {"code": code, "message": message}


async def _app_error_handler(_: Request, exc: AppError) -> JSONResponse:
    if exc.status_code >= 500:
        logger.error("AppError %s: %s", exc.code, exc.message)
    headers = {"WWW-Authenticate": "Bearer"} if exc.status_code == 401 else None
    return JSONResponse(_body(exc.code, exc.message), status_code=exc.status_code, headers=headers)


async def _http_exception_handler(_: Request, exc: StarletteHTTPException) -> JSONResponse:
    code = _HTTP_STATUS_CODES.get(exc.status_code, "HTTP_ERROR" if exc.status_code < 500 else "INTERNAL_ERROR")
    message = exc.detail if isinstance(exc.detail, str) else "Request failed."
    return JSONResponse(_body(code, message), status_code=exc.status_code,
                        headers=getattr(exc, "headers", None))


async def _validation_error_handler(_: Request, exc: RequestValidationError) -> JSONResponse:
    # Summarise without echoing raw input values back to the client.
    parts = []
    for err in exc.errors()[:5]:
        loc = ".".join(str(p) for p in err.get("loc", ()) if p != "body") or "request"
        parts.append(f"{loc}: {err.get('msg', 'invalid value')}")
    return JSONResponse(_body("VALIDATION_ERROR", "; ".join(parts) or "Invalid request."),
                        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)


async def _unhandled_error_handler(_: Request, exc: Exception) -> JSONResponse:
    logger.exception("Unhandled error: %s", type(exc).__name__)
    return JSONResponse(_body("INTERNAL_ERROR", "An unexpected error occurred."),
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


def register_error_handlers(app: FastAPI) -> None:
    app.add_exception_handler(AppError, _app_error_handler)
    app.add_exception_handler(StarletteHTTPException, _http_exception_handler)
    app.add_exception_handler(RequestValidationError, _validation_error_handler)
    app.add_exception_handler(Exception, _unhandled_error_handler)
