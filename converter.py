"""
MP4 → APNG Converter (with trim support)
A local web app for converting short video clips to Animated PNG format.
Run this script, then open http://localhost:5000 in your browser.

Requirements:
    pip install flask
    FFmpeg must be installed and on your system PATH, or in the same folder as this script.
"""

import os
import re
import sys
import uuid
import subprocess
import shutil
from pathlib import Path
from flask import Flask, request, jsonify, send_file, send_from_directory

# ── Check for FFmpeg ──────────────────────────────────────────────
SCRIPT_DIR = Path(__file__).parent
LOCAL_FFMPEG = SCRIPT_DIR / "ffmpeg.exe"

if LOCAL_FFMPEG.exists():
    FFMPEG = str(LOCAL_FFMPEG)
    print(f"✅  Found FFmpeg at: {FFMPEG}")
else:
    FFMPEG = shutil.which("ffmpeg")
    if not FFMPEG:
        print("\n❌  FFmpeg not found!")
        print("    Place ffmpeg.exe in this folder, or add it to your system PATH.")
        print("    Download from https://ffmpeg.org/download.html\n")
        sys.exit(1)
    else:
        print(f"✅  Found FFmpeg at: {FFMPEG}")

# ── App setup ─────────────────────────────────────────────────────
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # 500 MB max upload

BASE_DIR = Path(__file__).parent
UPLOAD_DIR = BASE_DIR / "uploads"
OUTPUT_DIR = BASE_DIR / "outputs"
UPLOAD_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

# ── Global error handlers (always return JSON, never HTML) ────────
@app.errorhandler(413)
def too_large(e):
    return jsonify({"error": "File too large. Max size is 500 MB."}), 413

@app.errorhandler(500)
def server_error(e):
    return jsonify({"error": f"Server error: {str(e)}"}), 500

@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Not found"}), 404

# ── Serve the frontend ────────────────────────────────────────────
@app.route("/")
def index():
    return send_from_directory(BASE_DIR, "index.html")

# ── Serve uploaded videos for preview ─────────────────────────────
@app.route("/uploads/<filename>")
def serve_upload(filename):
    if not filename.endswith(".mp4"):
        return "Invalid file", 400
    filepath = UPLOAD_DIR / filename
    if not filepath.exists():
        return "File not found", 404
    return send_file(filepath, mimetype="video/mp4")

# ── Upload endpoint (for preview) ────────────────────────────────
@app.route("/upload", methods=["POST"])
def upload():
    try:
        if "file" not in request.files:
            return jsonify({"error": "No file uploaded"}), 400

        file = request.files["file"]
        if not file.filename or not file.filename.lower().endswith(".mp4"):
            return jsonify({"error": "Only .mp4 files are supported"}), 400

        job_id = uuid.uuid4().hex[:8]
        filename = f"{job_id}.mp4"
        input_path = UPLOAD_DIR / filename
        file.save(str(input_path))

        # Get video duration using ffprobe
        duration = None
        ffprobe_path = FFMPEG.replace("ffmpeg", "ffprobe")
        if Path(ffprobe_path).exists():
            try:
                result = subprocess.run(
                    [ffprobe_path, "-v", "error", "-show_entries", "format=duration",
                     "-of", "default=noprint_wrappers=1:nokey=1", str(input_path)],
                    capture_output=True, text=True, timeout=10
                )
                duration = float(result.stdout.strip())
            except Exception:
                pass

        # Fallback: parse duration from ffmpeg stderr
        if duration is None:
            try:
                result = subprocess.run(
                    [FFMPEG, "-i", str(input_path)],
                    capture_output=True, text=True, timeout=10
                )
                match = re.search(r"Duration: (\d+):(\d+):(\d+)\.(\d+)", result.stderr)
                if match:
                    h, m, s, ms = match.groups()
                    duration = int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 100
            except Exception:
                pass

        return jsonify({
            "success": True,
            "job_id": job_id,
            "filename": filename,
            "preview_url": f"/uploads/{filename}",
            "duration": duration,
            "file_size": input_path.stat().st_size
        })

    except Exception as e:
        return jsonify({"error": f"Upload failed: {str(e)}"}), 500

# ── Convert endpoint ──────────────────────────────────────────────
@app.route("/convert", methods=["POST"])
def convert():
    data = request.get_json()
    if not data or "job_id" not in data:
        return jsonify({"error": "Missing job_id"}), 400

    job_id = data["job_id"]
    input_path = UPLOAD_DIR / f"{job_id}.mp4"

    if not input_path.exists():
        return jsonify({"error": "Source file not found. Please re-upload."}), 400

    # Get settings
    try:
        fps = max(1, min(60, int(data.get("fps", 15))))
        width = max(0, min(3840, int(data.get("width", 0))))
        loops = max(0, min(100, int(data.get("loops", 0))))
        trim_start = float(data.get("trim_start", 0))
        trim_end = float(data.get("trim_end", 0))
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid settings"}), 400

    output_path = OUTPUT_DIR / f"{job_id}.apng"

    # Build FFmpeg command
    cmd = [FFMPEG, "-y"]

    if trim_start > 0:
        cmd += ["-ss", f"{trim_start:.3f}"]

    cmd += ["-i", str(input_path)]

    if trim_end > 0 and trim_end > trim_start:
        duration = trim_end - trim_start
        cmd += ["-t", f"{duration:.3f}"]

    vf_filters = [f"fps={fps}"]
    if width > 0:
        vf_filters.append(f"scale={width}:-1")

    cmd += [
        "-plays", str(loops),
        "-vf", ",".join(vf_filters),
        str(output_path)
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)

        if result.returncode != 0:
            input_path.unlink(missing_ok=True)
            error_msg = result.stderr[-500:] if result.stderr else "Unknown error"
            return jsonify({"error": f"FFmpeg failed:\n{error_msg}"}), 500

        input_size = input_path.stat().st_size
        output_size = output_path.stat().st_size
        input_path.unlink(missing_ok=True)

        return jsonify({
            "success": True,
            "filename": f"{job_id}.apng",
            "input_size": input_size,
            "output_size": output_size
        })

    except subprocess.TimeoutExpired:
        input_path.unlink(missing_ok=True)
        return jsonify({"error": "Conversion timed out (2 min limit)"}), 500
    except Exception as e:
        input_path.unlink(missing_ok=True)
        return jsonify({"error": str(e)}), 500

# ── Download endpoint ─────────────────────────────────────────────
@app.route("/download/<filename>")
def download(filename):
    if not filename.endswith(".apng"):
        return "Invalid file", 400
    filepath = OUTPUT_DIR / filename
    if not filepath.exists():
        return "File not found", 404
    return send_file(filepath, as_attachment=True, download_name=filename)

# ── Preview endpoint ──────────────────────────────────────────────
@app.route("/preview/<filename>")
def preview(filename):
    if not filename.endswith(".apng"):
        return "Invalid file", 400
    filepath = OUTPUT_DIR / filename
    if not filepath.exists():
        return "File not found", 404
    return send_file(filepath, mimetype="image/apng")

# ── Start the server ──────────────────────────────────────────────
if __name__ == "__main__":
    print("\n🎬  MP4 → APNG Converter is running!")
    print("    Open http://localhost:5000 in your browser.\n")
    print("    Press Ctrl+C to stop.\n")
    app.run(host="127.0.0.1", port=5000, debug=False)
