resource "github_repository" "this" {
  name        = ".github"
  description = "A repository for subhamay's profile"
  visibility  = "public"
  auto_init   = true

  pages {
    source {
      branch = "main"
      path   = "/"
    }
  }

  provisioner "local-exec" {
    command = "gh repo view subhamay-bhattacharyya/subhamay-profile --web"
  }
}

data "github_user" "current" {
  username = "bsubhamay"
}

resource "time_static" "this" {}


resource "github_repository_file" "readme" {
  repository          = github_repository.this.name
  branch              = "main"
  file                = "profile/README.md"
  overwrite_on_create = true

  content = templatefile("${path.module}/template/README.tftpl",
    {
      avatar     = data.github_user.current.avatar_url
      name       = data.github_user.current.name
      date       = time_static.this.year
      time-stamp = time_static.this.rfc3339
      cfn-repos  = local.cloudformation-repos
      tf-repos   = local.terraform-repos
      curr-repos = local.currently-working-repos
    }
  )
}