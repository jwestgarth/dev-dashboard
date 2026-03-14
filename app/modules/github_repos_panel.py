import os
import requests
from datetime import datetime, timezone
from textual.widgets import Static


class GithubReposPanel(Static):

    def on_mount(self):
        # refresh every 2 minutes
        self.set_interval(120, self.update_repos)
        self.update_repos()

    def update_repos(self):

        token = os.getenv("GITHUB_TOKEN")

        if not token:
            self.update("GitHub Repositories\n\nNo token configured")
            return

        headers = {
            "Authorization": f"token {token}"
        }

        try:

            r = requests.get(
                "https://api.github.com/user/repos?sort=updated",
                headers=headers,
                timeout=10
            )

            repos = r.json()

            text = "GitHub Repositories\n\n"

            if not repos:
                text += "No repositories found"
                self.update(text)
                return

            for repo in repos[:10]:

                name = repo["name"]
                stars = repo["stargazers_count"]
                language = repo["language"] or "N/A"
                updated = repo["updated_at"]

                updated_time = datetime.fromisoformat(
                    updated.replace("Z", "+00:00")
                )

                age = datetime.now(timezone.utc) - updated_time

                if age.days < 1:
                    activity = "[green]🟢 active[/]"
                elif age.days < 7:
                    activity = "[yellow]🟡 recent[/]"
                else:
                    activity = "[red]🔴 stale[/]"

                text += (
                    f"• {name}\n"
                    f"  ⭐ {stars}  [{language}]  {activity}\n"
                )

            self.update(text)

        except Exception as e:

            self.update(
                "GitHub Repositories\n\n"
                f"Error: {str(e)}"
            )