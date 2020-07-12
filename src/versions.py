import requests

def get_latest_version(repo_slug):
    latest_release = requests.get(f"https://api.github.com/repos/{repo_slug}/releases/latest").json()
    if latest_release["tag_name"].startswith("v"):
        version = latest_release["tag_name"][1:]
    else:
        version = latest_release["tag_name"]
    return {
        "release_url": latest_release["html_url"],
        "version": version,
        "published_at": latest_release["published_at"]
    }

