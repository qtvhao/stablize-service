from sentence_operations import split_sentences_by_highest_similarity_to_segments
from utils import calculate_similarity_ratio

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

def get_valid_segments(segments):
    for i, segment in enumerate(segments):
        if segment['end'] == segment['start']:
            return valid_segments
        else:
        # print(f"Segment {i}: {segment['text']}")
        # words_avg_probability càng lớn, segment càng chính xác
        # tolerance càng lớn, nghĩa là càng chấp nhận được nhiều segment không chính xác
        # tolerance càng nhỏ, nghĩa là khắt khe hơn với các segment không chính xác
            tolerance = 14131791
            words = segment.get('words', [])
            if words:
                words_avg_probability = sum([word['probability'] for word in words]) / len(words)
                segment_text_length = len(segment['text'].strip())
                print(f"Words avg probability: {words_avg_probability} ({segment_text_length})")
                if words_avg_probability <= tolerance and segment_text_length > 2:
                    print(f"Segment {i}: ({segment['text']}) has low probability ({words_avg_probability})")
                    valid_segments = segments[:i]
                    print(f"i: {i}")
                    if 0 == i:
                        continue
                    if valid_segments:
                        last_valid_segment = valid_segments[-1]
                        print(f"Last valid segment: {last_valid_segment['text']}")
                    return valid_segments
            else:
                print(f"Segment {i}: {segment['text']}")
                # raise ValueError("Segment doesn't have words")
            valid_segments = segments[:i]
    # print(f"Valid segments: {valid_segments}")
    return segments

def find_best_segment_match(segments, sentences_texts):
    """
    Tìm segments tối đa, mà segments đó có độ tương đồng cao nhất với sentences_texts.
    """
    segments = get_valid_segments(segments)
    processed_sentences, remaining_sentences = split_sentences_by_highest_similarity_to_segments(sentences_texts, segments)
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
