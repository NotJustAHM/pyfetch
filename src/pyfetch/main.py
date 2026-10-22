from pathlib import Path
from typing import Annotated

import typer

from pyfetch.downloader import download_video


def main(
    url: Annotated[
        str,
        typer.Argument(help="YouTube video or playlist URL"),
    ],
    quality: Annotated[
        int,
        typer.Option(
            "--quality",
            "-q",
            min=144,
            max=4320,
            help="Maximum video resolution",
        ),
    ] = 720,
    output: Annotated[
        Path,
        typer.Option(
            "--output",
            "-o",
            help="Directory where downloaded files are saved",
        ),
    ] = Path("downloads"),
    playlist: Annotated[
        bool,
        typer.Option(
            "--playlist",
            "-p",
            help="Download the entire playlist",
        ),
    ] = False,
) -> None:
    """Download YouTube videos and playlists."""
    typer.echo("PyFetch")
    typer.echo("YouTube Downloader")
    typer.echo("")

    download_video(
        url=url,
        output_dir=str(output),
        quality=quality,
        playlist=playlist,
    )


def cli() -> None:
    typer.run(main)


if __name__ == "__main__":
    cli()
