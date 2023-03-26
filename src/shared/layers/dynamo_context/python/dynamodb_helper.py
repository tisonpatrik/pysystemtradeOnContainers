import boto3

dynamodb = boto3.resource("dynamodb")

def batch_write_to_dynamodb(table_name, items):
    """
    Batch write a list of items to DynamoDB table.
    """
    table = dynamodb.Table(table_name)
    with table.batch_writer() as batch:
        for item in items:
            batch.put_item(Item=item)