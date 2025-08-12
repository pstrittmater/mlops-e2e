locals {
  api_credentials = var.secrets.api_credentials

  # Pre-compute a map of secret items keyed by a unique composite key
  # to avoid rebuilding the map in the resource's for_each.
  secret_items = merge([
    for scope, kvs in local.api_credentials : {
      for key, value in kvs : "${scope}_${key}" => {
        scope = scope
        key   = key
        value = value
      }
    }
  ]...)

  # Derive a stable map of unique scopes from the items
  scopes_map = { for s in toset([for i in values(local.secret_items) : i.scope]) : s => true }
}

resource "databricks_secret_scope" "scopes" {
  for_each                 = local.scopes_map
  name                     = "mlops_${var.environment}_${each.key}"
  initial_manage_principal = "users"
}

resource "databricks_secret" "secrets" {
  for_each     = local.secret_items
  scope        = databricks_secret_scope.scopes[each.value.scope].name
  key          = each.value.key
  # Store JSON for easier parsing downstream (e.g., Python)
  string_value = jsonencode({
    key   = each.value.key,
    value = each.value.value
  })
}
