from typing import Optional, TypeVar, List, Union
from uuid import UUID
from sqlmodel import select, SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from src.db.errors import EntityDoesNotExist
from src.db.enums import StatusEnum
from backend.shared.src.repository.base_repository import IDatabaseRepository

# Define the type variables
Entity = TypeVar("Entity", bound=SQLModel)
EntityCreate = TypeVar("EntityCreate")
EntityRead = TypeVar("EntityRead")
EntityPatch = TypeVar("EntityPatch")

class PostgreSQLRepository(IDatabaseRepository[Entity, EntityCreate, EntityRead, EntityPatch]):

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def _get_instance(self, entity_id: Union[UUID, str]) -> Optional[Entity]:
        statement = (
            select(Entity)
            .where(Entity.id == entity_id)
            .where(Entity.status != StatusEnum.deleted)
        )
        results = await self.session.exec(statement)
        return results.first()

    async def create(self, entity_create: EntityCreate) -> EntityRead:
        db_entity = Entity.from_orm(entity_create)
        self.session.add(db_entity)
        await self.session.commit()
        await self.session.refresh(db_entity)
        return EntityRead(**db_entity.dict())

    async def list(self, limit: int = 10, offset: int = 0) -> List[EntityRead]:
        statement = (
            (select(Entity).where(Entity.status != StatusEnum.deleted))
            .offset(offset)
            .limit(limit)
        )
        results = await self.session.exec(statement)
        return [EntityRead(**entity.dict()) for entity in results]

    async def get(self, entity_id: Union[UUID, str]) -> Optional[EntityRead]:
        db_entity = await self._get_instance(entity_id)
        if db_entity is None:
            raise EntityDoesNotExist
        return EntityRead(**db_entity.dict())

    async def patch(self, entity_id: Union[UUID, str], entity_patch: EntityPatch) -> Optional[EntityRead]:
        db_entity = await self._get_instance(entity_id)
        if db_entity is None:
            raise EntityDoesNotExist
        entity_data = entity_patch.dict(exclude_unset=True, exclude={"id"})
        for key, value in entity_data.items():
            setattr(db_entity, key, value)
        self.session.add(db_entity)
        await self.session.commit()
        await self.session.refresh(db_entity)
        return EntityRead(**db_entity.dict())

    async def delete(self, entity_id: Union[UUID, str]) -> None:
        db_entity = await self._get_instance(entity_id)
        if db_entity is None:
            raise EntityDoesNotExist
        setattr(db_entity, "status", StatusEnum.deleted)
        self.session.add(db_entity)
        await self.session.commit()

