locals {
  buckets = toset([
    for source in var.external_sources : source.source_bucket_name
    if source.source_bucket_name != "" && source.source_bucket_name != null
  ])
  schemas = toset(concat(
    [ for source in var.external_sources : source.target_schema_name ],
    [ "static" ]
  ))
  secrets = toset([
    for source in var.external_sources : source.auth_secret_name
  ])
}

module "databricks_catalog" {
  source            = "../../../modules/databricks/catalog"
  catalog_base_name = "external"
  schemas           = local.schemas
}

module "aws_secretsmanager" {
  source        = "../../../modules/aws/secretsmanager"
  for_each      = local.secrets
  iam_role_name = var.databricks_external_api_access_iam_role
  secret_name   = each.value
}

module "databricks_external_location" {
  source             = "../../../modules/databricks/external_location"
  for_each           = local.buckets
  catalog_base_name  = "external"
  bucket_name        = each.value
  storage_credential = var.databricks_external_bulk_access_storage_credential
}
