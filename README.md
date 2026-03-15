# Local_.mp4_to_.apng_converter

Features

Drag & drop — no command line needed
Video preview — see your clip before converting
Trim slider — drag handles to select exactly the portion you want
Adjustable settings — frame rate, width, and loop count
One-click setup — START.bat handles all dependencies automatically
100% local — your files never leave your computer
Free & open source — no accounts, no ads, no tracking


Quick Start (Windows)
Prerequisites

Python 3.8+ — Download here

⚠️ During install, check "Add Python to PATH"



Setup & Run

Download the latest release (or clone this repo)
Double-click START.bat
That's it! The script will:

Install Flask (Python web framework)
Download FFmpeg automatically if needed (~90MB, first run only)
Open the converter in your browser



Usage

Drop an MP4 onto the upload area (or click to browse)
Trim your clip using the draggable handles or type exact timestamps
Adjust settings — 15fps and 320px width work great for SillyTavern
Click Convert and download your .apng file

Recommended Settings for SillyTavern
SettingRecommendedWhyFPS10–15Smooth enough, keeps file size downWidth320pxMatches typical card portrait sizeLoopInfiniteKeeps the animation goingClip lengthUnder 5sKeeps file size manageable

Tip: APNG files are larger than MP4s since there's no inter-frame video compression. A 5-second clip at 320px/15fps will typically be 2–10MB depending on content complexity.

Using APNG in SillyTavern

Convert your clip with this tool
In SillyTavern, edit a character card
Click the avatar/portrait image
Select your .apng file
The portrait will now animate!

Project Structure
mp4-to-apng/
├── START.bat        # One-click setup & launcher (Windows)
├── converter.py     # Python/Flask backend
├── index.html       # Web frontend
├── README.md        # You are here
├── LICENSE          # MIT License
├── uploads/         # Temporary (auto-created, auto-cleaned)
└── outputs/         # Your converted files end up here
Manual Setup (if START.bat doesn't work)
bash# Install Flask
python -m pip install flask

# Place ffmpeg.exe in the same folder as converter.py
# Download from: https://www.gyan.dev/ffmpeg/builds/

# Run the app
python converter.py

# Open in your browser
# http://localhost:5000
Running on macOS / Linux
The converter works on any platform, but START.bat is Windows-only. On Mac/Linux:
bash# Install FFmpeg via your package manager
# macOS:
brew install ffmpeg
# Ubuntu/Debian:
sudo apt install ffmpeg

# Install Flask
pip install flask

# Run
python converter.py
Tech Stack

Backend: Python + Flask
Frontend: Vanilla HTML/CSS/JS (no build tools, no frameworks)
Conversion: FFmpeg (bundled or system-installed)

Acknowledgments
FFmpeg — the engine that makes it all work
SillyTavern — the community that inspired this tool
Built with help from Claude by Anthropic

FFmpeg — the engine that makes it all work
SillyTavern — the community that inspired this tool
Built with help from Claude by Anthropic
