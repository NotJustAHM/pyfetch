from pathlib import Path

import yt_dlp


def progress_hook(data: dict) -> None:
    """Display download progress."""
    status = data.get("status")

    if status == "downloading":
        downloaded = data.get("downloaded_bytes", 0)
        total = data.get("total_bytes") or data.get("total_bytes_estimate")

        speed = data.get("speed")
        eta = data.get("eta")

        if total:
            percent = downloaded / total * 100
            percent_text = f"{percent:5.1f}%"
        else:
            percent_text = "  --.-%"

        if speed:
            speed_mb = speed / 1024 / 1024
            speed_text = f"{speed_mb:.2f} MiB/s"
        else:
            speed_text = "-- MiB/s"

        if eta is not None:
            minutes, seconds = divmod(eta, 60)
            eta_text = f"{minutes:02d}:{seconds:02d}"
        else:
            eta_text = "--:--"

        print(
            f"\rDownloading: {percent_text} | {speed_text} | ETA {eta_text}",
            end="",
            flush=True,
        )

    elif status == "finished":
        print("\rDownload complete!                    ")


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

    options = {
        "outtmpl": output_template,
        "noplaylist": not playlist,
        "format": (f"bestvideo[height<={quality}]+bestaudio/best[height<={quality}]"),
        "progress_hooks": [progress_hook],
    }

    with yt_dlp.YoutubeDL(options) as ydl:
        ydl.download([url])
