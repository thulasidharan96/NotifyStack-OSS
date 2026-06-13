from app.modules.auth.services.authorization import Principal, require_permission
from app.modules.providers.services.providers import (
    AmazonSESProvider,
    ResendProvider,
    SendGridProvider,
    SMTPProvider,
)
from fastapi import APIRouter, Depends

router = APIRouter(prefix="/providers", tags=["providers"])


@router.get("", response_model=list[str])
async def list_providers(
    _: Principal = Depends(require_permission("provider:read")),
) -> list[str]:
    providers = [SMTPProvider(), AmazonSESProvider(), ResendProvider(), SendGridProvider()]
    return [provider.provider_name for provider in providers]
