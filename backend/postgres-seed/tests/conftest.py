import asyncio
import pytest
import asyncpg
import pytest_asyncio
from fastapi import FastAPI
from typing import AsyncGenerator
from httpx import AsyncClient
from src.core.config import settings
from src.db.repositories.repository import PostgresRepository

@pytest_asyncio.fixture(scope="session")
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope='function')
@pytest.mark.asyncio
async def postgres_repository(event_loop):
    repo = PostgresRepository(settings.test_database_url)
    yield repo

# @pytest.fixture()
# def override_get_db(db_session: AsyncSession) -> Callable:
#     async def _override_get_db():
#         yield db_session

#     return _override_get_db


# @pytest.fixture()
# def app(override_get_db: Callable) -> FastAPI:
#     from src.api.dependencies.repositories import get_db
#     from src.main import app

#     app.dependency_overrides[get_db] = override_get_db

#     return app


@pytest_asyncio.fixture()
async def async_client(app: FastAPI) -> AsyncGenerator:
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


# @pytest.fixture()
# def create_transaction():
#     def _create_transaction(
#         amount: int = 10,
#         description: str = "Text description",
#     ):
#         return TransactionCreate(amount=amount, description=description)

#     return _create_transaction


# @pytest.fixture()
# def create_transactions(create_transaction):
#     def _create_transactions(_qty: int = 1):
#         return [
#             create_transaction(amount=i, description=f"Transaction number {i}")
#             for i in range(_qty)
#         ]

#     return _create_transactions
