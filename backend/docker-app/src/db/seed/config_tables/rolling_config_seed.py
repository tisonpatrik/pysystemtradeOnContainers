from sqlmodel.ext.asyncio.session import AsyncSession

from src.db.tables.config_tables.roll_config_table import RollConfigTable

import pandas as pd
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

ROLL_CONFIG_MAPPING = {'Instrument': 'SYMBOL', 'HoldRollCycle': 'HOLD_ROLL_CYCLE', 'RollOffsetDays': 'ROLL_OFFSET_DAYS', 'CarryOffset': 'CARRY_OFFSET', 'PricedRollCycle': 'PRICED_ROLL_CYCLE', 'ExpiryOffset': 'EXPIRY_OFFSET'}

async def seed_roll_config_table(session: AsyncSession):
    logger.info(f"Seeding of roll_config table started.")
    csv_file_path = "/path/in/container/csvconfig/rollconfig.csv"
    df = pd.read_csv(csv_file_path)
    
    df.rename(columns=ROLL_CONFIG_MAPPING, inplace=True)
    
    for _, row in df.iterrows():
        items = RollConfigTable(**row.to_dict())
        session.add(items)
    
    await session.commit()
    logger.info(f"Seeding of roll_config table finished.")