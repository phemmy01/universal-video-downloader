#!/usr/bin/env python3
"""
Universal Video Downloader - FIXED VERSION
Resolves 'unhashable type: dict' error for audio downloads
Created by KYOP
"""

from flask import Flask, request, jsonify, send_file, render_template_string
from flask_cors import CORS
import yt_dlp
import os
import threading
import uuid
from datetime import datetime
import subprocess

app = Flask(__name__)
CORS(app)

# Configuration
DOWNLOAD_DIR = 'downloads'
os.makedirs(DOWNLOAD_DIR, exist_ok=True)
downloads = {}

def check_ffmpeg():
    """Check if FFmpeg is available"""
    try:
        subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True, timeout=5)
        return True
    except:
        return False

FFMPEG_AVAILABLE = check_ffmpeg()

def get_fixed_ytdl_opts(download_id, output_path, download_type, quality, format_type, audio_quality, audio_format):
    """Get properly configured yt-dlp options - FIXED VERSION"""

    def custom_progress_hook(d):
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
            print(f"Progress hook error: {e}")

    # Base configuration - FIXED
    base_opts = {
        'outtmpl': output_path,
        'progress_hooks': [custom_progress_hook],
        'no_warnings': False,
        'extractor_retries': 3,
        'fragment_retries': 5,
        'extract_flat': False,
        'ignoreerrors': False,
    }

    # FIXED: Audio download configuration
    if download_type == 'audio':
        if not FFMPEG_AVAILABLE:
            # Without FFmpeg - use direct audio formats
            base_opts['format'] = 'bestaudio[ext=m4a]/bestaudio[ext=webm]/bestaudio/best'
        else:
            # With FFmpeg - FIXED postprocessor configuration
            if audio_format == 'mp3':
                base_opts.update({
                    'format': 'bestaudio/best',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': str(audio_quality),  # FIXED: Convert to string
                    }]
                })
            elif audio_format == 'wav':
                base_opts.update({
                    'format': 'bestaudio/best',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'wav',
                        'preferredquality': str(audio_quality),  # FIXED: Convert to string
                    }]
                })
            elif audio_format == 'flac':
                base_opts.update({
                    'format': 'bestaudio/best',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'flac',
                        'preferredquality': str(audio_quality),  # FIXED: Convert to string
                    }]
                })
            elif audio_format == 'm4a':
                # For M4A, don't use postprocessor if not needed
                base_opts['format'] = 'bestaudio[ext=m4a]/bestaudio/best'
            else:
                base_opts['format'] = 'bestaudio/best'
    else:
        # Video download configuration - FIXED
        quality_formats = {
            '4k': 'best[height<=2160]/bestvideo[height<=2160]+bestaudio/best',
            '1440p': 'best[height<=1440]/bestvideo[height<=1440]+bestaudio/best',
            '1080p': 'best[height<=1080]/bestvideo[height<=1080]+bestaudio/best',
            '720p': 'best[height<=720]/bestvideo[height<=720]+bestaudio/best',
            '480p': 'best[height<=480]/bestvideo[height<=480]+bestaudio/best',
            '360p': 'best[height<=360]/bestvideo[height<=360]+bestaudio/best',
            'best': 'best/bestvideo+bestaudio/best'
        }

        base_opts['format'] = quality_formats.get(quality, 'best/bestvideo+bestaudio/best')

        # Add format preference if specified
        if format_type and format_type != 'auto':
            current_format = base_opts['format']
            base_opts['format'] = current_format.replace('best', f'best[ext={format_type}]')

    return base_opts

