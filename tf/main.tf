resource "github_repository" "this" {
  name        = ".github"
  description = "A GitHub profile repository of Subhamay Bhattacharyya"
  visibility  = "public"
  auto_init   = true

  pages {
    source {
      branch = "main"
      path   = "/"
    }
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
      gha-repos  = local.gha-repos
      cfn-repos  = local.cloudformation-repos
      tf-repos   = local.terraform-repos
      curr-repos = local.currently-working-repos
    }
  )
}

resource "github_repository_file" "jekyll_layout" {
  repository          = github_repository.this.name
  branch              = "main"
  file                = "_layouts/default.html"

  content = templatefile("${path.module}/template/jekyll_default.tftpl",
    {
      readme_content = github_repository_file.readme.content
    }
  )
}

resource "github_config_file" "jekyll_config" {
  repository          = github_repository.this.name
  branch              = "main"
  file                = "_config.yaml"

  content = templatefile("${path.module}/template/jekyll_config.tftpl", {})
}