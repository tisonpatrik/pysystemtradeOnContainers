from typing import Generic, List, Optional, Type, TypeVar

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from common.database.models.base_model import BaseModel
from common.logging.logger import AppLogger

T = TypeVar("T", bound=BaseModel)


class EntityRepository(Generic[T]):
    """
    Generic repository for CRUD operations on entities.
    """

    def __init__(self, db_session: AsyncSession, entity_class: Type[T]):
        self.db_session = db_session
        self.entity_class = entity_class
        self.logger = AppLogger.get_instance().get_logger()

    async def insert_async(self, entity: T) -> None:
        """
        Adds a new entity to the database.
        """
        try:
            self.db_session.add(entity)
            await self.db_session.commit()
        except Exception as exc:
            await self.db_session.rollback()
            error_message = f"Error adding entity: {exc}"
            self.logger.error(error_message)
            raise

    async def get_by_id_async(self, id: int) -> Optional[T]:
        """
        Fetches an entity by its ID.
        """
        try:
            result = await self.db_session.execute(
                select(self.entity_class).where(self.entity_class.id == id)
            )
            entity = result.scalars().first()
            return entity
        except Exception as exc:
            error_message = f"Error fetching entity by ID: {exc}"
            self.logger.error(error_message)
            raise

    async def get_all_async(self) -> List[T]:
        """
        Fetches all entities of a type and returns them as a pandas DataFrame.
        """
        try:
            result = await self.db_session.execute(select(self.entity_class))
            entities = result.scalars().all()
            return list(entities)
        except Exception as exc:
            error_message = f"Error fetching all entities: {exc}"
            self.logger.error(error_message)
            raise

    async def delete_async(self, entity: T) -> None:
        """
        Deletes an entity from the database.
        """
        try:
            await self.db_session.delete(entity)
            await self.db_session.commit()
        except Exception as exc:
            await self.db_session.rollback()
            error_message = f"Error deleting entity: {exc}"
            self.logger.error(error_message)
            raise

    async def update_async(self) -> None:
        """
        Commits current transactions to update the entity in the database.
        """
        try:
            await self.db_session.commit()
        except Exception as exc:
            await self.db_session.rollback()
            error_message = f"Error updating entity: {exc}"
            self.logger.error(error_message)
            raise
