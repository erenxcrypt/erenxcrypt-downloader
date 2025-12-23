from flask import Flask, render_template, request, jsonify, Response
import yt_dlp
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get-video', methods=['POST'])
def get_video():
    data = request.json
    url = data.get('url')
    if not url:
        return jsonify({'error': 'No URL'}), 400
    try:
        ydl_opts = {'format': 'best', 'quiet': True, 'no_warnings': True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            video_url = info.get('url')
            return jsonify({'status': 'success', 'download_url': video_url})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/proxy-download')
def proxy_download():
    video_url = request.args.get('url')
    if not video_url:
        return "Error", 400
    r = requests.get(video_url, stream=True)
    def generate():
        for chunk in r.iter_content(chunk_size=1024*1024):
            yield chunk
    return Response(generate(), headers={
        "Content-Type": "video/mp4",
        "Content-Disposition": "attachment; filename=video.mp4"
    })

if __name__ == '__main__':
    app.run(debug=True)
