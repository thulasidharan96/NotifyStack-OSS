from app.modules.auth.services.authorization import Principal, require_permission
from app.modules.notifications.schemas.common import NotificationCreateRequest, NotificationRead
from app.modules.notifications.services.notification_service import NotificationService
from app.shared.queue.dependencies import get_queue_service
from fastapi import APIRouter, Depends, Request

router = APIRouter(prefix="/notifications", tags=["notifications"])


@router.post("", response_model=NotificationRead)
async def create_notification(
    payload: NotificationCreateRequest,
    request: Request,
    _: Principal = Depends(require_permission("notification:create")),
) -> NotificationRead:
    service = NotificationService(get_queue_service())
    notification = await service.create_notification(
        organization_id=request.state.organization_id,
        project_id=request.headers.get("X-Project-Id", "default-project"),
        user_id=payload.user_id,
        channel=payload.channel,
        content=payload.content,
    )
    queued = await service.queue_notification(notification.id)
    return NotificationRead(
        id=queued.id,
        user_id=queued.user_id,
        channel=queued.channel,
        status=queued.status.value,
    )
