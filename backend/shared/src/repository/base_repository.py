from typing import Optional, TypeVar, List, Generic, Union
from uuid import UUID
from abc import ABC, abstractmethod
from sqlmodel import SQLModel

Entity = TypeVar("Entity", bound=SQLModel)
EntityCreate = TypeVar("EntityCreate")
EntityRead = TypeVar("EntityRead")
EntityPatch = TypeVar("EntityPatch")

class IDatabaseRepository(ABC, Generic[Entity, EntityCreate, EntityRead, EntityPatch]):

    @abstractmethod
    async def create(self, entity_create: EntityCreate) -> EntityRead:
        """Create a new entity"""
        pass

    @abstractmethod
    async def list(self, limit: int = 10, offset: int = 0) -> List[EntityRead]:
        """List entities with optional pagination"""
        pass

    @abstractmethod
    async def get(self, entity_id: Union[UUID, str]) -> Optional[EntityRead]:
        """Get an entity by its ID"""
        pass

    @abstractmethod
    async def patch(self, entity_id: Union[UUID, str], entity_patch: EntityPatch) -> Optional[EntityRead]:
        """Update an entity by its ID"""
        pass

    @abstractmethod
    async def delete(self, entity_id: Union[UUID, str]) -> None:
        """Delete an entity by its ID"""
        pass

# Note:
# - This interface uses abstract methods, which means any concrete class inheriting from it must implement these methods.
# - The `Union[UUID, str]` type hint for `entity_id` is to accommodate both UUID (common in PostgreSQL) and string IDs (common in DynamoDB).
# - Depending on the use cases and the nature of the operations in DynamoDB vs PostgreSQL, you may need to adjust or add methods to this interface.
