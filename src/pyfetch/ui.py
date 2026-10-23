from rich.console import Console
from rich.panel import Panel
from rich.progress import (
    BarColumn,
    DownloadColumn,
    Progress,
    TextColumn,
    TimeRemainingColumn,
    TransferSpeedColumn,
)


console = Console()


def create_progress() -> Progress:
    """Create the download progress display."""
    return Progress(
        TextColumn("[bold cyan]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>5.1f}%"),
        DownloadColumn(),
        TransferSpeedColumn(),
        TimeRemainingColumn(),
    )


def show_video_info(title: str, quality: int) -> None:
    """Display information about the video."""
    console.print(
        Panel(
            f"[bold white]{title}[/bold white]\n"
            f"[cyan]Video[/cyan] • [yellow]{quality}p[/yellow]",
            title="PyFetch",
            border_style="cyan",
        )
    )


def show_success(message: str = "Download completed") -> None:
    """Display a success message."""
    console.print(f"\n[bold green]✓ {message}[/bold green]")
