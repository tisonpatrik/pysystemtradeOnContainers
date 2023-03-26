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

module "api_gateway" {
  source = "./modules/api_gateway"

  common_tags = local.common_tags
  lambda_function_arns = module.lambda_functions.lambda_function_arns
}

resource "aws_dynamodb_table" "multiple_prices" {
  name           = "multiple_prices"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "Instrument"
  range_key      = "UnixTimeStamp"

  attribute {
    name = "Instrument"
    type = "S"
  }

  attribute {
    name = "UnixTimeStamp"
    type = "S"
  }

  tags = var.common_tags
}
resource "aws_dynamodb_table" "instrument_config" {
  name           = "instrument_config"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "Instrument"

  attribute {
    name = "Instrument"
    type = "S"
  }

  attribute {
    name = "Description"
    type = "S"
  }

  attribute {
    name = "Pointsize"
    type = "N"
  }

  attribute {
    name = "Currency"
    type = "S"
  }

  attribute {
    name = "AssetClass"
    type = "S"
  }

  attribute {
    name = "PerBlock"
    type = "N"
  }

  attribute {
    name = "Percentage"
    type = "N"
  }

  attribute {
    name = "PerTrade"
    type = "N"
  }

  attribute {
    name = "Region"
    type = "S"
  }

  tags = var.common_tags
}
