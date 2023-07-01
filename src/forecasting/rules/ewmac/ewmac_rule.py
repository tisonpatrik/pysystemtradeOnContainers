import json
from typing import Dict, Any
from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.typing import LambdaContext
from core.rules.ewmac import EWMAComputer

logger = Logger()

def lambda_handler(event: Dict[str, Any], context: LambdaContext):
    try:
        data = json.loads(event['body'])
        ewmac_computer = EWMAComputer(data, data['speed'])
        result = ewmac_computer.process_data()
        logger.info({"message": "Processed input data", "result": result})
        return {
            'statusCode': 200,
            'body': json.dumps(result)
        }
    except Exception as e:
        logger.exception("Error processing input data")
        return {
            'statusCode': 500,
            'body': json.dumps({"message": str(e)})
        }