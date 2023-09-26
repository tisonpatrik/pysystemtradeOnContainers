import pytest
from src.db.repositories.repository import PostgresRepository

@pytest.mark.asyncio
async def test_db_connection(db_connection):
    repo = PostgresRepository()
    assert (await repo._connect()) is not None
