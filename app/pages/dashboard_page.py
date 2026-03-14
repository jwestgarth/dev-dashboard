from textual.containers import Grid, Vertical

from modules.logo_panel import LogoPanel
from modules.system_panel import SystemPanel
from modules.repo_panel import RepoPanel
from modules.todo_panel import TodoPanel
from modules.github_repos_panel import GithubReposPanel
from modules.docker_panel import DockerPanel
from modules.activity_panel import ActivityPanel


class DashboardPage(Vertical):

    def compose(self):

        with Grid():

            yield LogoPanel(classes="panel")
            yield SystemPanel(classes="panel")

            yield GithubReposPanel(classes="panel")
            yield TodoPanel(classes="panel")

            yield RepoPanel(classes="panel")
            yield ActivityPanel(classes="panel")