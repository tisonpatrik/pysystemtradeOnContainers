from sqlmodel.ext.asyncio.session import AsyncSession

from src.db.tables.config_tables.instrument_config_table import InstrumentConfigTable

import pandas as pd
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

INSTRUMENTS_CONFIG_MAPPING = {'Instrument': 'SYMBOL', 'Description': 'DESCRIPTION', 'Pointsize': 'POINTSIZE', 'Currency': 'CURRENCY', 'AssetClass': 'ASSET_CLASS', 'PerBlock': 'PER_BLOCK', 'Percentage': 'PERCENTAGE', 'PerTrade': 'PER_TRADE', 'Region': 'REGION'}

async def seed_instrumnent_config_table(session: AsyncSession):
    logger.info(f"Seeding of instrumnent config table started.")
    csv_file_path = "/path/in/container/csvconfig/instrumentconfig.csv"
    df = pd.read_csv(csv_file_path)
    
    df.rename(columns=INSTRUMENTS_CONFIG_MAPPING, inplace=True)
    
    for _, row in df.iterrows():
        items = InstrumentConfigTable(**row.to_dict())
        session.add(items)
    
    await session.commit()
    logger.info(f"Seeding of instrumnent config table finished.")