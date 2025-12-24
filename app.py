from flask import Flask, render_template, request, jsonify
import yt_dlp
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get-video', methods=['POST'])
def get_video():
    data = request.json
    url = data.get('url')
    if not url:
        return jsonify({'error': 'No URL provided'}), 400

    try:
        # Simple options with User-Agent to prevent blocking
        ydl_opts = {
            'format': 'best',
            'quiet': True,
            'no_warnings': True,
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            }
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            video_url = info.get('url', None)
            
            if video_url:
                return jsonify({
                    'status': 'success',
                    'download_url': video_url
                })
            else:
                return jsonify({'error': 'Video URL not found'}), 404

    except Exception as e:
        return jsonify({'error': 'Internal Server Error'}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
