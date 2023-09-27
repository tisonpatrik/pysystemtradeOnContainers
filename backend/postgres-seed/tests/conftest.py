import pytest
import asyncpg
from src.core.config import settings
from unittest.mock import Mock

@pytest.fixture
def mock_connection():
    return Mock()

@pytest.fixture(scope="function")
async def db_connection():
    conn = await asyncpg.connect(settings.test_database_url)
    yield conn
    await conn.close()
