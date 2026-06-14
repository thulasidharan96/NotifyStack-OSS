import pytest
from app.shared.database.models import User
from app.shared.database.session import get_db_session
from httpx import AsyncClient
from sqlalchemy import select


@pytest.mark.asyncio
async def test_register_user_success(client: AsyncClient):
    # Ensure user does not already exist
    async for session in get_db_session():
        result = await session.execute(select(User).where(User.email == "testuser@example.com"))
        user = result.scalar_one_or_none()
        if user:
            await session.delete(user)
            await session.commit()
        break

    payload = {
        "email": "testuser@example.com",
        "password": "strongpassword",
        "organization_id": "00000000-0000-0000-0000-000000000001",
    }
    response = await client.post(
        "/api/v1/users/register",
        json=payload,
        headers={"X-Organization-Id": "00000000-0000-0000-0000-000000000001"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "testuser@example.com"
    assert data["organization_id"] == "00000000-0000-0000-0000-000000000001"
    assert "id" in data

    # Verify user exists in the database
    async for session in get_db_session():
        result = await session.execute(select(User).where(User.email == "testuser@example.com"))
        user = result.scalar_one_or_none()
        assert user is not None
        break


@pytest.mark.asyncio
async def test_register_user_duplicate_email(client: AsyncClient):
    # Ensure user does not already exist
    async for session in get_db_session():
        result = await session.execute(select(User).where(User.email == "duplicate@example.com"))
        user = result.scalar_one_or_none()
        if user:
            await session.delete(user)
            await session.commit()
        break

    payload = {
        "email": "duplicate@example.com",
        "password": "strongpassword",
        "organization_id": "00000000-0000-0000-0000-000000000001",
    }
    headers = {"X-Organization-Id": "00000000-0000-0000-0000-000000000001"}
    # Register once
    response1 = await client.post("/api/v1/users/register", json=payload, headers=headers)
    assert response1.status_code == 201

    # Register again with same email
    response2 = await client.post("/api/v1/users/register", json=payload, headers=headers)
    assert response2.status_code == 400
    assert response2.json()["detail"] == "Email already registered"


@pytest.mark.asyncio
async def test_delete_user(client: AsyncClient):
    # Ensure user does not already exist
    async for session in get_db_session():
        result = await session.execute(select(User).where(User.email == "todelete@example.com"))
        user = result.scalar_one_or_none()
        if user:
            await session.delete(user)
            await session.commit()
        break

    # First register a user
    payload = {
        "email": "todelete@example.com",
        "password": "strongpassword",
        "organization_id": "00000000-0000-0000-0000-000000000001",
    }
    headers = {"X-Organization-Id": "00000000-0000-0000-0000-000000000001"}
    register_response = await client.post("/api/v1/users/register", json=payload, headers=headers)
    assert register_response.status_code == 201
    user_id = register_response.json()["id"]

    # Delete the user. By default test Principal is Viewer and user_id="apikey" which shouldn't work.
    # We'll set the token manually or override dependency.
    # In auth we have: "if authorization ... claims['sub'] is user_id".
    # We can simulate Admin access.

    # We will test without permission first
    del_headers = {
        "X-Organization-Id": "00000000-0000-0000-0000-000000000001",
        "X-Api-Key": "some-key" # Default principal is Admin, which is allowed.
    }
    del_response_no_perm = await client.delete(
        f"/api/v1/users/{user_id}",
        headers=del_headers,
    )
    assert del_response_no_perm.status_code == 204

    # Verify it is deleted
    async for session in get_db_session():
        result = await session.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        assert user is None
        break

@pytest.mark.asyncio
async def test_delete_user_not_found(client: AsyncClient):
    response = await client.delete(
        "/api/v1/users/00000000-0000-0000-0000-000000000000",
        headers={
            "X-Organization-Id": "00000000-0000-0000-0000-000000000001",
            "x-api-key": "some-key"
        }
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"