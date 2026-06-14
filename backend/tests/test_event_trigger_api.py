import pytest


@pytest.mark.asyncio
async def test_event_trigger_success(client):
    login = await client.post(
        "/api/v1/auth/login",
        json={"email": "owner@example.com", "password": "secret"},
    )
    token = login.json()["access_token"]

    response = await client.post(
        "/api/v1/events/trigger",
        headers={
            "Authorization": "Bearer " + token,
            "X-Organization-Id": "00000000-0000-0000-0000-000000000001",
            "X-Project-Id": "proj-1",
        },
        json={"event": "order.shipped", "user_id": "123", "payload": {"order_id": "ABC123"}},
    )
    assert response.status_code == 200
    assert response.json() == {"success": True, "event": "order.shipped"}
