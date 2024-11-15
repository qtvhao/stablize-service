from typing import List, Tuple
from difflib import SequenceMatcher


class Segment:
    """
    Represents a text segment.
    """
    def __init__(self, text: str):
        self.text = text

    def similarity(self, sentence: str) -> float:
        """
        Calculates similarity between the segment and a sentence using SequenceMatcher.
        """
        return SequenceMatcher(None, self.text, sentence).ratio()


class SentenceMatcher:
    """
    Matches sentences to segments based on highest similarity.
    """
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

        for sentence in self.sentences:
            best_match = self._find_best_match(sentence)
            if best_match:  # If a best match is found
                processed.append(sentence)
            else:
                remaining.append(sentence)

        return processed, remaining

    def _find_best_match(self, sentence: str) -> Segment:
        """
        Finds the segment with the highest similarity to the given sentence.
        If no match is found, returns None.
        """
        best_ratio = 0
        best_segment = None

        for segment in self.segments:
            ratio = segment.similarity(sentence)
            print(f"Ratio: {ratio}")
            if ratio > best_ratio and ratio > 0.5:
                # Update if a better match is found
                best_ratio = ratio
                best_segment = segment

        return best_segment

    @classmethod
    def split_sentences_by_highest_similarity_to_segments(
        cls, sentences_texts: List[str], corrected_segments: List[dict]
    ) -> Tuple[List[str], List[str]]:
        """
        Class method to process sentence-segment matching from raw input.
        Converts corrected_segments into Segment objects and processes them.
        """
        # Convert corrected_segments to Segment objects
        segments = [Segment(segment['text']) for segment in corrected_segments]

        # Create an instance of SentenceMatcher
        matcher = cls(segments, sentences_texts)

        # Perform matching
        return matcher.match_sentences()

