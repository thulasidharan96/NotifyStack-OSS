from pydantic import BaseModel


class ProjectCreate(BaseModel):
    name: str


class ProjectRead(BaseModel):
    id: str
    organization_id: str
    name: str
