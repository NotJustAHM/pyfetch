from pathlib import Path

import yt_dlp
from rich.console import Console
from rich.progress import (
    BarColumn,
    DownloadColumn,
    Progress,
    TextColumn,
    TimeRemainingColumn,
    TransferSpeedColumn,
)
from rich.panel import Panel


console = Console()


def download_video(
    url: str,
    output_dir: str = "downloads",
    quality: int = 720,
    playlist: bool = False,
) -> None:
    output_path = Path(output_dir).expanduser()
    output_path.mkdir(parents=True, exist_ok=True)

    if playlist:
        output_template = str(
            output_path
            / "%(playlist_title)s"
            / "%(playlist_index)03d - %(title)s.%(ext)s"
        )
    else:
        output_template = str(output_path / "%(title)s.%(ext)s")

    progress = Progress(
        TextColumn("[bold cyan]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>5.1f}%"),
        DownloadColumn(),
        TransferSpeedColumn(),
        TimeRemainingColumn(),
    )

    current_task = None

    def progress_hook(data: dict) -> None:
        nonlocal current_task

        status = data.get("status")

        if status == "downloading":
            downloaded = data.get("downloaded_bytes", 0)
            total = data.get("total_bytes") or data.get("total_bytes_estimate")

            if current_task is None:
                current_task = progress.add_task(
                    "Downloading",
                    total=total,
                )

            if total:
                progress.update(
                    current_task,
                    total=total,
                    completed=downloaded,
                )
            else:
                progress.update(
                    current_task,
                    completed=downloaded,
                )

        elif status == "finished":
            if current_task is not None:
                progress.update(
                    current_task,
                    completed=progress.tasks[current_task].total,
                )

    options = {
        "outtmpl": output_template,
        "noplaylist": not playlist,
        "format": (f"bestvideo[height<={quality}]+bestaudio/best[height<={quality}]"),
        "progress_hooks": [progress_hook],
        "quiet": True,
        "no_warnings": True,
    }

    with yt_dlp.YoutubeDL(options) as ydl:
        info = ydl.extract_info(url, download=False)

        title = info.get("title", "Unknown")
        console.print(
            Panel(
                f"[bold white]{title}[/bold white]\n"
                f"[cyan]Video[/cyan] • [yellow]{quality}p[/yellow]",
                title="PyFetch",
                border_style="cyan",
            )
        )

        with progress:
            ydl.download([url])

    console.print("\n[bold green]✓ Download completed[/bold green]")
