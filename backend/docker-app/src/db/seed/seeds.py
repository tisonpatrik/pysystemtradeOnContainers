from sqlalchemy.orm import sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession
import asyncio

from src.db.seed.config_tables.instrument_config_seed import seed_instrumnent_config_table
from src.db.seed.config_tables.instrument_metadata_seed import seed_instrumnent_metadata_table
from src.db.seed.config_tables.rolling_config_seed import seed_roll_config_table
from src.db.seed.config_tables.spread_cost_seed import seed_spread_cost_table
from src.db.seed.business_data_tables.adjusted_prices_seed import seed_adjusted_prices_table
from src.db.seed.business_data_tables.multiple_prices_seed import seed_multiple_prices_table
from src.db.seed.business_data_tables.fx_prices_seed import seed_fx_prices_table
from src.db.seed.business_data_tables.roll_calendars_seed import seed_roll_calendars_table

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
        await seed_instrumnent_config_table(session),
        await seed_instrumnent_metadata_table(session),
        await seed_roll_config_table(session),
        await seed_spread_cost_table(session)
    
    logger.info(f"Seeding of config tables is finished.")

async def seed_business_data_tables_async(async_session: AsyncSession):
    logger.info(f"Seeding of business data tables started.")
    tasks = [
        seed_multiple_prices_table(async_session),
        seed_adjusted_prices_table(async_session),
        seed_fx_prices_table(async_session),
        seed_roll_calendars_table(async_session)
    ]
    await asyncio.gather(*tasks)
    logger.info(f"Seeding of business data tables is finished.")