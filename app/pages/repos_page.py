import os
import subprocess
import webbrowser

from textual.widgets import Static, Input
from textual.containers import Vertical
from textual.reactive import reactive
from textual import events


PROJECT_PATH = "/projects"


class ReposPage(Vertical):

    can_focus = True

    repos = reactive([])
    selected = reactive(0)

    def on_mount(self):

        self.repo_list = Static()
        self.output = Static()
        self.clone_input = Input(placeholder="Paste repo URL and press Enter")

        self.clone_input.display = False
        self.output.display = False

        self.mount(self.repo_list)
        self.mount(self.output)
        self.mount(self.clone_input)

        self.scan_repos()

        self.focus()

    # ------------------------------------------------
    # Scan for repos
    # ------------------------------------------------

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

        if self.selected >= len(self.repos):
            self.selected = max(0, len(self.repos) - 1)

        self.render_repos()

    # ------------------------------------------------
    # Git helper
    # ------------------------------------------------

    def git(self, args, repo):

        path = os.path.join(PROJECT_PATH, repo)

        try:

            result = subprocess.check_output(
                ["git"] + args,
                cwd=path,
                stderr=subprocess.DEVNULL
            ).decode().strip()

            return result

        except:
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

        if ahead and ahead != "0" and ahead != "?":
            return f"▲ {ahead} ahead"

        return "● clean"

    # ------------------------------------------------
    # Render repos
    # ------------------------------------------------

    def render_repos(self):

        text = "Repositories\n\n"

        if not self.repos:

            text += "No repositories found"

        else:

            for i, repo in enumerate(self.repos):

                prefix = ">" if i == self.selected else " "

                branch = self.repo_branch(repo)
                health = self.repo_health(repo)
                last = self.repo_last_commit(repo)

                text += f"{prefix} {repo:<25} {health}\n"
                text += f"    branch: {branch}\n"
                text += f"    last: {last}\n\n"

        text += (
            "\n"
            "↑ ↓ select\n\n"
            "p pull   s status   h history\n"
            "c clone\n"
            "o open vscode   b open github\n"
            "ESC close output"
        )

        self.repo_list.update(text)

    # ------------------------------------------------
    # Run git commands
    # ------------------------------------------------

    def run_git(self, args):

        repo = self.repos[self.selected]

        path = os.path.join(PROJECT_PATH, repo)

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
    # Clone repo
    # ------------------------------------------------

    def clone_repo(self, url):

        try:

            result = subprocess.check_output(
                ["git", "clone", url],
                cwd=PROJECT_PATH
            ).decode()

        except Exception as e:

            result = str(e)

        self.output.display = True

        self.output.update(result)

        self.clone_input.display = False

        self.scan_repos()

    # ------------------------------------------------
    # Keyboard controls
    # ------------------------------------------------

    async def on_key(self, event: events.Key):

        # close output window
        if self.output.display:

            if event.key == "escape":
                self.output.display = False

            return

        # clone input mode
        if self.clone_input.display:

            if event.key == "escape":
                self.clone_input.display = False

            return

        if not self.repos:
            return

        # navigation

        if event.key == "down":

            self.selected = min(self.selected + 1, len(self.repos) - 1)
            self.render_repos()

        elif event.key == "up":

            self.selected = max(self.selected - 1, 0)
            self.render_repos()

        # git commands

        elif event.key == "p":

            self.run_git(["pull"])

        elif event.key == "h":

            self.run_git(["log", "--oneline", "-n", "10"])

        elif event.key == "s":

            self.run_git(["status"])

        # clone

        elif event.key == "c":

            self.clone_input.display = True
            self.clone_input.focus()

        # open vscode

        elif event.key == "o":

            repo = self.repos[self.selected]

            path = os.path.join(PROJECT_PATH, repo)

            subprocess.Popen(["code", path], shell=True)

        # open github

        elif event.key == "b":

            repo = self.repos[self.selected]

            url = self.git(
                ["config", "--get", "remote.origin.url"],
                repo
            )

            if url and url != "?":

                webbrowser.open(url)

    # ------------------------------------------------
    # Input submit
    # ------------------------------------------------

    async def on_input_submitted(self, message: Input.Submitted):

        url = message.value.strip()

        if url:
            self.clone_repo(url)

        message.input.value = ""