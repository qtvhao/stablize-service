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
        self_text_last_5_words = " ".join(self.text.split()[-15:])
        words_count = len(self_text_last_5_words.split())
        sentence_last_5_words = " ".join(sentence.split()[(words_count * -1):])
        return SequenceMatcher(
            None,
            self_text_last_5_words,
            sentence_last_5_words
        ).ratio()


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

        processed_index = self._find_best_match()
        if processed_index is None:
            return [], self.sentences
        processed = self.sentences[:processed_index+1]
        remaining = self.sentences[processed_index:]
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

