import boto3
from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.batch import BatchProcessor, EventType, batch_processor
from aws_lambda_powertools.utilities.data_classes.sqs_event import SQSRecord
from aws_lambda_powertools.utilities.typing import LambdaContext
from dynamo_context import get_time_series, write_time_series

logger = Logger()
processor = BatchProcessor(event_type=EventType.SQS)

dynamodb_resource = boto3.resource("dynamodb")


def record_handler(record: SQSRecord):
    data = record.body
    instrument = data['instrument']
    speed = data['speed']

    table = dynamodb_resource.Table("multiple_prices")
    # Retrieve the time series data for the instrument from the DynamoDB table
    time_series_data = get_time_series.get_time_series_from_dynamodb(instrument, table)

    # Calculate the EWMAC trading rule using the time series data
    ewmac = compute_ewmac(time_series_data, speed)

    # Save the EWMAC list to DynamoDB
    write_time_series.write_daily_prices(table, ewmac, instrument, speed)

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
    fast_ewma = time_series_data.ewm(span=Lfast,min_periods=1).mean()
    slow_ewma = time_series_data.ewm(span=Lslow,min_periods=1).mean()
    ewmac = fast_ewma - slow_ewma
    return ewmac


@batch_processor(record_handler=record_handler, processor=processor)
def lambda_handler(event, context: LambdaContext):
    return processor.response()
