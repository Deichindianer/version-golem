import logging
import os
import sys
import time

import requests


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
ch.setLevel(logging.INFO)
logger.addHandler(ch)


def check_version(repo):
    if repo["latest_version"] != repo["tracked_version"]:
        return False
    return True


def send_message(repo):
    teams_url = os.environ["TEAMS_URL"] 
    body = {
      "@context": "https://schema.org/extensions",
      "@type":"MessageCard",
      "themeColor":"$3",
      "summary":f"Version alert for {repo['name']}",
      "sections": [
          {
              "activityTitle": f"Version alert for {repo['name']}",
              "facts": [
                  {"name": "Name", "value": f"{repo['name']}"},
                  {"name": "Tracked version", "value": f"{repo['tracked_version']}"},
                  {"name": "Latest version", "value": f"{repo['latest_version']}"},
                  {"name": "Release URL", "value": f"{repo['latest_release_url']}"},
                  {"name": "Publish date", "value": f"{repo['latest_version_publish_date']}"}
              ]
          }
      ]
    }
    requests.post(teams_url, json=body)


if __name__ == "__main__":
    for env_var in ["API_ENDPOINT", "ALERT_INTERVAL", "TEAMS_URL"]:
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
            logger.debug(f"Checking versions of {repo['name']}")
            if not check_version(repo):
                logger.info(f"Version of {repo['name']} is outdated!")
                send_message(repo)
            else:
                logger.info(f"Version of {repo['name']} is still up to date.")
        logger.info(f"Sleeping for {os.environ['ALERT_INTERVAL']} seconds.")
        time.sleep(int(os.environ["ALERT_INTERVAL"]))
