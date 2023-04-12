import boto3
import json

# Initialize the Step Functions client
stepfunctions = boto3.client('stepfunctions')

# The ARN of your Step Function State Machine
STATE_MACHINE_ARN = 'arn:aws:states:REGION:ACCOUNT_ID:stateMachine:your-state-machine-name'

def process_dynamodb_record(record):
    # Extract the new item from the DynamoDB Stream record
    new_item = record['dynamodb']['NewImage']

    # Process the new item as needed
    # For example, convert the new_item to the format required by your Step Function
    processed_item = {
        'key': new_item['key']['S'],
        'value': new_item['value']['N']
    }

    return processed_item

def lambda_handler(event, context):
    # Process each record in the DynamoDB Stream event
    processed_items = [process_dynamodb_record(record) for record in event['Records']]

    # Start the Step Function with the batch of processed items
    response = stepfunctions.start_execution(
        stateMachineArn=STATE_MACHINE_ARN,
        input=json.dumps({
            'batch': processed_items
        })
    )

    print(f'Started Step Function execution: {response["executionArn"]}')

    return {
        'statusCode': 200,
        'body': json.dumps('Success')
    }
