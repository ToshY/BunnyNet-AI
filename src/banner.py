"""Rich and pyfiglet imports"""
import pyfiglet
from rich.console import Console

console = Console()


def cli_banner(
    banner_title: str,
    banner_font: str = "standard",
    banner_color: str = "#FFA500",
    banner_width: int = 200,
) -> None:
    """
    CLI banner

    Parameters
    ----------
    banner_title : str
        Main file.
    banner_font : str, optional
        Banner font type. The default is "isometric3".
    banner_color : str, optional
        Banner color. The default is "#FFA500" (orange).
    banner_width : int, optional
        Banner width. The default is 200.

    Returns
    -------
    None.

    """

    banner = pyfiglet.figlet_format(banner_title, font=banner_font, width=banner_width)
    console.print(banner, style=banner_color)
