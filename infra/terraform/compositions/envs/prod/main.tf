module "databricks" {
  source      = "../../../modules/databricks"
  environment = var.environment
  schemas     = var.schemas
}
