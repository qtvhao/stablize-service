import pytest
from segment_validator import SegmentValidator

@pytest.mark.parametrize(
    "words, expected_avg",
    [
        ([{"probability": 0.8}, {"probability": 0.9}], 1),  # Normal case
        ([{"probability": 1.0}, {"probability": 0.5}], 1),  # Mixed probabilities
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
                "text": "Hello", 
                "words": [
                    {
                        "probability": 0.5
                    }
                ]
            }, 
            1, 
            True
        ),  # Valid segment
        ({"start": 0, "end": 1, "text": "5.", "words": [{"probability": 0.5}]}, 1, False),   # Invalid text length
        ({"start": 0, "end": 1, "text": "Hello", "words": [{"probability": 2.0}]}, 1, False),  # High probability
        ({"start": 0, "end": 0, "text": "Hello", "words": [{"probability": 0.5}]}, 1, False),  # Termination segment
        ({"start": 0, "end": 1, "text": "", "words": []}, 1, False),                        # Missing words
    ],
)
def test_process_segment(segment, tolerance, expected_result):
    processor = SegmentValidator(tolerance)
    result = processor.process_segment(segment)
    assert result == expected_result


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
