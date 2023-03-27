import aioboto3
from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.data_classes import event_source, SQSEvent
from aws_lambda_powertools.utilities.typing import LambdaContext
from get_time_series import get_time_series_from_dynamodb
from write_time_series import write_daily_prices

logger = Logger()

dynamodb_resource = aioboto3.resource("dynamodb")

async def process_record(record):
    data = record.body
    instrument = data['instrument']
    speed = data['speed']

    table = dynamodb_resource.Table("multiple_prices")
    # Retrieve the time series data for the instrument from the DynamoDB table
    time_series_data = await get_time_series_from_dynamodb(table, instrument)

    # Calculate the EWMAC trading rule using the time series data
    ewmac = compute_ewmac(time_series_data, speed)

    # Save the EWMAC list to DynamoDB
    await write_daily_prices(table, ewmac, instrument, speed)

    # Return a confirmation message and the input parameters
        # Return a confirmation message and the input parameters as the result of the function
    return {
        'message': 'EWMAC calculation and save completed successfully',
        'rule': 'MAC',
        'instrument': instrument,
        'speed': speed
    }

def compute_ewmac(time_series_data, speed):
    # Calculate the EWMAC trading rule
    Lfast = speed
    Lslow = speed * 4
    fast_ewma = time_series_data.ewm(span=Lfast, min_periods=1).mean()
    slow_ewma = time_series_data.ewm(span=Lslow, min_periods=1).mean()
    ewmac = fast_ewma - slow_ewma
    return ewmac

@event_source(data_class=SQSEvent)
async def lambda_handler(event: SQSEvent, context: LambdaContext):
    results = []
    for record in event.records:
        result = await process_record(record)
        results.append(result)


