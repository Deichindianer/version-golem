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


def update_versions():
    repositories = requests.get("localhost:5000/repositories")
    for repo in repositories:
        name = repo["name"]
        repo_slug = f"{repo['author']}/{name}"
        latest_version = get_latest_version(repo_slug)
        if repo["latest_version"] != latest_version["version"]:
            repo["latest_version"] = latest_version
            requests.put(f"localhost:5000/repositories/{name}", json=repo)


if __name__ == "__main__":
    print("Running update versions now")
    update_versions()
