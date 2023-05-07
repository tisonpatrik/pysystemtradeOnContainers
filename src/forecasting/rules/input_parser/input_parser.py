import os
import json
import boto3
from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.typing import LambdaContext
from boto3.dynamodb.conditions import Key

logger = Logger()

# Initialize Step Functions and DynamoDB clients
stepfunctions = boto3.client('stepfunctions')
dynamodb = boto3.resource('dynamodb')

# Retrieve the Step Function ARN and DynamoDB table name from the environment variables
FORECAST_WORKFLOW_ARN = os.environ["FORECAST_WORKFLOW_ARN"]
MULTIPLE_PRICES = os.environ["MULTIPLE_PRICES"]

def lambda_handler(event, context: LambdaContext):
    logger.info(f"Received event: {json.dumps(event)}")
    
    # Access the DynamoDB table and check if the item count is equal to 730
    table = dynamodb.Table(MULTIPLE_PRICES)

    # Extract the instrument from the event
    instrument = event['Records'][0]['dynamodb']['NewImage']['instrument']['S']
    
    # Query the table for the specified instrument sorted by UnixTimeDate
    response = table.query(
        KeyConditionExpression=Key('instrument').eq(instrument),
        ScanIndexForward=True,
    )
    
    # Check if the time series length is less than 2 years (730 days)
    if len(response['Items']) < 730:
        # Fetch the missing data
        missing_data = []  # Replace this with the actual code to fetch missing data
        
        # Append the missing data to the event
        for item in missing_data:
            event['Records'].append({
                'dynamodb': {
                    'NewImage': item
                }
            })

    try:
        # Trigger the data_processing_workflow Step Function with the event data
        response = stepfunctions.start_execution(
            stateMachineArn=FORECAST_WORKFLOW_ARN,
            input=json.dumps(event)
        )
        logger.info(f"Step Function started: {response['executionArn']}")

    except Exception as e:
        logger.exception(f"Failed to start Step Function: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({
                "error": "Failed to start Step Function",
                "message": str(e)
            })
        }

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Step Function started successfully",
            "executionArn": response['executionArn']
        })
    }
