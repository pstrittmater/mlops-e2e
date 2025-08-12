data "databricks_catalog" "catalog" {
  name = "mlops_${var.environment}"
}

resource "databricks_schema" "schemas" {
  for_each = var.schemas
  catalog_name = data.databricks_catalog.catalog.name
  name = each.value
}
