import psutil
from textual.widgets import Static


class SystemPanel(Static):

    def on_mount(self):

        self.set_interval(2, self.update_stats)

        self.update_stats()

    def update_stats(self):

        cpu = psutil.cpu_percent()

        mem = psutil.virtual_memory().percent

        disk = psutil.disk_usage("/").percent

        load = psutil.getloadavg()[0] if hasattr(psutil, "getloadavg") else 0

        text = f"""
System Monitor

CPU      {cpu}%
Memory   {mem}%
Disk     {disk}%
Load     {load:.2f}
"""

        self.update(text)