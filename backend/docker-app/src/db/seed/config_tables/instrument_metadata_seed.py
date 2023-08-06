from sqlmodel.ext.asyncio.session import AsyncSession

from src.db.tables.instrument_metadata_table import InstrumentMetadataTable

import pandas as pd
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

INSTRUMENT_METADATA_MAPPING = {'Instrument': 'SYMBOL', 'AssetClass': 'ASSET_CLASS', 'SubClass': 'SUB_CLASS', 'SubSubClass': 'SUB_SUB_CLASS', 'Style': 'STYLE', 'Country': 'COUNTRY', 'Duration': 'DURATION', 'Description': 'DESCRIPTION'}

async def seed_instrumnent_metadata_table(session: AsyncSession):
    logger.info(f"Seeding of instrumnent metadata table started.")
    csv_file_path = "/path/in/container/csvconfig/moreinstrumentinfo.csv"
    df = pd.read_csv(csv_file_path)
    
    df.rename(columns=INSTRUMENT_METADATA_MAPPING, inplace=True)
    
    for _, row in df.iterrows():
        items = InstrumentMetadataTable(**row.to_dict())
        session.add(items)
    
    await session.commit()
    logger.info(f"Seeding of instrumnent metadata table finished.")