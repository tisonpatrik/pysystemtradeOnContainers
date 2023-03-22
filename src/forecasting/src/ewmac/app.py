import os
import boto3
import pandas as pd
from boto3.dynamodb.conditions import Key
from aws_lambda_powertools import Logger
from aws_lambda_powertools.event_handler import APIGatewayRestResolver
from aws_lambda_powertools.logging import correlation_paths
from aws_lambda_powertools.utilities.typing import LambdaContext

logger = Logger()
app = APIGatewayRestResolver()

TABLE_NAME = os.environ["TABLE_NAME"]

@app.post("/ewmac")
def calculate_ewmac():   
    data = app.current_event.json_body
    instrument = data['instrument']
    speed = data['speed']

    table = get_table_resource()
    # Retrieve the time series data for the instrument from the DynamoDB table
    time_series_data = get_time_series_data(instrument, table)

    # Calculate the EWMAC trading rule using the time series data
    ewmac = compute_ewmac(time_series_data, speed)

    # Save the EWMAC list to DynamoDB
    save_ewmac_to_dynamodb(table, ewmac, instrument, speed)

    # Return a confirmation message and the input parameters as the result of the function
    return {
        'message': 'EWMAC calculation and save completed successfully',
        'rule': 'MAC',
        'instrument': instrument,
        'speed': speed
    }

def get_table_resource():
    dynamodb_resource = boto3.resource("dynamodb")
    table_name = os.environ[TABLE_NAME]
    return dynamodb_resource.Table(table_name)

def get_time_series_data(instrument, table):
    # Connect to the DynamoDB table and retrieve the time series data for the instrument
    response = table.query(
        KeyConditionExpression=Key('instrument').eq(instrument)
    )
    items = response['Items']

    # Convert the time series data to a Pandas DataFrame
    df = pd.DataFrame(items, columns=['datetime', 'price'])
    return df

def save_ewmac_to_dynamodb(table,ewmac, instrument, speed):
    # Convert the EWMAC list to a DynamoDB-compatible format
    ewmac_items = [{'value': {'N': str(value)}} for value in ewmac]

    # Define the primary key for the EWMAC item
    primary_key = {
        'instrument': {'S': instrument},
        'speed': {'N': str(speed)}
    }
    
    # Save the EWMAC item to the DynamoDB table
    table.put_item(TableName='ewmac_table', Item=primary_key, EWMAC=ewmac_items)

def compute_ewmac(time_series_data, speed):
    # Calculate the EWMAC trading rule
    Lfast = speed
    Lslow = speed * 4
    fast_ewma = time_series_data['price'].ewm(span=Lfast).mean()
    slow_ewma = time_series_data['price'].ewm(span=Lslow).mean()
    ewmac = fast_ewma - slow_ewma
    return ewmac

@logger.inject_lambda_context(correlation_id_path=correlation_paths.API_GATEWAY_REST)
def lambda_handler(event: dict, context: LambdaContext) -> dict:
    return app.resolve(event, context)

