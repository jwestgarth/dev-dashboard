import os
import subprocess

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

    # ------------------------------------------------

    def render_repos(self):

        text = "Repositories\n\n"

        if not self.repos:

            text += "No repositories found"

        else:

            for i, repo in enumerate(self.repos):

                prefix = ">" if i == self.selected else " "

                text += f"{prefix} {repo}\n"

        text += "\n↑ ↓ select   p pull   s status   h history   c clone"

        self.repo_list.update(text)

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

    async def on_key(self, event: events.Key):

        if self.output.display:

            if event.key == "escape":
                self.output.display = False

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