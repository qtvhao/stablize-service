def get_remaining_tokens(all_tokens, match_index, segment_length):
    """
    Get the remaining tokens after the matched segment in list format.
    
    Args:
        all_tokens (list of str): Flattened list of tokens from tokens_texts.
        match_index (int): The starting index of the matched tokens.
        segment_length (int): The length of the matched segment.
        
    Returns:
        list of str: The remaining tokens after the matched segment.
    """
    return all_tokens[match_index + segment_length:]