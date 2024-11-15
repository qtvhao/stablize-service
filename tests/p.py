import json

file_json = "./tests/synthesize-result-2532432836.json"
fopen = open(file_json, "r")
data = json.load(fopen)

segments = data.get('segments', [])
segments = [
    {
        "start": segment['start'],
        "end": segment['end'],
        "text": segment['text'],
        "words": [{
            "word": word['word'],
            "start": word['start'],
            "end": word['end'],
            "probability": round(word['probability'] * 1e5) / 1e5,
        } for word in segment['words']]
    } for segment in segments
]
print(json.dumps(segments, indent=2, ensure_ascii=False))

with open(file_json.replace('.json', '-segments.json'), 'w') as file:
    json.dump(segments, file, indent=2, ensure_ascii=False)