from utils.logger import get_logger

from textual.app import App, ComposeResult
from textual.containers import Container
from textual.widgets import Header, Footer

from modules.nav_bar import NavBar

from pages.dashboard_page import DashboardPage
from pages.repos_page import ReposPage
from pages.docker_page import DockerPage
from pages.logs_page import LogsPage


logger = get_logger()


class DevDashboard(App):

    ENABLE_COMMAND_PALETTE = False
    ENABLE_MOUSE = True

    CSS = """
Screen {
    layout: vertical;
    background: black;
    color: green;
}

Header, Footer {
    background: black;
    color: green;
}

NavBar {
    height: 3;
    layout: horizontal;
    align: left middle;
    padding-left: 1;
    border-bottom: solid green;
}

.navbtn {
    margin-right: 2;
    color: green;
    background: black;
}

.navbtn.-active {
    color: black;
    background: green;
}

#content {
    height: 1fr;
}

Grid {
    grid-size: 2 3;
    grid-gutter: 1 1;
    height: 1fr;
}

.panel {
    border: round green;
    padding: 1;
    height: 1fr;
    content-align: center middle;
}

Static {
    color: green;
}

Input {
    background: black;
    color: green;
    border: solid green;
}
"""

    BINDINGS = [
        ("1", "dashboard", "Dashboard"),
        ("2", "repos", "Repositories"),
        ("3", "docker", "Docker"),
        ("4", "logs", "Logs"),
        ("q", "quit", "Quit"),
    ]

    # ------------------------------------------------

    def compose(self) -> ComposeResult:

        yield Header(show_clock=True)

        yield NavBar()

        self.content = Container(id="content")
        yield self.content

        yield Footer()

    # ------------------------------------------------

    def on_mount(self):

        logger.info("Dashboard started")

        # Create pages once
        self.pages = {
            "dashboard": DashboardPage(),
            "repos": ReposPage(),
            "docker": DockerPage(),
            "logs": LogsPage(),
        }

        # Mount all pages but hide them
        for page in self.pages.values():
            page.display = False
            self.content.mount(page)

        # Show dashboard first
        self.show_page("dashboard")

    # ------------------------------------------------

    def show_page(self, page):

        logger.info(f"Switched to page: {page}")

        # Show selected page, hide others
        for name, widget in self.pages.items():
            widget.display = (name == page)

        # Move keyboard focus to active page
        self.set_focus(self.pages[page])

        nav = self.query_one(NavBar)
        nav.set_active(page)

    # ------------------------------------------------

    def action_dashboard(self):
        self.show_page("dashboard")

    def action_repos(self):
        self.show_page("repos")

    def action_docker(self):
        self.show_page("docker")

    def action_logs(self):
        self.show_page("logs")


if __name__ == "__main__":
    DevDashboard().run()