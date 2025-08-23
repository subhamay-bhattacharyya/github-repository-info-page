
# GitHub Repository Info Page

## Purpose

This repository automates the refresh of your GitHub profile page by dynamically listing all your repositories and their current statuses. It helps keep your profile up-to-date, providing an overview of your projects and their progress at a glance.

## Functionality

- **Automated Repository Listing:** Uses Python scripts to fetch repository data from the GitHub API, categorizing repositories (CloudFormation, Terraform, GitHub Actions) and generating JSON summaries.
- **Profile Automation with Terraform:** Employs Terraform to manage and update the profile repository, including the main README and Jekyll site files, using templates and the processed data.
- **Status Badges:** Displays the current status of each repository (e.g., in-progress, completed, not started) using visual badges.
- **Continuous Updates:** Keeps your profile up-to-date with the latest information about your projects, their categories, and progress, all in an automated and reproducible way.

## How It Works

1. **Python Automation:**
	- The `process_repositories.py` script fetches all repositories for a given GitHub organization, processes their metadata and topics, and outputs categorized JSON files.
2. **Terraform Infrastructure:**
	- Terraform resources use these JSON files and templates to update the profile repository's README and Jekyll site files, ensuring your profile always reflects the latest repository information.
3. **GitHub Actions:**
	- Workflows can be set up to run the Python and Terraform automation on a schedule or trigger, ensuring your profile stays current without manual intervention.

## Getting Started

1. Clone this repository.
2. Configure your GitHub and AWS credentials as needed for automation.
3. Run the Python script to generate repository data.
4. Apply the Terraform configuration to update your profile repository.

---


