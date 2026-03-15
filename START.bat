@echo off
title MP4 to APNG Converter - Setup & Launch
color 0A

echo.
echo  ========================================
echo   MP4 to APNG Converter - Setup ^& Launch
echo  ========================================
echo.

:: ── Step 1: Check for Python ──────────────────────────────────
echo [1/3] Checking for Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo  ERROR: Python is not installed or not on your PATH.
    echo  Download it from https://www.python.org/downloads/
    echo  IMPORTANT: Check "Add Python to PATH" during install!
    echo.
    pause
    exit /b 1
)
for /f "tokens=*" %%i in ('python --version 2^>^&1') do echo        Found: %%i
echo.

:: ── Step 2: Install Flask ─────────────────────────────────────
echo [2/3] Installing Flask (if needed)...
python -m pip install flask --quiet >nul 2>&1
if errorlevel 1 (
    echo        Trying with --user flag...
    python -m pip install flask --user --quiet >nul 2>&1
)
echo        Flask is ready.
echo.

:: ── Step 3: Get FFmpeg ────────────────────────────────────────
echo [3/3] Checking for FFmpeg...

:: First check if ffmpeg.exe is already in this folder
if exist "%~dp0ffmpeg.exe" (
    echo        Found ffmpeg.exe in app folder.
    goto :ready
)

:: Check if it's on the system PATH
where ffmpeg >nul 2>&1
if not errorlevel 1 (
    echo        Found FFmpeg on system PATH.
    goto :ready
)

:: Need to download FFmpeg
echo        FFmpeg not found. Downloading now...
echo        (This is ~90MB, may take a minute)
echo.

:: Use PowerShell to download and extract
powershell -NoProfile -ExecutionPolicy Bypass -Command ^
    "$ProgressPreference = 'SilentlyContinue'; " ^
    "$url = 'https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip'; " ^
    "$zip = Join-Path '%~dp0' 'ffmpeg-download.zip'; " ^
    "$extract = Join-Path '%~dp0' 'ffmpeg-temp'; " ^
    "Write-Host '        Downloading...'; " ^
    "try { " ^
    "    Invoke-WebRequest -Uri $url -OutFile $zip -UseBasicParsing; " ^
    "    Write-Host '        Extracting...'; " ^
    "    Expand-Archive -Path $zip -DestinationPath $extract -Force; " ^
    "    $bin = Get-ChildItem -Path $extract -Recurse -Filter 'ffmpeg.exe' | Select-Object -First 1; " ^
    "    if ($bin) { " ^
    "        Copy-Item $bin.FullName (Join-Path '%~dp0' 'ffmpeg.exe'); " ^
    "        Write-Host '        FFmpeg installed successfully!'; " ^
    "    } else { " ^
    "        Write-Host '        ERROR: Could not find ffmpeg.exe in download.'; " ^
    "    } " ^
    "    Remove-Item $zip -Force -ErrorAction SilentlyContinue; " ^
    "    Remove-Item $extract -Recurse -Force -ErrorAction SilentlyContinue; " ^
    "} catch { " ^
    "    Write-Host '        ERROR: Download failed. Check your internet connection.'; " ^
    "    Write-Host \"        Details: $_\"; " ^
    "    Remove-Item $zip -Force -ErrorAction SilentlyContinue; " ^
    "}"

:: Verify it worked
if not exist "%~dp0ffmpeg.exe" (
    echo.
    echo  FFmpeg download failed. You can manually fix this:
    echo  1. Go to https://www.gyan.dev/ffmpeg/builds/
    echo  2. Download "ffmpeg-release-essentials.zip"
    echo  3. Unzip it, find ffmpeg.exe in the bin folder
    echo  4. Copy ffmpeg.exe into this folder: %~dp0
    echo  5. Run this script again.
    echo.
    pause
    exit /b 1
)

:ready
echo.
echo  ========================================
echo   All set! Launching the converter...
echo  ========================================
echo.
echo   Opening http://localhost:5000 in your browser...
echo   (Keep this window open while using the app)
echo   Press Ctrl+C here to stop the server.
echo.

:: Wait a moment then open the browser
start "" "http://localhost:5000"

:: Launch the Python app from the script's directory
cd /d "%~dp0"
python converter.py

:: If we get here, the server stopped
echo.
echo  Server stopped. Close this window or press any key.
pause >nul
