variable "aws_region" {
  description = "The AWS region to deploy the resources in"
  default     = "eu-central-1"
}

variable "dynamodb_table_name" {
  description = "Name of the DynamoDB table"
  default     = "grayfox_dynamodb_table"
}

variable "lambda_function_names" {
  description = "Names of the Lambda functions"
  type        = list(string)
}
