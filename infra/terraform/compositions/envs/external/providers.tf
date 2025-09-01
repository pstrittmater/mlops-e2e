terraform {
  required_version = ">= 1.12.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.11"
    }
    databricks = {
      source  = "databricks/databricks"
      version = "~> 1.86"
    }
  }
}

provider "aws" {
  # for local dev, use your ~/.aws/credentials profile
  profile = var.aws.profile
  region  = var.aws.region
}

provider "databricks" {
  # for local dev, use your ~/.databrickscfg profile
  profile = var.databricks_profile
}
