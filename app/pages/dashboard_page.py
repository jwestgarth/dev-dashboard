from textual.containers import Grid, Vertical

from app.modules.logo_panel import LogoPanel
from app.modules.system_panel import SystemPanel
from app.modules.repo_panel import RepoPanel
from app.modules.todo_panel import TodoPanel
from app.modules.github_repos_panel import GithubReposPanel
from app.modules.docker_panel import DockerPanel
from app.modules.activity_panel import ActivityPanel


class DashboardPage(Vertical):

    def compose(self):

        with Grid():

            yield LogoPanel(classes="panel")
            yield SystemPanel(classes="panel")

            yield GithubReposPanel(classes="panel")
            yield TodoPanel(classes="panel")

            yield RepoPanel(classes="panel")
            yield ActivityPanel(classes="panel")