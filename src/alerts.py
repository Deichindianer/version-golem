import time
import logging
import requests
import os
from tinydb import Query

from versions import get_latest_version


def version_checks(db):
    repository = Query()
    while True:
        for repo in db:
            name = repo["name"]
            repo_slug = f"{repo['author']}/{name}"
            latest_version = get_latest_version(repo_slug)
            if repo["latest_version"] != latest_version["version"]:
                db.update(
                    {"latest_version": latest_version},
                    repository.name == repo["name"]
                )
            if repo["tracked_version"] != latest_version:
                send_message(name, repo["tracked_version"], latest_version["version"])
        time.sleep(os.environ["ALERT_INTERVAL"])


def send_message(name, tracked_version, latest_version):
    teams_url = os.environ["TEAMS_URL"] 
    body = {
      "@context": "https://schema.org/extensions",
      "@type":"MessageCard",
      "themeColor":"$3",
      "summary":f"Version alert for {name}",
      "sections": [
          {
              "activityTitle": f"Version alert for {name}",
              "facts": [
                  {"name": "Name", "value": f"{name}"},
                  {"name": "Tracked version", "value": f"{tracked_version}"},
                  {"name": "Latest version", "value": f"{latest_version}"}
              ]
          }
      ]
    }
    requests.post(teams_url, json=body)

