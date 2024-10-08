import yt_dlp
from flask import Flask, request, jsonify, send_file

app = Flask(__name__)


# New Hello World endpoint
@app.route('/', methods=['GET'])
def hello_world():
    return "Hello, World!,This service is working as expected"


@app.route('/download', methods=['GET'])
def download():
    song_name = request.args.get('song_name')
    download_type = request.args.get('type', 'video')  # Default is 'video'

    if not song_name:
        return jsonify({"error": "Please provide a song name"}), 400

    # Configure yt-dlp options
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best' if download_type == 'video' else 'bestaudio/best',
        'ffmpeg_location': r"/home/ecs-assist-user/youtube_downloader/ffmpeg/bin",  # Adjust this path if needed
        'outtmpl': '%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }] if download_type == 'audio' else [],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(f"ytsearch:{song_name}", download=True)
            file_name = ydl.prepare_filename(info['entries'][0])

            # For audio, convert file extension from webm to mp3 if necessary
            if download_type == 'audio':
                file_name = file_name.replace('.webm', '.mp3')

            return send_file(file_name, as_attachment=True)

        except Exception as e:
            return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=False)
