# fixture.py
import asyncio
import pytest
import pytest_asyncio
from src.core.config import settings
from unittest.mock import Mock
from contextlib import asynccontextmanager
from src.db.db_client import Db_client

db = Db_client(settings.test_database_url)

@pytest.fixture
def mock_connection():
    return Mock()

@pytest.fixture(scope='session')
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()

@asynccontextmanager 
async def get_test_db():
    await db.connect()
    conn = await db.get_conn()
    try:
        yield conn
    finally:
        await db.release_conn(conn)

@pytest_asyncio.fixture(scope="session")
async def db_connection():
    conn = None
    try:
        await db.connect()
        conn = await db.get_conn()
        yield conn
    finally:
        if conn:
            await db.release_conn(conn)
