# PyFetch

A simple command-line YouTube downloader built with Python and `yt-dlp`.

PyFetch started as a small project for learning Python and building something practical. The goal is to keep the project simple, understandable, and useful while adding features step by step.

Currently, PyFetch supports downloading individual videos and playlists, selecting video quality, choosing an output directory, browser cookies, and displaying download progress in the terminal.

> **PyFetch is still under development.**

---

## Features

- Download individual YouTube videos
- Download YouTube playlists
- Select maximum video quality
- Custom output directory
- Automatic playlist numbering
- Download progress with speed and ETA
- Resume interrupted downloads
- Automatic retries for failed downloads
- Continue playlists when individual videos fail
- Browser cookie support
- YouTube JavaScript challenge solving through EJS
- Windows and Linux support
- Clean terminal interface

---

## Requirements

- Python 3.10+
- FFmpeg
- Deno 2.x
- `yt-dlp` and other Python dependencies installed through the project

If you want to use browser cookies, you also need a supported browser such as Firefox, Chrome, or Edge.

---

## Installation

### Clone the repository

```bash
git clone https://github.com/NotJustAHM/pyfetch.git
cd pyfetch
```

### Create a virtual environment

#### Linux

```bash
python -m venv .venv
source .venv/bin/activate
```

#### Windows PowerShell

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### Install PyFetch

```bash
pip install -e .
```

Check that everything is working:

```bash
pyfetch --help
```

---

## Usage

The basic syntax is:

```bash
pyfetch <URL>
```

### Download a video

```bash
pyfetch "https://www.youtube.com/watch?v=VIDEO_ID"
```

The default maximum quality is `720p`.

### Choose video quality

```bash
pyfetch "https://www.youtube.com/watch?v=VIDEO_ID" -q 1080
```

You can also use:

```bash
pyfetch "https://www.youtube.com/watch?v=VIDEO_ID" --quality 1080
```

### Choose an output directory

Use `-o` or `--output`:

```bash
pyfetch "https://www.youtube.com/watch?v=VIDEO_ID" -o videos
```

You can also use an absolute path:

```powershell
pyfetch "https://www.youtube.com/watch?v=VIDEO_ID" -o "C:\Users\username\Videos"
```

The default output directory is:

```text
downloads/
```

### Download a playlist

Use `-p` or `--playlist`:

```bash
pyfetch "https://www.youtube.com/playlist?list=PLAYLIST_ID" -p
```

You can combine it with quality and output options:

```bash
pyfetch "https://www.youtube.com/playlist?list=PLAYLIST_ID" \
    -p \
    -q 1080 \
    -o videos
```

Playlist files are automatically numbered:

```text
001 - First Video
002 - Second Video
003 - Third Video
```

---

## Browser Cookies

Some YouTube videos may require an authenticated session or trigger bot detection.

PyFetch can use cookies directly from a supported browser.

### Firefox

```bash
pyfetch "https://www.youtube.com/watch?v=VIDEO_ID" \
    --cookies-from-browser firefox
```

### Chrome

```bash
pyfetch "https://www.youtube.com/watch?v=VIDEO_ID" \
    --cookies-from-browser chrome
```

### Edge

```bash
pyfetch "https://www.youtube.com/watch?v=VIDEO_ID" \
    --cookies-from-browser edge
```

You can also use cookies while downloading a playlist:

```bash
pyfetch "https://www.youtube.com/playlist?list=PLAYLIST_ID" \
    -p \
    -q 1080 \
    --cookies-from-browser firefox
```

> **Important:** Browser cookies are sensitive information. Never upload or commit cookie files to the repository.

---

## YouTube JavaScript Challenges

YouTube sometimes requires JavaScript challenges to be solved before video formats can be accessed.

PyFetch uses `yt-dlp`'s EJS support with Deno to handle these challenges.

The relevant configuration is:

```python
"remote_components": "ejs:github"
```

You can check your Deno installation with:

```bash
deno --version
```

When everything is configured correctly, `yt-dlp` should show:

```text
[youtube] [jsc:deno] Solving JS challenges using deno
```

---

## Command Options

Run:

```bash
pyfetch --help
```

Current options:

