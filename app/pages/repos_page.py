import os
import subprocess
import requests

from textual.widgets import Static, Input
from textual.containers import Vertical
from textual.reactive import reactive
from textual import events


PROJECT_PATH = "/projects"


class ReposPage(Vertical):

    repos = reactive([])
    selected = reactive(0)

    def on_mount(self):

        self.logo = Static(
"""[green]
   ██████╗ ██╗████████╗██╗  ██╗██╗   ██╗██████╗
  ██╔════╝ ██║╚══██╔══╝██║  ██║██║   ██║██╔══██╗
  ██║  ███╗██║   ██║   ███████║██║   ██║██████╔╝
  ██║   ██║██║   ██║   ██╔══██║██║   ██║██╔══██╗
  ╚██████╔╝██║   ██║   ██║  ██║╚██████╔╝██████╔╝
   ╚═════╝ ╚═╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═════╝

        GitHub Control Center
[/green]"""
        )

        self.repo_list = Static()
        self.activity = Static()
        self.output = Static()
        self.clone_input = Input(placeholder="Paste repo URL and press Enter")

        self.clone_input.display = False
        self.output.display = False

        self.mount(self.logo)
        self.mount(self.repo_list)
        self.mount(self.activity)
        self.mount(self.output)
        self.mount(self.clone_input)

        self.scan_repos()
        self.update_github_activity()

        self.set_interval(60, self.update_github_activity)

    # --------------------------
    # REPO SCANNER
    # --------------------------

    def scan_repos(self):

        repos = []

        if not os.path.exists(PROJECT_PATH):
            self.repo_list.update("No /projects directory found")
            return

        for folder in os.listdir(PROJECT_PATH):

            repo_path = os.path.join(PROJECT_PATH, folder)

            if os.path.isdir(os.path.join(repo_path, ".git")):
                repos.append(folder)

        self.repos = sorted(repos)

        self.render_repos()

    def git(self, args, repo):

        try:
            result = subprocess.check_output(
                ["git"] + args,
                cwd=os.path.join(PROJECT_PATH, repo),
                stderr=subprocess.STDOUT
            ).decode().strip()

            return result

        except:
            return "?"

    def repo_info(self, repo):

        branch = self.git(["rev-parse", "--abbrev-ref", "HEAD"], repo)
        last = self.git(["log", "-1", "--pretty=format:%cr"], repo)

        status = self.git(["status", "--porcelain"], repo)

        modified = "clean"
        if status:
            modified = f"{len(status.splitlines())} files"

        ahead = self.git(["rev-list", "--count", "@{upstream}..HEAD"], repo)

        return branch, ahead, modified, last

    def render_repos(self):

        text = "Repositories\n\n"

        if not self.repos:
            text += "No repositories found"

        else:
            for i, repo in enumerate(self.repos):

                prefix = ">" if i == self.selected else " "

                branch, ahead, modified, last = self.repo_info(repo)

                text += f"{prefix} {repo}\n"
                text += f"   branch: {branch}\n"
                text += f"   ahead: {ahead} | modified: {modified}\n"
                text += f"   last: {last}\n\n"

        text += "↑ ↓ select   p pull   h history   s status   c clone\n"
        text += "ESC close output"

        self.repo_list.update(text)

    # --------------------------
    # GITHUB ACTIVITY
    # --------------------------

    def update_github_activity(self):

        token = os.getenv("GITHUB_TOKEN")

        if not token:
            self.activity.update("GitHub Activity\n\nNo GitHub token configured")
            return

        headers = {
            "Authorization": f"token {token}"
        }

        try:

            r = requests.get(
                "https://api.github.com/users/" + os.getenv("GITHUB_USER") + "/events",
                headers=headers,
                timeout=10
            )

            data = r.json()

            if not isinstance(data, list):
                message = data.get("message", "GitHub API error")
                self.activity.update(f"GitHub Activity\n\nAPI Error:\n{message}")
                return

            text = "GitHub Activity\n\n"

            for event in data[:6]:

                repo = event["repo"]["name"]
                etype = event["type"]

                if etype == "PushEvent":
                    icon = "⬆ push"
                elif etype == "PullRequestEvent":
                    icon = "🔀 PR"
                elif etype == "IssuesEvent":
                    icon = "🐛 issue"
                elif etype == "WatchEvent":
                    icon = "⭐ star"
                else:
                    icon = "⚡ event"

                text += f"• {icon} → {repo}\n"

            self.activity.update(text)

        except Exception as e:

            self.activity.update(f"GitHub Activity\n\nError:\n{str(e)}")

    # --------------------------
    # GIT COMMANDS
    # --------------------------

    def run_git(self, args):

        repo = self.repos[self.selected]

        result = self.git(args, repo)

        self.output.display = True

        self.output.update(
f"""
Git Output

{result}

Press ESC to close
"""
        )

    def clone_repo(self, url):

        try:
            result = subprocess.check_output(
                ["git", "clone", url],
                cwd=PROJECT_PATH
            ).decode()

        except Exception as e:
            result = str(e)

        self.output.display = True

        self.output.update(
f"""
Clone Result

{result}

Press ESC to close
"""
        )

        self.clone_input.display = False
        self.scan_repos()

    # --------------------------
    # KEYBOARD CONTROLS
    # --------------------------

    async def on_key(self, event: events.Key):

        if self.clone_input.display:

            if event.key in ("escape", "q"):
                self.clone_input.display = False

            return

        if self.output.display:

            if event.key == "escape":
                self.output.display = False

            return

        if event.key == "c":
            self.clone_input.display = True
            self.clone_input.focus()
            return

        if not self.repos:
            return

        if event.key == "down":
            self.selected = min(self.selected + 1, len(self.repos) - 1)
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

    async def on_input_submitted(self, message: Input.Submitted):

        url = message.value.strip()

        if url:
            self.clone_repo(url)

        message.input.value = ""