from flask import Flask, render_template, request, jsonify, Response
import yt_dlp
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get-video', methods=['POST'])
def get_video():
    url = request.json.get('url')
    
    if not url:
        return jsonify({'error': 'No URL provided'}), 400

    try:
        ydl_opts = {
            'format': 'best',
            'quiet': True,
            'no_warnings': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            video_url = info.get('url', None)
            title = info.get('title', 'xcrypt_tech_video')
            
            return jsonify({
                'status': 'success',
                'download_url': video_url,
                'title': title
            })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# 🔥 NEW: Direct Download Route (Three dots wala jhamela khatam karne ke liye)
@app.route('/proxy-download')
def proxy_download():
    video_url = request.args.get('url')
    if not video_url:
        return "No URL", 400
    
    # Video fetch karke browser ko as an attachment dena
    r = requests.get(video_url, stream=True)
    def generate():
        for chunk in r.iter_content(chunk_size=1024*1024):
            yield chunk
            
    return Response(generate(), headers={
        "Content-Type": "video/mp4",
        "Content-Disposition": "attachment; filename=XcryptTech_Video.mp4"
    })

if __name__ == '__main__':
    app.run(debug=True)
