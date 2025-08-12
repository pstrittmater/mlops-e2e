module "databricks" {
  source      = "../../../modules/databricks"
  environment = var.environment
  schemas     = var.schemas
  secrets     = {
    api_credentials = var.api_credentials
  }
}
