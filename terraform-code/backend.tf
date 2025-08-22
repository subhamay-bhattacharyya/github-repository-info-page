# terraform {
#   backend "local" {
#     path = "../terraform-state/terraform.tfstate"
#   }
# }

terraform {
  backend "s3" {}
}
