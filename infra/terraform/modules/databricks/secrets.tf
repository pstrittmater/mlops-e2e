# TODO: this should be moved to aws secrets mgr

locals {
  # Root-level keys are logical scopes; nested maps are secrets in those scopes
  scopes = var.secrets != null ? var.secrets : {}

  # Flatten nested secrets to a uniform map for resource iteration
  # Key format: "<scope>_<secretKey>"
  secret_items = merge([
    for scope, entries in local.scopes : {
      for key, value in (entries != null ? entries : {}) : "${scope}_${key}" => {
        scope = scope
        key   = key
        value = value
      }
    }
  ]...)
}

# Create one Databricks secret scope per root-level key, with base environment name
resource "databricks_secret_scope" "scopes" {
  for_each                 = local.scopes
  name                     = "${local.environment_name}_${each.key}"
  initial_manage_principal = "users"
}

# Create one secret per nested key inside its parent scope
resource "databricks_secret" "secrets" {
  for_each = local.secret_items

  scope = databricks_secret_scope.scopes[each.value.scope].name
  key   = each.value.key

  # If value is a string, store as-is; otherwise JSON-encode maps/numbers/bools
  string_value = can(regex(".*", each.value.value)) ? tostring(each.value.value) : jsonencode(each.value.value)
}
