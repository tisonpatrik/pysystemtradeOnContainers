import aioboto3
from datetime import datetime
from boto3.dynamodb.conditions import Key

def build_key_expression(instrument: str, start_time: int) -> Key:
    end_time = int(datetime.now().timestamp())
    return Key('Instrument').eq(instrument) & Key('UnixDateTime').between(start_time, end_time)

async def paginate_dynamodb_operation(operation, *args, **kwargs):
    items = []
    response = await operation(*args, **kwargs)
    items += response['Items']
    
    while 'LastEvaluatedKey' in response:
        kwargs.update(ExclusiveStartKey=response['LastEvaluatedKey'])
        response = await operation(*args, **kwargs)
        items += response['Items']
    
    return items

async def query_items(table, key_expr):
    return await paginate_dynamodb_operation(table.query, KeyConditionExpression=key_expr)

async def get_time_series_from_dynamodb(tableName: str, instrument: str, start_time: int):
    key_expression = build_key_expression(instrument, start_time)
    table = get_table(tableName)
    items = await query_items(table, key_expression)    
    return items

async def batch_write_to_dynamodb(table_name, items):
    table = get_table(table_name)

    async with table.batch_writer() as batch:
        for item in items:
            await batch.put_item(Item=item)

async def write_daily_prices(tableName: str, dailyPrices: dict):
    def to_batch_item(dailyPrice):
        return {'PutRequest': {'Item': dailyPrice}}

    batch_items = list(map(to_batch_item, dailyPrices))

    for i in range(0, len(batch_items), 25):
        await batch_write_to_dynamodb(tableName, batch_items[i:i+25])

async def get_table(tableName: str):
    session = aioboto3.Session()
    async with session.resource('dynamodb') as dynamodb:
        return await dynamodb.Table(tableName)