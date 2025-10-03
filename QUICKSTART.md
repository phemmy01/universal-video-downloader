# 🚀 Quick Start Guide

## For Windows Users (Easiest)

### One-Click Setup
1. Download all files from GitHub
2. Double-click **setup_windows.bat**
3. Follow the installation prompts
4. Run **python server.py** when setup completes
5. Open **http://localhost:5000** in your browser

### Manual Setup
```cmd
# Check Python
python --version

# Install packages
pip install flask flask-cors yt-dlp

# Run server
python server.py

# Open browser
http://localhost:5000
```

## For Mac/Linux Users

### Installation
```bash
# Install packages
pip3 install flask flask-cors yt-dlp

# Install FFmpeg (optional for audio conversion)
# Mac:
brew install ffmpeg

# Ubuntu/Debian:
sudo apt install ffmpeg

# Run server
python3 server.py

# Open browser
http://localhost:5000
```

## 🌐 Use Online (No Installation)

Deploy for free on:
- **Railway:** [![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/template)
- **Render:** Click "Deploy" button on their website
- **PythonAnywhere:** Upload files and create web app

## 🎯 Features Overview

### When you select "Video + Audio":
- **Quality options:** 360p, 480p, 720p, 1080p, 1440p, 4K
- **Format options:** MP4, WebM, MKV

### When you select "Audio Only":  
- **Quality options:** 96kbps, 128kbps, 192kbps, 256kbps, 320kbps
- **Format options:** MP3, M4A, WAV, FLAC (with FFmpeg)

### Supported Platforms:
YouTube, Instagram, TikTok, Facebook, Twitter, Vimeo, Reddit, Twitch, SoundCloud, and 1000+ more!

---

**Created by KYOP** • Star ⭐ this repository if you find it helpful!
