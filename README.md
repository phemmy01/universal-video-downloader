# 🌍 Universal Video Downloader

<div align="center">

![Video Downloader Banner]([https://img.shields.io/badge/Universal-Video%20Downloader-blue?style=for-the-badge&logo=youtube](https://youtu.be/0wkS79Bt1Lo))
![Quality](https://img.shields.io/badge/Quality-360p%20to%204K-green?style=for-the-badge)
![Platforms](https://img.shields.io/badge/Platforms-1000%2B-red?style=for-the-badge)
![Free](https://img.shields.io/badge/Hosting-Free-brightgreen?style=for-the-badge)

**Download videos from ANY platform with intelligent quality selection and dynamic interface**

</div>

---

## ✨ Features

🎬 **Universal Platform Support**
- YouTube, Instagram, TikTok, Facebook, Twitter, Vimeo
- Reddit, Twitch, Dailymotion, SoundCloud, Bandcamp
- **1000+ platforms worldwide** supported via yt-dlp

🎚️ **Complete Quality Range**
- **Video**: 360p, 480p, 720p, 1080p, 1440p, 4K Ultra HD
- **Audio**: 96kbps, 128kbps, 192kbps, 256kbps, 320kbps

🔄 **Smart Dynamic Interface**
- Select "Video + Audio" → Shows video quality & format options
- Select "Audio Only" → Shows audio quality & format options
- No clutter - only see what you need!

🎵 **Multiple Format Support**
- **Video**: MP4 (most compatible), WebM, MKV
- **Audio**: MP3, M4A, WAV, FLAC, OGG (with FFmpeg)

⚡ **Advanced Features**
- Real-time download progress tracking
- Automatic platform detection
- FFmpeg auto-detection with fallbacks
- Rate limiting and security features
- Auto-cleanup after 2 hours
<div align="center">
<img width="701" height="844" alt="image" src="https://github.com/user-attachments/assets/cec676a8-187e-4c9c-a142-e90b62c61221" />


---

## 🖥️ Windows Installation Guide

### Prerequisites
- **Windows 10/11** (Windows 7/8 may work)
- **Python 3.7 or newer**
- **Internet connection**

### Step 1: Install Python
1. Go to **https://python.org/downloads**
2. Download **Python 3.12** (latest version)
3. **IMPORTANT**: Check ✅ **"Add Python to PATH"** during installation
4. Click **"Install Now"**
5. Verify installation:
   ```cmd
   python --version
   ```
   Should show: `Python 3.12.x`

### Step 2: Download the Project
**Option A: Download ZIP (Easiest)**
1. Click the **green "Code"** button above
2. Select **"Download ZIP"**
3. Extract to a folder (e.g., `C:\VideoDownloader`)

**Option B: Clone with Git**
```cmd
git clone https://github.com/KYOOOOP/universal-video-downloader.git
cd universal-video-downloader
```

### Step 3: Install Dependencies
1. Open **Command Prompt** (type `cmd` in Start menu)
2. Navigate to your project folder:
   ```cmd
   cd C:\VideoDownloader\universal-video-downloader
   ```
3. Install required packages:
   ```cmd
   pip install -r requirements.txt
   ```

   If `pip` doesn't work, try:
   ```cmd
   python -m pip install -r requirements.txt
   ```

### Step 4: Install FFmpeg (For Audio Conversion)
**Option A: Automatic (Recommended)**
```cmd
pip install ffmpeg-python
```

**Option B: Manual Installation**
1. Download from **https://ffmpeg.org/download.html#build-windows**
2. Extract to `C:\ffmpeg`
3. Add `C:\ffmpeg\bin` to Windows PATH:
   - Press `Win + R`, type `sysdm.cpl`
   - Click **"Environment Variables"**
   - Under **"System Variables"**, find **"Path"**
   - Click **"Edit"** → **"New"** → Add `C:\ffmpeg\bin`
   - Click **"OK"** on all windows
   - Restart Command Prompt

### Step 5: Run the Application
1. In Command Prompt, run:
   ```cmd
   python server.py
   ```
2. You should see:
   ```
   🌍 UNIVERSAL VIDEO DOWNLOADER
   ✅ Server starting at: http://localhost:5000
   ```
3. Open your browser and go to: **http://localhost:5000**

### Step 6: Start Downloading! 🎉
1. Paste any video URL
2. Choose Video+Audio or Audio Only
3. Select your preferred quality and format
4. Click **"Start Download"**
5. Watch real-time progress
6. Download your file when complete!

---

## 🌐 Use Online (No Installation Required)

**Live Demo:** [Deploy on Railway](https://railway.app) or [Deploy on Render](https://render.com)

Just click the deployment button and have your own online video downloader in 2 minutes!

---

## 🎯 How to Use

### Video + Audio Download
1. Paste any video URL (YouTube, Instagram, TikTok, etc.)
2. Select **"Video + Audio"**
3. Choose quality: **360p** (small) to **4K** (huge)
4. Pick format: **MP4** (recommended), WebM, or MKV
5. Click **"Start Download"**

### Audio Only Download  
1. Paste any video/music URL
2. Select **"Audio Only"**
3. Choose bitrate: **96kbps** (small) to **320kbps** (high quality)
4. Pick format: **MP3** (universal), M4A, WAV, FLAC
5. Click **"Start Download"**

The interface automatically shows only relevant options based on your selection!

---

## 🛠️ Troubleshooting

### "Script crashes immediately"
```cmd
python --version
pip install flask flask-cors yt-dlp
```

### "FFmpeg not found" (for audio conversion)
- Install FFmpeg using the guide above
- Or use M4A/WebM formats (no conversion needed)

### "Port already in use"
- Close other applications using port 5000
- Or change the port in `server.py`

### "Permission denied"
- Run Command Prompt as Administrator
- Or choose a different folder with write permissions

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## ⚠️ Legal Notice

This tool is for educational purposes and personal use only. Please respect:
- Copyright laws and intellectual property rights
- Platform terms of service
- Fair use guidelines
- Content creator rights

Users are responsible for ensuring their use complies with applicable laws and regulations.

---

## 🙏 Credits & Acknowledgments

**Created by:** [KYOOOOP](https://github.com/KYOOOOP)

**Built with:**
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - Universal video downloader
- [Flask](https://flask.palletsprojects.com/) - Web framework
- [FFmpeg](https://ffmpeg.org/) - Audio/video processing

**Special Thanks:**
- yt-dlp community for maintaining 1000+ extractors
- Flask community for the excellent web framework
- All contributors who help improve this project

---

## 📊 Statistics

- **Supported Platforms:** 1000+
- **Quality Options:** 7 (360p to 4K)
- **Audio Bitrates:** 5 (96kbps to 320kbps)
- **Video Formats:** MP4, WebM, MKV
- **Audio Formats:** MP3, M4A, WAV, FLAC, OGG

---

## 🔗 Links

- **Issues:** [Report bugs or request features](https://github.com/KYOOOOP/universal-video-downloader/issues)
- **Discussions:** [Community discussions](https://github.com/KYOOOOP/universal-video-downloader/discussions)
- **Releases:** [Download stable releases](https://github.com/KYOOOOP/universal-video-downloader/releases)

---

<div align="center">

**⭐ Star this repository if you find it helpful!**

**Made with ❤️ by KYOP**

*Bringing free video downloading to everyone worldwide*

</div>
