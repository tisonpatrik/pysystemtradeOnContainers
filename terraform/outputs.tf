output "lambda_function_arns" {
  description = "ARNs of the Lambda functions"
  value       = module.lambda_functions.lambda_function_arns
}