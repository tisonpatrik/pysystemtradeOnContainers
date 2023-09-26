from src.db.repositories.repository import PostgresRepository
import pytest

@pytest.mark.asyncio
async def test_connect_method(postgres_repository: PostgresRepository):
    conn = await postgres_repository.connect()
    assert conn is not None  # You might want to use a more specific assertion

@pytest.mark.asyncio
async def test_disconnect_method(postgres_repository: PostgresRepository):
    conn = await postgres_repository.connect()
    await postgres_repository.disconnect(conn)
    # You may want to test that the connection was actually closed, perhaps by
    # trying an operation and confirming it fails as expected.