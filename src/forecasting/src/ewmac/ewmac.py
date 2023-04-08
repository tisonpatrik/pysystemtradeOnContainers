import os
from typing import Dict, Any, List
from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.data_classes import event_source, SQSEvent
from aws_lambda_powertools.utilities.typing import LambdaContext
from time_series_layer import get_time_series_from_dynamodb, write_daily_prices

logger = Logger()

def get_config() -> Dict[str, str]:
    return {
        "RAW_DATA_TABLE": os.environ["RAW_DATA_TABLE"],
        "RAW_FORECAST_TABLE": os.environ["RAW_FORECAST_TABLE"]
    }

config = get_config()

async def process_record(record) -> Dict[str, Any]:
    data = record.body
    instrument = data['instrument']
    speed = data['speed']

    ewmac = await compute_and_save_ewmac(instrument, speed)

    return {
        'message': 'EWMAC calculation and save completed successfully',
        'rule': 'MAC',
        'instrument': instrument,
        'speed': speed
    }

async def compute_and_save_ewmac(instrument: str, speed: int) -> List[float]:
    time_series_data = await get_time_series_from_dynamodb(config["RAW_DATA_TABLE"], instrument)
    ewmac = compute_ewmac(time_series_data, speed)
    await write_daily_prices(config["RAW_FORECAST_TABLE"], ewmac, instrument, speed)
    return ewmac

def compute_ewmac(time_series_data, speed: int) -> List[float]:
    Lfast = speed
    Lslow = speed * 4
    fast_ewma = time_series_data.ewm(span=Lfast, min_periods=1).mean()
    slow_ewma = time_series_data.ewm(span=Lslow, min_periods=1).mean()
    ewmac = fast_ewma - slow_ewma
    return ewmac

@event_source(data_class=SQSEvent)
async def lambda_handler(event: SQSEvent, context: LambdaContext):
    results = [await process_record(record) for record in event.records]
