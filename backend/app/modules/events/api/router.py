from app.modules.auth.services.authorization import Principal, require_permission
from app.modules.events.schemas.common import EventTriggerRequest, EventTriggerResponse
from app.modules.events.services.event_service import EventService
from app.modules.notifications.services.notification_service import NotificationService
from app.shared.queue.dependencies import get_queue_service
from fastapi import APIRouter, Depends, Request

router = APIRouter(prefix="/events", tags=["events"])


@router.post("/trigger", response_model=EventTriggerResponse)
async def trigger_event(
    payload: EventTriggerRequest,
    request: Request,
    _: Principal = Depends(require_permission("event:trigger")),
) -> EventTriggerResponse:
    queue_service = get_queue_service()
    notification_service = NotificationService(queue_service)
    service = EventService(queue_service, notification_service)
    organization_id = request.state.organization_id
    project_id = request.headers.get("X-Project-Id", "default-project")
    await service.trigger(organization_id=organization_id, project_id=project_id, payload=payload)
    return EventTriggerResponse(success=True, event=payload.event)
