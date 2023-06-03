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
module "ewmac_rule" {
  source = "terraform-aws-modules/lambda/aws"

  function_name = "${var.app_name}-${var.enviroment}-ewmac_rule"
  description   = "EWMAC rule Lambda function"
  handler       = "ewmac_rule.lambda_handler"
  runtime       = "python3.9"

  source_path = "${path.root}/../../../src/forecasting/rules/ewmac/ewmac_rule.py"

  vpc_subnet_ids         = module.vpc.intra_subnets
  vpc_security_group_ids = [module.vpc.default_security_group_id]
  attach_network_policy = true

  cloudwatch_logs_retention_in_days = 7
  timeout =  60
  memory_size = 512
  layers = [ "arn:aws:lambda:eu-central-1:336392948345:layer:AWSSDKPandas-Python39:6", 
             "arn:aws:lambda:eu-central-1:017000801446:layer:AWSLambdaPowertoolsPythonV2:31",
              module.helper_layer_local.lambda_layer_arn, # Add your custom layer ARN
             ]

  putin_khuylo =  true
  tags = {
    Name = "ewmac_rule"
  }
}
module "helper_layer_local" {
  source = "terraform-aws-modules/lambda/aws"

  create_layer = true

  layer_name          = "helpers"
  description         = "My helpers for trading calculations"
  compatible_runtimes = ["python3.9"]

  source_path = "${path.root}/../../../src/shared/layers/helpers"
}

# module "step_function" {
#   source = "terraform-aws-modules/step-functions/aws"

#   name       = "my-step-function"
#   definition = jsonencode(local.state_machine_definition)

#   service_integrations = {
#     lambda = {
#       lambda = [
#         "arn:aws:lambda:REGION:ACCOUNT_ID:function:ParseInputFunction",
#         "arn:aws:lambda:REGION:ACCOUNT_ID:function:MACFunction",
#         "arn:aws:lambda:REGION:ACCOUNT_ID:function:BreakoutFunction",
#       ]
#     }
#   }

#   type = "STANDARD"

#   tags = {
#     Example = "AWS Step Function for Business Rules"
#   }
# }

# locals {
#   state_machine_definition = {
#     StartAt = "ParseInput"
#     States = {
#       ParseInput = {
#         Type     = "Task"
#         Resource = "arn:aws:lambda:REGION:ACCOUNT_ID:function:ParseInputFunction"
#         Next     = "ProcessRules"
#       }
#       ProcessRules = {
#         Type      = "Map"
#         ItemsPath = "$.rules"
#         Iterator  = {
#           StartAt = "SelectRule"
#           States  = {
#             SelectRule = {
#               Type     = "Choice"
#               Choices = [
#                 {
#                   Variable     = "$.name"
#                   StringEquals = "MAC"
#                   Next         = "ExecuteMACRule"
#                 },
#                 {
#                   Variable     = "$.name"
#                   StringEquals = "Breakout"
#                   Next         = "ExecuteBreakoutRule"
#                 }
#               ]
#             }
#             ExecuteMACRule = {
#               Type     = "Task"
#               Resource = "arn:aws:lambda:REGION:ACCOUNT_ID:function:MACFunction"
#               End      = true
#             }
#             ExecuteBreakoutRule = {
#               Type     = "Task"
#               Resource = "arn:aws:lambda:REGION:ACCOUNT_ID:function:BreakoutFunction"
#               End      = true
#             }
#           }
#         }
#         Next = "Done"
#       }
#       Done = {
#         Type = "Succeed"
#       }
#     }
#   }
# }
