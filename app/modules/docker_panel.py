import docker
from textual.widgets import Static
from textual.reactive import reactive
from textual import events


class DockerPanel(Static):

    containers = reactive([])
    selected = reactive(0)

    can_focus = True

    def on_mount(self):

        self.client = docker.from_env()

        self.refresh_containers()

        self.set_interval(5, self.refresh_containers)

    def on_focus(self):
        self.render_panel()

    def refresh_containers(self):

        try:

            self.containers = self.client.containers.list(all=True)

            self.render_panel()

        except Exception as e:

            self.update(f"Docker Error\n\n{str(e)}")

    def render_panel(self):

        text = "Docker Containers\n\n"

        if not self.containers:
            text += "No containers found"
            self.update(text)
            return

        for i, c in enumerate(self.containers):

            prefix = ">" if i == self.selected else " "

            status = c.status

            if status == "running":
                state = "[green]running[/green]"
            else:
                state = "[red]stopped[/red]"

            text += f"{prefix} {c.name:<20} {state}\n"

        text += "\n↑ ↓ select   r restart   s stop"

        self.update(text)

    async def on_key(self, event: events.Key):

        if not self.containers:
            return

        if event.key == "down":

            self.selected = min(self.selected + 1, len(self.containers) - 1)
            self.render_panel()

        elif event.key == "up":

            self.selected = max(self.selected - 1, 0)
            self.render_panel()

        elif event.key == "r":

            container = self.containers[self.selected]
            container.restart()

        elif event.key == "s":

            container = self.containers[self.selected]
            container.stop()