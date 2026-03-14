from textual.screen import Screen
from textual.widgets import Header, Footer, Static


class RepoScreen(Screen):

    BINDINGS = [
        ("1", "app.pop_screen", "Back to Dashboard"),
    ]

    def compose(self):

        yield Header(show_clock=True)

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

        yield Footer()