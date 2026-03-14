from textual.widgets import Static
from datetime import datetime
import os

LOG_FILE = "/app/logs/dashboard.log"


class ActivityPanel(Static):

    history = []

    def on_mount(self):

        os.makedirs("/app/logs", exist_ok=True)

        if os.path.exists(LOG_FILE):

            with open(LOG_FILE) as f:
                lines = f.readlines()

            self.history = [l.strip() for l in lines][-10:]

        self.update_panel()

    def log(self, message):

        timestamp = datetime.now().strftime("%H:%M:%S")

        entry = f"{timestamp}  {message}"

        self.history.insert(0, entry)
        self.history = self.history[:10]

        with open(LOG_FILE, "a") as f:
            f.write(entry + "\n")

        self.update_panel()

    def update_panel(self):

        text = "Activity Feed\n\n"

        if not self.history:

            text += "No events yet"

        else:

            for item in self.history:

                text += f"• {item}\n"

        self.update(text)