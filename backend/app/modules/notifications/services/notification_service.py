from dataclasses import dataclass
from uuid import uuid4

from app.shared.database.models import NotificationStatus
from app.shared.queue.base import QueueService


@dataclass(slots=True)
class NotificationEntity:
    id: str
    organization_id: str
    project_id: str
    user_id: str
    channel: str
    content: str
    status: NotificationStatus = NotificationStatus.PENDING


class NotificationService:
    def __init__(self, queue: QueueService) -> None:
        self.queue = queue
        self.store: dict[str, NotificationEntity] = {}

    async def create_notification(
        self,
        organization_id: str,
        project_id: str,
        user_id: str,
        channel: str,
        content: str,
    ) -> NotificationEntity:
        notification = NotificationEntity(
            id=str(uuid4()),
            organization_id=organization_id,
            project_id=project_id,
            user_id=user_id,
            channel=channel,
            content=content,
        )
        self.store[notification.id] = notification
        return notification

    async def queue_notification(self, notification_id: str) -> NotificationEntity:
        notification = self.store[notification_id]
        notification.status = NotificationStatus.QUEUED
        await self.queue.publish("notifications.created", {"notification_id": notification.id})
        return notification

    async def schedule_notification(self, notification_id: str) -> NotificationEntity:
        notification = self.store[notification_id]
        notification.status = NotificationStatus.QUEUED
        return notification

    async def cancel_notification(self, notification_id: str) -> NotificationEntity:
        notification = self.store[notification_id]
        notification.status = NotificationStatus.CANCELLED
        return notification

    async def retry_notification(self, notification_id: str) -> NotificationEntity:
        notification = self.store[notification_id]
        notification.status = NotificationStatus.RETRYING
        await self.queue.publish("notifications.retry", {"notification_id": notification.id})
        return notification
