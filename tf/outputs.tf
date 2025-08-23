
output "repository_name" {
  value = github_repository.this.name
}

output "repository_description" {
  value = github_repository.this.description
}

output "repository_url" {
  value = github_repository.this.html_url
}