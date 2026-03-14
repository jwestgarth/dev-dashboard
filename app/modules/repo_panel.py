import os
import requests
from textual.widgets import Static
from textual.reactive import reactive


class RepoPanel(Static):

    activity = reactive("Loading repository activity...")

    def on_mount(self):
        self.set_interval(120, self.fetch_activity)
        self.fetch_activity()

    def fetch_activity(self):

        token = os.getenv("GITHUB_TOKEN")

        if not token:
            self.activity = "Repository Activity\n\nNo GitHub token configured"
            return

        headers = {"Authorization": f"token {token}"}

        try:

            # Step 1 — get authenticated user
            user_resp = requests.get(
                "https://api.github.com/user",
                headers=headers,
                timeout=10
            )

            user_data = user_resp.json()

            username = user_data.get("login")

            if not username:
                self.activity = "Repository Activity\n\nUnable to determine GitHub user"
                return

            # Step 2 — get events for that user
            events_resp = requests.get(
                f"https://api.github.com/users/{username}/events",
                headers=headers,
                timeout=10
            )

            events = events_resp.json()

            text = "Repository Activity\n\n"

            if not isinstance(events, list) or not events:
                text += "No recent activity"
                self.activity = text
                return

            for event in events[:8]:

                repo = event.get("repo", {}).get("name", "unknown")
                event_type = event.get("type", "Event")

                if event_type == "PushEvent":
                    icon = "⬆ push"

                elif event_type == "PullRequestEvent":
                    icon = "🔀 PR"

                elif event_type == "IssuesEvent":
                    icon = "🐛 issue"

                elif event_type == "WatchEvent":
                    icon = "⭐ star"

                else:
                    icon = "⚡ event"

                text += f"• {icon}  {repo}\n"

            self.activity = text

        except Exception as e:

            self.activity = (
                "Repository Activity\n\n"
                f"Error: {str(e)}"
            )

    def render(self) -> str:
        return self.activity