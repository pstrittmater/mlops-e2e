module "databricks" {
  source            = "../../../modules/databricks/catalog"
  catalog_base_name = "mlops"
  environment       = var.environment
  schemas           = var.schemas
}
