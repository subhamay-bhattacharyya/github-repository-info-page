locals {

  cloudformation-repos    = jsondecode(file("${path.module}/all-repositories/cloudformation-repos.json"))
  terraform-repos         = jsondecode(file("${path.module}/all-repositories/terraform-repos.json"))
  currently-working-repos = jsondecode(file("${path.module}/all-repositories/currently-working-repos.json"))

  flat_cloudformation_repos = flatten([for repo in local.cloudformation-repos : repo])

}
