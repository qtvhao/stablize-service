import pytest
from hypothesis import given, strategies as st
from sentence_operations import split_sentences_by_highest_similarity_to_segments

@pytest.mark.parametrize("sentences_texts, corrected_segments, expected_processed, expected_remaining", [
    (
        ["Lorem ipsum dolor sit amet", "consectetur adipiscing elit.", "Nullam nec nulla ac libero."],
        [
            {
                "text": "Lorem ipsum dolor sit amet",
            },
            {
                "text": "consectetur adipiscing elit.",
            },
            {
                "text": "Nullam nec",
            },
        ],
        [
            "Lorem ipsum dolor sit amet",
            "consectetur adipiscing elit.",
        ],
        [
            "Nullam nec nulla ac libero.",
        ]
    ),
    (
        ["The quick brown fox", "jumps over the lazy dog", "and runs away."],
        [
            {
                "text": "The quick brown fox",
            },
            {
                "text": "jumps over the lazy dog",
            },
        ],
        [
            "The quick brown fox",
            "jumps over the lazy dog",
        ],
        [
            "and runs away.",
        ]
    ),
    (
        ["Hello world", "This is a test", "Another sentence"],
        [
            {
                "text": "Hello world",
            },
            {
                "text": "This is a test",
            },
        ],
        [
            "Hello world",
            "This is a test",
        ],
        [
            "Another sentence",
        ]
    ),
    (
        ["One sentence", "Two sentence", "Three sentence"],
        [
            {
                "text": "One sentence",
            },
            {
                "text": "Two sentence",
            },
        ],
        [
            "One sentence",
            "Two sentence",
        ],
        [
            "Three sentence",
        ]
    ),
    # Unhappy cases
    # (
    #     ["Sentence without match"],
    #     [
    #         {
    #             "text": "No match here",
    #         },
    #     ],
    #     [],
    #     [
    #         "Sentence without match",
    #     ]
    # ),
    # (
    #     ["Partial match . sentence . . . . ", "Another one"],
    #     [
    #         {
    #             "text": "Partial 1, 2, 3, 4, 5, 6 match.",
    #         },
    #     ],
    #     [],
    #     [
    #         "Partial match . sentence . . . . ",
    #         "Another one",
    #     ]
    # ),
    # (
    #     ["Completely different sentence"],
    #     [
    #         {
    #             "text": "Totally unrelated segment",
    #         },
    #     ],
    #     [],
    #     [
    #         "Completely different sentence",
    #     ]
    # ),
    # (
    #     [],
    #     [
    #         {
    #             "text": "Segment without sentence",
    #         },
    #     ],
    #     [],
    #     []
    # ),
    # (
    #     ["Sentence without segment"],
    #     [],
    #     [],
    #     [
    #         "Sentence without segment",
    #     ]
    # ),
    (
        ['4. Hình thức thi và đánh giá', 'Các kỳ thi của CompTIA được tổ chức theo tiêu chuẩn quốc tế, với hình thức câu hỏi đa lựa chọn, bài thực hành mô phỏng (performance-based), và bài kiểm tra kỹ năng thực tế. Thí sinh có thể đăng ký và tham gia thi trực tuyến hoặc tại các trung tâm thi được CompTIA ủy quyền.', '5. Tầm quan trọng trong ngành CNTT', 'Với uy tín và chất lượng đào tạo, CompTIA đóng góp rất lớn trong việc chuẩn hóa kiến thức và kỹ năng cho những người làm việc trong ngành CNTT. Các chứng chỉ của CompTIA không chỉ giúp cá nhân phát triển sự nghiệp mà còn hỗ trợ doanh nghiệp trong việc duy trì một lực lượng lao động CNTT chuyên nghiệp và đủ năng lực.', 'Tóm lại, CompTIA là một tổ chức hàng đầu với mục tiêu nâng cao chuẩn mực và chất lượng nguồn nhân lực CNTT toàn cầu. Các chứng chỉ của CompTIA giúp trang bị kiến thức chuyên sâu, kỹ năng thực tiễn, đồng thời mở rộng cơ hội cho người làm việc trong ngành công nghệ.'],
        [{'start': 1.08, 'end': 2.22, 'text': ' 4.', 'words': [{'probability': 86600.14718770981}]}, {'start': 2.84, 'end': 7.46, 'text': ' Hình thức thi và đánh giá  Các kỳ thi của CompTIA được tổ chức theo tiêu chuẩn quốc tế,', 'words': [{'probability': 348800.59538409114}, {'probability': 7219455.298036337}, {'probability': 128957.45458081365}, {'probability': 19663.195416796952}, {'probability': 2159349.201247096}, {'probability': 1401757.076382637}, {'probability': 4472601.395315223}, {'probability': 23940942.952564605}, {'probability': 47906.956751830876}, {'probability': 3938092.291355133}, {'probability': 29161268.804455176}, {'probability': 174316.7988024652}, {'probability': 1180068.84586066}, {'probability': 388476.112857461}, {'probability': 21997.270232532173}, {'probability': 2064485.2193072438}, {'probability': 54614471.227978356}, {'probability': 3235547.404619865}, {'probability': 11890069.581568241}]}, {'start': 7.74, 'end': 9.38, 'text': ' với hình thức câu hỏi đa lựa chọn,', 'words': [{'probability': 530137.3545080423}, {'probability': 2560064.2897188663}, {'probability': 81734046.33998871}, {'probability': 45099914.90579069}, {'probability': 3159595.699980855}, {'probability': 1169365.9602315165}, {'probability': 30824757.398416597}, {'probability': 2437759.656459093}]}],
        [],
        []
    )
])
def test_get_processed_and_remaining_sentences(sentences_texts, corrected_segments, expected_processed, expected_remaining):
    processed, remaining = split_sentences_by_highest_similarity_to_segments(sentences_texts, corrected_segments)
    assert processed == expected_processed
    assert remaining == expected_remaining

# @given(st.lists(st.text()), st.lists(st.text()))
# def test_get_processed_and_remaining_sentences_random(sentences_texts, corrected_segments):
#     processed, remaining = get_processed_and_remaining_sentences(sentences_texts, corrected_segments)
#     assert isinstance(processed, (str, type(None)))
#     assert isinstance(remaining, list)

# @given(st.lists(st.text()), st.lists(st.text()))
# def test_get_processed_and_remaining_sentences_random(sentences_texts, corrected_segments):
#     processed, remaining = get_processed_and_remaining_sentences(sentences_texts, corrected_segments)
#     assert isinstance(processed, (str, type(None)))
#     assert isinstance(remaining, list)