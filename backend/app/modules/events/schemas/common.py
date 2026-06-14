from pydantic import BaseModel


class EventTriggerRequest(BaseModel):
    event: str
    user_id: str
    payload: dict[str, object]


class EventTriggerResponse(BaseModel):
    success: bool
    event: str
