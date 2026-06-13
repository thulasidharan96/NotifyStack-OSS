from pydantic import BaseModel


class NotificationCreateRequest(BaseModel):
    user_id: str
    channel: str
    content: str


class NotificationRead(BaseModel):
    id: str
    user_id: str
    channel: str
    status: str
