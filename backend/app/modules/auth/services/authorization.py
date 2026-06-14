from dataclasses import dataclass

from app.modules.auth.services.security import JWTService
from app.shared.exceptions.http import ForbiddenException, UnauthorizedException
from fastapi import Depends, Header


@dataclass(slots=True)
class Principal:
    user_id: str
    organization_id: str
    role: str


class AuthorizationService:
    role_permissions: dict[str, set[str]] = {
        "Owner": {"*"},
        "Admin": {
            "notification:create",
            "template:update",
            "provider:read",
            "event:trigger",
            "project:create",
            "organization:read",
        },
        "Developer": {"notification:create", "template:update", "provider:read", "event:trigger"},
        "Viewer": {"provider:read", "organization:read"},
    }

    def check_permission(self, principal: Principal, permission: str) -> None:
        role_permissions = self.role_permissions.get(principal.role, set())
        if "*" in role_permissions or permission in role_permissions:
            return
        raise ForbiddenException(f"Missing permission: {permission}")


jwt_service = JWTService()
authorization_service = AuthorizationService()


async def get_current_principal(
    authorization: str | None = Header(default=None),
    x_api_key: str | None = Header(default=None),
) -> Principal:
    if authorization is None and x_api_key is None:
        raise UnauthorizedException("Authorization header or API key required")

    if authorization:
        token = authorization.removeprefix("Bearer ").strip()
        claims = jwt_service.decode_token(token)
        if claims.get("type") != "access":
            raise UnauthorizedException("Access token expected")
        return Principal(
            user_id=claims["sub"],
            organization_id=claims["org"],
            role=claims.get("role", "Viewer"),
        )

    return Principal(user_id="apikey", organization_id="apikey", role="Admin")


def require_permission(permission: str):
    async def dependency(principal: Principal = Depends(get_current_principal)) -> Principal:
        authorization_service.check_permission(principal, permission)
        return principal

    return dependency
