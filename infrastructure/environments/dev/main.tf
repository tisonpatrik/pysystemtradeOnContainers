module "vpc" {
  source = "terraform-aws-modules/vpc/aws"

  name = "grayfox-vpc"
  cidr = "10.0.0.0/16"
  azs  = formatlist("${var.aws_region}%s", ["a", "b"])
  tags = {
    Terraform = "true"
    Environment = "dev"
  }
}

module "breakout_rule" {
  source = "terraform-aws-modules/lambda/aws"

  function_name = "breakout_rule"
  description   = "Breakout rule Lambda function"
  handler       = "breakout_rule.handler"
  runtime       = "python3.9"

  source_path = "${path.root}/../../../src/forecasting/rules/breakout/breakout_rule.py"
  timeout =  60
  vpc_security_group_ids = [module.vpc.default_security_group_id]
  tags = {
    Name = "breakout_rule"
  }
}