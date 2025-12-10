from flask import Flask, render_template, request, redirect, url_for
from yt_dlp import YoutubeDL
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download_video():
    url = request.form.get('video_url')
    
    if not url:
        return "Error: Link toh dalo bhai!"

    # Options to get direct link (Server pe file save nahi karenge, direct URL denge)
    ydl_opts = {
        'format': 'best',
        'quiet': True,
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False) # Sirf info nikalo
            video_title = info.get('title', 'Video')
            video_url = info.get('url') # Direct video link (googlevideo.com wala)
            thumbnail = info.get('thumbnail')
            
            return render_template('index.html', 
                                   title=video_title, 
                                   link=video_url, 
                                   thumb=thumbnail,
                                   show_result=True)
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)