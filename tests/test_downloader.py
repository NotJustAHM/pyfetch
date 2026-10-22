from pathlib import Path

from pyfetch.downloader import download_video


def test_download_function_exists():
    assert callable(download_video)
