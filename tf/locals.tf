locals {

  gha-repos               = jsondecode(file("${path.module}/all-repositories/gha-repos.json"))
  cloudformation-repos    = jsondecode(file("${path.module}/all-repositories/cloudformation-repos.json"))
  terraform-repos         = jsondecode(file("${path.module}/all-repositories/terraform-repos.json"))
  currently-working-repos = jsondecode(file("${path.module}/all-repositories/currently-working-repos.json"))
}
