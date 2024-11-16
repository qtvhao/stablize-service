from difflib import SequenceMatcher
from typing import List

DEFAULT_WORD_LIMIT = 15

class Segment:
    def __init__(self, text: str, end: float, start: float, words: List[dict] = []):
        self.text = text
        self.end = end
        self.start = start
        self.words = words
        self.last_15_words = " ".join(text.split()[-DEFAULT_WORD_LIMIT:])
        self.last_15_words_count = len(self.last_15_words.split())

    def similarity(self, sentence: str) -> float:
        """
        Calculates similarity between the segment and a sentence using SequenceMatcher.
        """
        sentence_last_5_words = " ".join(sentence.split()[(-self.last_15_words_count):])
        return SequenceMatcher(
            None,
            self.last_15_words,
            sentence_last_5_words
        ).ratio()
