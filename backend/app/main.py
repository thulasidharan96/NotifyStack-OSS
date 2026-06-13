from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from app.core.config.settings import settings
from app.modules.auth.api.router import router as auth_router
from app.modules.events.api.router import router as events_router
from app.modules.notifications.api.router import router as notifications_router
from app.modules.organizations.api.router import router as organizations_router
from app.modules.projects.api.router import router as projects_router
from app.modules.providers.api.router import router as providers_router
from app.modules.templates.api.router import router as templates_router
from app.modules.workflows.api.router import router as workflows_router
from app.shared.database.base import Base
from app.shared.database.session import engine
from app.shared.exceptions.handlers import register_exception_handlers
from app.shared.middleware.tenant import TenantMiddleware
from fastapi import FastAPI


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(title=settings.app_name, lifespan=lifespan)
register_exception_handlers(app)
app.add_middleware(TenantMiddleware)

api_prefix = settings.api_v1_prefix
app.include_router(auth_router, prefix=api_prefix)
app.include_router(organizations_router, prefix=api_prefix)
app.include_router(projects_router, prefix=api_prefix)
app.include_router(events_router, prefix=api_prefix)
app.include_router(templates_router, prefix=api_prefix)
app.include_router(notifications_router, prefix=api_prefix)
app.include_router(providers_router, prefix=api_prefix)
app.include_router(workflows_router, prefix=api_prefix)


@app.get("/health")
async def health() -> dict[str, bool]:
    return {"ok": True}
