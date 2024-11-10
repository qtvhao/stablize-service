import pytest
import json
from hypothesis import given, strategies as st
from audio_operations import recursive_get_segments_from_audio_file, get_segments_from_segments_file
from utils import calculate_similarity_ratio
import subprocess

@pytest.mark.parametrize("tokens_json, audio_file, output_file, startStampToCompare, cutAudioDuration, segmentsTextToCompare, remainingTokensStartsWith", [
    (
        "tests/tokens.json",
        "tests/synthesize-result-2532432836.mp3",
        "tests/output.json",
        61.54,
        183.48,
        "tổ chức hiểu rõ xu hướng và yêu cầu công nghệ hiện đại.",
        "2. Các chứng chỉ nổi bật của CompTIA"
    ),
    (
        "tests/tokens.json",
        "tests/synthesize-result-2532432836___61_54_end.mp3",
        "tests/synthesize-result-2532432836___61_54_end.mp3.json",
        23.5,
        159.792,
        "và chuẩn bị cho các chứng chỉ cao cấp hơn.",
        "CompTIA A+: Một chứng chỉ căn bản nhưng quan trọng"
    ),
    (
        "tests/tokens.json",
        "tests/synthesize-result-2532432836___61_54___23_5_end.mp3",
        "tests/synthesize-result-2532432836___61_54___23_5_end.mp3.json", 
        57.32,
        102.288,
        "và triển khai các giải pháp an ninh mạng.",
        "3. Ưu điểm khi sở hữu chứng chỉ CompTIA"
    ),
    (
        "tests/tokens.json",
        "tests/synthesize-result-2532432836___61_54___23_5___57_32_end.mp3",
        "tests/synthesize-result-2532432836___61_54___23_5___57_32_end.mp3.json",
        100.98,
        1.128,
        "đồng thời mở rộng cơ hội cho người làm việc trong ngành công nghệ.",
        False
    ),
])
def test_get_segments_from_segments_file(tokens_json, audio_file, output_file, startStampToCompare, cutAudioDuration, segmentsTextToCompare, remainingTokensStartsWith): 
    tokens = json.loads(open(tokens_json).read())
    tokens_texts = [token['text'] for token in tokens]
    trimmed_audio_file, remaining_tokens, start, segments = get_segments_from_segments_file(audio_file, tokens_texts, output_file)
    print(f"Trimmed audio file: {trimmed_audio_file}")
    # 
    segments_joined = " ".join([segment['text'].strip() for segment in segments])
    assert segments_joined.endswith(segmentsTextToCompare), "Segments don't end with {segmentsTextToCompare}"
    # 
    if remainingTokensStartsWith:
        assert remaining_tokens[0].startswith(remainingTokensStartsWith), f"Remaining tokens don't start with {remainingTokensStartsWith}"
    assert startStampToCompare == start, f"Start is not {startStampToCompare}"
    # 
    trimmed_audio_duration = subprocess.check_output(f"ffprobe -i {trimmed_audio_file} -show_entries format=duration -v quiet -of csv=\"p=0\"", shell=True).decode("utf-8")
    print(f"Trimmed audio duration: {trimmed_audio_duration}")
    assert float(trimmed_audio_duration) == cutAudioDuration, f"Trimmed audio duration is not {cutAudioDuration}"

@pytest.mark.parametrize("tokens_json, audio_file", [
    (
        "tests/tokens.json",
        "tests/synthesize-result.aac"
    ),
])
def test_recursive_get_segments_from_audio_file(tokens_json, audio_file):
    tokens = json.loads(open(tokens_json).read())
    tokens_texts = [token['text'] for token in tokens]
    segments = recursive_get_segments_from_audio_file(audio_file, tokens_texts)
    print(segments)
    for segment in segments:
        assert segment['start'] != segment['end'], f"Segment {segment} don't have time"
    tokens_joined = " ".join(tokens_texts)
    segments_joined = " ".join([segment['text'] for segment in segments])
    print(f"Tokens: {tokens_joined}")
    print(f"Segments: {segments_joined}")
    similarity_ratio = calculate_similarity_ratio(tokens_joined, segments_joined)
    print(f"Similarity ratio: {similarity_ratio}")
    assert similarity_ratio >= 0.8, "Similarity ratio is too low"
    for segment in segments:
        assert segment['start'] != segment['end'], f"Segment {segment} don't have time"
        print(f"Segment {segment['start']} - {segment['end']}: {segment['text']}")

