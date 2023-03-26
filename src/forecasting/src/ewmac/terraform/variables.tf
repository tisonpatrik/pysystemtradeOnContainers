variable "aws_region" {
  type = string
  description = "The AWS region where the resources will be created"
}

variable "lambda_iam_role_name" {
  type = string
  description = "The name of the IAM role for the Lambda function"
}

variable "lambda_zip_file_path" {
  type = string
  description = "The path to the Lambda function's deployment package (ZIP file)"
}

variable "lambda_function_name" {
  type = string
  description = "The name of the Lambda function"
}

variable "lambda_handler_function_name" {
  type = string
  description = "The name of the handler function in the Lambda function code"
}

variable "lambda_runtime" {
  type = string
  description = "The runtime environment for the Lambda function"
}

variable "lambda_timeout" {
  type = number
  description = "The maximum amount of time (in seconds) that the Lambda function can run before timing out"
}

variable "lambda_memory_size" {
  type = number
  description = "The amount of memory (in MB) to allocate to the Lambda function"
}

variable "dynamodb_table_name" {
  type = string
  description = "The name of the DynamoDB table for storing data"
}

variable "sqs_queue_name" {
  type = string
  description = "The name of the SQS queue for the Lambda function to consume from"
}
