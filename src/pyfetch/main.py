from pyfetch.downloader import download_video


def main() -> None:
    print("PyFetch")
    print("YouTube Downloader")

    url = input("\nEnter YouTube URL: ").strip()

    if not url:
        print("Error: URL cannot be empty.")
        return

    download_video(url)


if __name__ == "__main__":
    main()
