from audio_operations import recursive_get_segments_from_audio_file
import json
audio_file = "synthesize-result-2532432836.mp3"
tokens_texts_file = "tokens.json"
tokens = json.load(open(tokens_texts_file))
tokens_texts = [token['text'] for token in tokens]
segments = recursive_get_segments_from_audio_file(audio_file, tokens_texts)
