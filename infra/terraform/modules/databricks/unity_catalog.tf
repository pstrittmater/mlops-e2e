data "databricks_catalog" "catalog" {
  name = "mlops_${var.environment}"
}

resource "databricks_schema" "schemas" {
  for_each = var.schemas
  catalog_name = data.databricks_catalog.catalog.name
  name = each.value
}

locals {
  api_credentials = var.secrets.api_credentials

  secret_items = flatten([
    for scope, kvs in local.api_credentials : [
      for key, value in kvs : {
        scope = scope
        key   = key
        value = value
      }
    ]
  ])
}

resource "databricks_secret_scope" "scopes" {
  for_each = local.api_credentials
  name                    = "mlops_${var.environment}_${each.key}"
  initial_manage_principal = "users"
}

resource "databricks_secret" "secrets" {
  for_each     = { for item in local.secret_items : "${item.scope}:${item.key}" => item }
  scope        = databricks_secret_scope.scopes[each.value.scope].name
  key          = each.value.key
  string_value = each.value.value
}
