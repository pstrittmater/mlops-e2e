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
