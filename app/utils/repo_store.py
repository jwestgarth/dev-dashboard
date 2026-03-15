import json
from pathlib import Path

CONFIG_DIR = Path.home() / ".dev-dashboard"
CONFIG_DIR.mkdir(exist_ok=True)

REPO_FILE = CONFIG_DIR / "repos.json"


def load_repos():
    if not REPO_FILE.exists():
        return []

    with open(REPO_FILE) as f:
        data = json.load(f)

    return data.get("repos", [])


def save_repos(repos):
    with open(REPO_FILE, "w") as f:
        json.dump({"repos": repos}, f, indent=2)


def add_repo(url):
    repos = load_repos()

    if url not in repos:
        repos.append(url)

    save_repos(repos)


def remove_repo(url):
    repos = load_repos()

    repos = [r for r in repos if r != url]

    save_repos(repos)