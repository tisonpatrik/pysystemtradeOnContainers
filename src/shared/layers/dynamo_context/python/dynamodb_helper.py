import aioboto3

dynamodb = aioboto3.resource("dynamodb")

async def batch_write_to_dynamodb(table_name, items):
    """
    Batch write a list of items to DynamoDB table.
    """
    table = dynamodb.Table(table_name)

    async with table.batch_writer() as batch:
        for item in items:
            await batch.put_item(Item=item)
