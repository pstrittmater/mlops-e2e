locals {
  # Name of the Databricks catalog for this environment (scope base name)
  environment_name = var.environment == "" || var.environment == null ? var.catalog_base_name : "${var.catalog_base_name}_${var.environment}"
}

data "databricks_storage_credential" "this" {
  name = var.storage_credential
}

module "aws_external_bucket" {
  source        = "../../aws/external_bucket"
  iam_role_name = split("/", data.databricks_storage_credential.this.storage_credential_info[0].aws_iam_role[0].role_arn)[1]
  bucket_name   = var.bucket_name
}

resource "databricks_external_location" "this" {
  depends_on      = [ module.aws_external_bucket ]
  name            = "${local.environment_name}-${var.bucket_name}"
  credential_name = data.databricks_storage_credential.this.name
  read_only       = true
  url             = "s3://${var.bucket_name}"
}
