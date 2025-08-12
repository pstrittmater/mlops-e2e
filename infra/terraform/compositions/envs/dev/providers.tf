terraform {
  required_version = ">= 1.12.0"
  required_providers {
    databricks = {
      source  = "databricks/databricks"
      version = "~> 1.86"
    }
  }
}

provider "databricks" {
  # for local dev, use your ~/.databrickscfg profile
  profile = var.databricks_profile
}
