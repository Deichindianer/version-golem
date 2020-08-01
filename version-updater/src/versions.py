import os
import time

import requests


def get_latest_version(repo_slug):
    print("Getting latest version...")
    latest_release = requests.get(f"https://api.github.com/repos/{repo_slug}/releases/latest").json()
    if latest_release["tag_name"].startswith("v"):
        version = latest_release["tag_name"][1:]
    else:
        version = latest_release["tag_name"]
    print(f"Got {version}")
    return {
        "release_url": latest_release["html_url"],
        "version": version,
        "published_at": latest_release["published_at"]
    }


def update_versions():
    api_endpoint = os.environ["API_ENDPOINT"]
    print(f"Running against {api_endpoint}")
    repositories = requests.get(f"{api_endpoint}/repositories").json()
    for repo in repositories:
        print(f"Looking through {repo['name']}")
        name = repo["name"]
        repo_slug = f"{repo['author']}/{name}"
        latest_version = get_latest_version(repo_slug)
        if repo["latest_version"] != latest_version["version"]:
            print(f"{repo['name']} is outdated!")
            print(repo)
            repo["latest_version"] = latest_version
            result = requests.put(f"{api_endpoint}/repository/{name}", json=repo)
            print(result)


if __name__ == "__main__":
    print("Running update versions now")
    while True:
        update_versions()
        time.sleep(15)
