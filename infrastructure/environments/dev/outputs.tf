output "vpc_id" {
  value = aws_vpc.grayfox_vpc.id
  description = "VPC ID for the grayfox dev environment"
}
output "public_subnet_ids" {
  value       = aws_subnet.public.*.id
  description = "The IDs of the public subnets created in the VPC"
}
output "internet_gateway_id" {
  value       = aws_internet_gateway.igw.id
  description = "The ID of the Internet Gateway attached to the VPC"
}

output "lambda_bucket_id" {
  value       = aws_s3_bucket.lambda_bucket.id
  description = "The ID of the S3 bucket for storing Lambda function packages"
}




output "lambda_security_group_id" {
  value       = aws_security_group.lambda.id
  description = "The ID of the security group used for Lambda functions"
}
output "forecasting_lambda_role_arn" {
  value       = aws_iam_role.forecasting_lambda_role.arn
  description = "The ARN of the IAM role for Forecasting domain Lambda functions"
}
output "forecasting_lambda_log_group_arn" {
  value       = aws_cloudwatch_log_group.forecasting_lambda_log_group.arn
  description = "The ARN of the CloudWatch log group for the Forecasting domain Lambda functions"
}

