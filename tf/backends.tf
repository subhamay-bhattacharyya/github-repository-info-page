# --- root/backends.tf ---

## Uncomment the following lines to use S3 as the backend for Terraform state management when running locally.
## For GitHub Actions, the backend is configured in the workflow file.

terraform {
  backend "s3" {}
}


# terraform {
#   backend "s3" {
#     bucket = var.tf-state-bucket
#     key    = local.tf-state-key
#     region = var.aws-region
#   }
# }