import argparse
import os
import sys
import json
from pathlib import Path
from typing import Dict, Any, List, Tuple
from collections import Counter
import requests

STATUS_BADGES = {
    "not-started": "https://img.shields.io/badge/-NOT%20STARTED-6C63FF?style=flat&labelColor=00000000",
    "in-progress": "https://img.shields.io/badge/-IN%20PROGRESS-6C63FF?style=flat&labelColor=00000000",
    "completed": "https://img.shields.io/badge/-COMPLETED-6C63FF?style=flat&labelColor=00000000"
}

def parse_args():

    """
    Main entry point for processing GitHub repositories from a specified organization.

    Parses command-line arguments to specify the GitHub organization, output file path, and debug mode.
    Prints debug information if enabled. Handles argument parsing and prepares for further processing
    of repository data.

    Arguments:
        --org (str): GitHub organization name (required).
        --output-dir (str, optional): Path to the output directory.
        --debug (flag): Enable debug output.

    Returns:
        None
    """

    parser = argparse.ArgumentParser(
        description="Retrieve repositories from a GitHub organization and process them."
    )
    parser.add_argument(
        "--org",
        required=True,
        type=str,
        help="GitHub organization name."
    )
    parser.add_argument(
        "--output-dir",
        required=True,
        type=str,
        help="Path to the output directory."
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug output."
    )
    return parser.parse_args()

    
def get_all_repositories(org: str, debug: bool = False) -> List[Dict[str, Any]]:
    """
    Fetch all repositories for the specified GitHub organization.

    Args:
        org (str): GitHub organization name.
        debug (bool): Enable debug output.

    Returns:
        List[Dict[str, Any]]: List of repository data dictionaries.
    """
    repos = []
    session = requests.Session()
    url = f"https://api.github.com/orgs/{org}/repos"
    params = {"per_page": 100, "type": "all"}
    page = 1

    # Add authentication if GITHUB_TOKEN is set in environment
    github_token = os.environ.get("GITHUB_TOKEN")
    if github_token:
        session.headers.update({"Authorization": f"Bearer {github_token}"})

    try:
        while True:
            params["page"] = page
            if debug:
                print(f"Fetching page {page} from {url} with params {params}")
            response = session.get(url, params=params)
            if response.status_code != 200:
                print(f"❌ Failed to fetch repositories: {response.status_code} {response.text}", file=sys.stderr)
                break
            data = response.json()
            if not data:
                break
            repos.extend(data)
            page += 1

        if debug:
            print(f"Fetched {len(repos)} repositories from organization '{org}'.")

        return repos
    except Exception as e:
        print(f"❌ Exception occurred while fetching repositories: {e}", file=sys.stderr)
        return []

def get_status(topics):
    for status in ["in-progress", "not-started", "completed"]:
        if status in topics:
            return STATUS_BADGES.get(status, "-")
        
    return STATUS_BADGES.get("not-started", "-")

def process_repositories(repositories: List[Dict[str, Any]], debug: bool = False) -> List[Dict[str, Any]]:
    """
    Process a list of repository dictionaries and return processed information.

    Args:
        repositories (List[Dict[str, Any]]): List of repository data dictionaries.
        debug (bool): Enable debug output.

    Returns:
        List[Dict[str, Any]]: List of processed repository information.
    """
    cloudformation_repos = {}
    terraform_repos = {}
    currently_working_repos = []

    for repo in repositories:

        repo_info = {
            "name": repo.get("name"),
            "description": repo.get("description"),
            "url": repo.get("html_url"),
            "status": get_status(repo.get("topics", [])),
        }

        repo_category = repo.get("custom_properties", {}).get("ProjectCategory", "No Category")
        if "cloudformation" in repo.get("topics", []):
            category_repos = cloudformation_repos.get(repo_category, [])
            category_repos.append(repo_info)
            cloudformation_repos[repo_category] = category_repos
        if "terraform" in repo.get("topics", []):
            category_repos = terraform_repos.get(repo_category, [])
            category_repos.append(repo_info)
            terraform_repos[repo_category] = category_repos

        elif "in-progress" in repo.get("topics", []):
            currently_working_repos.append(repo_info)

        # Sort the elements of the lists
        for key, val in cloudformation_repos.items():
            cloudformation_repos[key] = sorted(val, key=lambda x: x["name"])

        for key, val in terraform_repos.items():
            terraform_repos[key] = sorted(val, key=lambda x: x["name"])


    if debug:
        num_cloudformation_repos = sum([len(v) for v in cloudformation_repos.values()])
        num_terraform_repos = sum([len(v) for v in terraform_repos.values()])
        print(f"Total processed repositories: {num_cloudformation_repos + num_terraform_repos + len(currently_working_repos)}")
        print(f"CloudFormation Repositories: {num_cloudformation_repos}")
        print(f"Terraform Repositories: {num_terraform_repos}")
        print(f"Currently Working Repositories: {len(currently_working_repos)}")

    return cloudformation_repos, terraform_repos, currently_working_repos

def main():
    """
    Main entry point for processing repositories.

    Parses command-line arguments, sets up debug output, and prepares input/output paths.
    Performs initial validation and setup for further processing of repository data.
    """
    args = parse_args()

    debug = getattr(args, "debug", False)
    debug = args.debug
    output_dir = os.path.abspath(os.path.expanduser(args.output_dir))

    if not os.path.isdir(output_dir):
        print(f"Output directory '{output_dir}' does not exist.", file=sys.stderr)
        sys.exit(1)
    try:
        cloudformation_repo_path = Path(output_dir).expanduser().resolve() / "cloudformation_repos.json"
        terraform_repo_path = Path(output_dir).expanduser().resolve() / "terraform_repos.json"
        currently_working_repos_repo_path = Path(output_dir).expanduser().resolve() / "currently_working_repos.json"
    except (OSError, json.JSONDecodeError) as e:
        print(f"Failed to load input JSON: {e}", file=sys.stderr)
        sys.exit(1)

    if getattr(args, "debug", False):
        print("---------------------------------------------------------")
        print(f"Organization                     => {args.org}")
        print(f"Output Path                      => {output_dir}")
        print(f"Debug                            => {args.debug}")
        print(f"CloudFormation Repo Path         => {cloudformation_repo_path}")
        print(f"Terraform Repo Path              => {terraform_repo_path}")
        print(f"Currently Working Repos Path     => {currently_working_repos_repo_path}")
        print("---------------------------------------------------------")

    repositories = get_all_repositories(args.org, debug=debug)

    cloudformation_repos, terraform_repos, currently_working_repos = process_repositories(repositories, debug=debug)

    try:
        with cloudformation_repo_path.open("w", encoding="utf-8") as f:
            json.dump(cloudformation_repos, f, indent=2)
        print(f"CloudFormation Repo JSON written to {cloudformation_repo_path}")
    except OSError as e:
        print(f"Failed to write CloudFormation Repo JSON: {e}", file=sys.stderr)

    try:
        with terraform_repo_path.open("w", encoding="utf-8") as f:
            json.dump(terraform_repos, f, indent=2)
        print(f"Terraform Repo JSON written to {terraform_repo_path}")
    except OSError as e:
        print(f"Failed to write Terraform Repo JSON: {e}", file=sys.stderr)

    try:
        with currently_working_repos_repo_path.open("w", encoding="utf-8") as f:
            json.dump(currently_working_repos, f, indent=2)
        print(f"Currently Working Repos JSON written to {currently_working_repos_repo_path}")
    except OSError as e:
        print(f"Failed to write Currently Working Repos JSON: {e}", file=sys.stderr)

if __name__ == "__main__":
    main()