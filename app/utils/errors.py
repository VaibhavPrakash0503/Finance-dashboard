"""
Custom exception classes and error handlers for the Finance Dashboard API
"""

from fastapi import HTTPException, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError, SQLAlchemyError


# Custom Exception Classes
class FinanceAPIException(Exception):
    """Base exception for Finance Dashboard API"""

    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class NotFoundError(FinanceAPIException):
    """Raised when a resource is not found"""

    def __init__(self, message: str = "Resource not found"):
        super().__init__(message, status_code=status.HTTP_404_NOT_FOUND)


class UnauthorizedError(FinanceAPIException):
    """Raised when authentication fails"""

    def __init__(self, message: str = "Unauthorized access"):
        super().__init__(message, status_code=status.HTTP_401_UNAUTHORIZED)


class ForbiddenError(FinanceAPIException):
    """Raised when user lacks permissions"""

    def __init__(self, message: str = "Insufficient permissions"):
        super().__init__(message, status_code=status.HTTP_403_FORBIDDEN)


class ValidationException(FinanceAPIException):
    """Raised when data validation fails"""

    def __init__(self, message: str = "Validation error"):
        super().__init__(message, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)


class DuplicateResourceError(FinanceAPIException):
    """Raised when trying to create a duplicate resource"""

    def __init__(self, message: str = "Resource already exists"):
        super().__init__(message, status_code=status.HTTP_409_CONFLICT)


# Error Response Handler Functions
async def finance_api_exception_handler(
    request: Request, exc: FinanceAPIException
) -> JSONResponse:
    """Handle custom Finance API exceptions"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.__class__.__name__,
            "message": exc.message,
            "path": str(request.url.path),
        },
    )


async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """Handle FastAPI HTTPException with custom format"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": "HTTPException",
            "message": exc.detail,
            "path": str(request.url.path),
        },
    )


async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    """Handle Pydantic validation errors with detailed messages"""
    errors = []
    for error in exc.errors():
        field = " -> ".join(str(loc) for loc in error["loc"])
        errors.append({"field": field, "message": error["msg"], "type": error["type"]})

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": "ValidationError",
            "message": "Invalid input data",
            "details": errors,
            "path": str(request.url.path),
        },
    )


async def integrity_error_handler(
    request: Request, exc: IntegrityError
) -> JSONResponse:
    """Handle database integrity errors (e.g., unique constraint violations)"""
    error_message = str(exc.orig)

    # Parse common integrity errors
    if "UNIQUE constraint failed" in error_message:
        if "email" in error_message:
            message = "Email address already exists"
        elif "username" in error_message:
            message = "Username already taken"
        else:
            message = "Duplicate entry detected"
    else:
        message = "Database integrity error"

    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={
            "error": "IntegrityError",
            "message": message,
            "path": str(request.url.path),
        },
    )


async def sqlalchemy_exception_handler(
    request: Request, exc: SQLAlchemyError
) -> JSONResponse:
    """Handle general SQLAlchemy database errors"""
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "DatabaseError",
            "message": "A database error occurred",
            "path": str(request.url.path),
        },
    )


async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handle all uncaught exceptions"""
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "InternalServerError",
            "message": "An unexpected error occurred",
            "path": str(request.url.path),
        },
    )
