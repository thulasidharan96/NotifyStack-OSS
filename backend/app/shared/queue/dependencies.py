from app.shared.queue.base import LocalQueueService, QueueService

queue_service: QueueService = LocalQueueService()


def get_queue_service() -> QueueService:
    return queue_service
