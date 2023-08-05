from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel, create_engine
from sqlmodel.ext.asyncio.session import AsyncSession

from src.core.config import settings
from src.db.seed.seeds import check_tables_exist_async, seed_grayfox_db_async, fill_empty_tables_async

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
    logger.info("Initializing database...")
    async with async_session() as session:
        # Check if tables exist
        async with async_engine.begin() as conn:
            try:
                tables_exist = await check_tables_exist_async(conn)
                logger.info(f"Tables exist: {tables_exist}")
            except Exception as e:
                logger.error(f"Error checking tables: {e}")
                return
        
        # If tables don't exist, create them
        if not tables_exist:
            try:
                # await create_tables_async()
                await seed_grayfox_db_async(session)
                logger.info("Seeded the database.")
            except Exception as e:
                logger.error(f"Error seeding the database: {e}")
        else:
            try:
               await fill_empty_tables_async(session)
               logger.info("Filled empty tables.")
            except Exception as e:
                logger.error(f"Error filling empty tables: {e}")

async def reset_db_async():
    logger.info("Resetting database...")
    async with async_engine.begin() as conn:
        try:
            await conn.run_sync(SQLModel.metadata.drop_all)
            logger.info("Dropped all tables.")
        except Exception as e:
            logger.error(f"Error dropping tables: {e}")
            return
    async with async_session() as session:
        try:
            await seed_grayfox_db_async(session)
            logger.info("Seeded the database after reset.")
        except Exception as e:
            logger.error(f"Error seeding the database after reset: {e}")
