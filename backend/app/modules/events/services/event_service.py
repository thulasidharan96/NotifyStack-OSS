from app.modules.events.schemas.common import EventTriggerRequest
from app.modules.notifications.services.notification_service import NotificationService
from app.shared.queue.base import QueueService


class EventService:
    def __init__(self, queue_service: QueueService, notification_service: NotificationService) -> None:
        self.queue_service = queue_service
        self.notification_service = notification_service

    async def trigger(self, organization_id: str, project_id: str, payload: EventTriggerRequest) -> None:
        if not payload.event.strip():
            raise ValueError("event is required")

        await self.queue_service.publish(
            "events.created",
            {
                "organization_id": organization_id,
                "project_id": project_id,
                "event": payload.event,
                "user_id": payload.user_id,
                "payload": payload.payload,
            },
        )

        notification = await self.notification_service.create_notification(
            organization_id=organization_id,
            project_id=project_id,
            user_id=payload.user_id,
            channel="in_app",
            content=f"Event received: {payload.event}",
        )
        await self.notification_service.queue_notification(notification.id)
