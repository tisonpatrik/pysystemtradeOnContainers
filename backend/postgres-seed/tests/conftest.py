import asyncio
import pytest
import asyncpg
import pytest_asyncio
from fastapi import FastAPI
from httpx import AsyncClient

from src.core.config import settings

test_db = (
    f"postgresql+asyncpg://{settings.postgres_user}:{settings.postgres_password}"
    f"@{settings.postgres_server}:{settings.postgres_port}/{settings.postgres_db_tests}"
)


@pytest.fixture(scope='function')
async def db_connection():
    conn = await asyncpg.connect(test_db)
    yield conn
    await conn.close()


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


# @pytest_asyncio.fixture()
# async def async_client(app: FastAPI) -> AsyncGenerator:
#     async with AsyncClient(app=app, base_url="http://test") as ac:
#         yield ac


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
