module "databricks" {
  source            = "../../../modules/databricks"
  catalog_base_name = "mlops"
  environment       = var.environment
  schemas           = var.schemas
}
