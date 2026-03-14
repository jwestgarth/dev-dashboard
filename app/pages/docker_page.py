from textual.widgets import Static
from textual.widget import Widget


class DockerPage(Widget):

    def compose(self):

        yield Static(
            """
Docker Page

Future features:
- container stats
- start / stop containers
- logs
"""
        )