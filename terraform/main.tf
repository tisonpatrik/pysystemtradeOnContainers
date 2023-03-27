provider "aws" {
  region = var.aws_region
}

locals {
  common_tags = {
    Project = "grayfox"
  }
}

module "dynamodb" {
  source = "./modules/dynamodb"

  common_tags = local.common_tags
}

module "lambda_functions" {
  source = "./modules/lambda_functions"

  common_tags = local.common_tags
  dynamodb_table_arn = module.dynamodb.dynamodb_table_arn
}