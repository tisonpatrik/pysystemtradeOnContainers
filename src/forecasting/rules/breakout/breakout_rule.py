import json
import pandas as pd
import numpy as np
from typing import Dict, Any
from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.typing import LambdaContext

logger = Logger()

def process_data(data: Dict[str, Any]) -> Dict[str, Any]:
    instrument = data['instrument']
    speed = data['speed']
    raw_data = data['raw_data']

    forecast = compute_breakdown(raw_data, speed)

    return {
        'message': 'Breakdown calculation and save completed successfully',
        'rule': 'Breakdown',
        'instrument': instrument,
        'speed': speed,
        'forecast': forecast
    }

def compute_breakdown(price: pd.Series, speed: int, smooth=None) -> pd.Series:

    if smooth is None:
        smooth = max(int(speed / 4.0), 1)

    assert smooth < speed

    roll_max = price.rolling(
        speed, min_periods=int(min(len(price), np.ceil(speed / 2.0)))
    ).max()
    roll_min = price.rolling(
        speed, min_periods=int(min(len(price), np.ceil(speed / 2.0)))
    ).min()

    roll_mean = (roll_max + roll_min) / 2.0

    output = 40.0 * ((price - roll_mean) / (roll_max - roll_min))
    smoothed_output = output.ewm(span=smooth, min_periods=np.ceil(smooth / 2.0)).mean()

    return smoothed_output

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
