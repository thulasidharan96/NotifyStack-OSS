from app.modules.auth.schemas.common import LoginRequest, RefreshRequest, TokenPair
from app.modules.auth.services.authorization import Principal, get_current_principal
from app.modules.auth.services.security import JWTService
from app.shared.exceptions.http import UnauthorizedException
from fastapi import APIRouter, Depends

router = APIRouter(prefix="/auth", tags=["auth"])
jwt_service = JWTService()


@router.post("/login", response_model=TokenPair)
async def login(payload: LoginRequest) -> TokenPair:
    if payload.email != "owner@example.com" or payload.password != "secret":
        raise UnauthorizedException("Invalid email or password")

    user_id = payload.email
    org_id = "00000000-0000-0000-0000-000000000001"
    role = "Owner"
    return TokenPair(
        access_token=jwt_service.create_access_token(user_id, org_id, role),
        refresh_token=jwt_service.create_refresh_token(user_id, org_id),
    )


@router.post("/refresh", response_model=TokenPair)
async def refresh(payload: RefreshRequest) -> TokenPair:
    claims = jwt_service.decode_token(payload.refresh_token)
    return TokenPair(
        access_token=jwt_service.create_access_token(claims["sub"], claims["org"], "Owner"),
        refresh_token=jwt_service.create_refresh_token(claims["sub"], claims["org"]),
    )


@router.get("/me", tags=["auth"])
async def me(principal: Principal = Depends(get_current_principal)) -> dict[str, str]:
    return {
        "user_id": principal.user_id,
        "organization_id": principal.organization_id,
        "role": principal.role,
    }
