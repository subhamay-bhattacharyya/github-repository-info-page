locals {

  gha-repos               = jsondecode(file("${path.module}/${var.source-dir}/${var.github-action-repos-json-file}"))
  cloudformation-repos    = jsondecode(file("${path.module}/${var.source-dir}/${var.cloudformation-repos-json-file}"))
  terraform-repos         = jsondecode(file("${path.module}/${var.source-dir}/${var.terraform-repos-json-file}"))
  currently-working-repos = jsondecode(file("${path.module}/${var.source-dir}/${var.currently-working-repos-json-file}"))
}
