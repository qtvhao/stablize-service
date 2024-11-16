import pytest
from segment_validator import SegmentValidator

@pytest.mark.parametrize(
    "words, expected_avg",
    [
        ([{"probability": 0.8}, {"probability": 0.9}], 0.85),  # Normal case
        ([{"probability": 1.0}, {"probability": 0.5}], 0.75),  # Mixed probabilities
        ([{"probability": 0.0}], 0),                       # Single value
        ([], 0),                                            # Empty list (edge case)
    ],
)
def test_calculate_avg_probability(words, expected_avg):
    processor = SegmentValidator(tolerance=1)
    if not words:
        with pytest.raises(ZeroDivisionError):  # If no words, expect an exception
            processor.calculate_avg_probability(words)
    else:
        assert processor.calculate_avg_probability(words) == expected_avg


@pytest.mark.parametrize(
    "segment, tolerance, expected_result",
    [
        (
            {
                "start": 0, 
                "end": 1, 
                "text": "Hello 0", 
                "words": [
                    {
                        "probability": 0.5
                    }
                ]
            },
            1,
            False
        ), # invalid segment
        ({"start": 0, "end": 1, "text": "5.", "words": [{"probability": 0}]}, 1, True),  # Special case
        ({"start": 0, "end": 1, "text": "Hello 1", "words": [{"probability": 2.0}]}, 1, True),  # Good segment
        ({"start": 0, "end": 0, "text": "Hello 2", "words": [{"probability": 0.5}]}, 1, False),  # Termination segment
        ({"start": 0, "end": 1, "text": "", "words": []}, 1, False),                        # Missing words
    ],
)
def test_process_segment(segment, tolerance, expected_result):
    processor = SegmentValidator(tolerance)
    result = processor.process_segment(segment)
    assert result == expected_result, f"Expected {expected_result}, but got {result}"


@pytest.mark.parametrize(
    "segments, tolerance, expected_valid_segments",
    [
        (
            [
                {"start": 0, "end": 1, "text": "Hello", "words": [{"probability": 0.5}]},
                {"start": 1, "end": 1, "text": "End", "words": [{"probability": 0.4}]},
            ],
            1,
            1,  # Stops at termination
        ),
        (
            [
                {"start": 0, "end": 1, "text": "Hello", "words": [{"probability": 0.5}]},
                {"start": 1, "end": 2, "text": "World", "words": [{"probability": 1.0}]},
            ],
            2,
            2,  # All valid segments
        ),
        (
            [
                {"start": 0, "end": 1, "text": "Hi", "words": [{"probability": 0.5}]},
                {"start": 1, "end": 2, "text": "Hello", "words": [{"probability": 0.5}]},
            ],
            1,
            0,  # First segment invalid
        ),
    ],
)
def test_get_valid_segments(segments, tolerance, expected_valid_segments):
    processor = SegmentValidator(tolerance)
    valid_segments = processor.get_valid_segments(segments)
    assert len(valid_segments) == expected_valid_segments

# Tolerance càng cao thì càng ít segment được chấp nhận, nhưng càng chính xác
# Tolerance càng thấp thì càng nhiều segment được chấp nhận, nhưng càng không chính xác
# probability là accuracy của từng từ trong segment (0 <= probability <= 1)
@pytest.mark.parametrize(
    "segments_test_suite, tolerance, expected_valid_segments, expected_last_segment_text",
    [
        (
            # Invalid segment due to low probability
            ["./tests/synthesize-result-2532432836-segments.json", 0],
            .08,
            21, # number of valid segments
            "CompTIA IT Fundamentals (ITF+):" # Last segment text
        ),
        (
            # Invalid segment due to low probability
            ["./tests/synthesize-result-2532432836-segments.json", 0],
            .1,
            18, # number of valid segments
            "Các chứng chỉ nổi bật của" # Last segment text
        ),
        (
            # Invalid segment due to low probability
            ["./tests/synthesize-result-2532432836-segments.json", 0],
            .3, # Tolerance
            18, # number of valid segments
            " Các chứng chỉ nổi bật của" # Last segment text
        ),
        (
            # Invalid segment due to low probability
            ["./tests/synthesize-result-2532432836-segments.json", 0],
            .5, # Tolerance
            5, # number of valid segments
            " đặc biệt trong các lĩnh vực quản trị hệ thống," # Last segment text
        ),
        (
            ["./tests/synthesize-result-2532432836-segments.json", 0],
            .6,
            0, # number of valid segments
            " Thành lập vào năm 1982, " # Last segment text
        ),
        ####
        (
            # Invalid segment due to low probability
            ["./tests/synthesize-result-2532432836___61_54_end-segments.json", 0],
            .3,
            9, # number of valid segments
            "và bảo trì hệ thống máy tính." # Last segment text
        ),
        (
            # Invalid segment due to low probability. Special case, starts with CompTIA
            ["./tests/synthesize-result-2532432836___61_54___23_5_end-segments.json", 0],
            .4,
            13, # number of valid segments
            "và bảo vệ hệ thống khỏi các mối đe dọa bảo mật." # Last segment text
        ),
        (
            # Invalid segment due to low probability. Special case, starts with CompTIA
            ["./tests/synthesize-result-1456204682-segments.json", 0],
            .4,
            8, # number of valid segments
            "Vân Nam giáp ranh với các quốc gia Đông Nam Á như Việt Nam," # Last segment text
        ),
        (
            ["./tests/2.json", 0],
            .4,
            18, # number of valid segments
            "Các chứng chỉ nổi bật của" # Last segment text
        ),
    ]
)
def test_get_valid_segments(segments_test_suite, tolerance, expected_valid_segments, expected_last_segment_text):
    processor = SegmentValidator(tolerance)
    [segments_json, start] = segments_test_suite
    segments = processor.load_segments(segments_json)
    segments = segments[start:]
    the_first_segment = segments[0]
    print(f"The first segment: {the_first_segment['text']}")
    valid_segments = processor.get_valid_segments(segments)
    valid_segments_count = len(valid_segments)
    assert valid_segments_count == expected_valid_segments, f"Expected {expected_valid_segments} valid segments, but got {valid_segments_count}"
    if valid_segments:
        assert valid_segments[-1]["text"].strip() == expected_last_segment_text.strip(), f"Expected last segment text to be '{expected_last_segment_text}', but got '{valid_segments[-1]['text']}'"