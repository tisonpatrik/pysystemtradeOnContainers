import aioboto3
from datetime import datetime
from boto3.dynamodb.conditions import Key

dynamodb = aioboto3.resource("dynamodb")

def build_key_expression(instrument: str, start_time: int) -> Key:
    """
    Build a Key expression for DynamoDB query or scan operation.
    """
    end_time = int(datetime.now().timestamp())
    return Key('Instrument').eq(instrument) & Key('UnixDateTime').between(start_time, end_time)

async def query_items(table, key_expr):
    """
    Retrieve all items from a DynamoDB table that match the specified Key expression.
    """
    items = []
    response = await table.query(KeyConditionExpression=key_expr)
    items += response['Items']
    while 'LastEvaluatedKey' in response:
        response = await table.query(KeyConditionExpression=key_expr, ExclusiveStartKey=response['LastEvaluatedKey'])
        items += response['Items']
    return items
async def scan_items(table, key_expr):
    """
    Retrieve all items from a DynamoDB table that match the specified Key expression.
    """
    items = []
    response = await table.scan(FilterExpression=key_expr)
    items += response['Items']
    while 'LastEvaluatedKey' in response:
        response = await table.scan(FilterExpression=key_expr, ExclusiveStartKey=response['LastEvaluatedKey'])
        items += response['Items']
    return items

async def get_time_series_from_dynamodb(tableName: str, instrument: str, start_time: int):
    """
    Retrieve a list of daily prices from a DynamoDB table for a given instrument and time range.
    """
    key_expression = build_key_expression(instrument, start_time)
    table = dynamodb.Table(tableName)
    if key_expression.__sizeof__() <= 4000:
        items = await query_items(table, key_expression)
    else:
        items = await scan_items(table, key_expression)
    return items
