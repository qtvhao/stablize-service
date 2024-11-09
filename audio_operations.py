import subprocess
import json
import os
import stable_whisper
# from time import sleep
from alignutils import find_best_segment_match
model = stable_whisper.load_model(name="tiny", in_memory=True)

from random import randint
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
        process = subprocess.run(["ffmpeg", "-y", "-i", audio_file, "-to", seconds_to_ffmpeg_time(end), "-c", "copy", output_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    elif end is None:
        process = subprocess.run(["ffmpeg", "-y", "-i", audio_file, "-ss", seconds_to_ffmpeg_time(start), "-c", "copy", output_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    else:
        process = subprocess.run(["ffmpeg", "-y", "-i", audio_file, "-ss", seconds_to_ffmpeg_time(start), "-to", seconds_to_ffmpeg_time(end), "-c", "copy", output_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    # Print stdout and stderr
    print("=== ffmpeg stdout ===")
    # print(process.stdout)
    print("=== ffmpeg stderr ===")
    # print(process.stderr)

    process.check_returncode()  # Ensure the subprocess completed successfully
    return output_file

def get_segments_from_audio_file(audio_file, tokens_texts, output_file='output.json'):
    # Step 1: Align the tokens with the audio file
    tokens_texts_joined = "\n\n".join(tokens_texts)
    print(f"Aligning {audio_file} with {tokens_texts_joined}")
    # is_pytest = os.environ.get('PYTEST_CURRENT_TEST')
    if True:
        # stable-ts audio.mp3 --align text.txt --language en
        tmp_file = '/tmp/align-input-' + str(randint(0, 1000000)) + '.txt'
        open(tmp_file, 'w').write(tokens_texts_joined)
        # Open the process with Popen
        process = subprocess.Popen([
            "stable-ts", 
            audio_file,
            "-y",
            "--align", tmp_file,
            "--language", "vi",
            "--output_format", "json",
            "--model", "tiny",
            "--output", output_file,
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # Print outputs in real-time
        print("=== Output ===")

        for line in process.stderr:
            print(line, end='')
        for line in process.stdout:
            print(line, end='')  # `end=''` to avoid double newlines

        process.stdout.close()
        process.stderr.close()

        # Wait for the process to complete
        process.wait()

        print("=== Output === ")
        if 1 == process.returncode:
            raise ValueError("Alignment failed")
    else:
        alignment_result = model.align(audio_file, tokens_texts_joined, language="vi")
        alignment_result.save_as_json(output_file)
        
    return get_segments_from_segments_file(audio_file, tokens_texts, output_file)

def get_segments_from_segments_file(audio_file, tokens_texts, output_file='output.json'):
    # Step 2: Load the alignment results
    with open(output_file, 'r') as file:
        human_written_segments = json.load(file)
    
    segments = human_written_segments.get('segments', [])
    with open(output_file.replace('.json', '.txt'), 'w') as file:
        file.write("\n\n".join([str(segment['start']) + ' - ' + str(segment['end']) + ': ' + segment['text'] for segment in segments]))
    # remove output_file
    # os.remove(output_file)

    # Step 3: Find the best match segment for the tokens
    map_segments = [{
        "start": segment['start'],
        "end": segment['end'],
        "text": segment['text'],
        "words": [{
            "probability": word['probability'] * 1e8,
        } for word in segment['words']]
    } for segment in segments]
    segments_to_add, segments_end, remaining_tokens, matched_sentences = find_best_segment_match(map_segments, tokens_texts)
    start = segments_end
    
    # Step 4: Print debug information
    # print(f"Matched sentences: {matched_sentences}")
    # print('===')
    # print(f"Best match segment text: {segments_to_add}")
    # print('===')
    # raise ValueError("Stop")
    # if None == segments_end:
        # raise ValueError("segments_end is None")
    # print(f"Best match segment end: {segments_end}")
    # print(f"Best match: {best_match}")
    # print('===')
    # print(best_match_segment)
    # print(f"Remaining tokens: {remaining_tokens}")

    # Step 5: If there are no remaining tokens, return the initial matched segments
    if None == start:
        trimmed_audio_file = ''
        if len(remaining_tokens) > 0:
            print("segments_to_add)")
            print(map_segments)
            print(tokens_texts)
            raise ValueError("remaining_tokens is not empty")

        return trimmed_audio_file, remaining_tokens, start, segments_to_add
    
    # Step 6: Determine starting point for the next segment and process remaining tokens
    # remaining_tokens_joined = "\n\n".join(remaining_tokens)
    matched_sentences_joined = "\n\n".join(matched_sentences)

    # Step 7: Cut the audio file from the best match endpoint and save remaining tokens
    none_start = cut_audio_file(audio_file, None, start)
    trimmed_audio_file = cut_audio_file(audio_file, start, None)
    with open(f"{trimmed_audio_file}-processed.txt", 'w') as file:
        file.write(matched_sentences_joined)
    # with open(f"{trimmed_audio_file}-remaining.txt", 'w') as file:
        # file.write(remaining_tokens_joined)
        
    return trimmed_audio_file, remaining_tokens, start, segments_to_add

def recursive_get_segments_from_audio_file(audio_file, tokens_texts):
    if None == tokens_texts:
        return []
    if len(tokens_texts) == 0:
        return []
    output_file = audio_file.replace('.mp3', '.json')
    trimmed_audio_file, remaining_tokens, start, segments = get_segments_from_audio_file(audio_file, tokens_texts, output_file)

    # Step 8: Recursively process remaining audio and tokens
    remaining_segments = recursive_get_segments_from_audio_file(trimmed_audio_file, remaining_tokens)
    # Step 9: Adjust the start and end times for the remaining segments and combine results
    aligned_segments = [{
        'start': segment['start'] + start,
        'end': segment['end'] + start,
        'text': segment['text']
    } for segment in remaining_segments]

    # Assuming corrected_segments is defined or meant to be the initially aligned segments
    return segments + aligned_segments

