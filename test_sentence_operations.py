import pytest
from sentence_matcher import SentenceMatcher
from sentence_operations import split_sentences_by_highest_similarity_to_segments

@pytest.mark.parametrize(
    "corrected_segments, sentences_texts, expected_processed",
    [
        (
            # Trường hợp 1: Câu đầu tiên khớp với đoạn đầu tiên
            [{"text": "Lorem ipsum dolor sit amet"}],
            ["Lorem ipsum dolor sit amet _", "Extra sentence here"],
            1 # trả về 1 câu khớp
        ),
        (
            # Trường hợp 2: Không có câu nào khớp
            [{"text": "Non-matching segment"}],
            ["Lorem ipsum dolor sit amet", "Extra sentence here"],
            0 # không có câu nào khớp
        ),
        (
            # Trường hợp 3: Nhiều câu khớp với nhiều đoạn
            [
                {"text": "Lorem ipsum dolor sit amet"},
                {"text": "consectetur adipiscing elit"},
            ],
            ["Lorem ipsum dolor sit amet", "consectetur adipiscing elit", "Extra sentence here"],
            2 # trả về 2 câu khớp
        ),
        (
            # Trường hợp 3: Nhiều câu khớp với nhiều đoạn, vì similiarity > 0.8
            [
                {"text": "Lorem ipsum dolor, sit amet,"},
                {"text": "consectetur adipiscing, elit"},
            ],
            ["Lorem ipsum, dolor sit amet.", " Consectetur, adipiscing elit", "Extra sentence here"],
            2 # trả về 2 câu khớp
        ),
        (
            # Trường hợp 4: Một phần của câu khớp
            # 3.	Kết quả mong đợi:
            # •	Câu đầu tiên "Lorem ipsum dolor sit amet" khớp với đoạn hợp nhất "Lorem ipsum" + " dolor sit amet".
            # •	Câu còn lại "Extra sentence here" không khớp đầy đủ vì chứa từ "sentence", không có trong các đoạn.
            # 4.	Xử lý:
            # •	Các đoạn hợp nhất thành một câu khớp ("Lorem ipsum dolor sit amet").
            # •	Câu còn lại không khớp ("Extra sentence here") được trả về trong phần còn lại (remaining).
            [{"text": "Lorem ipsum"}, {"text": "dolor sit amet"}, {"text": "Extra"}],
            ["Lorem ipsum dolor sit amet", "Extra sentence here"],
            1 # trả về 1 câu khớp
        ),
        (
            # Trường hợp 6: Khớp một phần nhưng không đầy đủ
            # Trong trường hợp này, đoạn "Lorem ipsum" chỉ khớp một phần với câu "Lorem ipsum consectetur".
            # Kết quả mong đợi:
            # • Không có đoạn nào được chọn, vì không có khớp đầy đủ.
            # • Tất cả các câu được trả về trong phần còn lại (remaining).
            [
                {
                    "text": "Lorem ipsum"
                }
            ],
            ["Lorem ipsum consectetur 2 3 4 5 6", "Another sentence"],
            0 # không có câu nào khớp
        ),
    ],
)

def test_split_sentences_by_highest_similarity_to_segments(
    corrected_segments, sentences_texts, expected_processed
):
    # Use the class method
    processed, remaining = SentenceMatcher.split_sentences_by_highest_similarity_to_segments(
        sentences_texts, corrected_segments
    )
    print(f"Processed: {processed}")
    print(f"Expected: {expected_processed}")
    assert len(processed) == expected_processed
