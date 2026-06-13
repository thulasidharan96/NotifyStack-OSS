import pytest


@pytest.mark.asyncio
async def test_login_returns_tokens(client):
    response = await client.post(
        "/api/v1/auth/login",
        json={"email": "owner@example.com", "password": "secret"},
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["access_token"]
    assert payload["refresh_token"]


@pytest.mark.asyncio
async def test_login_rejects_invalid_credentials(client):
    response = await client.post(
        "/api/v1/auth/login",
        json={"email": "invalid@example.com", "password": "wrong"},
    )
    assert response.status_code == 401
