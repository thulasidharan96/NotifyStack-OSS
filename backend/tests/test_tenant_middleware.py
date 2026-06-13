import pytest


@pytest.mark.asyncio
async def test_tenant_header_required(client):
    login = await client.post(
        "/api/v1/auth/login",
        json={"email": "owner@example.com", "password": "secret"},
    )
    token = login.json()["access_token"]

    response = await client.post(
        "/api/v1/projects",
        headers={"Authorization": "Bearer " + token},
        json={"name": "acme-project"},
    )
    assert response.status_code == 401
    assert response.json()["error"]["code"] == "UNAUTHORIZED"
