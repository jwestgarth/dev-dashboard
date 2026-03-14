import docker

from textual.widgets import Static
from textual.containers import Vertical
from textual.reactive import reactive
from textual import events


class DockerPage(Vertical):

    can_focus = True

    containers = reactive([])
    selected = reactive(0)

    def on_mount(self):

        self.client = docker.from_env()

        self.container_list = Static()
        self.logs = Static()

        self.logs.display = False

        self.mount(self.container_list)
        self.mount(self.logs)

        self.update_containers()

        self.set_interval(5, self.update_containers)

        self.focus()

    # ------------------------------------------------
    # Update container list
    # ------------------------------------------------

    def update_containers(self):

        try:

            self.containers = self.client.containers.list(all=True)

            if self.selected >= len(self.containers):
                self.selected = max(0, len(self.containers) - 1)

            self.draw_container_list()

        except Exception as e:

            self.container_list.update(f"Docker error:\n{str(e)}")

    # ------------------------------------------------
    # Draw container list
    # ------------------------------------------------

    def draw_container_list(self):

        text = "Docker Containers\n\n"

        if not self.containers:

            text += "No containers found"

        else:

            for i, container in enumerate(self.containers):

                prefix = ">" if i == self.selected else " "

                state = "[green]running[/green]" if container.status == "running" else "[red]stopped[/red]"

                text += f"{prefix} {container.name:<25} {state}\n"

        text += "\n↑ ↓ select   l logs   r restart   s stop"

        self.container_list.update(text)

    # ------------------------------------------------
    # Show logs
    # ------------------------------------------------

    def show_logs(self):

        if not self.containers:
            return

        container = self.containers[self.selected]

        try:
            logs = container.logs(tail=20).decode()
        except Exception as e:
            logs = str(e)

        self.logs.display = True

        self.logs.update(
            f"""
Container Logs

{logs}

Press ESC to close
"""
        )

    # ------------------------------------------------
    # Keyboard controls
    # ------------------------------------------------

    async def on_key(self, event: events.Key):

        if self.logs.display:

            if event.key == "escape":
                self.logs.display = False

            return

        if not self.containers:
            return

        if event.key == "down":

            self.selected = min(self.selected + 1, len(self.containers) - 1)
            self.draw_container_list()

        elif event.key == "up":

            self.selected = max(self.selected - 1, 0)
            self.draw_container_list()

        elif event.key == "l":

            self.show_logs()

        elif event.key == "r":

            try:
                self.containers[self.selected].restart()
            except:
                pass

        elif event.key == "s":

            try:
                self.containers[self.selected].stop()
            except:
                pass