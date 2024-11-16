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
        "và nghiên cứu để giúp các công ty và tổ chức hiểu rõ xu hướng và yêu cầu công nghệ hiện đại.",
        "2. Các chứng chỉ nổi bật của CompTIA"
    ),
    (
        "tests/tokens.json",
        "tests/synthesize-result-2532432836___61_54_end.mp3",
        "tests/synthesize-result-2532432836___61_54_end.mp3.json",
        30.38,
        152.928,
        "Một chứng chỉ căn bản nhưng quan trọng, tập trung vào các kỹ năng hỗ trợ kỹ thuật, xử lý sự cố,",
        "1. Mục tiêu và vai trò của CompTIA"
    ),
    # (
    #     "tests/tokens.json",
    #     "tests/synthesize-result-2532432836___61_54___23_5_end.mp3",
    #     "tests/synthesize-result-2532432836___61_54___23_5_end.mp3.json", 
    #     105.6,
    #     54.0,
    #     "được công nhận rộng rãi và đánh giá cao bởi các doanh nghiệp và tổ chức trên thế giới.",
    #     "4. Hình thức thi và đánh giá"
    # ),
    # (
    #     "tests/tokens.json",
    #     "tests/synthesize-result-2532432836___61_54___23_5___57_32_end.mp3",
    #     "tests/synthesize-result-2532432836___61_54___23_5___57_32_end.mp3.json",
    #     100.98,
    #     1.128,
    #     "đồng thời mở rộng cơ hội cho người làm việc trong ngành công nghệ.",
    #     False
    # ),
])
def test_get_segments_from_segments_file(tokens_json, audio_file, output_file, startStampToCompare, cutAudioDuration, segmentsTextToCompare, remainingTokensStartsWith): 
    tokens_texts = json.loads(open(tokens_json).read())
    trimmed_audio_file, remaining_tokens, start, segments = get_segments_from_segments_file(audio_file, tokens_texts, output_file)
    print(f"Trimmed audio file: {trimmed_audio_file}")
    # 
    segments_joined = " ".join([segment.text.strip() for segment in segments])
    print(f"Expect segments to end with: {segmentsTextToCompare}")
    assert segments_joined.endswith(segmentsTextToCompare), "Segments don't end with {segmentsTextToCompare}"
    # 
    if remainingTokensStartsWith:
        assert remaining_tokens[0].startswith(remainingTokensStartsWith), f"Remaining tokens don't start with {remainingTokensStartsWith}"
    assert startStampToCompare == start, f"Start is not {startStampToCompare}"
    # 
    trimmed_audio_duration = subprocess.check_output(f"ffprobe -i {trimmed_audio_file} -show_entries format=duration -v quiet -of csv=\"p=0\"", shell=True).decode("utf-8")
    print(f"Trimmed audio duration: {trimmed_audio_duration}")
    trimmed_audio_duration = trimmed_audio_duration.strip()
    assert float(trimmed_audio_duration) == cutAudioDuration, f"Trimmed audio duration is not {cutAudioDuration}"

@pytest.mark.parametrize("tokens_json, audio_file", [
    (
        "tests/tokens-2.json",
        "tests/synthesize-result-1456204682.aac"
    ),
    (
        "tests/tokens.json",
        "tests/synthesize-result.aac"
    ),
])
def test_recursive_get_segments_from_audio_file(tokens_json, audio_file):
    tokens_texts = json.loads(open(tokens_json).read())
    segments = recursive_get_segments_from_audio_file(audio_file, tokens_texts)
    print(segments)
    for segment in segments:
        assert segment.start != segment.end, f"Segment {segment} don't have time"
    tokens_joined = " ".join(tokens_texts)
    segments_joined = " ".join([segment.text for segment in segments])
    print(f"Tokens: {tokens_joined}")
    print(f"Segments: {segments_joined}")
    similarity_ratio = calculate_similarity_ratio(tokens_joined, segments_joined)
    print(f"Similarity ratio: {similarity_ratio}")
    assert similarity_ratio >= 0.8, "Similarity ratio is too low"
    for segment in segments:
        assert segment.start != segment.end, f"Segment {segment} don't have time"
        print(f"Segment {segment.start} - {segment.end}: {segment.text}")

