from uuid import uuid4

from app.modules.auth.services.authorization import Principal, require_permission
from app.modules.projects.schemas.common import ProjectCreate, ProjectRead
from fastapi import APIRouter, Depends, Request

router = APIRouter(prefix="/projects", tags=["projects"])
_projects: dict[str, ProjectRead] = {}


@router.post("", response_model=ProjectRead)
async def create_project(
    payload: ProjectCreate,
    request: Request,
    _: Principal = Depends(require_permission("project:create")),
) -> ProjectRead:
    org_id = request.state.organization_id
    project = ProjectRead(id=str(uuid4()), organization_id=org_id, name=payload.name)
    _projects[project.id] = project
    return project
