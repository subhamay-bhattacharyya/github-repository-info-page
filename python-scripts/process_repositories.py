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