from textual.widgets import Static
from textual.widget import Widget


class ReposPage(Widget):

    def compose(self):

        yield Static(
            """
Repositories Page

Future features:
- repo cloning
- git pull
- repo health
- commit history
"""
        )