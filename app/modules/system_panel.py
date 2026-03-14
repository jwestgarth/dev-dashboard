import psutil
from textual.widgets import Static


class SystemPanel(Static):

    def on_mount(self):

        self.cpu_history = [0] * 30
        self.ram_history = [0] * 30

        self.set_interval(1, self.update_stats)

    def sparkline(self, values):

        blocks = "▁▂▃▄▅▆▇"

        result = ""

        for v in values:

            index = int((v / 100) * (len(blocks) - 1))
            result += blocks[index]

        return result

    def update_stats(self):

        cpu = psutil.cpu_percent()
        ram = psutil.virtual_memory().percent

        self.cpu_history.append(cpu)
        self.cpu_history = self.cpu_history[-30:]

        self.ram_history.append(ram)
        self.ram_history = self.ram_history[-30:]

        cpu_graph = self.sparkline(self.cpu_history)
        ram_graph = self.sparkline(self.ram_history)

        self.update(
f"""Dev System Monitor

CPU  {cpu:.1f}%
{cpu_graph}

RAM  {ram:.1f}%
{ram_graph}
"""
        )