#!/usr/bin/env python3
"""
Enhanced Bulletproof Video Downloader
Dynamic quality and format options with 360p-4K support
"""

import sys
import os

def safe_print(msg):
    try:
        print(msg)
    except:
        pass

def safe_input(msg):
    try:
        return input(msg)
    except:
        return ""

safe_print("Enhanced Video Downloader with Dynamic Options")
safe_print("=" * 50)

# Check Python version
try:
    safe_print(f"Python version: {sys.version}")
    if sys.version_info < (3, 6):
        safe_print("ERROR: Need Python 3.6 or newer")
        safe_input("Press Enter to exit...")
        sys.exit(1)
    safe_print("✅ Python version OK")
except Exception as e:
    safe_print(f"Python check failed: {e}")
    safe_input("Press Enter to exit...")
    sys.exit(1)

# Test basic imports
basic_modules = ['os', 'sys', 'threading', 'json', 'urllib', 'subprocess']
for module in basic_modules:
    try:
        __import__(module)
        safe_print(f"✅ {module} - OK")
    except Exception as e:
        safe_print(f"❌ {module} - FAILED: {e}")
        safe_input("Press Enter to exit...")
        sys.exit(1)

# Test required packages
packages_to_test = [
    ('flask', 'pip install flask'),
    ('flask_cors', 'pip install flask-cors'),
    ('yt_dlp', 'pip install yt-dlp')
]

missing_packages = []

for package_name, install_cmd in packages_to_test:
    try:
        __import__(package_name)
        safe_print(f"✅ {package_name} - OK")
    except ImportError:
        safe_print(f"❌ {package_name} - MISSING")
        safe_print(f"   Install with: {install_cmd}")
        missing_packages.append((package_name, install_cmd))
    except Exception as e:
        safe_print(f"❌ {package_name} - ERROR: {e}")
        missing_packages.append((package_name, install_cmd))

if missing_packages:
    safe_print("\n" + "=" * 50)
    safe_print("MISSING PACKAGES FOUND!")
    safe_print("=" * 50)
    safe_print("Run these commands to install missing packages:")
    safe_print("")
    for package_name, install_cmd in missing_packages:
        safe_print(f"  {install_cmd}")
    safe_print("")
    safe_print("After installing, run this script again.")
    safe_input("\nPress Enter to exit...")
    sys.exit(1)

safe_print("\n✅ All packages are installed!")

# Check FFmpeg availability
def check_ffmpeg():
    try:
        import subprocess
        subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True, timeout=5)
        return True
    except:
        try:
            subprocess.run(['ffmpeg.exe', '-version'], capture_output=True, check=True, timeout=5)
            return True
        except:
            return False

ffmpeg_available = check_ffmpeg()
safe_print(f"🔧 FFmpeg: {'✅ Available' if ffmpeg_available else '❌ Not found (limited audio formats)'}")

