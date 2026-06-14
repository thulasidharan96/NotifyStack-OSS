from collections.abc import Awaitable, Callable
from typing import Any

from app.shared.queue.base import QueueService


class NATSJetStreamQueueService(QueueService):
    def __init__(self) -> None:
        self._handlers: dict[str, list[Callable[[dict[str, Any]], Awaitable[None]]]] = {}

    async def publish(self, topic: str, payload: dict[str, Any]) -> None:
        for handler in self._handlers.get(topic, []):
            await handler(payload)

    async def subscribe(self, topic: str, handler: Callable[[dict[str, Any]], Awaitable[None]]) -> None:
        self._handlers.setdefault(topic, []).append(handler)
