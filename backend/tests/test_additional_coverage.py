from uuid import uuid4

import pytest
from app.main import app
from app.modules.auth.services.security import JWTService, hash_password, verify_password
from app.modules.notifications.services.notification_service import NotificationService
from app.modules.providers.services.providers import (
    BaseProvider,
    ProviderFailoverService,
    ResendProvider,
    SMTPProvider,
)
from app.modules.templates.services.template_service import TemplateService
from app.shared.database.base import Base
from app.shared.database.models import Organization, Project
from app.shared.database.repositories import TenantRepository
from app.shared.database.session import SessionLocal, engine
from app.shared.exceptions.handlers import (
    api_exception_handler,
    register_exception_handlers,
    validation_exception_handler,
)
from app.shared.exceptions.http import ApiException, UnauthorizedException
from app.shared.queue.base import LocalQueueService
from app.shared.queue.nats_queue import NATSJetStreamQueueService
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.requests import Request


@pytest.mark.asyncio
async def test_auth_refresh_and_me(client):
    login = await client.post("/api/v1/auth/login", json={"email": "owner@example.com", "password": "secret"})
    tokens = login.json()

    refreshed = await client.post("/api/v1/auth/refresh", json={"refresh_token": tokens["refresh_token"]})
    assert refreshed.status_code == 200

    me = await client.get("/api/v1/auth/me", headers={"Authorization": "Bearer " + tokens["access_token"]})
    assert me.status_code == 200
    assert me.json()["role"] == "Owner"


@pytest.mark.asyncio
async def test_organization_project_notification_and_providers(client):
    login = await client.post("/api/v1/auth/login", json={"email": "owner@example.com", "password": "secret"})
    access = login.json()["access_token"]
    headers = {"Authorization": "Bearer " + access, "X-Organization-Id": "00000000-0000-0000-0000-000000000001"}

    created_org = await client.post("/api/v1/organizations", headers=headers, json={"name": "Acme"})
    assert created_org.status_code == 200

    fetched_org = await client.get("/api/v1/organizations/00000000-0000-0000-0000-000000000001", headers=headers)
    assert fetched_org.status_code == 200

    project = await client.post("/api/v1/projects", headers=headers, json={"name": "Core"})
    assert project.status_code == 200

    notification = await client.post(
        "/api/v1/notifications",
        headers={**headers, "X-Project-Id": "core"},
        json={"user_id": "u1", "channel": "email", "content": "Hi"},
    )
    assert notification.status_code == 200
    assert notification.json()["status"] == "QUEUED"

    providers = await client.get("/api/v1/providers", headers=headers)
    assert providers.status_code == 200
    assert "smtp" in providers.json()

    workflows = await client.get("/api/v1/workflows", headers=headers)
    assert workflows.status_code == 200


@pytest.mark.asyncio
async def test_services_and_queue_and_repository():
    queue = LocalQueueService()
    service = NotificationService(queue)
    created = await service.create_notification("org", "proj", "u1", "email", "hello")
    await service.schedule_notification(created.id)
    retried = await service.retry_notification(created.id)
    assert retried.status.value == "RETRYING"
    cancelled = await service.cancel_notification(created.id)
    assert cancelled.status.value == "CANCELLED"

    nats_queue = NATSJetStreamQueueService()
    seen: list[dict[str, object]] = []

    async def handler(payload: dict[str, object]) -> None:
        seen.append(payload)

    await nats_queue.subscribe("events.created", handler)
    await nats_queue.publish("events.created", {"ok": True})
    assert seen == [{"ok": True}]

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with SessionLocal() as session:
        org = Organization(name=f"RepoOrg-{uuid4()}")
        session.add(org)
        await session.flush()
        project = Project(organization_id=org.id, name="RepoProject")
        session.add(project)
        await session.commit()

        repo = TenantRepository(session=session, model=Project)
        found = await repo.get_by_id(org.id, project.id)
        missing = await repo.get_by_id("00000000-0000-0000-0000-000000000999", project.id)

    assert found is not None
    assert missing is None


@pytest.mark.asyncio
async def test_provider_failover_and_template_rendering():
    class BrokenProvider(BaseProvider):
        async def send(self, to: str, content: str) -> dict[str, str]:
            raise RuntimeError("down")

        async def validate(self) -> bool:
            return False

        async def health_check(self) -> bool:
            return True

    failover = ProviderFailoverService([BrokenProvider(), SMTPProvider(), ResendProvider()])
    sent = await failover.send("user@example.com", "hello")
    assert sent["provider"] in {"smtp", "resend"}

    output = TemplateService().render("{{ user.name }}", {"user": {"name": "Alex"}})
    assert output == "Alex"


@pytest.mark.asyncio
async def test_exception_handlers_and_password_helpers():
    request = Request({"type": "http", "headers": []})
    custom = await api_exception_handler(request, ApiException(404, "NOT_FOUND", "no"))
    assert custom.status_code == 404

    generic = await api_exception_handler(request, Exception("oops"))
    assert generic.status_code == 500

    validation = await validation_exception_handler(request, RequestValidationError([]))
    assert validation.status_code == 422

    fallback_validation = await validation_exception_handler(request, Exception("x"))
    assert fallback_validation.status_code == 422

    hashed = hash_password("password")
    assert verify_password("password", hashed)

    mini_app = FastAPI()
    register_exception_handlers(mini_app)
    assert mini_app.exception_handlers

    assert app.title


@pytest.mark.asyncio
async def test_jwt_decode_error_raises():
    with pytest.raises(UnauthorizedException):
        JWTService().decode_token("not-a-jwt")
