from pathlib import Path

import yt_dlp


def download_video(url: str, output_dir: str = "downloads") -> None:
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    options = {
        "outtmpl": str(output_path / "%(title)s.%(ext)s"),
        "noplaylist": True,
    }

    with yt_dlp.YoutubeDL(options) as ydl:
        ydl.download([url])
