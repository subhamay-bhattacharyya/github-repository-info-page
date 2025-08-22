locals {

  cloudformation-repos    = jsondecode(file("${path.module}/all-repositories/cloudformation-repos.json"))
  terraform-repos         = jsondecode(file("${path.module}/all-repositories/terraform-repos.json"))
  currently-working-repos = jsondecode(file("${path.module}/all-repositories/currently-working-repos.json"))

  flat_cloudformation_repos = flatten([for repo in local.cloudformation-repos : repo])

}

output "cloudformation-repos" {
  value = local.flat_cloudformation_repos
}


# output "terraform-repos" {
#   value = local.terraform-repos
# }

# output "currently-working-repos" {
#   value = local.currently-working-repos
# }