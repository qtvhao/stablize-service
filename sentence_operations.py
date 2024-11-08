from utils import calculate_similarity_ratio

def split_sentences_by_highest_similarity_to_segments(sentences_texts, corrected_segments):
    """
    Tìm sentences_text tối đa, mà sentences_text đó có độ tương đồng cao nhất với corrected_segments.
    
    Ví dụ corrected segments:
    - ["Lorem ipsum dolor sit amet", "consectetur adipiscing elit.", "Nullam nec"]
    
    Ví dụ sentences_texts:
    - ["Lorem ipsum dolor sit amet", "consectetur adipiscing elit.", "Nullam nec nulla ac libero."]
    
    Kết quả trả về:
    - ["Lorem ipsum dolor sit amet", "consectetur adipiscing elit."]
    - ["Nullam nec nulla ac libero."]
    
    Tìm segment có độ tương đồng cao nhất với sentences_text (nhưng không vượt quá sentences_text, bởi vì sentences_text có thể chứa nhiều hơn 1 segment).
    """
    highest_ratio = 0
    similarSegments = []
    processed = []
    remaining = sentences_texts
    # print("+-=")
    # print(sentences_texts)
    # print(corrected_segments)
    # print("=====")
    for i, segment_ in enumerate(corrected_segments):
        segments_to_compare = [segment["text"] for segment in corrected_segments[:i+1]]
        segments_to_compare_joined = " ".join(segments_to_compare)
        for j, sentence_ in enumerate(sentences_texts):
            sentences_to_compare = sentences_texts[:j+1]
            sentences_to_compare_joined = " ".join(sentences_to_compare)
            ratio = calculate_similarity_ratio(segments_to_compare_joined, sentences_to_compare_joined)
            if ratio >= highest_ratio and ratio > 0.5:
                highest_ratio = ratio
                similarSegments = segments_to_compare_joined
                processed = sentences_texts[:j+1]
                remaining = sentences_texts[j+1:]

    if len(processed) == 0:
        print("=.=")
        print(f"Similar segments: {similarSegments}")
        print(f"Processed: {processed}")
        print(f"Remaining: {remaining}")
        raise ValueError("No processed sentences")
    return processed, remaining
