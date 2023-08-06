from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.future import Connection

from src.db.tables.multiple_prices_table import MultiplePricesTable
from src.db.tables.adjusted_prices_table import AdjustedPricesTable
from src.db.tables.fx_prices_table import FxPricesTable
from src.db.tables.roll_calendars_table import RollCalendarsTable

from src.db.seed.config_tables.instrument_config_seed import seed_instrumnent_config_table
from src.db.seed.config_tables.instrument_metadata_seed import seed_instrumnent_metadata_table
from src.db.seed.config_tables.rolling_config_seed import seed_roll_config_table
from src.db.seed.config_tables.spread_cost_seed import seed_spread_cost_table

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Column mappings for each table
MULTIPLE_PRICES_MAPPING = {'CARRY': 'CARRY', 'CARRY_CONTRACT': 'CARRY_CONTRACT', 'PRICE': 'PRICE', 'PRICE_CONTRACT': 'PRICE_CONTRACT', 'FORWARD': 'FORWARD', 'FORWARD_CONTRACT': 'FORWARD_CONTRACT'}
ADJUSTED_PRICES_MAPPING = {'PRICE': 'price'}
FX_PRICES_MAPPING = {'PRICE': 'PRICE'}
ROLL_CALENDAR_MAPPING = {'CURRENT_CONTRACT': 'current_contract', 'NEXT_CONTRACT': 'next_contract', 'CARRY_CONTRACT':'carry_contract'}

# Configuration for tables and their corresponding directories
TABLES_TO_SEED = [
    {"model": MultiplePricesTable, "directory": "/path/in/container/multiple_prices_csv", "mapping": MULTIPLE_PRICES_MAPPING},
    {"model": AdjustedPricesTable, "directory": "/path/in/container/adjusted_prices_csv", "mapping": ADJUSTED_PRICES_MAPPING},
    {"model": FxPricesTable, "directory": "/path/in/container/fx_prices_csv", "mapping": FX_PRICES_MAPPING},
    {"model": RollCalendarsTable, "directory": "/path/in/container/roll_calendars_csv", "mapping": ROLL_CALENDAR_MAPPING}
]

async def seed_grayfox_db(session: AsyncSession):
   logger.info(f"Seeding of grayfox_db started.")
   await seed_config_tables_async(session)
   await seed_business_data_tables_async(session)
   logger.info(f"Seeding of grayfox_db is finished.")

async def seed_config_tables_async(session: AsyncSession):
    logger.info(f"Seeding of config tables started.")
    await seed_instrumnent_config_table(session)
    await seed_instrumnent_metadata_table(session)
    await seed_roll_config_table(session)
    await seed_spread_cost_table(session)
    logger.info(f"Seeding of config tables is finished.")

async def seed_business_data_tables_async(session: AsyncSession):
    logger.info(f"Seeding of business data tables started.")
    
    logger.info(f"Seeding of business data tables is finished.")