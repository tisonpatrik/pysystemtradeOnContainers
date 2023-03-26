output "lambda_function_arn" {
  value = aws_lambda_function.lambda.arn
}

output "sqs_queue_url" {
  value = aws_sqs_queue.sqs.url
}
