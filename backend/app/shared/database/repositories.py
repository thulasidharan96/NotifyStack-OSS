from app.shared.database.base import Base
from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession


class TenantRepository:
    def __init__(self, session: AsyncSession, model: type[Base]) -> None:
        self.session = session
        self.model = model

    def scoped_query(self, organization_id: str) -> Select[tuple[Base]]:
        return select(self.model).where(
            self.model.deleted_at.is_(None),  # type: ignore[attr-defined]
            self.model.organization_id == organization_id,  # type: ignore[attr-defined]
        )

    async def get_by_id(self, organization_id: str, entity_id: str) -> Base | None:
        result = await self.session.execute(
            self.scoped_query(organization_id).where(self.model.id == entity_id)  # type: ignore[attr-defined]
        )
        return result.scalar_one_or_none()
