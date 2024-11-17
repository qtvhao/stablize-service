from flask import Flask, request, jsonify
from flask_cors import CORS
from threading import Lock
from audio_operations import recursive_get_segments_from_audio_file
from log import Log
import json
from segment import Segment

# Initialize logger
logger = Log("/tmp/server.log")
# Lock to ensure only one request is processed at a time
request_lock = Lock()

def create_app():
    app = Flask(__name__)
    CORS(app)  # Enable CORS for all routes
    
    def to_dict(segment: Segment):
        """
        Converts a Segment object to a dictionary.
        """
        return {
            "text": segment.text,
            "start": segment.start,
            "end": segment.end,
            "words": [
                {
                    "word": word.word,
                    "start": word.start,
                    "end": word.end,
                } for word in segment.words
            ]
        }
    def to_json(segments):
        """
        Converts Segment objects to JSON format.
        """
        segments = [
            to_dict(segment) for segment in segments
        ]
        
        return json.dumps(segments, ensure_ascii=False)
    
    @app.route('/')
    def index():
        return "Hello, World!"

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
                logger.log(f"Segments: {len(segments)}")
                segments = to_json(segments)
                return segments
            except Exception as e:
                return jsonify({"error": str(e)}), 500

    return app
