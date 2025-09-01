variable "aws" {
  type = object({
    profile    = string
    region     = string
  })
}

variable "databricks_profile" {
  type = string
}

# TODO: replace with storage credential reference, if the api ever allows
variable "databricks_external_api_access_iam_role" {
  type        = string
  description = "The name of the role used to access and ingest external api data"
}

variable "databricks_external_bulk_access_storage_credential" {
  type        = string
  description = "The name of the role used to access and ingest external bulk data"
}

variable "external_sources" {
  type = list(object({
    # the name of the AWS Secrets Manager that contains auth credentials
    auth_secret_name   = string
    # the name of the external AWS S3 Bucket that contains data for this source
    source_bucket_name = optional(string, null)
    # the name of the Databricks UC schema that will store data from this source
    target_schema_name = string
  }))
}
