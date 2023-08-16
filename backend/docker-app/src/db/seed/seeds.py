from sqlalchemy.orm import sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession
import asyncio

from src.db.seed.business_data_tables.raw_adjusted_prices_seed import seed_raw_adjusted_prices_table
from src.db.seed.business_data_tables.raw_multiple_prices_seed import seed_raw_multiple_prices_table
from src.db.seed.business_data_tables.fx_prices_seed import seed_fx_prices_table
from src.db.seed.business_data_tables.roll_calendars_seed import seed_roll_calendars_table

from src.db.seed.daily_prices_tables.multiple_prices_seed import seed_daily_multiple_prices_table

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def seed_grayfox_db(async_session: sessionmaker):
   logger.info(f"Seeding of grayfox_db started.")
   await seed_config_tables_async(async_session)
   await seed_business_data_tables_async(async_session)
   logger.info(f"Seeding of grayfox_db is finished.")

async def seed_config_tables_async(async_session: AsyncSession):
    logger.info(f"Seeding of config tables started.")

    logger.info(f"Seeding of config tables is finished.")

async def seed_business_data_tables_async(async_session: AsyncSession):
    logger.info(f"Seeding of business data tables started.")
    tasks = [
        handle_seeding(seed_raw_multiple_prices_table, async_session, "Raw Multiple Prices Table"),
        handle_seeding(seed_raw_adjusted_prices_table, async_session, "Raw Adjusted Prices Table"),
        handle_seeding(seed_fx_prices_table, async_session, "FX Prices Table"),
        handle_seeding(seed_roll_calendars_table, async_session, "Roll Calendars Table")
    ]
    await asyncio.gather(*tasks)
    logger.info(f"Seeding of business data tables is finished.")

async def seed_daily_prices():
    logger.info(f"Seeding of daily prices tables started.")
    await seed_daily_multiple_prices_table()
    logger.info(f"Seeding of daily prices tables is finished.")
 
async def handle_seeding(seed_function, session, table_name: str):
    try:
        await seed_function(session)
        logger.info(f"Seeding of {table_name} is successful.")
    except Exception as e:
        logger.error(f"Error seeding {table_name}: {e}")
