from pathlib import Path

import yt_dlp

from pyfetch.ui import (
    create_progress,
    show_success,
    show_playlist_info,
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
    overall_task = None
    active_index = None
    completed_indices = set()
    total_videos = None
    video_states = {}

    def format_bytes(value: float | None) -> str:
        if value is None:
            return "Unknown size"

        size = float(value)

        for unit in ("B", "KB", "MB", "GB", "TB"):
            if size < 1024 or unit == "TB":
                return f"{size:.1f} {unit}"
            size /= 1024

        return "Unknown size"

    def progress_hook(data: dict) -> None:
        nonlocal current_task, overall_task, active_index
        status = data.get("status")
        info_dict = data.get("info_dict") or {}

        index = info_dict.get("playlist_index", 1)
        video_id = info_dict.get("id") or str(index)
        video_title = info_dict.get("title", "Downloading")

        if status == "finished" and playlist:
            video_states[video_id] = "finished"

            if index not in completed_indices:
                completed_indices.add(index)

                if overall_task is not None:
                    progress.update(
                        overall_task,
                        completed=len(completed_indices),
                        detail=(
                            f"{len(completed_indices)}/{total_videos} videos completed"
                        ),
                    )

            return

        if status == "downloading":
            # A new playlist item has started.
            if active_index != index:
                if active_index is not None and playlist:
                    completed_indices.add(active_index)

                    if overall_task is not None:
                        progress.update(
                            overall_task,
                            completed=len(completed_indices),
                            detail=(
                                f"{len(completed_indices)}"
                                f"/{total_videos} videos completed"
                            ),
                        )

                active_index = index

                description = (
                    f"Video {index}/{total_videos}: {video_title}"
                    if playlist and total_videos
                    else video_title
                )

                if current_task is None:
                    current_task = progress.add_task(
                        description,
                        total=None,
                        detail="Preparing download...",
                    )
                else:
                    progress.update(
                        current_task,
                        description=description,
                        total=None,
                        completed=0,
                        detail="Preparing download...",
                    )

            downloaded = data.get("downloaded_bytes", 0)
            total = data.get("total_bytes") or data.get("total_bytes_estimate")

            speed = data.get("speed")
            eta = data.get("eta")

            details = (
                f"{format_bytes(downloaded)} / {format_bytes(total)}"
                f" • {format_bytes(speed)}/s"
            )

            if eta is not None:
                details += f" • ETA {int(eta)}s"

            progress.update(
                current_task,
                total=total,
                completed=downloaded,
                detail=details,
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

        if playlist and info.get("_type") == "playlist":
            title = info.get("title", "Unknown Playlist")
            total_videos = info.get("playlist_count")

            if total_videos is None:
                total_videos = sum(
                    1 for entry in info.get("entries", []) if entry is not None
                )

            overall_task = progress.add_task(
                "Overall playlist progress",
                total=total_videos,
                completed=0,
                detail=f"0/{total_videos} videos completed",
            )

            show_playlist_info(
                title=title,
                total_videos=total_videos,
                quality=quality,
            )
        else:
            title = info.get("title", "Unknown")

            show_video_info(
                title=title,
                quality=quality,
            )

        with progress:
            ydl.download([url])

    show_success()
