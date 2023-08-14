import json
import os
import random

from dotenv import load_dotenv
from github import Auth
from github import Github

load_dotenv()

# todo: replace the print statements and save the information to a json file


def get_random_line():
    """Calls the github API to retrieve repositories and eventually returns a single line of code."""

    # Look up the GitHub auth token from the environment, then set up authentication
    auth = Auth.Token(os.getenv("GITHUB_TOKEN"))

    # Create the GitHub api object
    g = Github(auth=auth)

    # List all repositories for thebytebunch
    repos = list(g.get_user("thebytebunch").get_repos())

    # Shuffle the order of the list of repositories
    random.shuffle(repos)

    # Start an empty list to house content files.
    content_files = []

    # Start a while loop that will continue until at least one content file is found
    while not content_files:

        # remove one repo from the list of repos and save it to a repo variable
        chosen_repo = repos.pop()

        # call the Github api to get the contents of the repository, starting at the root ("")

        contents = chosen_repo.get_contents("")

        # Start a loop that will end when all of the content of the repo has been processed
        while len(contents) > 0:
            # remove one file_content object from the list of contents and store it in the file_content variable
            file_content = contents.pop(0)

            # if the type of the object found is a directory, get the contents from within that directory
            if file_content.type == "dir":
                # add those content items to the list of content_files
                contents.extend(chosen_repo.get_contents(file_content.path))
            else:  # if the type is not a directory, then it is a file. Add it to the content_files list.
                content_files.append(file_content)

        # Filter content files down to those which have a filename ending in ".py"
        content_files = [
            content_file
            for content_file in content_files
            if content_file.path.endswith(".py")
        ]

    print("chosen_repo_name:", chosen_repo.name)  # todo save me to json

    # Randomly choose one of the content files from the available list
    chosen_file = random.choice(content_files)

    chosen_file_path = chosen_file.path
    print("chosen_file_path:", chosen_file_path)  # todo save me to json

    # Decode the content to access the text, then split it on the newline character
    lines = chosen_file.decoded_content.decode("ASCII").split("\n")

    # start a loop that will continue until a non-empty line is found
    chosen_line = ""
    while not chosen_line.strip():
        chosen_line = random.choice(lines)

    print("chosen_line:", chosen_line)  # todo: save me to json

    # return that chosen line
    return chosen_line
