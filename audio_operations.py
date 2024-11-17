import subprocess
import json
import os
from sentence_matcher import SentenceMatcher
from segment import Segment
from os.path import basename, dirname
# import stable_whisper
# from time import sleep
from alignutils import find_best_segment_match
from log import Log
# model = stable_whisper.load_model(name="tiny", in_memory=True)

from random import randint

logger = Log("/tmp/audio_operations.log")
ffmpeg_executable = "/usr/bin/ffmpeg"
if not os.path.exists(ffmpeg_executable):
    ffmpeg_executable = "ffmpeg"
    # raise ValueError("ffmpeg not found")

def seconds_to_ffmpeg_time(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    sec = seconds % 60
    return f"{hours:02}:{minutes:02}:{sec:06.3f}"

def build_ffmpeg_command(audio_file, start=None, end=None, output_file=None):
    """
    Constructs an FFmpeg command to cut an audio file.
    :param audio_file: Path to the input audio file.
    :param start: Start time in seconds (float or int), or None to start from the beginning.
    :param end: End time in seconds (float or int), or None to end at the file's duration.
    :param output_file: Path for the output file. If None, generate a default name.
    :return: List of FFmpeg command arguments.
    """
    # Prepare output file name if not provided
    start_str = str(start).replace('.', '_') if start is not None else 'start'
    end_str = str(end).replace('.', '_') if end is not None else 'end'
    if output_file is None:
        output_file = audio_file.replace('.mp3', f'___{start_str}_{end_str}.mp3')

    # Construct the FFmpeg arguments
    if start is None:
        args = [ffmpeg_executable, "-y", "-i", audio_file, "-to", seconds_to_ffmpeg_time(end), "-c", "copy", output_file]
    elif end is None:
        args = [ffmpeg_executable, "-y", "-i", audio_file, "-ss", seconds_to_ffmpeg_time(start), "-c", "copy", output_file]
    else:
        args = [ffmpeg_executable, "-y", "-i", audio_file, "-ss", seconds_to_ffmpeg_time(start), "-to", seconds_to_ffmpeg_time(end), "-c", "copy", output_file]

    return args, output_file


def cut_audio_file(audio_file, start=None, end=None):
    """
    Cuts an audio file using FFmpeg.
    :param audio_file: Path to the input audio file.
    :param start: Start time in seconds (float or int), or None to start from the beginning.
    :param end: End time in seconds (float or int), or None to end at the file's duration.
    :return: Path to the output audio file.
    """
    # Build the FFmpeg command
    args, output_file = build_ffmpeg_command(audio_file, start=start, end=end)

    command = ' '.join(args) + ' 2>&1 | tee -a /tmp/ffmpeg.log'
    logger.log(f"Running command: {command}")

    try:
        # Run the ffmpeg command and capture output
        result = subprocess.run(command, shell=True, text=True, capture_output=True)
        returncode = result.returncode
        stdout = result.stdout
        stderr = result.stderr
        # Print stdout and stderr for debugging
        logger.log("=== ffmpeg return code ===")
        logger.log(returncode)
        logger.log("=== ffmpeg stdout ===")
        logger.log(stdout)
        logger.log("=== ffmpeg stderr ===")
        logger.log(stderr)
        logger.log("=== End of ffmpeg output ===")

    except subprocess.CalledProcessError as e:
        # Handle ffmpeg errors
        logger.log("Error during ffmpeg execution:")
        logger.log(f"Return code: {e.returncode}")
        logger.log(f"Output: {e.output}")
        logger.log(f"Error output: {e.stderr}")
        raise ValueError(f"ffmpeg command failed with return code: {e.returncode}")

    except Exception as e:
        # Handle unexpected errors
        logger.log(f"Unexpected error: {e}")
        raise

    logger.log(f"Cut audio file from {start} to {end} successfully. Output: {output_file}")
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
    logger.log(f"Running command: {args}")
    env = prepare_environment()
    process = subprocess.Popen(
        args,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        env=env,
    )
    logger.log("=== Command Output ===")
    for line in process.stderr:
        logger.log(line)
    for line in process.stdout:
        logger.log(line)

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
    logger.log(f"Remaining tokens 1: {len(remaining_tokens)}")
    start = segments_end
    
    # Step 5: If there are no remaining tokens, return the initial matched segments
    if None == start:
        trimmed_audio_file = ''
        if len(remaining_tokens) > 0:
            logger.log("segments_to_add)")
            raise ValueError("remaining_tokens is not empty")

        return trimmed_audio_file, remaining_tokens, start, segments_to_add
    
    # Step 6: Determine starting point for the next segment and process remaining tokens
    remaining_tokens_joined = "\n\n".join(remaining_tokens)
    logger.log(f"Remaining tokens 2: {remaining_tokens_joined}")
    # matched_sentences_joined = "\n\n".join(matched_sentences)

    # Step 7: Cut the audio file from the best match endpoint and save remaining tokens
    # none_start = cut_audio_file(audio_file, None, start)
    logger.log(f"Cutting audio file from {start} to END")
    if len(remaining_tokens) > 0:
        trimmed_audio_file = cut_audio_file(audio_file, start, None)
    else:
        trimmed_audio_file = None
    logger.log(f"Trimmed audio file: {trimmed_audio_file}")

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
    logger.log(f"Remaining tokens 3: {len(remaining_tokens)}")

    # Step 8: Recursively process remaining audio and tokens
    if len(remaining_tokens) == 0:
        remaining_segments = []
    else:    
        remaining_segments = recursive_get_segments_from_audio_file(trimmed_audio_file, remaining_tokens)
    # Step 9: Adjust the start and end times for the remaining segments and combine results
    logger.log(f"Remaining segments: {len(remaining_segments)}")
    aligned_segments = [Segment(
        start=round(segment.start + start, 2),
        end=round(segment.end + start, 2),
        words=get_words(segment.words, start),
        text=segment.text,
        segments=segment.segments
    ) for segment in remaining_segments]

    # Assuming corrected_segments is defined or meant to be the initially aligned segments
    return segments + aligned_segments

