from sqlmodel.ext.asyncio.session import AsyncSession

from src.db.tables.config_tables.spread_costs_table import SpreadCostTable

import pandas as pd
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SPREAD_COST_MAPPING = {'Instrument': 'SYMBOL', 'SpreadCost': 'SPREAD_COST'}

async def seed_spread_cost_table(session: AsyncSession):
    logger.info(f"Seeding of spread cost table started.")
    csv_file_path = "/path/in/container/csvconfig/spreadcosts.csv"
    df = pd.read_csv(csv_file_path)
    
    df.rename(columns=SPREAD_COST_MAPPING, inplace=True)
    
    for _, row in df.iterrows():
        items = SpreadCostTable(**row.to_dict())
        session.add(items)
    
    await session.commit()
    logger.info(f"Seeding of spread cost table finished.")