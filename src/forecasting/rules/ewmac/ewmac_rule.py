import json
import pandas as pd
from typing import Dict, Any
from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.typing import LambdaContext
from shared.layers.helpers.python.estimators.vol import robust_vol_calc
logger = Logger()

def process_data(data: Dict[str, Any]) -> Dict[str, Any]:
    instrument = data['instrument']
    speed = data['speed']
    raw_data = data['raw_data']
    volatility = robust_vol_calc(raw_data)
    ewmac = compute_ewmac(raw_data, speed, volatility)

    return {
        'message': 'EWMAC calculation and save completed successfully',
        'rule': 'MAC',
        'instrument': instrument,
        'speed': speed,
        'forecast': ewmac
    }

def validate_speed(speed: int):
    if speed <= 0:
        raise ValueError("Speed should be a positive integer")

def validate_time_series_data(time_series_data: pd.Series):
    if time_series_data.empty:
        raise ValueError("Time series data cannot be empty")

def compute_ewmac(time_series_data: pd.Series, speed: int, volatility: pd.Series) -> pd.Series:
    validate_speed(speed)
    validate_time_series_data(time_series_data)

    Lfast = speed
    Lslow = speed * 4
    fast_ewma = time_series_data.ewm(span=Lfast, min_periods=1).mean()
    slow_ewma = time_series_data.ewm(span=Lslow, min_periods=1).mean()
    ewmac = fast_ewma - slow_ewma

    return ewmac / volatility.ffill()

def lambda_handler(event: Dict[str, Any], context: LambdaContext):
    try:
        data = json.loads(event['body'])
        result = process_data(data)
        logger.info({"message": "Processed input data", "result": result})
        return {
            'statusCode': 200,
            'body': json.dumps(result)
        }
    except Exception as e:
        logger.exception("Error processing input data")
        return {
            'statusCode': 500,
            'body': json.dumps({"message": str(e)})
        }
