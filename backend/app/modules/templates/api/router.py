from app.modules.auth.services.authorization import Principal, require_permission
from app.modules.templates.schemas.common import TemplateRenderRequest, TemplateRenderResponse
from app.modules.templates.services.template_service import TemplateService
from fastapi import APIRouter, Depends

router = APIRouter(prefix="/templates", tags=["templates"])
service = TemplateService()


@router.post("/render", response_model=TemplateRenderResponse)
async def render_template(
    payload: TemplateRenderRequest,
    _: Principal = Depends(require_permission("template:update")),
) -> TemplateRenderResponse:
    return TemplateRenderResponse(output=service.render(payload.template, payload.context))
