from screens.repos_screen import RepoScreen
from textual.app import App, ComposeResult
from textual.containers import Grid
from textual.widgets import Header, Footer

from modules.logo_panel import LogoPanel
from modules.system_panel import SystemPanel
from modules.repo_panel import RepoPanel
from modules.todo_panel import TodoPanel
from modules.github_repos_panel import GithubReposPanel
from modules.docker_panel import DockerPanel


class DevDashboard(App):

    CSS = """
    Screen {
        layout: vertical;
        background: black;
    }

    Grid {
        grid-size: 2 3;
        grid-gutter: 1;
        height: 1fr;
    }

    .panel {
        border: round green;
        padding: 1;
        height: 1fr;
        content-align: center middle;
    }
    """

    # Register additional screens
    SCREENS = {
        "repos": RepoScreen
    }

    BINDINGS = [
        ("q", "quit", "Quit"),
        ("r", "refresh", "Refresh Dashboard"),
        ("2", "repos", "Open Repositories Page"),
    ]

    def compose(self) -> ComposeResult:

        yield Header(show_clock=True)

        with Grid():

            yield LogoPanel(classes="panel")
            yield SystemPanel(classes="panel")

            yield GithubReposPanel(classes="panel")
            yield TodoPanel(classes="panel")

            yield RepoPanel(classes="panel")
            yield DockerPanel(classes="panel")

        yield Footer()

    def action_refresh(self):

        for widget in self.query(".panel"):

            if hasattr(widget, "refresh_stats"):
                widget.refresh_stats()

            if hasattr(widget, "scan_repos"):
                widget.scan_repos()

            if hasattr(widget, "update_containers"):
                widget.update_containers()

            if hasattr(widget, "update_repos"):
                widget.update_repos()

    # New action to open the repo screen
    def action_repos(self):
        self.push_screen("repos")


if __name__ == "__main__":
    DevDashboard().run()