module "vpc" {
  source = "terraform-aws-modules/vpc/aws"

  name = "${var.app_name}-${var.enviroment}-vpc"
  cidr = "10.10.0.0/16"

  # Specify at least one of: intra_subnets, private_subnets, or public_subnets
  azs           = ["eu-central-1a", "eu-central-1b"]
  intra_subnets = ["10.10.101.0/24", "10.10.102.0/24"]
}

module "breakout_rule" {
  source = "terraform-aws-modules/lambda/aws"

  function_name = "${var.app_name}-${var.enviroment}-breakout_rule"
  description   = "Breakout rule Lambda function"
  handler       = "breakout_rule.lambda_handler"
  runtime       = "python3.9"

  source_path = "${path.root}/../../../src/forecasting/rules/breakout/breakout_rule.py"

  vpc_subnet_ids         = module.vpc.intra_subnets
  vpc_security_group_ids = [module.vpc.default_security_group_id]
  attach_network_policy = true

  cloudwatch_logs_retention_in_days = 7
  timeout =  60
  memory_size = 512
  layers = [ "arn:aws:lambda:eu-central-1:336392948345:layer:AWSSDKPandas-Python39:6", "arn:aws:lambda:eu-central-1:017000801446:layer:AWSLambdaPowertoolsPythonV2:31" ]

  putin_khuylo =  true
  tags = {
    Name = "breakout_rule"
  }
}