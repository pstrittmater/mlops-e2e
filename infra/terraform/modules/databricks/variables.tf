variable "environment" {
  type = string
}

variable "schemas" {
  type = set(string)
}

variable "secrets" {
  description = "Secrets configuration"
  type = object({
    api_credentials = map(map(string))
  })
  default = {
    api_credentials = {}
  }
}
