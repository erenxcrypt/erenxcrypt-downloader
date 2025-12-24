from flask import Flask, render_template, request, jsonify, Response
import yt_dlp
import requests
import os

app = Flask(__name__)

# Fake Browser Headers taaki Instagram block na kare
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Connection': 'keep-alive',
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get-video', methods=['POST'])
def get_video():
    data = request.json
    url = data.get('url')
    
    if not url or 'instagram.com' not in url:
        return jsonify({'error': 'Invalid Instagram URL'}), 400

    try:
        # Optimized options for Instagram
        ydl_opts = {
            'format': 'best',
            'quiet': True,
            'no_warnings': True,
            'ignoreerrors': True,
            'no_color': True,
            'socket_timeout': 10,
            'http_headers': HEADERS,
            # 'nocheckcertificate': True, # Agar SSL error aaye toh ye enable karein
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            if not info:
                return jsonify({'error': 'Video private hai ya link galat hai'}), 404
                
            video_url = info.get('url')
            return jsonify({'status': 'success', 'download_url': video_url})

    except Exception as e:
        print(f"Server Error: {str(e)}")
        return jsonify({'error': 'Instagram ne request block kar di hai. Thodi der baad try karein.'}), 500

@app.route('/proxy-download')
def proxy_download():
    video_url = request.args.get('url')
    if not video_url:
        return "URL missing", 400
    
    try:
        # Video ko stream karke download karwana
        r = requests.get(video_url, stream=True, headers=HEADERS, timeout=15)
        r.raise_for_status()
        
        def generate():
            for chunk in r.iter_content(chunk_size=1024*1024):
                yield chunk
        
        return Response(generate(), headers={
            "Content-Type": "video/mp4",
            "Content-Disposition": "attachment; filename=XcryptTech_Video.mp4"
        })
    except Exception as e:
        return f"Download failed: {str(e)}", 500

if __name__ == '__main__':
    # Render ke liye port management
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
