import docker
from textual.widgets import Static


class DockerPanel(Static):

    def on_mount(self):

        self.client = docker.from_env()
        self.set_interval(5, self.update_containers)

    def update_containers(self):

        containers = self.client.containers.list()

        text = "Docker Containers\n\n"

        if not containers:
            text += "No running containers"

        for c in containers:

            if c.status == "running":
                status = "[green]running[/]"
            else:
                status = "[red]stopped[/]"

            text += f"• {c.name} {status}\n"

        self.update(text)