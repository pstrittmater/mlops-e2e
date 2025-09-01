databricks_external_api_access_iam_role = "DatabricksExternalApiAccess"
databricks_external_bulk_access_storage_credential = "external-bulk-access"
external_sources = [
  {
    "auth_secret_name": "Kaggle"
    "target_schema_name": "kaggle",
  },
  {
    "auth_secret_name": "OpenAQ"
    "source_bucket_name": "openaq-data-archive",
    "target_schema_name": "openaq",
  }
]
