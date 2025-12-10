from flask import Flask, render_template, request, jsonify
import yt_dlp

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
        # Options set karte hain taaki direct download link mile
        ydl_opts = {
            'format': 'best',  # Best quality
            'quiet': True,
            'no_warnings': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            video_url = info.get('url', None)
            title = info.get('title', 'Video')
            
            return jsonify({
                'status': 'success',
                'download_url': video_url,
                'title': title
            })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
