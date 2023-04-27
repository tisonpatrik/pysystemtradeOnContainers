variable "vpc_cidr" {
  description = "VPC CIDR block"
  default     = "10.0.0.0/16"
}
variable "aws_region" {
  description = "AWS region for the deployment"
  default     = "eu-central-1"
}

variable "app_name" {
  description = "Application name"
  default     = "grayfox"
}
variable "enviroment_name" {
  description = "Enviroment name"
  default     = "dev"
}
