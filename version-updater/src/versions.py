import logging
import os
import sys
import time

import requests


logger = logging.getLogger(__name__)
ch = logging.StreamHandler()
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
ch.setLevel(logging.INFO)
logger.addHandler(ch)


def get_latest_version(repo_slug):
    logger.info(f"Getting latest version for {repo_slug}")
    latest_release = requests.get(f"https://api.github.com/repos/{repo_slug}/releases/latest").json()
    if latest_release["tag_name"].startswith("v"):
        version = latest_release["tag_name"][1:]
    else:
        version = latest_release["tag_name"]
    logger.info(f"Got {version} for {repo_slug}")
    return {
        "release_url": latest_release["html_url"],
        "version": version,
        "published_at": latest_release["published_at"]
    }


def update_version(repo):
    logger.debug(f"Checking version of {repo['name']}")
    latest_version = get_latest_version(f"{repo['author']}/{repo['name']}")
    logger.debug(
        f"Checking {repo['latest_version']}(current) against {latest_version['version']}(latest)"
    )
    if repo["latest_version"] != latest_version["version"]:
        logger.info(f"{repo['name']} is outdated!")
        repo["latest_version"] = latest_version["version"]
        repo["latest_release_url"] = latest_version["release_url"]
        repo["latest_version_publish_date"] = latest_version["published_at"]
        logger.debug(f"Updating version of {repo['name']} with {latest_version['version']}")
        result = requests.put(f"{api_endpoint}/repository/{repo['name']}", json=repo)


if __name__ == "__main__":
    for env_var in ["API_ENDPOINT", "UPDATE_INTERVAL"]:
        if not os.environ.get(env_var): 
            logger.critical(
                f"Make sure {env_var} environment variable is set!"
            )
            sys.exit(1)
    while True:
        api_endpoint = os.environ["API_ENDPOINT"]
        logger.debug(f"Running against {api_endpoint}")
        repositories = requests.get(f"{api_endpoint}/repositories").json()
        for repo in repositories:
            update_version(repo)
        logger.info(f"Waiting for {os.environ['UPDATE_INTERVAL']} seconds.")
        time.sleep(int(os.environ["UPDATE_INTERVAL"]))
