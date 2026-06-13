from app.shared.exceptions.http import ApiException
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


async def api_exception_handler(_: Request, exc: Exception) -> JSONResponse:
    if isinstance(exc, ApiException):
        api_exc = exc
    else:
        api_exc = ApiException(500, "INTERNAL_ERROR", "Unexpected error")
    return JSONResponse(status_code=api_exc.status_code, content={"success": False, "error": api_exc.detail})


async def validation_exception_handler(_: Request, exc: Exception) -> JSONResponse:
    if isinstance(exc, RequestValidationError):
        details = exc.errors()
    else:
        details = []
    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "error": {"code": "VALIDATION_ERROR", "message": "Invalid request payload"},
            "details": details,
        },
    )


def register_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(ApiException, api_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
