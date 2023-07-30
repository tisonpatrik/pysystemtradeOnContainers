from typing import Optional
from uuid import UUID

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.db.errors import EntityDoesNotExist
from src.db.tables.base_class import StatusEnum
from src.db.tables.multiple_prices import MultiplePrices
from src.schemas.multiple_prices import MultiplePricesCreate, MultiplePricesPatch, MultiplePricesRead


class MultiplePricesRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def _get_instance(self, MultiplePrices_id: UUID):
        statement = (
            select(MultiplePrices)
            .where(MultiplePrices.id == MultiplePrices_id)
            .where(MultiplePrices.status != StatusEnum.deleted)
        )
        results = await self.session.exec(statement)

        return results.first()

    async def create(self, MultiplePrices_create: MultiplePricesCreate) -> MultiplePricesRead:
        db_MultiplePrices = MultiplePrices.from_orm(MultiplePrices_create)
        self.session.add(db_MultiplePrices)
        await self.session.commit()
        await self.session.refresh(db_MultiplePrices)

        return MultiplePricesRead(**db_MultiplePrices.dict())

    async def list(self, limit: int = 10, offset: int = 0) -> list[MultiplePricesRead]:
        statement = (
            (select(MultiplePrices).where(MultiplePrices.status != StatusEnum.deleted))
            .offset(offset)
            .limit(limit)
        )
        results = await self.session.exec(statement)

        return [MultiplePricesRead(**MultiplePrices.dict()) for MultiplePrices in results]

    async def get(self, MultiplePrices_id: UUID) -> Optional[MultiplePricesRead]:
        db_MultiplePrices = await self._get_instance(MultiplePrices_id)

        if db_MultiplePrices is None:
            raise EntityDoesNotExist

        return MultiplePricesRead(**db_MultiplePrices.dict())

    async def patch(
        self, MultiplePrices_id: UUID, MultiplePrices_patch: MultiplePricesPatch
    ) -> Optional[MultiplePricesRead]:
        db_MultiplePrices = await self._get_instance(MultiplePrices_id)

        if db_MultiplePrices is None:
            raise EntityDoesNotExist

        MultiplePrices_data = MultiplePrices_patch.dict(exclude_unset=True, exclude={"id"})
        for key, value in MultiplePrices_data.items():
            setattr(db_MultiplePrices, key, value)

        self.session.add(db_MultiplePrices)
        await self.session.commit()
        await self.session.refresh(db_MultiplePrices)

        return MultiplePricesRead(**db_MultiplePrices.dict())

    async def delete(self, MultiplePrices_id: UUID) -> None:
        db_MultiplePrices = await self._get_instance(MultiplePrices_id)

        if db_MultiplePrices is None:
            raise EntityDoesNotExist

        setattr(db_MultiplePrices, "status", StatusEnum.deleted)
        self.session.add(db_MultiplePrices)

        await self.session.commit()
