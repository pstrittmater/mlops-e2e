module "databricks" {
  source            = "../../../modules/databricks"
  catalog_base_name = "external"
  schemas           = var.schemas
  secrets           = {
    api_credentials = var.api_credentials
  }
}
