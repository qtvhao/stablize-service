from flask import Flask, request, jsonify
from threading import Lock
from audio_operations import recursive_get_segments_from_audio_file

# Lock to ensure only one request is processed at a time
request_lock = Lock()

def create_app():
    app = Flask(__name__)

    @app.route('/stablize', methods=['POST'])
    def stablize():
        # Acquire lock to ensure single request handling
        with request_lock:
            data = request.get_json()
            if not data or 'audio_file' not in data or 'tokens_texts' not in data:
                return jsonify({"error": "Missing required parameters"}), 400

            audio_file = data['audio_file']
            tokens_texts = data['tokens_texts']

            try:
                segments = recursive_get_segments_from_audio_file(audio_file, tokens_texts)
                return jsonify(segments), 200
            except Exception as e:
                return jsonify({"error": str(e)}), 500

    return app
