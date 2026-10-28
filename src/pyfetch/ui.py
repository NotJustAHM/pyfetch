from rich.console import Console
from rich.live import Live
from rich.panel import Panel
from rich.text import Text


console = Console()


def create_download_display() -> Live:
    """Create a live download progress display."""
    return Live(
        Text("Preparing download..."),
        console=console,
        refresh_per_second=8,
        transient=False,
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


def show_playlist_info(
    title: str,
    total_videos: int,
    quality: int,
) -> None:
    """Display information about the playlist."""
    console.print(
        Panel(
            f"[bold white]{title}[/bold white]\n"
            f"[cyan]Videos:[/cyan] {total_videos}\n"
            f"[cyan]Quality:[/cyan] [yellow]{quality}p[/yellow]",
            title="PyFetch — Playlist Downloader",
            border_style="cyan",
        )
    )


def show_download_start(
    index: int,
    total_videos: int,
    title: str,
) -> None:
    """Display the start of a playlist video download."""
    console.print(
        f"\n[bold cyan]▶ Video {index}/{total_videos}[/bold cyan]\n"
        f"  [white]{title}[/white]"
    )


def update_download_display(
    live: Live,
    percentage: float,
    downloaded: str,
    total: str,
    speed: str,
    eta: str | None = None,
) -> None:
    """Update the live download progress display."""
    percentage = max(0.0, min(100.0, percentage))

    bar_width = 30
    completed = int(bar_width * percentage / 100)
    bar = "━" * completed + "─" * (bar_width - completed)

    details = f"{downloaded} / {total} • {speed}"

    if eta is not None:
        details += f" • ETA {eta}"

    live.update(
        Text.from_markup(
            f"[cyan]  {bar}[/cyan] [bold]{percentage:5.1f}%[/bold]  {details}"
        )
    )


def show_video_completed(
    index: int,
    total_videos: int,
) -> None:
    """Display completion of a playlist video."""
    console.print(
        f"  [bold green]✓ Video {index}/{total_videos} completed[/bold green]"
    )


def show_playlist_completed(total_videos: int) -> None:
    """Display playlist completion."""
    console.print(
        Panel(
            f"[bold green]✓ Playlist download completed[/bold green]\n"
            f"[cyan]{total_videos}/{total_videos} videos[/cyan]",
            border_style="green",
        )
    )
