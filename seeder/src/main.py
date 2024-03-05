import sys
from pathlib import Path

root_path = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(root_path))


from fastapi import FastAPI

from common.src.logging.logger import AppLogger
from data_management.src.app.csv_to_db_configs.config_files_config import (
    InstrumentConfigConfig,
    InstrumentMetadataConfig,
    RollConfigConfig,
    SpreadCostConfig,
)
from seeder.src.csv_loader import get_full_path, load_csv

logger = AppLogger.get_instance().get_logger()

app = FastAPI()


@app.get("/")
async def root():
    """
    Root endpoint returning a ping response.
    """
    return {"Ping": "Pong!"}
