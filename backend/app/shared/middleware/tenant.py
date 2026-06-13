from uuid import UUID

from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware


class TenantMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):  # type: ignore[no-untyped-def]
        if request.url.path.startswith("/api/v1/auth"):
            return await call_next(request)

        org_id = request.headers.get("X-Organization-Id")
        if org_id is None:
            return JSONResponse(
                status_code=401,
                content={
                    "success": False,
                    "error": {"code": "UNAUTHORIZED", "message": "X-Organization-Id header is required"},
                },
            )
        try:
            UUID(org_id)
        except ValueError:
            return JSONResponse(
                status_code=422,
                content={
                    "success": False,
                    "error": {"code": "VALIDATION_ERROR", "message": "X-Organization-Id must be a valid UUID"},
                },
            )
        request.state.organization_id = org_id
        return await call_next(request)
