"""
Database Utility Module
-----------------------
This module provides database utility functions and configurations using SQLAlchemy. 
It includes the creation of an asynchronous engine and session factory, 
as well as a method to get a database session.
"""

from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from common.src.database.settings import settings as global_settings
from common.src.logging.logger import AppLogger

logger = AppLogger.get_instance().get_logger()

if global_settings.database_url is None:
    raise ValueError("Database URL must be set")


async def get_db() -> AsyncGenerator:
    """
    Generate a new database session using an asynchronous session maker.
    Yields a new session that is closed when exiting the context.
    """
    engine = create_async_engine(
        global_settings.database_url.unicode_string(),  # type: ignore
        future=True,
        echo=False,
        pool_size=10,
        max_overflow=20,
    )
    # expire_on_commit=False will prevent attributes from being expired
    # after commit.
    AsyncSessionFactory = async_sessionmaker(
        engine,
        autoflush=False,
        expire_on_commit=False,
    )
    async with AsyncSessionFactory() as session:
        # logger.debug(f"ASYNC Pool: {engine.pool.status()}")
        yield session
