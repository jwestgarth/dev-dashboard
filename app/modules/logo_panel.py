from textual.widgets import Static
from rich.align import Align
from rich.text import Text


class LogoPanel(Static):

    def render(self):

        logo = Text("""
 ██████╗ ███████╗██╗   ██╗
 ██╔══██╗██╔════╝██║   ██║
 ██║  ██║█████╗  ██║   ██║
 ██║  ██║██╔══╝  ╚██╗ ██╔╝
 ██████╔╝███████╗ ╚████╔╝
 ╚═════╝ ╚══════╝  ╚═══╝
""", style="bold green")

        title = Text("\nDEV Dashboard\n", style="bold bright_green")
        subtitle = Text("Terminal Control Center", style="green dim")

        logo.append_text(title)
        logo.append_text(subtitle)

        return Align.center(logo)