provider "aws" {
  region = var.region
}

resource "aws_lambda_layer_version" "dynamo_context" {
  filename   = "dynamo_context.zip"
  layer_name = var.layer_name
  compatible_runtimes = [
    "python3.9"
  ]
  description = var.description
  license_info = var.license_info
}
