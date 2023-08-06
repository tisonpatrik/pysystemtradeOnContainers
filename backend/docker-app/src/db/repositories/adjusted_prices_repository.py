from typing import Optional
from uuid import UUID

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.db.errors import EntityDoesNotExist
from src.db.tables.base_class import StatusEnum
from src.db.tables.adjusted_prices_table import AdjustedPricesTable
from src.schemas.adjusted_prices_schema import AdjustedPricesCreate, AdjustedPricesPatch, AdjustedPricesRead


class AdjustedPricesRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def _get_instance(self, MultiplePrices_id: UUID):
        statement = (
            select(AdjustedPricesTable)
            .where(AdjustedPricesTable.id == MultiplePrices_id)
            .where(AdjustedPricesTable.status != StatusEnum.deleted)
        )
        results = await self.session.exec(statement)

        return results.first()

    async def create(self, MultiplePrices_create: AdjustedPricesCreate) -> AdjustedPricesRead:
        db_MultiplePrices = AdjustedPricesTable.from_orm(MultiplePrices_create)
        self.session.add(db_MultiplePrices)
        await self.session.commit()
        await self.session.refresh(db_MultiplePrices)

        return AdjustedPricesRead(**db_MultiplePrices.dict())

    async def list(self, limit: int = 10, offset: int = 0) -> list[AdjustedPricesRead]:
        statement = (
            (select(AdjustedPricesTable).where(AdjustedPricesTable.status != StatusEnum.deleted))
            .offset(offset)
            .limit(limit)
        )
        results = await self.session.exec(statement)

        return [AdjustedPricesRead(**MultiplePrices.dict()) for MultiplePrices in results]

    async def get(self, MultiplePrices_id: UUID) -> Optional[AdjustedPricesRead]:
        db_MultiplePrices = await self._get_instance(MultiplePrices_id)

        if db_MultiplePrices is None:
            raise EntityDoesNotExist

        return AdjustedPricesRead(**db_MultiplePrices.dict())

    async def patch(
        self, MultiplePrices_id: UUID, MultiplePrices_patch: AdjustedPricesPatch
    ) -> Optional[AdjustedPricesRead]:
        db_MultiplePrices = await self._get_instance(MultiplePrices_id)

        if db_MultiplePrices is None:
            raise EntityDoesNotExist

        MultiplePrices_data = MultiplePrices_patch.dict(exclude_unset=True, exclude={"id"})
        for key, value in MultiplePrices_data.items():
            setattr(db_MultiplePrices, key, value)

        self.session.add(db_MultiplePrices)
        await self.session.commit()
        await self.session.refresh(db_MultiplePrices)

        return AdjustedPricesRead(**db_MultiplePrices.dict())

    async def delete(self, MultiplePrices_id: UUID) -> None:
        db_MultiplePrices = await self._get_instance(MultiplePrices_id)

        if db_MultiplePrices is None:
            raise EntityDoesNotExist

        setattr(db_MultiplePrices, "status", StatusEnum.deleted)
        self.session.add(db_MultiplePrices)

        await self.session.commit()
