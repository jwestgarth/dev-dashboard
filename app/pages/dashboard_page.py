from textual.containers import Grid
from textual.widget import Widget

from modules.logo_panel import LogoPanel
from modules.system_panel import SystemPanel
from modules.repo_panel import RepoPanel
from modules.todo_panel import TodoPanel
from modules.github_repos_panel import GithubReposPanel
from modules.docker_panel import DockerPanel


class DashboardPage(Widget):

    def compose(self):

        with Grid():

            yield LogoPanel(classes="panel")
            yield SystemPanel(classes="panel")

            yield GithubReposPanel(classes="panel")
            yield TodoPanel(classes="panel")

            yield RepoPanel(classes="panel")
            yield DockerPanel(classes="panel")