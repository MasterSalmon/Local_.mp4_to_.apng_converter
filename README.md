# 🎬 MP4 → APNG Converter

A free, local, one-click tool for converting MP4 video clips to **Animated PNG (APNG)** — perfect for creating animated character card portraits in [SillyTavern](https://github.com/SillyTavern/SillyTavern) and other LLM frontends.

![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)
![Platform: Windows](https://img.shields.io/badge/Platform-Windows-0078D6.svg)
![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-3776AB.svg)


---

## Why APNG?

**GIF** is limited to 256 colors and looks terrible for character art. **MP4** isn't supported as an image format in most apps. **APNG** is the sweet spot — it's a full-quality animated image format with 24-bit color and transparency support, and it works anywhere PNG works (including SillyTavern character cards).

## Features

- **Drag & drop** — no command line needed
- **Video preview** — see your clip before converting
- **Trim slider** — drag handles to select exactly the portion you want
- **Adjustable settings** — frame rate, width, and loop count
- **One-click setup** — `START.bat` handles all dependencies automatically
- **100% local** — your files never leave your computer
- **Free & open source** — no accounts, no ads, no tracking

## Screenshot

![MP4 to APNG Converter](Screenshot%202026-03-15%20031103.png)


## Quick Start (Windows)

### Prerequisites

- **Python 3.8+** — [Download here](https://www.python.org/downloads/)
  - ⚠️ During install, check **"Add Python to PATH"**

### Setup & Run

1. [Download the latest release](../../releases/latest) (or clone this repo)
2. Double-click **`START.bat`**
3. That's it! The script will:
   - Install Flask (Python web framework)
   - Download FFmpeg automatically if needed (~90MB, first run only)
   - Open the converter in your browser

### Usage

1. **Drop an MP4** onto the upload area (or click to browse)
2. **Trim** your clip using the draggable handles or type exact timestamps
3. **Adjust settings** — 15fps and 320px width work great for SillyTavern
4. **Click Convert** and download your `.apng` file

## Recommended Settings for SillyTavern

| Setting | Recommended | Why |
|---------|-------------|-----|
| FPS | 10–15 | Smooth enough, keeps file size down |
| Width | 320px | Matches typical card portrait size |
| Loop | Infinite | Keeps the animation going |
| Clip length | Under 5s | Keeps file size manageable |

> **Tip:** APNG files are larger than MP4s since there's no inter-frame video compression. A 5-second clip at 320px/15fps will typically be 2–10MB depending on content complexity.

## Using APNG in SillyTavern

1. Convert your clip with this tool
2. In SillyTavern, edit a character card
3. Click the avatar/portrait image
4. Select your `.apng` file
5. The portrait will now animate!

## Project Structure

```
mp4-to-apng/
├── START.bat        # One-click setup & launcher (Windows)
├── converter.py     # Python/Flask backend
├── index.html       # Web frontend
├── README.md        # You are here
├── LICENSE          # MIT License
├── uploads/         # Temporary (auto-created, auto-cleaned)
└── outputs/         # Your converted files end up here
```

## Manual Setup (if START.bat doesn't work)

```bash
# Install Flask
python -m pip install flask

# Place ffmpeg.exe in the same folder as converter.py
# Download from: https://www.gyan.dev/ffmpeg/builds/

# Run the app
python converter.py

# Open in your browser
# http://localhost:5000
```

## Running on macOS / Linux

The converter works on any platform, but `START.bat` is Windows-only. On Mac/Linux:

```bash
# Install FFmpeg via your package manager
# macOS:
brew install ffmpeg
# Ubuntu/Debian:
sudo apt install ffmpeg

# Install Flask
pip install flask

# Run
python converter.py
```

## Tech Stack

- **Backend:** Python + Flask
- **Frontend:** Vanilla HTML/CSS/JS (no build tools, no frameworks)
- **Conversion:** FFmpeg (bundled or system-installed)


## License

MIT — do whatever you want with it.

## Acknowledgments

- [FFmpeg](https://ffmpeg.org/) — the engine that makes it all work
- [SillyTavern](https://github.com/SillyTavern/SillyTavern) — the community that inspired this tool
- Built with help from [Claude](https://claude.ai) by Anthropic
