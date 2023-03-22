import boto3
from datetime import datetime
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource("dynamodb")

def retrieve_prices_from_dynamodb(tableName: str, instrument: str, start_time: int) -> dict: 
    end_time = int(datetime.now().timestamp())
    try:
        table = dynamodb.Table(tableName)
        items = []
        response = table.query(
            KeyConditionExpression=Key('Instrument').eq(instrument) & Key('UnixDateTime').between(start_time, end_time),
        )
        items += response['Items']
        while 'LastEvaluatedKey' in response:
            response = table.query(
                KeyConditionExpression=Key('Instrument').eq(instrument) & Key('UnixDateTime').between(start_time, end_time),
                ExclusiveStartKey=response['LastEvaluatedKey']
            )
            items += response['Items']
        return items

    except Exception as e:
        # log the error message
        raise ValueError("Error occurred while retrieving prices from DynamoDB")