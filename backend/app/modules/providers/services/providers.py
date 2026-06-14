from abc import ABC, abstractmethod


class BaseProvider(ABC):
    @abstractmethod
    async def send(self, to: str, content: str) -> dict[str, str]:
        raise NotImplementedError

    @abstractmethod
    async def validate(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def health_check(self) -> bool:
        raise NotImplementedError


class MockProvider(BaseProvider):
    provider_name = "mock"

    async def send(self, to: str, content: str) -> dict[str, str]:
        return {"provider": self.provider_name, "to": to, "status": "accepted", "content": content}

    async def validate(self) -> bool:
        return True

    async def health_check(self) -> bool:
        return True


class SMTPProvider(MockProvider):
    provider_name = "smtp"


class AmazonSESProvider(MockProvider):
    provider_name = "amazon_ses"


class ResendProvider(MockProvider):
    provider_name = "resend"


class SendGridProvider(MockProvider):
    provider_name = "sendgrid"


class ProviderFailoverService:
    def __init__(self, providers: list[BaseProvider]) -> None:
        self.providers = providers

    async def send(self, to: str, content: str) -> dict[str, str]:
        last_error: Exception | None = None
        for provider in self.providers:
            try:
                if not await provider.health_check():
                    continue
                return await provider.send(to, content)
            except Exception as exc:  # pragma: no cover
                last_error = exc
        if last_error is not None:
            raise last_error
        raise RuntimeError("No healthy provider available")
