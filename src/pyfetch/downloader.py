from pathlib import Path

import yt_dlp


def download_video(
    url: str,
    output_dir: str = "downloads",
    quality: int = 720,
) -> None:
    output_path = Path(output_dir).expanduser()
    output_path.mkdir(parents=True, exist_ok=True)

    options = {
        "outtmpl": str(output_path / "%(title)s.%(ext)s"),
        "noplaylist": True,
        "format": (f"bestvideo[height<={quality}]+bestaudio/best[height<={quality}]"),
    }

    with yt_dlp.YoutubeDL(options) as ydl:
        ydl.download([url])
