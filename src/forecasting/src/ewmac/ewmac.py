from typing import Dict, Any, List
from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.data_classes import event_source, SQSEvent
from aws_lambda_powertools.utilities.typing import LambdaContext

logger = Logger()
multiplier = 4

def process_record(record) -> Dict[str, Any]:
    data = record.body
    instrument = data['instrument']
    speed = data['speed']
    raw_data = data['raw_data']

    ewmac = compute_ewmac(raw_data, speed)

    return {
        'message': 'EWMAC calculation and save completed successfully',
        'rule': 'MAC',
        'instrument': instrument,
        'speed': speed,
        'forecast': ewmac
    }

def compute_ewmac(time_series_data, speed: int) -> List[float]:
    Lfast = speed
    Lslow = speed * multiplier
    fast_ewma = time_series_data.ewm(span=Lfast, min_periods=1).mean()
    slow_ewma = time_series_data.ewm(span=Lslow, min_periods=1).mean()
    ewmac = fast_ewma - slow_ewma
    return ewmac

@event_source(data_class=SQSEvent)
def lambda_handler(event: SQSEvent, context: LambdaContext):
    results = [process_record(record) for record in event.records]
    logger.info({"message": "Processed SQS messages", "results": results})