import typer

from pyfetch.downloader import download_video


app = typer.Typer(
    name="pyfetch",
    help="A simple and beautiful CLI YouTube downloader.",
    add_completion=False,
)


@app.callback(invoke_without_command=True)
def main(
    url: str = typer.Argument(
        None,
        help="YouTube video URL",
    ),
) -> None:
    """Download a YouTube video."""

    if url is None:
        return

    typer.echo("PyFetch")
    typer.echo("YouTube Downloader")
    typer.echo("")

    download_video(url)


if __name__ == "__main__":
    app()
