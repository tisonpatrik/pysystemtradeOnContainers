import asyncio
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.orm.attributes import QueryableAttribute

from common.src.database.base_model import BaseEntity
from common.src.logging.logger import AppLogger

T = TypeVar("T", bound=BaseEntity)


class EntityRepository(Generic[T]):
    """
    Generic repository for CRUD operations on entities.
    """

    def __init__(self, db_session: AsyncSession, schema: Type[T]):
        self.db_session = db_session
        self.entity_class = schema
        self.logger = AppLogger.get_instance().get_logger()

    async def insert_many_async(self, entities: List[T]) -> None:
        """
        Adds multiple new entities to the database in a bulk operation using `bulk_save_objects`,
        run in a thread pool for async compatibility.
        """
        sync_session = self.db_session.sync_session

        def do_bulk_save(sync_session: Session, entities: List[T]):
            sync_session.bulk_save_objects(entities)
            sync_session.commit()

        try:
            loop = asyncio.get_running_loop()
            await loop.run_in_executor(None, do_bulk_save, sync_session, entities)
        except SQLAlchemyError as exc:
            sync_session.rollback()
            error_message = (
                f"Error during bulk insert of {type(entities[0]).__name__}: {exc}"
            )
            self.logger.error(error_message)
            raise

    async def insert_async(self, entity: T) -> None:
        """
        Adds a new entity to the database.
        """
        try:
            self.db_session.add(entity)
            await self.db_session.commit()
        except SQLAlchemyError as exc:
            await self.db_session.rollback()
            error_message = f"Error adding {self.entity_class.__name__}: {exc}"
            self.logger.error(error_message)
            raise

    async def get_all_async(self) -> List[T]:
        """
        Fetches all entities of a type.
        """
        try:
            result = await self.db_session.execute(select(self.entity_class))
            entities = result.scalars().all()
            return list(entities)
        except SQLAlchemyError as exc:
            error_message = f"Error fetching all {self.entity_class.__name__}: {exc}"
            self.logger.error(error_message)
            raise

    async def delete_async(self, entity: T) -> None:
        """
        Deletes an entity from the database.
        """
        try:
            await self.db_session.delete(entity)
            await self.db_session.commit()
        except SQLAlchemyError as exc:
            await self.db_session.rollback()
            error_message = f"Error deleting {self.entity_class.__name__}: {exc}"
            self.logger.error(error_message)
            raise

    async def get_related_data_async(
        self,
        relations: Optional[List[QueryableAttribute]] = None,
        filters: Optional[Dict[str, Any]] = None,
    ) -> List[T]:
        """
        Fetches entities of a type along with their specified relations and optional filters.

        :param relations: List of relation names to join load.
        :param filters: Optional filters to apply on the query.
        """
        try:
            query = select(self.entity_class)

            if relations:
                for relation in relations:
                    query = query.options(joinedload(relation))

            if filters:
                for key, value in filters.items():
                    query = query.filter(getattr(self.entity_class, key) == value)

            result = await self.db_session.execute(query)
            entities = result.scalars().all()
            return list(entities)  # Explicitní konverze na List[T]
        except SQLAlchemyError as exc:
            error_message = f"Error fetching related {self.entity_class.__name__} data with filters {filters}: {exc}"
            self.logger.error(error_message)
            raise
