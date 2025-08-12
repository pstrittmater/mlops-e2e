variable "catalog_base_name" {
  type = string
}

variable "environment" {
  type    = string
  default = ""
}

variable "schemas" {
  type = set(string)
}

variable "secrets" {
  description = "Map of secret scopes to their key-value maps"
  type        = map(map(any))
  default     = {}
}
