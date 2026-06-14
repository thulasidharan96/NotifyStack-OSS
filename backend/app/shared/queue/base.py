from collections import defaultdict
from collections.abc import Awaitable, Callable
from typing import Any


class QueueService:
    async def publish(self, topic: str, payload: dict[str, Any]) -> None:
        raise NotImplementedError

    async def subscribe(self, topic: str, handler: Callable[[dict[str, Any]], Awaitable[None]]) -> None:
        raise NotImplementedError


class LocalQueueService(QueueService):
    def __init__(self) -> None:
        self.messages: dict[str, list[dict[str, Any]]] = defaultdict(list)

    async def publish(self, topic: str, payload: dict[str, Any]) -> None:
        self.messages[topic].append(payload)

    async def subscribe(self, topic: str, handler: Callable[[dict[str, Any]], Awaitable[None]]) -> None:
        for message in self.messages.get(topic, []):
            await handler(message)
