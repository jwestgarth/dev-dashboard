import psutil
import docker
from textual.widgets import Static


class SystemPanel(Static):

    history = []

    def on_mount(self):
        self.client = docker.from_env()
        self.set_interval(2, self.update_monitor)

    def bar(self, percent):

        total = 20
        filled = int((percent / 100) * total)

        return "█" * filled + "░" * (total - filled)

    def update_monitor(self):

        cpu = psutil.cpu_percent()
        ram = psutil.virtual_memory().percent
        disk = psutil.disk_usage("/").percent

        net = psutil.net_io_counters()

        containers = self.client.containers.list()

        cpu_bar = self.bar(cpu)
        ram_bar = self.bar(ram)
        disk_bar = self.bar(disk)

        text = f"""
Dev System Monitor

CPU  [{cpu_bar}] {cpu}%

RAM  [{ram_bar}] {ram}%

Disk [{disk_bar}] {disk}%

Network
↓ {round(net.bytes_recv / 1024 / 1024, 1)} MB
↑ {round(net.bytes_sent / 1024 / 1024, 1)} MB

Docker
Running containers: {len(containers)}
"""

        self.update(text)