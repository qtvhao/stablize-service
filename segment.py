from difflib import SequenceMatcher
from typing import List

DEFAULT_WORD_LIMIT = 12

class Segment:
    def __init__(self, text: str, end: float, start: float, words: List[dict] = [], segments: List[dict] = None):
        if len(segments) == None:
            raise ValueError("Segments cannot be None.")
        self.segments = segments
        segments_txt = " ".join([segment['text'] for segment in segments])
        self.segments_txt_len = len(segments_txt)
        self.text = text
        self.end = end
        self.start = start
        self.words = words
        self.last_15_words = " ".join(segments_txt.split()[-DEFAULT_WORD_LIMIT:])
        self.last_15_words_count = len(self.last_15_words.split())

    def similarity(self, sentences: List[str]) -> float:
        """
        Calculates similarity between the segment and a sentence using SequenceMatcher.
        """
        sentence = " ".join(sentences)
        sentence_word_len = len(sentence)
        the_count_ratio = self.segments_txt_len / sentence_word_len
        if the_count_ratio < 0.9 or the_count_ratio > 1.1:
            return 0
        sentence_last_5_words = " ".join(sentence.split()[(-self.last_15_words_count):])
        ratio = SequenceMatcher(
            None,
            self.last_15_words,
            sentence_last_5_words
        ).ratio()
        
        return ratio
