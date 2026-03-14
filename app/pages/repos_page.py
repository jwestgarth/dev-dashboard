import os
import subprocess
import requests

from textual.widgets import Static, Input
from textual.containers import Vertical
from textual.reactive import reactive
from textual import events

from modules.activity_panel import ActivityPanel


PROJECT_PATH = "/projects"
GITHUB_API = "https://api.github.com/repos"


class ReposPage(Vertical):

    repos = reactive([])
    selected = reactive(0)

    can_focus = True

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
        self.output = Static()
        self.clone_input = Input(placeholder="Paste repo URL and press Enter")

        self.clone_input.display = False
        self.output.display = False

        self.mount(self.logo)
        self.mount(self.repo_list)
        self.mount(self.output)
        self.mount(self.clone_input)

        self.scan_repos()

    def activity(self):

        try:
            return self.app.query_one(ActivityPanel)
        except:
            return None

    def scan_repos(self):

        repos = []

        if not os.path.exists(PROJECT_PATH):
            self.repo_list.update("No /projects directory found")
            return

        for folder in os.listdir(PROJECT_PATH):

            repo_path = os.path.join(PROJECT_PATH, folder)

            if os.path.isdir(os.path.join(repo_path, ".git")):
                repos.append(folder)

        self.repos = repos

        self.render_repos()

    def repo_health(self, repo):

        path = os.path.join(PROJECT_PATH, repo)

        try:

            branch = subprocess.check_output(
                ["git", "rev-parse", "--abbrev-ref", "HEAD"],
                cwd=path
            ).decode().strip()

            last_commit = subprocess.check_output(
                ["git", "log", "-1", "--pretty=format:%cr"],
                cwd=path
            ).decode()

            status = subprocess.check_output(
                ["git", "status", "--porcelain"],
                cwd=path
            ).decode()

            if status.strip():
                health = "[yellow]modified[/yellow]"
            else:
                health = "[green]clean[/green]"

            return branch, last_commit, health

        except:
            return "?", "?", "[red]error[/red]"

    def github_stats(self, repo):

        try:

            remote = subprocess.check_output(
                ["git", "config", "--get", "remote.origin.url"],
                cwd=os.path.join(PROJECT_PATH, repo)
            ).decode().strip()

            if "github.com" not in remote:
                return "-", "-"

            repo_path = remote.split("github.com/")[1].replace(".git", "")

            r = requests.get(f"{GITHUB_API}/{repo_path}")

            data = r.json()

            stars = data.get("stargazers_count", "-")
            issues = data.get("open_issues_count", "-")

            return stars, issues

        except:
            return "-", "-"

    def render_repos(self):

        text = "Repositories\n\n"

        if not self.repos:

            text += "No repositories found"

        else:

            for i, repo in enumerate(self.repos):

                prefix = ">" if i == self.selected else " "

                branch, last_commit, health = self.repo_health(repo)

                stars, issues = self.github_stats(repo)

                text += f"{prefix} {repo}\n"
                text += f"   branch: {branch} | last: {last_commit} | {health}\n"
                text += f"   ★ {stars} | issues: {issues}\n\n"

        text += "↑ ↓ select  p pull  h history  s status  c clone\n"
        text += "ESC close output"

        self.repo_list.update(text)

    def run_git(self, args):

        repo = self.repos[self.selected]

        path = os.path.join(PROJECT_PATH, repo)

        try:

            result = subprocess.check_output(
                ["git"] + args,
                cwd=path
            ).decode()

            activity = self.activity()
            if activity:
                activity.log(f"git {' '.join(args)} : {repo}")

        except Exception as e:

            result = str(e)

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

            activity = self.activity()
            if activity:
                activity.log(f"repo cloned: {url}")

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