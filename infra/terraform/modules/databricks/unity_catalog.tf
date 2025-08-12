locals {
  # Name of the Databricks catalog for this environment (scope base name)
  environment_name = var.environment == "" ? var.catalog_base_name : "${var.catalog_base_name}_${var.environment}"
}

data "databricks_catalog" "catalog" {
  name = local.environment_name
}

resource "databricks_schema" "schemas" {
  for_each = var.schemas
  catalog_name = data.databricks_catalog.catalog.name
  name = each.value
}
