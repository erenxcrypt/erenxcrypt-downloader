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
        # Advanced options taaki Instagram block na kare
        ydl_opts = {
            'format': 'best',
            'quiet': True,
            'no_warnings': True,
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-us,en;q=0.5',
            }
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            video_url = info.get('url')
            if not video_url:
                return jsonify({'error': 'Could not extract URL'}), 404
            return jsonify({'status': 'success', 'download_url': video_url})
            
    except Exception as e:
        print(f"Error: {str(e)}") # Ye Render logs mein dikhega
        return jsonify({'error': 'Failed to fetch video'}), 500

@app.route('/proxy-download')
def proxy_download():
    video_url = request.args.get('url')
    if not video_url:
        return "Error", 400
    
    # User-Agent ke saath fetch karna zaroori hai
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    r = requests.get(video_url, stream=True, headers=headers)
    
    def generate():
        for chunk in r.iter_content(chunk_size=1024*1024):
            yield chunk
            
    return Response(generate(), headers={
        "Content-Type": "video/mp4",
        "Content-Disposition": "attachment; filename=XcryptTech_Video.mp4"
    })

if __name__ == '__main__':
    app.run(debug=True)
