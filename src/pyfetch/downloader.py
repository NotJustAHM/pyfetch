from pathlib import Path

import yt_dlp

from pyfetch.ui import (
    create_download_display,
    show_download_start,
    show_playlist_completed,
    show_playlist_info,
    show_success,
    show_video_completed,
    show_video_info,
    update_download_display,
)


def download_video(
    url: str,
    output_dir: str = "downloads",
    quality: int = 720,
    playlist: bool = False,
    cookies_from_browser: str | None = None,
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

    current_index = None
    total_videos = 1
    completed_indices = set()
    failed_indices = set()

    live = create_download_display()

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
        nonlocal current_index

        status = data.get("status")
        info_dict = data.get("info_dict") or {}

        index = info_dict.get("playlist_index", 1)
        video_title = info_dict.get("title", "Downloading")

        if status == "error":
            if playlist:
                failed_indices.add(index)

            return

        if status != "downloading":
            return

        if playlist and current_index != index:
            current_index = index

            show_download_start(
                index=index,
                total_videos=total_videos,
                title=video_title,
            )

        elif not playlist:
            current_index = index

        downloaded = data.get("downloaded_bytes", 0)
        total = data.get("total_bytes") or data.get("total_bytes_estimate")
        speed = data.get("speed")
        eta = data.get("eta")

        percentage = downloaded / total * 100 if total else 0.0

        speed_text = (
            f"{format_bytes(speed)}/s" if speed is not None else "Calculating speed..."
        )

        eta_text = f"{int(eta)}s" if eta is not None else None

        update_download_display(
            live=live,
            percentage=percentage,
            downloaded=format_bytes(downloaded),
            total=format_bytes(total),
            speed=speed_text,
            eta=eta_text,
        )

    def post_hook(filename: str) -> None:
        """Handle a video after its post-processing finishes."""
        if not playlist or current_index is None:
            return

        if current_index in completed_indices:
            return

        completed_indices.add(current_index)

        show_video_completed(
            index=current_index,
            total_videos=total_videos,
        )

        options = {
            "outtmpl": output_template,
            "noplaylist": not playlist,
            "format": (
                f"bestvideo[height<={quality}]+bestaudio/best[height<={quality}]"
            ),
            "progress_hooks": [progress_hook],
            "post_hooks": [post_hook],
            # Download resilience
            "retries": 10,
            "fragment_retries": 10,
            "file_access_retries": 5,
            "continuedl": True,
            # Playlist should continue if one video fails
            "ignoreerrors": playlist,
            "quiet": True,
            "no_warnings": True,
            "noprogress": True,
        }

        if cookies_from_browser:
            options["cookiesfrombrowser"] = (cookies_from_browser,)
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

        with live:
            ydl.download([url])

    if playlist:
        show_playlist_completed(len(completed_indices))
    else:
        show_success()
