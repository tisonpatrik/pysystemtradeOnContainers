from sqlalchemy.orm import sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession
import asyncio

from src.db.seed.config_tables.instrument_config_seed import seed_instrumnent_config_table
from src.db.seed.config_tables.instrument_metadata_seed import seed_instrumnent_metadata_table
from src.db.seed.config_tables.rolling_config_seed import seed_roll_config_table
from src.db.seed.config_tables.spread_cost_seed import seed_spread_cost_table
from src.db.seed.business_data_tables.raw_adjusted_prices_seed import seed_raw_adjusted_prices_table
from src.db.seed.business_data_tables.raw_multiple_prices_seed import seed_raw_multiple_prices_table
from src.db.seed.business_data_tables.fx_prices_seed import seed_fx_prices_table
from src.db.seed.business_data_tables.roll_calendars_seed import seed_roll_calendars_table

from src.db.seed.daily_prices_tables.adjusted_prices_seed import seed_daily_adjusted_prices_table
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
    async with async_session() as session:
        await handle_seeding(seed_instrumnent_config_table, session, "Instrument Config Table"),
        await handle_seeding(seed_instrumnent_metadata_table, session, "Instrument Metadata Table"),
        await handle_seeding(seed_roll_config_table, session, "Roll Config Table"),
        await handle_seeding(seed_spread_cost_table, session, "Spread Cost Table")
    
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

async def seed_daily_prices(async_session: AsyncSession):
    logger.info(f"Seeding of daily prices tables started.")
    handle_seeding(seed_daily_multiple_prices_table, async_session, "Daily Multiple Prices Table"),
    handle_seeding(seed_daily_adjusted_prices_table, async_session, "Daily Adjusted Prices Table"),
    logger.info(f"Seeding of daily prices tables is finished.")
 
async def handle_seeding(seed_function, session, table_name: str):
    try:
        await seed_function(session)
        logger.info(f"Seeding of {table_name} is successful.")
    except Exception as e:
        logger.error(f"Error seeding {table_name}: {e}")

        