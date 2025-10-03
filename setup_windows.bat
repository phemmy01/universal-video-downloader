@echo off
echo.
echo ========================================
echo   Universal Video Downloader Setup
echo   Created by KYOP
echo ========================================
echo.

echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo.
    echo Please install Python from: https://python.org/downloads
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

echo ✅ Python found
echo.

echo Installing required packages...
echo.

pip install flask flask-cors yt-dlp gunicorn
if errorlevel 1 (
    echo.
    echo ERROR: Failed to install packages
    echo Trying alternative method...
    python -m pip install flask flask-cors yt-dlp gunicorn
    if errorlevel 1 (
        echo.
        echo ERROR: Package installation failed
        echo Please check your internet connection and try again
        pause
        exit /b 1
    )
)

echo.
echo ✅ All packages installed successfully!
echo.

echo Checking FFmpeg for audio conversion...
ffmpeg -version >nul 2>&1
if errorlevel 1 (
    echo ⚠️  FFmpeg not found
    echo Audio conversion will be limited to M4A and WebM formats
    echo.
    echo To install FFmpeg:
    echo 1. Download from: https://ffmpeg.org/download.html
    echo 2. Extract to C:\ffmpeg
    echo 3. Add C:\ffmpeg\bin to your PATH
    echo.
) else (
    echo ✅ FFmpeg found - All audio formats available
)

echo.
echo ========================================
echo   Setup Complete!
echo ========================================
echo.
echo To run the video downloader:
echo   1. Run: python server.py
echo   2. Open browser to: http://localhost:5000
echo   3. Start downloading from any platform!
echo.
echo Created by KYOP
echo Repository: github.com/KYOP/universal-video-downloader
echo.
pause