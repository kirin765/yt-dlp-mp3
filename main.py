from flask import Flask, request, jsonify, send_file
import yt_dlp
import os
import uuid

app = Flask(__name__)
SAVE_DIR = "/tmp"

@app.route('/download', methods=['POST'])
def download():
    data = request.get_json()
    url = data.get('url')
    if not url:
        return jsonify({'error': 'No URL provided'}), 400

    uid = str(uuid.uuid4())
    filename = f"{uid}.mp3"
    filepath = os.path.join(SAVE_DIR, filename)

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': filepath,
        'quiet': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
        }],
    'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'geo_bypass': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return jsonify({'download': f'/file/{filename}'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/file/<filename>')
def serve_file(filename):
    path = os.path.join(SAVE_DIR, filename)
    if os.path.exists(path):
        return send_file(path, mimetype='audio/mpeg', as_attachment=True)
    else:
        return "File not found", 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
