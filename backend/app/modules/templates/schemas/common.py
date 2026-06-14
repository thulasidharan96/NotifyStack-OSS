from pydantic import BaseModel


class TemplateRenderRequest(BaseModel):
    template: str
    context: dict[str, object]


class TemplateRenderResponse(BaseModel):
    output: str
