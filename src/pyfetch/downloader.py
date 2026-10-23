from pathlib import Path

import yt_dlp


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
    }

    with yt_dlp.YoutubeDL(options) as ydl:
        ydl.download([url])
