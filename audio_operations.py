import subprocess
import json
import os
from sentence_matcher import SentenceMatcher
from segment import Segment
from os.path import basename, dirname
# import stable_whisper
# from time import sleep
from alignutils import find_best_segment_match
# model = stable_whisper.load_model(name="tiny", in_memory=True)

from random import randint
ffmpeg_executable = "/usr/bin/ffmpeg"
if not os.path.exists(ffmpeg_executable):
    ffmpeg_executable = "ffmpeg"
    # raise ValueError("ffmpeg not found")

def seconds_to_ffmpeg_time(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    sec = seconds % 60
    return f"{hours:02}:{minutes:02}:{sec:06.3f}"

def cut_audio_file(audio_file, start=None, end=None):
    start_str = str(start).replace('.', '_') if start is not None else 'start'
    end_str = str(end).replace('.', '_') if end is not None else 'end'
    output_file = audio_file.replace('_end', '').replace('.mp3', f'___{start_str}_{end_str}.mp3')
    if start is None:
        args = [ffmpeg_executable, "-y", "-i", audio_file, "-to", seconds_to_ffmpeg_time(end), "-c", "copy", output_file]
    elif end is None:
        args = [ffmpeg_executable, "-y", "-i", audio_file, "-ss", seconds_to_ffmpeg_time(start), "-c", "copy", output_file]
    else:
        args = [ffmpeg_executable, "-y", "-i", audio_file, "-ss", seconds_to_ffmpeg_time(start), "-to", seconds_to_ffmpeg_time(end), "-c", "copy", output_file]

    process = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    return_code = process.returncode
    print(f"Return code: {return_code}")
    if return_code != 0:
        raise ValueError("ffmpeg command failed with return code: " + str(return_code))

    # Print stdout and stderr
    print("=== ffmpeg stdout ===")
    print(process.stdout)
    print("=== ffmpeg stderr ===")
    print(process.stderr)

    process.check_returncode()  # Ensure the subprocess completed successfully
    print(f"Cut audio file from {start} to {end} to {output_file}")
    return output_file

def get_segments_from_audio_file(audio_file, tokens_texts, output_file='output.json'):
    tokens_texts_joined = "\n\n".join(tokens_texts)
    tmp_file = prepare_tmp_file(tokens_texts_joined)
    stable_exec = find_stable_ts_executable()
    run_stable_ts(audio_file, tmp_file, output_file, stable_exec)
    check_output_file(output_file)
    return get_segments_from_segments_file(audio_file, tokens_texts, output_file)

def prepare_tmp_file(tokens_texts_joined):
    tmp_file = '/tmp/align-input-' + str(randint(0, 1000000)) + '.txt'
    with open(tmp_file, 'w') as f:
        f.write(tokens_texts_joined)
    if not os.path.exists(tmp_file):
        raise ValueError("Temporary file creation failed.")
    return tmp_file

def find_stable_ts_executable():
    paths = [
        "/usr/local/bin/stable-ts",
        "/root/.local/share/pypoetry/venv/bin/stable-ts",
        "/Library/Frameworks/Python.framework/Versions/3.11/bin/stable-ts",
    ]
    for path in paths:
        if os.path.exists(path):
            return path
    raise ValueError("stable-ts executable not found.")

def run_stable_ts(audio_file, tmp_file, output_file, stable_exec):
    args = [
        stable_exec,
        audio_file,
        "-y",
        "--device", "cpu",
        "--align", tmp_file,
        "--language", "vi",
        "--output_format", "json",
        "--model", "tiny",
        "--output", basename(output_file),
        "--output_dir", dirname(output_file)
    ]
    print(f"Running command: {args}")
    env = prepare_environment()
    process = subprocess.Popen(
        args,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        env=env,
    )
    print("=== Command Output ===")
    for line in process.stderr:
        print(line, end='')
    for line in process.stdout:
        print(line, end='')

    process.stdout.close()
    process.stderr.close()
    process.wait()
    if process.returncode != 0:
        raise ValueError("stable-ts command failed with return code: " + str(process.returncode))

def prepare_environment():
    env = {
        'PATH': "/opt/homebrew/bin:/usr/bin",
    }
    if os.environ.get('VIRTUAL_ENV'):
        ssl_cert_file = os.path.join(os.environ.get('VIRTUAL_ENV'), 'lib/python3.11/site-packages/certifi/cacert.pem')
        env['SSL_CERT_FILE'] = ssl_cert_file
    elif os.environ.get('SSL_CERT_FILE'):
        env['SSL_CERT_FILE'] = os.environ.get('SSL_CERT_FILE')
    return env

def check_output_file(output_file):
    if not os.path.exists(output_file):
        raise ValueError("Alignment failed, output file not found.")

def get_segments_from_segments_file(audio_file, tokens_texts, output_file='output.json'):
    # Step 2: Load the alignment results
    with open(output_file, 'r') as file:
        human_written_segments = json.load(file)
    
    segments = human_written_segments.get('segments', [])
    with open(output_file.replace('.json', '.txt'), 'w') as file:
        file.write("\n\n".join([str(segment['start']) + ' - ' + str(segment['end']) + ': ' + segment['text'] for segment in segments]))
    # Step 3: Find the best match segment for the tokens
    map_segments = [{
        "start": segment['start'],
        "end": segment['end'],
        "text": segment['text'],
        "words": [{
            "word": word['word'],
            "start": word['start'],
            "end": word['end'],
            "probability": word['probability'],
        } for word in segment['words']]
    } for segment in segments]
    matcher = SentenceMatcher(segments, tokens_texts)
    segments_to_add, segments_end, remaining_tokens, matched_sentences = matcher.find_best_segment_match(0.2)
    start = segments_end
    
    # Step 5: If there are no remaining tokens, return the initial matched segments
    if None == start:
        trimmed_audio_file = ''
        if len(remaining_tokens) > 0:
            print("segments_to_add)")
            raise ValueError("remaining_tokens is not empty")

        return trimmed_audio_file, remaining_tokens, start, segments_to_add
    
    # Step 6: Determine starting point for the next segment and process remaining tokens
    # remaining_tokens_joined = "\n\n".join(remaining_tokens)
    matched_sentences_joined = "\n\n".join(matched_sentences)

    # Step 7: Cut the audio file from the best match endpoint and save remaining tokens
    # none_start = cut_audio_file(audio_file, None, start)
    print(f"Cutting audio file from {start} to END")
    trimmed_audio_file = cut_audio_file(audio_file, start, None)
    print(f"Trimmed audio file: {trimmed_audio_file}")

    return trimmed_audio_file, remaining_tokens, start, segments_to_add

def convert_audio_file(audio_file):
    output_file = audio_file.replace('.aac', '.mp3')
    output_file = "/tmp/" + basename(output_file)
    process = subprocess.run([ffmpeg_executable, "-y", "-i", audio_file, "-acodec", "libmp3lame", output_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    process.check_returncode()  # Ensure the subprocess completed successfully
    return output_file

def get_words(words, start):
    return [{
        "word": word['word'],
        "start": round(word['start'] + start, 2),
        "end": round(word['end'] + start, 2),
    } for word in words]

def recursive_get_segments_from_audio_file(audio_file, tokens_texts):
    if audio_file.endswith('.aac'):
        audio_file = convert_audio_file(audio_file)

        return recursive_get_segments_from_audio_file(audio_file, tokens_texts)
    if None == tokens_texts:
        return []
    if len(tokens_texts) == 0:
        return []
    output_file = audio_file.replace('.mp3', '.json')
    trimmed_audio_file, remaining_tokens, start, segments = get_segments_from_audio_file(audio_file, tokens_texts, output_file)
    print(f"Remaining tokens: {len(remaining_tokens)}")

    # Step 8: Recursively process remaining audio and tokens
    remaining_segments = recursive_get_segments_from_audio_file(trimmed_audio_file, remaining_tokens)
    # Step 9: Adjust the start and end times for the remaining segments and combine results
    aligned_segments = [Segment(
        start=round(segment.start + start, 2),
        end=round(segment.end + start, 2),
        words=get_words(segment.words, start),
        text=segment.text,
        segments=segment.segments
    ) for segment in remaining_segments]

    # Assuming corrected_segments is defined or meant to be the initially aligned segments
    return segments + aligned_segments

