from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel, create_engine
from sqlmodel.ext.asyncio.session import AsyncSession

from src.core.config import settings
from src.db.seed.seeds import seed_grayfox_db

import logging

# Setting up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

engine = create_engine(
    url=settings.sync_database_url,
    echo=settings.db_echo_log,
)

async_engine = create_async_engine(
    url=settings.async_database_url,
    echo=settings.db_echo_log,
    future=True,
)

async_session = sessionmaker(
    bind=async_engine, class_=AsyncSession, expire_on_commit=False
)

async def init_db_async():
    """Initialize the database by creating tables and seeding them."""
    async with async_engine.begin() as conn:
        # Create tables based on the models
        await conn.run_sync(SQLModel.metadata.create_all)

    await seed_grayfox_db(async_session)       

async def drop_db_async():
    """Reset the database by dropping tables and re-initializing."""
    async with async_engine.begin() as conn:
        try:
            await conn.run_sync(SQLModel.metadata.drop_all)
            logger.info("Dropped all tables.")
        except Exception as e:
            logger.error(f"Error dropping tables: {e}")
            return
