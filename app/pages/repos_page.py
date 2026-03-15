import json
import subprocess
import webbrowser
from pathlib import Path

from textual.widgets import Static, Input
from textual.containers import Vertical
from textual.reactive import reactive
from textual import events


CONFIG_DIR = Path.home() / ".dev-dashboard"
CONFIG_DIR.mkdir(exist_ok=True)

REPO_FILE = CONFIG_DIR / "repos.json"

CLONE_DIR = Path.home() / "projects"
CLONE_DIR.mkdir(exist_ok=True)


# ------------------------------------------------
# Repo storage helpers
# ------------------------------------------------

def load_repos():

    if not REPO_FILE.exists():
        return []

    try:
        with open(REPO_FILE) as f:
            data = json.load(f)
            return data.get("repos", [])
    except Exception:
        return []


def save_repos(repos):

    with open(REPO_FILE, "w") as f:
        json.dump({"repos": repos}, f, indent=2)


def repo_name(url):

    return url.split("/")[-1].replace(".git", "")


# ------------------------------------------------
# Repos Page
# ------------------------------------------------

class ReposPage(Vertical):

    can_focus = True

    repos = reactive([])
    selected = reactive(0)

    # ------------------------------------------------

    def on_mount(self):

        self.repo_list = Static()
        self.output = Static()
        self.clone_input = Input(
            placeholder="Paste repo URL and press Enter"
        )

        self.clone_input.display = False
        self.output.display = False

        self.mount(self.repo_list)
        self.mount(self.output)
        self.mount(self.clone_input)

        self.scan_repos()

        self.focus()

    # ------------------------------------------------
    # Load repos
    # ------------------------------------------------

    def scan_repos(self):

        self.repos = load_repos()

        if self.selected >= len(self.repos):
            self.selected = max(0, len(self.repos) - 1)

        self.render_repos()

    # ------------------------------------------------
    # Clone repo if needed
    # ------------------------------------------------

    def ensure_cloned(self, url):

        name = repo_name(url)
        path = CLONE_DIR / name

        if not path.exists():

            subprocess.run(
                ["git", "clone", url],
                cwd=CLONE_DIR
            )

        return path

    # ------------------------------------------------
    # Git helper
    # ------------------------------------------------

    def git(self, args, repo):

        name = repo_name(repo)
        path = CLONE_DIR / name

        # auto clone if missing
        if not path.exists():
            self.ensure_cloned(repo)

        try:

            result = subprocess.check_output(
                ["git"] + args,
                cwd=path,
                stderr=subprocess.DEVNULL
            ).decode().strip()

            return result

        except Exception:
            return "?"

    # ------------------------------------------------
    # Repo info
    # ------------------------------------------------

    def repo_branch(self, repo):
        return self.git(["rev-parse", "--abbrev-ref", "HEAD"], repo)

    def repo_last_commit(self, repo):
        return self.git(["log", "-1", "--pretty=format:%cr"], repo)

    def repo_health(self, repo):

        status = self.git(["status", "--porcelain"], repo)

        ahead = self.git(["rev-list", "--count", "@{upstream}..HEAD"], repo)

        if status and status != "?":
            return "✖ modified"

        if ahead and ahead not in ["0", "?"]:
            return f"▲ {ahead} ahead"

        return "● clean"

    # ------------------------------------------------
    # Render UI
    # ------------------------------------------------

    def render_repos(self):

        text = "Repositories\n\n"

        if not self.repos:

            text += "No repositories added\n\n"
            text += "Press 'c' to add a repository URL\n"

        else:

            for i, repo in enumerate(self.repos):

                prefix = ">" if i == self.selected else " "

                name = repo_name(repo)

                branch = self.repo_branch(repo)
                health = self.repo_health(repo)
                last = self.repo_last_commit(repo)

                text += f"{prefix} {name:<25} {health}\n"
                text += f"    branch: {branch}\n"
                text += f"    last:   {last}\n\n"

        text += (
            "\n"
            "↑ ↓ select\n\n"
            "p pull   s status   h history\n"
            "r refresh\n"
            "c add repo\n"
            "o open vscode   b open github\n"
            "ESC close output"
)

        self.repo_list.update(text)

    # ------------------------------------------------
    # Run git command
    # ------------------------------------------------

    def run_git(self, args):

        if not self.repos:
            return

        repo = self.repos[self.selected]

        path = self.ensure_cloned(repo)

        try:

            result = subprocess.check_output(
                ["git"] + args,
                cwd=path
            ).decode()

        except Exception as e:

            result = str(e)

        self.output.display = True
        self.output.update(result)

    # ------------------------------------------------
    # Add repo
    # ------------------------------------------------

    def add_repo(self, url):

        repos = load_repos()

        if url not in repos:
            repos.append(url)

        save_repos(repos)

        self.scan_repos()

    # ------------------------------------------------
    # Keyboard controls
    # ------------------------------------------------

    async def on_key(self, event: events.Key):

        if self.output.display:

            if event.key == "escape":
                self.output.display = False

            return

        if self.clone_input.display:

            if event.key == "escape":
                self.clone_input.display = False

            return

        if event.key == "down":

            self.selected = min(
                self.selected + 1,
                len(self.repos) - 1
            )
            self.render_repos()

        elif event.key == "up":

            self.selected = max(self.selected - 1, 0)
            self.render_repos()

        elif event.key == "p":
            self.run_git(["pull"])

        elif event.key == "h":
            self.run_git(["log", "--oneline", "-n", "10"])

        elif event.key == "s":
            self.run_git(["status"])

        elif event.key == "c":

            self.clone_input.display = True
            self.clone_input.focus()

        elif event.key == "o":

            repo = self.repos[self.selected]
            path = self.ensure_cloned(repo)

            subprocess.Popen(["code", str(path)], shell=True)

        elif event.key == "b":

            repo = self.repos[self.selected]
            webbrowser.open(repo)

        elif event.key == "r":

            self.scan_repos()

    # ------------------------------------------------
    # Input handler
    # ------------------------------------------------

    async def on_input_submitted(self, message: Input.Submitted):

        url = message.value.strip()

        if url:
            self.add_repo(url)

        message.input.value = ""

        self.clone_input.display = False