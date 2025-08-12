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

variable "kaggle" {
  type        = map(string)
  description = "Kaggle OAuth credentials and configuration"
  default     = {}
}
