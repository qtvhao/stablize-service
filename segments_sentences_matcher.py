from typing import List, Tuple
from segment import Segment

class SegmentsSentencesMatcher:
    def __init__(self, segments: List[Segment], sentences: List[str]):
        self.segments = segments
        self.sentences = sentences
    def match_sentences(self) -> Tuple[List[str], List[str]]:
        """
        Matches sentences with segments based on the highest similarity ratio.
        Returns:
        - processed: List of sentences that matched with a segment.
        - remaining: List of sentences that didn't match any segment.
        """
        processed = []
        remaining = []

        processed_index = self._find_best_match()
        if processed_index is None:
            return [], self.sentences
        print(f"\nProcessed index: {processed_index}")
        processed = self.sentences[:processed_index + 1]
        remaining = self.sentences[processed_index + 1:]

        return processed, remaining

    def _find_best_match(self) -> int:
        """
        Finds the segment with the highest similarity to the given sentence.
        If no match is found, returns None.
        """
        best_ratio = 0
        processed_index = None

        for i, sentence in enumerate(self.sentences):
            for segment in self.segments:
                ratio = segment.similarity(sentence)
                if ratio >= best_ratio and ratio > 0.5:
                    # Update if a better match is found
                    best_ratio = ratio
                    processed_index = i

        return processed_index
