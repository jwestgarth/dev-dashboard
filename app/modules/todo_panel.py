import json
from textual.widgets import Static


class TodoPanel(Static):

    def on_mount(self):
        self.load_todos()

    def load_todos(self):

        try:
            with open("config/todos.json") as f:
                todos = json.load(f)
        except:
            todos = []

        text = "Todo List\n\n"

        for t in todos:
            text += f"□ {t}\n"

        self.update(text)