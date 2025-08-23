# variable "github_token" {
#   type      = string
#   sensitive = true
# }

variable "source-dir" {
  description = "The source directory for the Terraform configuration files"
  type        = string
  default     = "all-repositories"
}

variable "github-action-repos-json-file" {
  description = "The path to the GitHub Action JSON file"
  type        = string
  default     = "gha-repos.json"
}

variable "cloudformation-repos-json-file" {
  description = "The path to the CloudFormation JSON file"
  type        = string
  default     = "cloudformation-repos"
}

variable "terraform-repos-json-file" {
  description = "The path to the Terraform JSON file"
  type        = string
  default     = "terraform-repos.json"
}


variable "currently-working-repos-json-file" {
  description = "The path to the currently working Terraform JSON file"
  type        = string
  default     = "currently-working-repos.json"
}
