resource "aws_vpc" "grayfox_vpc" {
  cidr_block = var.vpc_cidr
  tags = {
    Name = "${var.app_name}-${var.enviroment_name}-vpc"
  }
}
data "aws_availability_zones" "available" {
  state = "available"
}

## VPC
resource "aws_subnet" "public" {
  count = length(data.aws_availability_zones.available.names)

  cidr_block = "10.0.${count.index + 1}.0/24"
  vpc_id     = aws_vpc.grayfox_vpc.id

  tags = {
    Name = "${var.app_name}-${var.enviroment_name}-public-subnet-${count.index + 1}"
  }
}
resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.grayfox_vpc.id

  tags = {
    Name = "${var.app_name}-${var.enviroment_name}-igw"
  }
}
resource "aws_route_table" "public" {
  vpc_id = aws_vpc.grayfox_vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.igw.id
  }

  tags = {
    Name = "${var.app_name}-${var.enviroment_name}-public-rt"
  }
}
resource "aws_route_table_association" "public" {
  count          = length(aws_subnet.public)
  subnet_id      = aws_subnet.public[count.index].id
  route_table_id = aws_route_table.public.id
}
resource "aws_security_group" "lambda" {
  name        = "${var.app_name}-${var.enviroment_name}-lambda-sg"
  description = "Security group for Lambda function"
  vpc_id      = aws_vpc.grayfox_vpc.id
}

## S3
resource "aws_s3_bucket" "lambda_bucket" {
  bucket = "${var.app_name}-${var.enviroment_name}-lambda"
}

## Rules Lambdas
resource "aws_iam_role" "forecasting_lambda_role" {
  name = "${var.app_name}-${var.enviroment_name}-forecasting-lambda-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}
resource "aws_iam_role_policy" "forecasting_lambda_policy" {
  name = "${var.app_name}-${var.enviroment_name}-forecasting-lambda-policy"
  role = aws_iam_role.forecasting_lambda_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ]
        Effect   = "Allow"
        Resource = "*"
      }
    ]
  })
}
resource "aws_cloudwatch_log_group" "forecasting_lambda_log_group" {
  name              = "/aws/lambda/${var.app_name}-${var.enviroment_name}-forecasting"
  retention_in_days = 3
}
data "archive_file" "breakout_rule" {
  type = "zip"

  source_file  = "${path.root}/../../../src/forecasting/rules/breakout/breakout_rule.py"
  output_path = "${path.root}/../../../dist/breakout_rule.zip"
}

resource "aws_s3_object" "breakout_rule_zip" {
  bucket = aws_s3_bucket.lambda_bucket.id

  key    = "breakout_rule.zip"
  source = data.archive_file.breakout_rule.output_path

  etag = filemd5(data.archive_file.breakout_rule.output_path)
}