| Option | Short | Default | Description |
|---|---|---:|---|
| `--quality` | `-q` | `720` | Maximum video resolution |
| `--output` | `-o` | `downloads` | Directory where files are saved |
| `--playlist` | `-p` | `False` | Download the entire playlist |
| `--cookies-from-browser` | — | `None` | Use cookies from a browser |

### Example

```bash
pyfetch "https://www.youtube.com/playlist?list=PLAYLIST_ID" \
    -p \
    -q 1080 \
    -o videos \
    --cookies-from-browser firefox
```

---

## How It Works

The current download flow is fairly simple:

```text
YouTube URL
     │
     ▼
   PyFetch
     │
     ▼
   yt-dlp
     │
     ├── Extract video / playlist information
     ├── Solve YouTube challenges
     ├── Select available formats
     └── Download media
             │
             ▼
           FFmpeg
             │
             ▼
       Final video file
```

For playlists, PyFetch also keeps track of completed and failed videos and shows the final result in the terminal.

---

## Project Structure

```text
pyfetch/
├── src/
│   └── pyfetch/
│       ├── main.py
│       ├── downloader.py
│       └── ui.py
│
├── pyproject.toml
├── README.md
└── ...
```

### `main.py`

Handles the command-line interface and command-line arguments.

### `downloader.py`

Contains the main downloading logic and communicates with `yt-dlp`.

It handles things such as:

- Video downloads
- Playlist downloads
- Format selection
- Download retries
- Browser cookies
- Progress hooks
- Playlist completion tracking

### `ui.py`

Contains the terminal interface.

It is responsible for:

- Download progress
- Video information
- Playlist information
- Success and failure messages

---

## Download Reliability

Downloads can fail for many different reasons, especially when downloading large files or using an unstable connection.

PyFetch currently uses several `yt-dlp` options to make downloads more reliable:

```text
retries: 10
fragment_retries: 10
file_access_retries: 5
continuedl: True
```

For playlists, PyFetch allows the remaining videos to continue downloading if one video fails:

```text
ignoreerrors: True
```

This means one failed video does not stop the entire playlist.

---

## Playlist Output

When downloading a playlist, PyFetch creates a directory using the playlist name.

For example:

```text
downloads/
└── Playlist Name/
    ├── 001 - First Video.mp4
    ├── 002 - Second Video.mp4
    ├── 003 - Third Video.mp4
    └── ...
```

At the end of the download, PyFetch shows the overall result:

```text
┌─────────────────────────────────┐
│ ✓ Playlist download completed   │
│                                 │
│ 18/18 videos                    │
└─────────────────────────────────┘
```

If some videos fail:

```text
┌─────────────────────────────────┐
│ ✓ Playlist download completed   │
│                                 │
│ 15/18 videos                    │
│ 3 failed                        │
└─────────────────────────────────┘
```

---

## Why I Built This

I wanted to build something small enough to understand from beginning to end, while still dealing with problems that appear in real projects.

PyFetch has been a way for me to practice:

- Python
- CLI application development
- Git and GitHub
- Working with third-party libraries
- Error handling
- File management
- FFmpeg
- `yt-dlp`
- Terminal UI
- Cross-platform development

I'm building the project step by step instead of trying to implement everything at once.

---

## Development

Clone the repository:

```bash
git clone https://github.com/NotJustAHM/pyfetch.git
cd pyfetch
```

Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

On Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Install the project in editable mode:

```bash
pip install -e .
```

Then:

```bash
pyfetch --help
```

---

## Main Dependencies

PyFetch is built around a few main tools:

| Tool | Purpose |
|---|---|
| Python | Programming language |
| Typer | CLI interface |
| Rich | Terminal UI |
| yt-dlp | Video extraction and downloading |
| FFmpeg | Media processing and merging |
| Deno | JavaScript runtime for YouTube challenge solving |

---

## Disclaimer

PyFetch is a personal and educational project built around `yt-dlp`.

Please respect YouTube's Terms of Service, copyright laws, and the rights of content creators. Only download content that you are legally allowed to download.

PyFetch does not provide or host any copyrighted content.

---

## License

This project is licensed under the MIT License.

See the `LICENSE` file for details.

---

## Author

**NotJustAHM**

Computer Engineering student interested in:

- Data Science
- Bioinformatics
- Python
- Linux
- Backend Development
- Systems
- Open Source

---

⭐ If you find the project interesting, feel free to star the repository.
