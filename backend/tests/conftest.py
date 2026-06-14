import os
from collections.abc import AsyncGenerator

import pytest
from httpx import ASGITransport, AsyncClient

os.environ.setdefault("NOTIFYSTACK_JWT_SECRET", "test-secret-key-at-least-32-characters-long")

from app.main import app


@pytest.fixture
async def client() -> AsyncGenerator[AsyncClient]:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
