from textual.widgets import Static
from textual.containers import Vertical
from textual.reactive import reactive
import os

LOG_FILE = "/app/dashboard.log"


class LogsPage(Vertical):

    log_content = reactive("")

    def on_mount(self):

        self.viewer = Static()

        self.mount(self.viewer)

        self.refresh_logs()

        self.set_interval(2, self.refresh_logs)

    def refresh_logs(self):

        if not os.path.exists(LOG_FILE):

            self.viewer.update("No logs yet")
            return

        with open(LOG_FILE, "r") as f:

            logs = f.readlines()

        logs = "".join(logs[-100:])

        self.viewer.update(
f"""Dashboard Logs

{logs}
"""
        )