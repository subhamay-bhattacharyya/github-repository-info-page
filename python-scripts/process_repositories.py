import argparse
import os
import sys
import json
from pathlib import Path
from typing import Dict, Any, List, Tuple
from collections import Counter
import requests

# def load_json(path: Path) -> List[Dict[str, Any]]:
#     """
#     Load a JSON file from the given path and return its contents as a list of dictionaries.
#     Raises an error and exits if the file cannot be read or does not contain a list.
#     """
#     try:
#         with path.open("r", encoding="utf-8") as f:
#             data = json.load(f)
#         if not isinstance(data, list):
#             raise ValueError("Input JSON must be a list of gist items.")
#         return data
#     except (OSError, json.JSONDecodeError) as e:
#         print(f"❌ Failed to read JSON from {path}: {e}", file=sys.stderr)
#         sys.exit(1)


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
        "--output",
        help="Path to the output JSON file."
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug output."
    )
    return parser.parse_args()

# def generate_repositories_json(repositories):
#     # Create a list to hold the repository information
#     repo_list = []

#     # Iterate through the repositories and extract the relevant information
#     try:
#         with all_gists_path.open("r", encoding="utf-8") as f:
#             gists = json.load(f)
#     except (OSError, json.JSONDecodeError) as e:
#         print(f"Failed to read {all_gists_path}: {e}", file=sys.stderr)
#         return
    
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

    for repo in repositories:
        repo_info = {
            "name": repo.get("name"),
            "description": repo.get("description"),
            "url": repo.get("html_url"),
            "topics": repo.get("topics", []),
        }
        if debug:
            print(f"Processed repository: {repo_info['name']}")
            if "cloudformation" in repo_info["topics"]:
                cloudformation_repos.append(repo_info)
            elif "terraform" in repo_info["topics"]:
                terraform_repos.append(repo_info)

            elif "in-progress" in repo_info["topics"]:
                currently_working_repos.append(repo_info)

    if debug:
        print(f"Total processed repositories: {len(cloudformation_repos) + len(terraform_repos) + len(currently_working_repos)}")
        print(f"CloudFormation Repositories: {len(cloudformation_repos)}")
        print(f"Terraform Repositories: {len(terraform_repos)}")
        print(f"Currently Working Repositories: {len(currently_working_repos)}")

    for repo in cloudformation_repos[0:10]:
        print(f"CloudFormation Repo: {repo['name']} - {repo['url']}")
    for repo in terraform_repos[0:10]:
        print(f"Terraform Repo: {repo['name']} - {repo['url']}")
    for repo in currently_working_repos[0:10]:
        print(f"Currently Working Repo: {repo['name']} - {repo['url']}")

    return cloudformation_repos, terraform_repos, currently_working_repos

def main():
    """
    Main entry point for processing repositories.

    Parses command-line arguments, sets up debug output, and prepares input/output paths.
    Performs initial validation and setup for further processing of repository data.
    """
    args = parse_args()

    output_path = args.output
    debug = getattr(args, "debug", False)

    if debug:
        print("---------------------------------------------------------")
        print(f"Organization    => {args.org}")
        print(f"Output file     => {output_path}")
        print(f"Debug           => {debug}")
        print("---------------------------------------------------------")
    output_path = args.output
    debug = args.debug


    if getattr(args, "debug", False):
        print("---------------------------------------------------------")
        print(f"Organization    => {args.org}")
        print(f"Output file    => {output_path}")
        print(f"Debug          => {args.debug}")

        print("---------------------------------------------------------")

    repositories = get_all_repositories(args.org, debug=debug)
    print(json.dumps(repositories[0:10], indent=2))

    cloudformation_repos, terraform_repos, currently_working_repos = process_repositories(repositories, debug=debug)


    # if not os.path.isfile(input_path):
    #     print(f"Input file '{input_path}' does not exist.", file=sys.stderr)
    #     sys.exit(1)

    # try:
    #     input_path = Path(args.input).expanduser().resolve()
    #     output_path = (
    #         Path(args.output).expanduser().resolve() if args.output else input_path
    #     )
    #     items = load_json(input_path)

    # except (OSError, json.JSONDecodeError) as e:
    #     print(f"Failed to load input JSON: {e}", file=sys.stderr)
    #     sys.exit(1)

    # try:
    #     if not isinstance(items, list):
    #         raise ValueError("Input JSON must be an array of items.")
    # except ValueError as e:
    #     print(str(e), file=sys.stderr)
    #     sys.exit(1)

    # session = requests.Session()

if __name__ == "__main__":
    main()