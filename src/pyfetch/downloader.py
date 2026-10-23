from pathlib import Path

import yt_dlp

from pyfetch.ui import (
    create_progress,
    show_success,
    show_video_info,
)


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

    progress = create_progress()
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

            progress.update(
                current_task,
                total=total,
                completed=downloaded,
            )

        elif status == "finished":
            if current_task is not None:
                task = progress.tasks[current_task]

                if task.total is not None:
                    progress.update(
                        current_task,
                        completed=task.total,
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
        info = ydl.extract_info(
            url,
            download=False,
        )

        title = info.get(
            "title",
            "Unknown",
        )

        show_video_info(
            title=title,
            quality=quality,
        )

        with progress:
            ydl.download([url])

    show_success()
