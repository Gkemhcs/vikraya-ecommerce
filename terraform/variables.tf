variable "PROJECT_ID" {
  type    = string
  default = "vikraya-deployment"
}


variable "subnets" {
  description = "The subnets to create"
  type = list(object({
    name          = string
    region        = string
    ip_cidr_range = string
    secondary_ranges = list(object({
      range_name    = string
      ip_cidr_range = string
    }))
  }))
}
variable "VECTOR_SEARCH_API_IMAGE"{
  type=string
}