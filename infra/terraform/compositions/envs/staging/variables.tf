variable "environment" {
  type    = string
}

variable "databricks_profile" {
  type    = string
  default = "terraform"
}

variable "schemas" {
  type    = set(string)
}

variable "api_credentials" {
  type = map(map(string))
  description = "Service API credentials (e.g., kaggle)"
  default = {}
}
