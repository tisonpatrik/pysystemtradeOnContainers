terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.16"
      profile = "default"
    }
  }

  required_version = ">= 1.2.0"
}