from app.modules.auth.services.authorization import Principal, require_permission
from app.modules.organizations.schemas.common import OrganizationCreate, OrganizationRead
from fastapi import APIRouter, Depends

router = APIRouter(prefix="/organizations", tags=["organizations"])
_organizations: dict[str, OrganizationRead] = {}


@router.post("", response_model=OrganizationRead)
async def create_organization(
    payload: OrganizationCreate,
    principal: Principal = Depends(require_permission("organization:read")),
) -> OrganizationRead:
    org = OrganizationRead(id=principal.organization_id, name=payload.name)
    _organizations[org.id] = org
    return org


@router.get("/{organization_id}", response_model=OrganizationRead)
async def get_organization(
    organization_id: str,
    _: Principal = Depends(require_permission("organization:read")),
) -> OrganizationRead:
    return _organizations[organization_id]