# HTML Template
HTML_TEMPLATE = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Universal Video Downloader - FIXED</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ 
            font-family: 'Segoe UI', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh; padding: 20px; 
        }}
        .container {{ 
            max-width: 700px; margin: 0 auto; background: white;
            border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            overflow: hidden;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white; text-align: center; padding: 30px;
        }}
        .header h1 {{ font-size: 2.2rem; margin-bottom: 10px; }}
        .main {{ padding: 30px; }}
        .status {{
            background: {'#d4edda' if FFMPEG_AVAILABLE else '#f8d7da'};
            color: {'#155724' if FFMPEG_AVAILABLE else '#721c24'};
            padding: 12px 20px; margin-bottom: 25px; border-radius: 8px;
            font-weight: 500;
        }}
        .form-group {{ margin-bottom: 25px; }}
        label {{ 
            display: block; margin-bottom: 10px; font-weight: 600;
            color: #333; font-size: 1.1rem;
        }}
        input, select {{ 
            width: 100%; padding: 15px; border: 2px solid #ddd;
            border-radius: 8px; font-size: 1rem; transition: border-color 0.3s;
        }}
        input:focus, select:focus {{ border-color: #667eea; outline: none; }}
        .radio-group {{ display: flex; gap: 20px; margin-top: 10px; flex-wrap: wrap; }}
        .radio-option {{ 
            display: flex; align-items: center; gap: 10px;
            padding: 15px 20px; border: 2px solid #ddd; border-radius: 25px;
            cursor: pointer; transition: all 0.3s; font-weight: 500;
        }}
        .radio-option:hover, .radio-option.active {{ 
            border-color: #667eea; background: rgba(102, 126, 234, 0.1); color: #667eea;
        }}
        .btn {{ 
            width: 100%; padding: 18px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white; border: none; border-radius: 8px;
            font-size: 1.2rem; font-weight: 600; cursor: pointer;
            margin-top: 30px; transition: transform 0.3s;
        }}
        .btn:hover {{ transform: translateY(-2px); }}
        .btn:disabled {{ opacity: 0.6; transform: none; }}
        .progress {{ 
            width: 100%; height: 25px; background: #f0f0f0;
            border-radius: 12px; margin: 20px 0; display: none; overflow: hidden;
        }}
        .progress-bar {{ 
            height: 100%; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            width: 0%; display: flex; align-items: center; justify-content: center;
            color: white; font-weight: 600; transition: width 0.3s;
        }}
        .message {{ 
            padding: 20px; border-radius: 8px; margin: 20px 0;
            display: none; line-height: 1.5;
        }}
        .error {{ background: #ffebee; color: #c62828; }}
        .success {{ background: #e8f5e8; color: #2e7d32; text-align: center; }}
        .status-msg {{ 
            text-align: center; margin: 20px 0; font-weight: 500;
            font-size: 1.1rem; display: none;
        }}
        .download-link {{ 
            display: inline-block; padding: 12px 25px; background: #4caf50;
            color: white; text-decoration: none; border-radius: 6px;
            margin-top: 15px; font-weight: 600;
        }}
        .download-link:hover {{ background: #45a049; }}
        .quality-info {{ 
            font-size: 0.9rem; color: #666; margin-top: 8px; font-style: italic;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🌍 Universal Video Downloader</h1>
            <p>FIXED - Audio Download Error Resolved</p>
            <small>Created by KYOP</small>
        </div>

        <div class="main">
            <div class="status">
                🔧 FFmpeg: {'✅ Available - All formats supported' if FFMPEG_AVAILABLE else '❌ Not found - M4A/WebM only'}
            </div>

            <form id="downloadForm">
                <div class="form-group">
                    <label for="url">Video URL (Any Platform):</label>
                    <input type="url" id="url" placeholder="https://youtube.com/... or any video URL" required>
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

                <!-- Video Options -->
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
                    <div class="quality-info">Higher quality = larger files</div>
                </div>

                <div class="form-group" id="videoFormatGroup">
                    <label for="videoFormat">Video Format:</label>
                    <select id="videoFormat">
                        <option value="mp4">MP4 (Most Compatible)</option>
                        <option value="webm">WebM</option>
                        <option value="mkv">MKV</option>
                        <option value="auto">Auto</option>
                    </select>
                </div>

                <!-- Audio Options -->
                <div class="form-group" id="audioQualityGroup" style="display: none;">
                    <label for="audioQuality">Audio Quality:</label>
                    <select id="audioQuality">
                        <option value="192">192 kbps (Recommended)</option>
                        <option value="320">320 kbps (High Quality)</option>
                        <option value="256">256 kbps</option>
                        <option value="128">128 kbps</option>
                        <option value="96">96 kbps</option>
                    </select>
                    <div class="quality-info">Higher bitrate = better quality</div>
                </div>

                <div class="form-group" id="audioFormatGroup" style="display: none;">
                    <label for="audioFormat">Audio Format:</label>
                    <select id="audioFormat">
                        {'<option value="m4a">M4A (Recommended)</option><option value="webm">WebM</option>' if not FFMPEG_AVAILABLE else '<option value="mp3">MP3 (Most Compatible)</option><option value="m4a">M4A (High Quality)</option><option value="wav">WAV (Uncompressed)</option><option value="flac">FLAC (Lossless)</option>'}
                    </select>
                    {'<div class="quality-info">Limited formats without FFmpeg</div>' if not FFMPEG_AVAILABLE else ''}
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

        // Handle download type change
        document.querySelectorAll('input[name="type"]').forEach(radio => {{
            radio.addEventListener('change', function() {{
                document.querySelectorAll('.radio-option').forEach(opt => opt.classList.remove('active'));
                this.closest('.radio-option').classList.add('active');

                const isVideo = this.value === 'video';
                document.getElementById('videoQualityGroup').style.display = isVideo ? 'block' : 'none';
                document.getElementById('videoFormatGroup').style.display = isVideo ? 'block' : 'none';
                document.getElementById('audioQualityGroup').style.display = isVideo ? 'none' : 'block';
                document.getElementById('audioFormatGroup').style.display = isVideo ? 'none' : 'block';
            }});
        }});

        document.querySelectorAll('.radio-option').forEach(option => {{
            option.addEventListener('click', function() {{
                this.querySelector('input').checked = true;
                this.querySelector('input').dispatchEvent(new Event('change'));
            }});
        }});

        document.getElementById('downloadForm').addEventListener('submit', async function(e) {{
            e.preventDefault();

            const url = document.getElementById('url').value.trim();
            const type = document.querySelector('input[name="type"]:checked').value;

            let requestData = {{ url: url, type: type }};

            if (type === 'video') {{
                requestData.quality = document.getElementById('videoQuality').value;
                requestData.format = document.getElementById('videoFormat').value;
            }} else {{
                requestData.audioQuality = document.getElementById('audioQuality').value;
                requestData.audioFormat = document.getElementById('audioFormat').value;
            }}

            if (!url || !url.startsWith('http')) {{
                showError('Please enter a valid URL');
                return;
            }}

            hideAll();
            showStatus('🚀 Starting download...');

            const btn = document.getElementById('downloadBtn');
            btn.disabled = true;
            btn.textContent = '⏳ Processing...';

            try {{
                const response = await fetch('/download', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify(requestData)
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
                        showSuccess(`✅ Download completed!<br><a href="/file/${{currentDownloadId}}" class="download-link" download>📁 Download File</a>`);
                        resetButton();
                    }} else if (data.status === 'error') {{
                        clearInterval(progressTimer);
                        showError(data.error || 'Download failed');
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
                    showError('Connection error');
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
            ['error', 'success', 'status', 'progress'].forEach(id => {{
                document.getElementById(id).style.display = 'none';
            }});
        }}

        function resetButton() {{
            const btn = document.getElementById('downloadBtn');
            btn.disabled = false;
            btn.textContent = '🚀 Start Download';
        }}
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/download', methods=['POST'])
def start_download():
    try:
        data = request.get_json()

        # FIXED: Proper parameter extraction
        url = data.get('url', '').strip()
        download_type = data.get('type', 'video')

        # Video parameters
        video_quality = data.get('quality', '1080p')
        video_format = data.get('format', 'mp4')

        # Audio parameters - FIXED
        audio_quality = data.get('audioQuality', '192')
        audio_format = data.get('audioFormat', 'm4a')

        print(f"Download request - URL: {url}, Type: {download_type}")
        print(f"Audio Quality: {audio_quality}, Audio Format: {audio_format}")

        if not url or not url.startswith(('http://', 'https://')):
            return jsonify({'error': 'Invalid URL format'}), 400

        download_id = str(uuid.uuid4())

        downloads[download_id] = {
            'status': 'starting',
            'progress': 0,
            'filename': None,
            'error': None,
            'created_at': datetime.now()
        }

        # Start download thread
        thread = threading.Thread(
            target=download_video_fixed,
            args=(download_id, url, download_type, video_quality, video_format, audio_quality, audio_format)
        )
        thread.daemon = True
        thread.start()

        return jsonify({'download_id': download_id, 'status': 'started'})

    except Exception as e:
        print(f"Download start error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/progress/<download_id>')
def get_progress(download_id):
    if download_id not in downloads:
        return jsonify({'error': 'Download not found'}), 404
    return jsonify(downloads[download_id])

@app.route('/file/<download_id>')
def download_file(download_id):
    if download_id not in downloads:
        return jsonify({'error': 'Download not found'}), 404

    info = downloads[download_id]
    if info['status'] != 'completed' or not info['filename']:
        return jsonify({'error': 'File not ready'}), 400

    if not os.path.exists(info['filename']):
        return jsonify({'error': 'File not found'}), 404

    return send_file(info['filename'], as_attachment=True)

def download_video_fixed(download_id, url, download_type, video_quality, video_format, audio_quality, audio_format):
    """FIXED download function that handles audio downloads properly"""
    try:
        print(f"Starting download {download_id}: {url}")
        downloads[download_id]['status'] = 'preparing'

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = os.path.join(DOWNLOAD_DIR, f'{download_id}_{timestamp}.%(ext)s')

        # FIXED: Use the corrected yt-dlp options
        ydl_opts = get_fixed_ytdl_opts(
            download_id, output_path, download_type, 
            video_quality, video_format, audio_quality, audio_format
        )

        print(f"yt-dlp options: {ydl_opts}")
        downloads[download_id]['status'] = 'downloading'

        # FIXED: Proper error handling for yt-dlp
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                ydl.download([url])
            except Exception as dl_error:
                print(f"yt-dlp error: {dl_error}")
                # Try simpler format if the complex one fails
                if download_type == 'audio':
                    print("Retrying with simpler audio format...")
                    simple_opts = ydl_opts.copy()
                    simple_opts['format'] = 'bestaudio/best'
                    simple_opts.pop('postprocessors', None)  # Remove postprocessors

                    with yt_dlp.YoutubeDL(simple_opts) as ydl_simple:
                        ydl_simple.download([url])
                else:
                    raise dl_error

        # Find downloaded file
        if downloads[download_id]['status'] != 'completed':
            for file in os.listdir(DOWNLOAD_DIR):
                if file.startswith(download_id):
                    downloads[download_id]['filename'] = os.path.join(DOWNLOAD_DIR, file)
                    downloads[download_id]['status'] = 'completed'
                    downloads[download_id]['progress'] = 100
                    print(f"Download completed: {file}")
                    break

    except Exception as e:
        error_msg = str(e)
        print(f"Download error for {download_id}: {error_msg}")
        downloads[download_id]['status'] = 'error'
        downloads[download_id]['error'] = f"Download failed: {error_msg}"

if __name__ == '__main__':
    print("=" * 60)
    print("🌍 UNIVERSAL VIDEO DOWNLOADER - FIXED VERSION")
    print("Created by KYOP")
    print("=" * 60)
    print("✅ Fixed 'unhashable type: dict' error")
    print("✅ Improved audio download handling")
    print("✅ Better error recovery")
    print(f"🔧 FFmpeg: {'Available' if FFMPEG_AVAILABLE else 'Not found'}")
    print("🚀 Server starting at: http://localhost:5000")
    print("=" * 60)

    try:
        app.run(host='0.0.0.0', port=5000, debug=False)
    except KeyboardInterrupt:
        print("\n✅ Server stopped")
    except Exception as e:
        print(f"\n❌ Server error: {e}")
        input("Press Enter to exit...")
