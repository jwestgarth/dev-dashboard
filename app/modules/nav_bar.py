from textual.containers import Horizontal
from textual.widgets import Button


class NavBar(Horizontal):

    def compose(self):

        yield Button("1 Dashboard", id="dashboard", classes="navbtn")
        yield Button("2 Repositories", id="repos", classes="navbtn")
        yield Button("3 Docker", id="docker", classes="navbtn")
        yield Button("4 Logs", id="logs", classes="navbtn")

    def set_active(self, page):

        for button in self.query(".navbtn"):

            if button.id == page:
                button.variant = "success"
            else:
                button.variant = "default"

    def on_button_pressed(self, event: Button.Pressed):

        page = event.button.id

        if page == "dashboard":
            self.app.action_dashboard()

        elif page == "repos":
            self.app.action_repos()

        elif page == "docker":
            self.app.action_docker()

        elif page == "logs":
            self.app.action_logs()