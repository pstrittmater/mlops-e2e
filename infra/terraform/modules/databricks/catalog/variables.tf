variable "catalog_base_name" {
  type = string
}

variable "environment" {
  type    = string
  default = null
}

variable "schemas" {
  type = set(string)
}
