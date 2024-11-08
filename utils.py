from difflib import SequenceMatcher
def ends_with(text, char):
    """
    Checks if the text ends with a character.
    
    Args:
        text (str): The text to check.
        char (str): The character to check.
        
    Returns:
        bool: True if text ends with char, False otherwise.
    """
    return text.endswith(char)

def calculate_similarity_ratio(segment_text, candidate_text):
    """
    Calculate the similarity ratio between the last 10 words of two strings.
    
    Args:
        segment_text (str): The text from corrected segments.
        candidate_text (str): The text from tokens.
        
    Returns:
        float: The similarity ratio between the last 10 words of the two strings.
    """
    if not segment_text or not candidate_text:
        return 0.0
    segment_words = segment_text.split()
    candidate_words = candidate_text.split()
    # 
    words_to_compare = min(10, len(segment_words), len(candidate_words))
    # 
    segment_words = segment_words[-words_to_compare:]
    candidate_words = candidate_words[-words_to_compare:]
    # 
    segment_last_10 = ' '.join(segment_words)
    candidate_last_10 = ' '.join(candidate_words)
    # print(f"Segment last 10: {segment_last_10}")
    # print(f"Candidate last 10: {candidate_last_10}")
    return SequenceMatcher(None, segment_last_10, candidate_last_10).ratio()