# Start server
try:
    from flask import Flask, request, jsonify, send_file
    from flask_cors import CORS
    import threading
    import uuid
    import json
    from datetime import datetime

    safe_print("✅ Imports successful")

    app = Flask(__name__)
    CORS(app)

    # Create downloads directory
    try:
        DOWNLOAD_DIR = 'downloads'
        os.makedirs(DOWNLOAD_DIR, exist_ok=True)
        safe_print(f"✅ Downloads directory: {os.path.abspath(DOWNLOAD_DIR)}")
    except Exception as e:
        safe_print(f"❌ Cannot create downloads directory: {e}")
        safe_input("Press Enter to exit...")
        sys.exit(1)

    downloads = {}

    # Enhanced HTML with dynamic options
    HTML_PAGE = f"""<!DOCTYPE html>
<html><head>
<title>Enhanced Video Downloader</title>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ 
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    min-height: 100vh; 
    padding: 20px; 
}}
.container {{ 
    max-width: 700px; 
    margin: 0 auto; 
    background: white; 
    border-radius: 15px; 
    box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    overflow: hidden;
}}
.header {{
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    text-align: center;
    padding: 30px;
}}
.header h1 {{ 
    font-size: 2.2rem; 
    margin-bottom: 10px; 
}}
.main {{ padding: 30px; }}
.ffmpeg-status {{
    background: {'#d4edda' if ffmpeg_available else '#f8d7da'};
    color: {'#155724' if ffmpeg_available else '#721c24'};
    padding: 12px 20px;
    margin-bottom: 25px;
    border-radius: 8px;
    font-weight: 500;
    font-size: 0.9rem;
}}
.form-group {{ margin-bottom: 25px; }}
label {{ 
    display: block; 
    margin-bottom: 10px; 
    font-weight: 600; 
    color: #333;
    font-size: 1.1rem;
}}
input[type="url"], select {{ 
    width: 100%; 
    padding: 15px; 
    border: 2px solid #ddd; 
    border-radius: 8px; 
    font-size: 1rem;
    transition: border-color 0.3s;
}}
input[type="url"]:focus, select:focus {{ 
    border-color: #667eea; 
    outline: none; 
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}}
.radio-group {{ 
    display: flex; 
    gap: 20px; 
    margin-top: 10px;
    flex-wrap: wrap;
}}
.radio-option {{ 
    display: flex; 
    align-items: center; 
    gap: 10px; 
    padding: 15px 20px; 
    border: 2px solid #ddd; 
    border-radius: 25px; 
    cursor: pointer;
    transition: all 0.3s;
    font-weight: 500;
}}
.radio-option:hover, .radio-option.active {{ 
    border-color: #667eea; 
    background: rgba(102, 126, 234, 0.1);
    color: #667eea;
}}
.btn {{ 
    width: 100%; 
    padding: 18px; 
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
    color: white; 
    border: none; 
    border-radius: 8px; 
    font-size: 1.2rem; 
    font-weight: 600; 
    cursor: pointer; 
    margin-top: 30px;
    transition: transform 0.3s;
}}
.btn:hover {{ transform: translateY(-2px); box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4); }}
.btn:disabled {{ opacity: 0.6; transform: none; cursor: not-allowed; }}
.progress {{ 
    width: 100%; 
    height: 25px; 
    background: #f0f0f0; 
    border-radius: 12px; 
    margin: 20px 0; 
    display: none;
    overflow: hidden;
}}
.progress-bar {{ 
    height: 100%; 
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
    border-radius: 12px; 
    width: 0%; 
    text-align: center; 
    line-height: 25px; 
    color: white; 
    font-weight: 600;
    transition: width 0.3s;
}}
.message {{ 
    padding: 20px; 
    border-radius: 8px; 
    margin: 20px 0; 
    display: none;
    font-size: 0.95rem;
    line-height: 1.5;
}}
.error {{ background: #ffebee; color: #c62828; }}
.success {{ background: #e8f5e8; color: #2e7d32; text-align: center; }}
.status-msg {{ 
    text-align: center; 
    margin: 20px 0; 
    font-weight: 500; 
    font-size: 1.1rem;
    display: none;
}}
.download-link {{ 
    display: inline-block; 
    padding: 12px 25px; 
    background: #4caf50; 
    color: white; 
    text-decoration: none; 
    border-radius: 6px; 
    margin-top: 15px;
    font-weight: 600;
    transition: background 0.3s;
}}
.download-link:hover {{ background: #45a049; }}
.quality-info {{
    font-size: 0.9rem;
    color: #666;
    margin-top: 8px;
    font-style: italic;
}}
.platform-detected {{
    background: #e8f5e8;
    color: #2e7d32;
    padding: 8px 15px;
    border-radius: 6px;
    margin-top: 10px;
    font-size: 0.9rem;
    display: none;
}}
@media (max-width: 768px) {{
    .radio-group {{ flex-direction: column; gap: 10px; }}
    .container {{ margin: 0 10px; }}
    .header h1 {{ font-size: 1.8rem; }}
}}
</style>
</head>
<body>
<div class="container">
    <div class="header">
        <h1>🌍 Enhanced Video Downloader</h1>
        <p>Download from any platform with dynamic quality options</p>
    </div>

    <div class="main">
        <div class="ffmpeg-status">
            🔧 FFmpeg: {'✅ Available - All audio formats supported' if ffmpeg_available else '❌ Not found - Limited to M4A/WebM audio'}
        </div>

        <form id="downloadForm">
            <div class="form-group">
                <label for="url">Video URL (Any Platform):</label>
                <input type="url" id="url" placeholder="https://youtube.com/... or any video URL" required>
                <div class="platform-detected" id="platformDetected"></div>
            </div>

            <div class="form-group">
                <label>Download Type:</label>
                <div class="radio-group">
                    <label class="radio-option active">
                        <input type="radio" name="type" value="video" checked>
                        <span>🎥 Video + Audio</span>
                    </label>
                    <label class="radio-option">
                        <input type="radio" name="type" value="audio">
                        <span>🎵 Audio Only</span>
                    </label>
                </div>
            </div>

            <!-- Video Quality Options -->
            <div class="form-group" id="videoQualityGroup">
                <label for="videoQuality">Video Quality:</label>
                <select id="videoQuality">
                    <option value="1080p">1080p Full HD (Recommended)</option>
                    <option value="720p">720p HD</option>
                    <option value="480p">480p SD</option>
                    <option value="360p">360p</option>
                    <option value="1440p">1440p 2K</option>
                    <option value="4k">4K Ultra HD</option>
                    <option value="best">Best Available</option>
                </select>
                <div class="quality-info">Higher quality = larger file size and longer download time</div>
            </div>

            <!-- Audio Quality Options -->
            <div class="form-group" id="audioQualityGroup" style="display: none;">
                <label for="audioQuality">Audio Quality:</label>
                <select id="audioQuality">
                    <option value="192">192 kbps (Recommended)</option>
                    <option value="320">320 kbps (High Quality)</option>
                    <option value="256">256 kbps</option>
                    <option value="128">128 kbps</option>
                    <option value="96">96 kbps (Low Quality)</option>
                </select>
                <div class="quality-info">Higher bitrate = better audio quality and larger file size</div>
            </div>

            <!-- Video Format Options -->
            <div class="form-group" id="videoFormatGroup">
                <label for="videoFormat">Video Format:</label>
                <select id="videoFormat">
                    <option value="mp4">MP4 (Most Compatible)</option>
                    <option value="webm">WebM (Smaller Size)</option>
                    <option value="mkv">MKV (High Quality)</option>
                    <option value="auto">Auto (Best for Platform)</option>
                </select>
            </div>

            <!-- Audio Format Options -->
            <div class="form-group" id="audioFormatGroup" style="display: none;">
                <label for="audioFormat">Audio Format:</label>
                <select id="audioFormat">
                    {'<option value="m4a">M4A (No FFmpeg Required)</option><option value="webm">WebM (No FFmpeg Required)</option>' if not ffmpeg_available else '<option value="mp3">MP3 (Most Compatible)</option><option value="m4a">M4A (High Quality)</option><option value="wav">WAV (Uncompressed)</option><option value="flac">FLAC (Lossless)</option><option value="ogg">OGG</option>'}
                </select>
                {'<div class="quality-info">⚠️ Install FFmpeg for MP3, WAV, FLAC conversion</div>' if not ffmpeg_available else '<div class="quality-info">Choose the format that works best for your device</div>'}
            </div>

            <button type="submit" class="btn" id="downloadBtn">
                🚀 Start Download
            </button>
        </form>

        <div class="progress" id="progress">
            <div class="progress-bar" id="progressBar">0%</div>
        </div>

        <div class="status-msg" id="status"></div>
        <div class="message error" id="error"></div>
        <div class="message success" id="success"></div>
    </div>
</div>

<script>
let currentDownloadId = null;
let progressTimer = null;

// Platform detection
function detectPlatform(url) {{
    const platforms = {{
        'YouTube': ['youtube.com', 'youtu.be'],
        'Instagram': ['instagram.com'],
        'TikTok': ['tiktok.com'],
        'Facebook': ['facebook.com', 'fb.watch'],
        'Twitter': ['twitter.com', 'x.com'],
        'Vimeo': ['vimeo.com'],
        'Reddit': ['reddit.com', 'v.redd.it'],
        'Twitch': ['twitch.tv'],
        'Dailymotion': ['dailymotion.com'],
        'SoundCloud': ['soundcloud.com']
    }};

    const urlLower = url.toLowerCase();
    for (const [platform, domains] of Object.entries(platforms)) {{
        if (domains.some(domain => urlLower.includes(domain))) {{
            return platform;
        }}
    }}
    return 'Supported Platform';
}}

// Update platform detection on URL change
document.getElementById('url').addEventListener('input', function() {{
    const url = this.value.trim();
    const platformDiv = document.getElementById('platformDetected');

    if (url && url.startsWith('http')) {{
        const platform = detectPlatform(url);
        platformDiv.innerHTML = `<i class="fas fa-check"></i> Platform detected: <strong>${{platform}}</strong>`;
        platformDiv.style.display = 'block';
    }} else {{
        platformDiv.style.display = 'none';
    }}
}});

// Handle download type change
document.querySelectorAll('input[name="type"]').forEach(radio => {{
    radio.addEventListener('change', function() {{
        // Update radio button styling
        document.querySelectorAll('.radio-option').forEach(opt => opt.classList.remove('active'));
        this.closest('.radio-option').classList.add('active');

        // Show/hide quality and format options based on selection
        const isVideo = this.value === 'video';

        document.getElementById('videoQualityGroup').style.display = isVideo ? 'block' : 'none';
        document.getElementById('audioQualityGroup').style.display = isVideo ? 'none' : 'block';
        document.getElementById('videoFormatGroup').style.display = isVideo ? 'block' : 'none';
        document.getElementById('audioFormatGroup').style.display = isVideo ? 'none' : 'block';
    }});
}});

// Handle radio button clicking
document.querySelectorAll('.radio-option').forEach(option => {{
    option.addEventListener('click', function() {{
        document.querySelectorAll('.radio-option').forEach(opt => opt.classList.remove('active'));
        this.classList.add('active');
        this.querySelector('input').checked = true;

        // Trigger change event
        this.querySelector('input').dispatchEvent(new Event('change'));
    }});
}});

// Handle form submission
document.getElementById('downloadForm').addEventListener('submit', async function(e) {{
    e.preventDefault();

    const url = document.getElementById('url').value.trim();
    const type = document.querySelector('input[name="type"]:checked').value;

    let quality, format, audioQuality, audioFormat;

    if (type === 'video') {{
        quality = document.getElementById('videoQuality').value;
        format = document.getElementById('videoFormat').value;
    }} else {{
        audioQuality = document.getElementById('audioQuality').value;
        audioFormat = document.getElementById('audioFormat').value;
    }}

    if (!url || !url.startsWith('http')) {{
        showError('Please enter a valid URL starting with http:// or https://');
        return;
    }}

    hideAll();
    showStatus('🚀 Starting download...');

    const downloadBtn = document.getElementById('downloadBtn');
    downloadBtn.disabled = true;
    downloadBtn.textContent = '⏳ Processing...';

    try {{
        const response = await fetch('/download', {{
            method: 'POST',
            headers: {{ 'Content-Type': 'application/json' }},
            body: JSON.stringify({{
                url: url,
                type: type,
                quality: quality,
                format: format,
                audioQuality: audioQuality,
                audioFormat: audioFormat
            }})
        }});

        const result = await response.json();

        if (result.error) {{
            throw new Error(result.error);
        }}

        currentDownloadId = result.download_id;
        showStatus('📥 Download started...');
        document.getElementById('progress').style.display = 'block';

        checkProgress();

    }} catch (error) {{
        showError('Download failed: ' + error.message);
        resetButton();
    }}
}});

async function checkProgress() {{
    if (!currentDownloadId) return;

    progressTimer = setInterval(async () => {{
        try {{
            const response = await fetch(`/progress/${{currentDownloadId}}`);
            const data = await response.json();

            if (data.status === 'completed') {{
                clearInterval(progressTimer);
                document.getElementById('progressBar').style.width = '100%';
                document.getElementById('progressBar').textContent = '100%';
                showSuccess(`<i class="fas fa-check-circle"></i> Download completed successfully!<br><a href="/file/${{currentDownloadId}}" class="download-link" download>📁 Download File</a>`);
                resetButton();
            }} else if (data.status === 'error') {{
                clearInterval(progressTimer);
                showError('Download failed: ' + (data.error || 'Unknown error'));
                resetButton();
            }} else if (data.status === 'downloading') {{
                const progress = Math.round(data.progress || 0);
                document.getElementById('progressBar').style.width = progress + '%';
                document.getElementById('progressBar').textContent = progress + '%';
                showStatus(`📥 Downloading... ${{progress}}%`);
            }} else {{
                showStatus('🔄 ' + data.status + '...');
            }}
        }} catch (error) {{
            clearInterval(progressTimer);
            showError('Connection error while checking progress');
            resetButton();
        }}
    }}, 2000);
}}

function showError(msg) {{
    hideAll();
    document.getElementById('error').innerHTML = '❌ ' + msg;
    document.getElementById('error').style.display = 'block';
}}

function showSuccess(msg) {{
    hideAll();
    document.getElementById('success').innerHTML = msg;
    document.getElementById('success').style.display = 'block';
}}

function showStatus(msg) {{
    document.getElementById('status').textContent = msg;
    document.getElementById('status').style.display = 'block';
}}

function hideAll() {{
    document.getElementById('error').style.display = 'none';
    document.getElementById('success').style.display = 'none';
    document.getElementById('status').style.display = 'none';
    document.getElementById('progress').style.display = 'none';
}}

function resetButton() {{
    document.getElementById('downloadBtn').disabled = false;
    document.getElementById('downloadBtn').textContent = '🚀 Start Download';
}}
</script>
</body></html>"""

    @app.route('/')
    def home():
        try:
            return HTML_PAGE
        except Exception as e:
            return f"Error loading page: {e}", 500

    @app.route('/download', methods=['POST'])
    def download():
        try:
            data = request.get_json()
            url = data.get('url', '').strip()
            download_type = data.get('type', 'video')
            quality = data.get('quality', '1080p')
            format_type = data.get('format', 'mp4')
            audio_quality = data.get('audioQuality', '192')
            audio_format = data.get('audioFormat', 'm4a')

            safe_print(f"Download request: {url}, type: {download_type}, quality: {quality}")

            if not url or not url.startswith(('http://', 'https://')):
                return jsonify({'error': 'Invalid URL format'})

            download_id = str(uuid.uuid4())
            downloads[download_id] = {
                'status': 'starting',
                'progress': 0,
                'filename': None,
                'error': None
            }

            # Start download in background
            thread = threading.Thread(target=download_video, args=(
                download_id, url, download_type, quality, format_type, audio_quality, audio_format
            ))
            thread.daemon = True
            thread.start()

            return jsonify({'download_id': download_id, 'status': 'started'})

        except Exception as e:
            safe_print(f"Download route error: {e}")
            return jsonify({'error': str(e)})

    @app.route('/progress/<download_id>')
    def get_progress(download_id):
        try:
            if download_id not in downloads:
                return jsonify({'error': 'Download not found'})
            return jsonify(downloads[download_id])
        except Exception as e:
            return jsonify({'error': str(e)})

    @app.route('/file/<download_id>')
    def get_file(download_id):
        try:
            if download_id not in downloads:
                return "Download not found", 404

            info = downloads[download_id]
            if info['status'] != 'completed' or not info['filename']:
                return "File not ready", 400

            if not os.path.exists(info['filename']):
                return "File not found", 404

            return send_file(info['filename'], as_attachment=True)
        except Exception as e:
            return f"File error: {e}", 500

    def progress_hook(d, download_id):
        try:
            if download_id in downloads:
                if d['status'] == 'downloading':
                    if 'total_bytes' in d and d['total_bytes']:
                        progress = (d['downloaded_bytes'] / d['total_bytes']) * 100
                        downloads[download_id]['progress'] = min(progress, 100)
                        downloads[download_id]['status'] = 'downloading'
                elif d['status'] == 'finished':
                    downloads[download_id]['status'] = 'completed'
                    downloads[download_id]['progress'] = 100
                    downloads[download_id]['filename'] = d['filename']
        except Exception as e:
            safe_print(f"Progress hook error: {e}")

    def download_video(download_id, url, download_type, quality, format_type, audio_quality, audio_format):
        try:
            import yt_dlp

            safe_print(f"Starting download: {url}")
            downloads[download_id]['status'] = 'preparing'

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = os.path.join(DOWNLOAD_DIR, f'{download_id}_{timestamp}.%(ext)s')

            # Enhanced yt-dlp options with quality support
            ydl_opts = {
                'outtmpl': output_path,
                'progress_hooks': [lambda d: progress_hook(d, download_id)],
                'no_warnings': True,
                'extractor_retries': 3,
                'fragment_retries': 5,
            }

            if download_type == 'audio':
                # Audio download options
                if not ffmpeg_available:
                    # Without FFmpeg - direct audio formats
                    ydl_opts['format'] = 'bestaudio[ext=m4a]/bestaudio[ext=webm]/bestaudio/best'
                else:
                    # With FFmpeg - conversion available
                    if audio_format == 'mp3':
                        ydl_opts.update({{
                            'format': 'bestaudio/best',
                            'postprocessors': [{{
                                'key': 'FFmpegExtractAudio',
                                'preferredcodec': 'mp3',
                                'preferredquality': audio_quality,
                            }}]
                        }})
                    elif audio_format == 'm4a':
                        ydl_opts['format'] = 'bestaudio[ext=m4a]/bestaudio/best'
                    else:
                        ydl_opts.update({{
                            'format': 'bestaudio/best',
                            'postprocessors': [{{
                                'key': 'FFmpegExtractAudio',
                                'preferredcodec': audio_format,
                                'preferredquality': audio_quality,
                            }}]
                        }})
            else:
                # Video download options with full quality range
                format_preference = ''
                if format_type != 'auto':
                    format_preference = f'[ext={format_type}]'

                if quality == 'best':
                    ydl_opts['format'] = f'best{format_preference}/best'
                elif quality == '4k':
                    ydl_opts['format'] = f'best[height<=2160]{format_preference}/best[height<=2160]/best'
                elif quality == '1440p':
                    ydl_opts['format'] = f'best[height<=1440]{format_preference}/best[height<=1440]/best'
                elif quality == '1080p':
                    ydl_opts['format'] = f'best[height<=1080]{format_preference}/best[height<=1080]/best'
                elif quality == '720p':
                    ydl_opts['format'] = f'best[height<=720]{format_preference}/best[height<=720]/best'
                elif quality == '480p':
                    ydl_opts['format'] = f'best[height<=480]{format_preference}/best[height<=480]/best'
                elif quality == '360p':
                    ydl_opts['format'] = f'best[height<=360]{format_preference}/best[height<=360]/best'
                else:
                    ydl_opts['format'] = f'best{format_preference}/best'

            safe_print(f"yt-dlp options: {ydl_opts}")
            downloads[download_id]['status'] = 'downloading'

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            # Find the downloaded file
            if downloads[download_id]['status'] != 'completed':
                for file in os.listdir(DOWNLOAD_DIR):
                    if file.startswith(download_id):
                        downloads[download_id]['filename'] = os.path.join(DOWNLOAD_DIR, file)
                        downloads[download_id]['status'] = 'completed'
                        downloads[download_id]['progress'] = 100
                        safe_print(f"Download completed: {file}")
                        break

        except Exception as e:
            error_msg = str(e)
            safe_print(f"Download error: {error_msg}")
            downloads[download_id]['status'] = 'error'
            downloads[download_id]['error'] = error_msg

    # Start the server
    safe_print("\n" + "=" * 50)
    safe_print("🚀 ENHANCED VIDEO DOWNLOADER")
    safe_print("=" * 50)
    safe_print("✅ Dynamic quality options: 360p to 4K")
    safe_print("✅ Separate video and audio settings")
    safe_print("✅ Universal platform support")
    safe_print(f"🔧 FFmpeg: {'Available' if ffmpeg_available else 'Limited audio formats'}")
    safe_print("🌐 Open browser: http://localhost:5000")
    safe_print("⏹️  Press Ctrl+C to stop")
    safe_print("=" * 50)
    safe_print("")

    try:
        app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)
    except KeyboardInterrupt:
        safe_print("\n✅ Server stopped by user")
    except Exception as e:
        safe_print(f"\n❌ Server error: {e}")

except Exception as e:
    safe_print(f"\n❌ Fatal error: {e}")
    import traceback
    traceback.print_exc()

safe_print("\nScript finished.")
safe_input("Press Enter to exit...")
