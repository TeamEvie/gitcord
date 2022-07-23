# haha funny pun file name
import os

from github import Github


def get_token():
    if os.environ.get("GITHUB_TOKEN"):
        return os.environ.get("GITHUB_TOKEN")
    else:
        return None


gh_instance = Github(get_token())
