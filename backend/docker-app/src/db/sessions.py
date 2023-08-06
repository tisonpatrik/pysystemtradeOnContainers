from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel, create_engine
from sqlmodel.ext.asyncio.session import AsyncSession

from src.core.config import settings
from src.db.seed.seeds import check_tables_exist_async, fill_empty_tables_config_based_async

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

    # Seed tables if they're empty
    async with async_session() as session:
        await fill_empty_tables_config_based_async(session)

async def check_and_initialize_tables(session: AsyncSession):
    """Check if tables exist and initialize them accordingly."""
    async with async_engine.begin() as conn:
        try:
            tables_exist = await check_tables_exist_async(conn)
            logger.info(f"Tables exist: {tables_exist}")
        except Exception as e:
            logger.error(f"Error checking tables: {e}")
            return
        
        if not tables_exist:
            await init_db_async()
        else:
            await fill_empty_tables_config_based_async(session)

async def reset_db_async():
    """Reset the database by dropping tables and re-initializing."""
    async with async_engine.begin() as conn:
        try:
            await conn.run_sync(SQLModel.metadata.drop_all)
            logger.info("Dropped all tables.")
        except Exception as e:
            logger.error(f"Error dropping tables: {e}")
            return
    await init_db_async()

async def create_tables_async():
    """Create database tables based on the defined models."""
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)