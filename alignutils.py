from sentence_operations import split_sentences_by_highest_similarity_to_segments
from segment_validator import SegmentValidator
from utils import calculate_similarity_ratio
from sentence_matcher import SentenceMatcher

def get_segments_by_index(segments, index):
    corrected_segments = segments[:index]
    incorrected_segments = segments[index:]
    corrected_segments_joined = " ".join(corrected_segments)
    incorrected_segments_joined = " ".join(incorrected_segments)
    segments_joined = " ".join(segments)
    # incorrected_start = incorrected_segments[0]['start']
    print("=====================================")
    print(f"Segments: {segments_joined}")
    print("=====================================")
    print(f"Corrected: {corrected_segments_joined}")
    print("=====================================")
    print(f"Incorrected: {incorrected_segments_joined}")
    print("=====================================")
    # print(f"Incorrected Start: {incorrected_start}")
    
    return corrected_segments, incorrected_segments

def get_valid_segments(segments, tolerance=.2):
    processor = SegmentValidator(tolerance)
    valid_segments = processor.get_valid_segments(segments)
    
    return valid_segments

def find_best_segment_match(segments, sentences_texts, min_tolerance=0.3):
    """
    Tìm segments tối đa, mà segments đó có độ tương đồng cao nhất với sentences_texts.
    """
    tolerance = .9
    while True:
        segments = get_valid_segments(segments, tolerance)
        processed_sentences, remaining_sentences = SentenceMatcher.split_sentences_by_highest_similarity_to_segments(
            sentences_texts, segments
        )
        if len(processed_sentences) > 0:
            print(f"Processed: {processed_sentences}")
            break
        tolerance *= 0.8
        tolerance = round(tolerance, 2)
        if tolerance < min_tolerance:
            print("Tolerance is too low")
            break

    # processed_sentences, remaining_sentences = split_sentences_by_highest_similarity_to_segments(sentences_texts, segments)
    highest_ratio = 0
    matched_segments = []
    matched_segment_end = None
    for i, segment in enumerate(segments):
        for sentence in processed_sentences:
            ratio = calculate_similarity_ratio(segment['text'], sentence)
            if ratio >= highest_ratio and ratio > 0.5:
                print(f"Ratio: {ratio}")
                highest_ratio = ratio
                matched_segments = segments[:i+1]
                matched_segment_end = matched_segments[-1]['end']
    print("-")
    # if None == matched_segment_end and len(processed_sentences) == 0:
    #     print("=.=")
    #     print(processed_sentences)
    #     print(remaining_sentences)
    #     raise ValueError("matched_segment_end is None")

    return matched_segments, matched_segment_end, remaining_sentences, processed_sentences
