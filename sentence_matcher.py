from typing import List, Tuple
from segment_validator import SegmentValidator
from segment import Segment

class SentenceMatcher:
    """
    Matches sentences to segments based on highest similarity.
    """
    def __init__(self, segments: List[dict], sentences: List[str]):
        """
        Initializes the SentenceMatcher with processed Segment objects and sentences.

        Parameters:
        - segments: List of dictionaries, each containing 'text' and 'end'.
        - sentences: List of sentences to match.
        """
        self.segments = [Segment(
            segment['text'], 
            segment['end'],
            segment['start'],
            segment.get('words', []),
        ) for segment in segments]
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

    @classmethod
    def split_sentences_by_highest_similarity_to_segments(
        cls, sentences_texts: List[str], corrected_segments: List[dict]
    ) -> Tuple[List[str], List[str]]:
        """
        Class method to process sentence-segment matching from raw input.
        Converts corrected_segments into Segment objects and processes them.
        """
        # Create an instance of SentenceMatcher
        matcher = cls(corrected_segments, sentences_texts)

        # Perform matching
        return matcher.match_sentences()

    def find_best_segment_match(
        self, min_tolerance=0.3
    ) -> Tuple[List[Segment], float, List[str], List[str]]:
        """
        Finds the best match for the given segments and sentences by iteratively adjusting the tolerance.

        Returns:
        - matched_segments: List of matched segments.
        - matched_segment_end: End timestamp of the last matched segment.
        - remaining_sentences: Sentences that were not matched.
        - processed_sentences: Sentences that were matched.
        """
        tolerance = 0.9
        processed_sentences = []
        remaining_sentences = self.sentences[:]

        while tolerance >= min_tolerance:
            # Validate segments within the current tolerance
            processor = SegmentValidator(tolerance)
            valid_segments = processor.get_valid_segments(self.segments)

            processed_sentences, remaining_sentences = self.match_sentences()

            if processed_sentences:
                break

            tolerance *= 0.8  # Reduce tolerance
            tolerance = round(tolerance, 2)  # Avoid floating-point imprecision

            if not valid_segments:
                print("Tolerance is too low")
                break

        highest_ratio = 0
        matched_segments = []
        matched_segment_end = None

        for i, segment in enumerate(valid_segments):
            for sentence in processed_sentences:
                ratio = segment.similarity(sentence)
                if ratio >= highest_ratio and ratio > 0.5:
                    highest_ratio = ratio
                    matched_segments = valid_segments[:i + 1]
                    matched_segment_end = matched_segments[-1].end

        return matched_segments, matched_segment_end, remaining_sentences, processed_sentences
    