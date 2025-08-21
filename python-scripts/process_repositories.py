import argparse
import os
import sys
import json
from pathlib import Path
from typing import Dict, Any, List, Tuple
from collections import Counter
import requests


def parse_args():

    """
    Main entry point for processing GitHub repositories from a specified organization.

    Parses command-line arguments to specify the GitHub organization, output file path, and debug mode.
    Prints debug information if enabled. Handles argument parsing and prepares for further processing
    of repository data.

    Arguments:
        --org (str): GitHub organization name (required).
        --output (str, optional): Path to the output JSON file.
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
        help="GitHub organization name."
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

def process_repositories(repositories: List[Dict[str, Any]], debug: bool = False) -> List[Dict[str, Any]]:
    """
    Process a list of repository dictionaries and return processed information.

    Args:
        repositories (List[Dict[str, Any]]): List of repository data dictionaries.
        debug (bool): Enable debug output.

    Returns:
        List[Dict[str, Any]]: List of processed repository information.
    """
    cloudformation_repos = []
    terraform_repos = []
    currently_working_repos = []
    all_topics = []


    for repo in repositories:
        repo_info = {
            "name": repo.get("name"),
            "description": repo.get("description"),
            "url": repo.get("html_url"),
            "topics": repo.get("topics", []),
            "category": repo.get("custom_properties", {}).get("ProjectCategory", "No Category"),
            "status": "in-progress" if "in-progress" in repo.get("topics", []) else "completed",
        }
        for topic in repo_info["topics"]:
            if topic not in all_topics:
                all_topics.append(topic)

        repo_detail = {k: v for k, v in repo_info.items() if k in ["name","description","url","status"]}
        if "cloudformation" in repo_info["topics"]:
            if cloudformation_repos.get(repo_info["category"]) is None:
                cloudformation_repos.append({repo_info["category"]: list(repo_detail)})
            else:
                cloudformation_repos[repo_info["category"]].extend(list(repo_detail))
        elif "terraform" in repo_info["topics"]:
            if terraform_repos.get(repo_info["category"]) is None:
                terraform_repos.append({repo_info["category"]: list(repo_detail)})
            else:
                terraform_repos[repo_info["category"]].extend(list(repo_detail))

        elif "in-progress" in repo_info["topics"]:
            repo_detail = {k: v for k, v in repo_info.items() if k in ["name","description","url"]}
            currently_working_repos.append({"in-progress": repo_detail})

    if debug:
        print(f"Total processed repositories: {len(cloudformation_repos) + len(terraform_repos) + len(currently_working_repos)}")
        print(f"CloudFormation Repositories: {len(cloudformation_repos)}")
        print(f"Terraform Repositories: {len(terraform_repos)}")
        print(f"Currently Working Repositories: {len(currently_working_repos)}")

    print(f"CloudFormation Repo: {cloudformation_repos[0:10]}")
    print(f"Terraform Repo: {terraform_repos[0:10]}")
    print(f"Currently Working Repo: {currently_working_repos[0:10]}")

    print(f"All Topics: {all_topics}")

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


    if getattr(args, "debug", False):
        print("---------------------------------------------------------")
        print(f"Organization   => {args.org}")
        print(f"Debug          => {args.debug}")

        print("---------------------------------------------------------")

    repositories = get_all_repositories(args.org, debug=debug)

    cloudformation_repos, terraform_repos, currently_working_repos = process_repositories(repositories, debug=debug)

    print("Cloudformation Repos:")
    print(json.dumps(cloudformation_repos[0:10], indent=2))

    print("Terraform Repos:")
    print(json.dumps(terraform_repos[0:10], indent=2))

    print("Currently Working Repos:")
    print(json.dumps(currently_working_repos[0:10], indent=2))

if __name__ == "__main__":
    main()