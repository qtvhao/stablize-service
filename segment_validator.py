import json
from segment import Segment
from typing import List
from log import Log

log_file = "/tmp/segment_validator.log"
logger = Log(log_file)

class SegmentValidator:
    def __init__(self, tolerance):
        """
        Initializes the SegmentProcessor with a specified tolerance.

        Parameters:
            tolerance (int): Maximum allowed average probability for a segment to be valid.
        """
        self.tolerance = tolerance

    def get_valid_segments(self, segments: List[Segment]):
        """
        Processes segments and returns a list of valid segments.

        Parameters:
            segments (list): List of dictionaries representing segments.

        Returns:
            list: Valid segments up to the first invalid one.
        """
        valid_segments = []

        for index, segment in enumerate(segments):
            if index == 0:
                continue
            if self.process_segment(segment):
                valid_segments = segments[:index + 1]
            else:
                break  # Stop at the first invalid segment
        log_line = f"Valid segments: {len(valid_segments)}"
        # write to log file
        logger.log(log_line)

        return valid_segments

    def process_segment(self, segment: Segment):
        """
        Validates a segment based on its probability and text length.

        Parameters:
            segment (dict): A dictionary containing segment data.
            index (int): Index of the current segment.

        Returns:
            bool: True if the segment is valid, False otherwise.
        """
        if self._is_termination_segment(segment):
            self._log_segment_status(segment, "Termination segment")
            return False
        words = segment.words

        if not words:
            self._log_segment_status(segment, "Missing 'words'")
            return False

        avg_probability = self.calculate_avg_probability(words)
        text_length = len(segment.text.strip())

        self._log_segment_details(segment, avg_probability)

        if text_length <= 2 and avg_probability == 0:
            self._log_segment_status(segment, "Valid segment. This is a special case")
            return True

        if avg_probability <= self.tolerance: # avg_probability nhỏ hơn ngưỡng tolerance, nghĩa là segment này có khả năng là sai
            self._log_segment_status(segment, f"Invalid segment due to low probability: {avg_probability} <= {self.tolerance}")
            return False
        else:
            self._log_segment_status(segment, "Average probability is within tolerance")
            return True

    @staticmethod
    def calculate_avg_probability(words):
        """
        Calculates the average probability for a list of words.

        Parameters:
            words (list): List of dictionaries with 'probability' keys.

        Returns:
            int: Rounded average probability.
        """
        total_probability = sum(word['probability'] for word in words)
        return round(total_probability * 1e3) / 1e3 / len(words)

    @staticmethod
    def _is_termination_segment(segment: Segment):
        """
        Checks if a segment is a termination segment.

        Parameters:
            segment (Segment): A dictionary representing a segment.

        Returns:
            bool: True if the segment's start equals its end, False otherwise.
        """
        return segment.end == segment.start

    @staticmethod
    def _log_segment_details(segment, avg_probability):
        """
        Logs details about a segment's validation process.

        Parameters:
            index (int): Segment index.
            segment (dict): Segment data.
            avg_probability (int): Average probability of the segment.
        """
        log_line = f"Segment: Avg Probability = {avg_probability}, Text = '{segment.text.strip()}'"
        logger.log(log_line)

    @staticmethod
    def _log_segment_status(segment, status):
        """
        Logs the status of a segment.

        Parameters:
            index (int): Segment index.
            segment (dict): Segment data.
            status (str): Status message.
        """
        log_line = f"Segment: {status}, Text: '{segment.text.strip()}'"
        logger.log(log_line)

    def load_segments(self, segments_json):
        """
        Loads segments from a JSON file.

        Parameters:
            segments_json (str): Path to a JSON file containing segments.

        Returns:
            list: List of dictionaries representing segments.
        """
        with open(segments_json) as file:
            return json.load(file)
