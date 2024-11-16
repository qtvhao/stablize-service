import pytest
from sentence_matcher import SentenceMatcher
from segment_validator import SegmentValidator

processor = SegmentValidator(.5)
segments = processor.load_segments("./tests/synthesize-result-2532432836-segments.json")
the_first_segment = segments[0]
print(f"The first segment: {the_first_segment['text']}")
valid_segments = segments
valid_segments = [{
    "text": segment["text"],
    "start": segment["start"],
    "end": segment["end"]
} for segment in valid_segments]
# 
tokens_1 = [
    "CompTIA (Computing Technology Industry Association) là một tổ chức phi lợi nhuận hàng đầu trong lĩnh vực chứng chỉ và tiêu chuẩn công nghệ thông tin (CNTT) trên toàn cầu. Thành lập vào năm 1982, CompTIA chuyên cung cấp các chứng chỉ CNTT nhằm trang bị kiến thức nền tảng và kỹ năng thực tế cho những người làm việc trong ngành công nghệ, đặc biệt trong các lĩnh vực quản trị hệ thống, an ninh mạng, hỗ trợ kỹ thuật, và mạng máy tính.",
    "1. Mục tiêu và vai trò của CompTIA",
    "CompTIA cam kết phát triển và thúc đẩy ngành CNTT thông qua việc cung cấp các chương trình đào tạo và chứng chỉ chất lượng. Các chứng chỉ của CompTIA được thiết kế theo tiêu chuẩn toàn cầu, đảm bảo đáp ứng nhu cầu thực tế của doanh nghiệp và các tổ chức trong việc tuyển dụng nhân sự CNTT có chuyên môn.",
    "Ngoài ra, CompTIA còn đóng vai trò xây dựng các chính sách và tiêu chuẩn công nghiệp, đồng thời cung cấp dữ liệu và nghiên cứu để giúp các công ty và tổ chức hiểu rõ xu hướng và yêu cầu công nghệ hiện đại.",
    "2. Các chứng chỉ nổi bật của CompTIA",
    "CompTIA cung cấp một loạt chứng chỉ chuyên sâu phù hợp cho từng giai đoạn phát triển trong sự nghiệp CNTT, bao gồm từ cơ bản đến nâng cao:",
    "CompTIA IT Fundamentals (ITF+): Dành cho người mới bắt đầu, giúp họ hiểu rõ các khái niệm cơ bản về CNTT và chuẩn bị cho các chứng chỉ cao cấp hơn.",
    "CompTIA A+: Một chứng chỉ căn bản nhưng quan trọng, tập trung vào các kỹ năng hỗ trợ kỹ thuật, xử lý sự cố, và bảo trì hệ thống máy tính.",
    "CompTIA Network+: Tập trung vào kiến thức mạng máy tính, hướng dẫn cách thiết lập, quản lý và khắc phục sự cố mạng.",
    "CompTIA Security+: Đây là chứng chỉ về an ninh mạng phổ biến, trang bị kiến thức nền tảng về bảo mật mạng, kiểm soát truy cập, và bảo vệ hệ thống khỏi các mối đe dọa bảo mật.",
    "CompTIA CySA+ (Cybersecurity Analyst): Chứng chỉ này tập trung vào phân tích an ninh mạng, phát hiện các mối đe dọa và phòng chống tấn công.",
    "CompTIA PenTest+: Dành cho những người làm trong lĩnh vực kiểm thử xâm nhập, cung cấp kiến thức về các kỹ thuật tấn công và khai thác điểm yếu hệ thống.",
    "CompTIA Advanced Security Practitioner (CASP+): Đây là chứng chỉ cao cấp nhất trong lĩnh vực an ninh mạng của CompTIA, tập trung vào việc thiết kế và triển khai các giải pháp an ninh mạng.",
    "3. Ưu điểm khi sở hữu chứng chỉ CompTIA",
    "Được công nhận toàn cầu: Chứng chỉ của CompTIA được công nhận rộng rãi và đánh giá cao bởi các doanh nghiệp và tổ chức trên thế giới.",
    "Không lệ thuộc nhà cung cấp (Vendor-neutral): CompTIA tập trung vào các khái niệm và kỹ năng cốt lõi, không phụ thuộc vào bất kỳ công nghệ hoặc nhà cung cấp cụ thể nào, giúp người học linh hoạt trong nhiều môi trường làm việc khác nhau.",
    "Cơ hội nghề nghiệp tốt hơn: Việc sở hữu các chứng chỉ của CompTIA có thể giúp các chuyên gia CNTT tăng cường kỹ năng, nâng cao năng lực và có cơ hội được tuyển dụng hoặc thăng tiến trong ngành CNTT.",
    "4. Hình thức thi và đánh giá",
    "Các kỳ thi của CompTIA được tổ chức theo tiêu chuẩn quốc tế, với hình thức câu hỏi đa lựa chọn, bài thực hành mô phỏng (performance-based), và bài kiểm tra kỹ năng thực tế. Thí sinh có thể đăng ký và tham gia thi trực tuyến hoặc tại các trung tâm thi được CompTIA ủy quyền.",
    "5. Tầm quan trọng trong ngành CNTT",
    "Với uy tín và chất lượng đào tạo, CompTIA đóng góp rất lớn trong việc chuẩn hóa kiến thức và kỹ năng cho những người làm việc trong ngành CNTT. Các chứng chỉ của CompTIA không chỉ giúp cá nhân phát triển sự nghiệp mà còn hỗ trợ doanh nghiệp trong việc duy trì một lực lượng lao động CNTT chuyên nghiệp và đủ năng lực.",
    "Tóm lại, CompTIA là một tổ chức hàng đầu với mục tiêu nâng cao chuẩn mực và chất lượng nguồn nhân lực CNTT toàn cầu. Các chứng chỉ của CompTIA giúp trang bị kiến thức chuyên sâu, kỹ năng thực tiễn, đồng thời mở rộng cơ hội cho người làm việc trong ngành công nghệ."
]
# 

@pytest.mark.parametrize(
    "corrected_segments, sentences_texts, expected_processed",
    [
        (
            # Trường hợp 1: Câu đầu tiên khớp với đoạn đầu tiên
            [{"text": "Lorem ipsum dolor sit amet", "end": 5, "start": 0}],
            ["Lorem ipsum dolor sit amet _", "Extra sentence here"],
            1 # trả về 1 câu khớp
        ),
        (
            # Trường hợp 2: Không có câu nào khớp
            [{"text": "Non-matching segment", "end": 5, "start": 0}],
            ["Lorem ipsum dolor sit amet", "Extra sentence here"],
            0 # không có câu nào khớp
        ),
        (
            # Trường hợp 3: Nhiều câu khớp với nhiều đoạn
            [
                {"text": "Lorem ipsum dolor sit amet", "end": 5, "start": 0},
                {"text": "consectetur adipiscing elit", "end": 10, "start": 6},
            ],
            ["Lorem ipsum dolor sit amet", "consectetur adipiscing elit", "Extra sentence here"],
            2 # trả về 2 câu khớp
        ),
        (
            # Trường hợp 3: Nhiều câu khớp với nhiều đoạn, vì similiarity > 0.8
            [
                {"text": "Lorem ipsum dolor, sit amet,", "end": 5, "start": 0},
                {"text": "consectetur adipiscing, elit", "end": 10, "start": 6},
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
            [
                {
                    "text": "Lorem ipsum",
                    "start": 0,
                    "end": 5
                }, 
                {
                    "text": "dolor sit amet",
                    "start": 6,
                    "end": 10
                }, {
                    "text": "Extra",
                    "start": 11,
                    "end": 15
                }
            ],
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
                    "end": 5,
                    "start": 0,
                    "text": "Lorem ipsum"
                }
            ],
            ["Lorem ipsum consectetur 2 3 4 5 6", "Another sentence"],
            0 # không có câu nào khớp
        ),
        (
            valid_segments,
            tokens_1,
            22
        ),
        (
            valid_segments[:68],
            tokens_1,
            19
        ),
        (
            valid_segments[:65],
            tokens_1,
            17
        ),
        (
            valid_segments[:58],
            tokens_1,
            16
        ),
        (
            valid_segments[:10],
            tokens_1,
            2
        ),
    ],
)

def test_split_sentences_by_highest_similarity_to_segments(
    corrected_segments, sentences_texts, expected_processed
):
    # Use the class method
    sentence_matcher = SentenceMatcher(corrected_segments, sentences_texts)
    processed, remaining = sentence_matcher.match_sentences(
        sentence_matcher.segments[:len(corrected_segments)]
    )
    print("\n\n")
    print("+")
    print(f"Corrected: {corrected_segments}")
    print("+")
    print(f"Sentences: {sentences_texts}")
    print("=====")
    print(f"Processed: {processed}")
    print(f"Expected: {expected_processed}")
    assert len(processed) == expected_processed

import pytest

@pytest.mark.parametrize("segments, sentences_texts, min_tolerance, expected", [
    # Trường hợp 1: Có một số đoạn khớp với các câu
    (
        [
            {"text": "Đây là câu đầu tiên.", "end": 5, "start": 0, "words": [{"word": "Đây", "probability": 1.0}, {"word": "là", "probability": 1.0}, {"word": "câu", "probability": 1.0}, {"word": "đầu", "probability": 1.0}, {"word": "tiên.", "probability": 1.0}]},
            {"text": "Câu thứ hai có độ dài vừa đủ.", "end": 10, "start": 6, "words": [{"word": "Câu", "probability": 1.0}, {"word": "thứ", "probability": 1.0}, {"word": "hai", "probability": 1.0}, {"word": "có", "probability": 1.0}, {"word": "độ", "probability": 1.0}, {"word": "dài", "probability": 1.0}, {"word": "vừa", "probability": 1.0}, {"word": "đủ.", "probability": 1.0}]},
            {"text": "Câu thứ ba là câu cuối.", "end": 15, "start": 11, "words": [{"word": "Câu", "probability": 1.0}, {"word": "thứ", "probability": 1.0}, {"word": "ba", "probability": 1.0}, {"word": "là", "probability": 1.0}, {"word": "câu", "probability": 1.0}, {"word": "cuối.", "probability": 1.0}]}
        ],
        [
            "Đây là câu đầu tiên.",
            "Câu thứ hai có độ dài vừa đủ.",
            "Câu này không khớp với bất kỳ đoạn nào."
        ],
        0.3,  # Ngưỡng tối thiểu
        {
            "matched_segments": 2,
            "matched_segment_end": 10,
            "remaining_sentences": 1,
            "processed_sentences": 2
        }
    ),
    # Trường hợp 2: Không có câu nào khớp
    # (
    #     [
    #         {"text": "Đây là một đoạn âm thanh khác.", "end": 3, "start": 0, "words": [{"word": "Đây", "probability": 1.0}, {"word": "là", "probability": 1.0}, {"word": "một", "probability": 1.0}, {"word": "đoạn", "probability": 1.0}, {"word": "âm", "probability": 1.0}, {"word": "thanh", "probability": 1.0}, {"word": "khác.", "probability": 1.0}]},
    #         {"text": "Nội dung không khớp.", "end": 6, "start": 4, "words": [{"word": "Nội", "probability": 1.0}, {"word": "dung", "probability": 1.0}, {"word": "không", "probability": 1.0}, {"word": "khớp.", "probability": 1.0}]},
    #     ],
    #     [
    #         "Câu này không khớp với bất kỳ đoạn nào.",
    #         "Một câu khác không khớp."
    #     ],
    #     0.3,
    #     {
    #         "matched_segments": 0,
    #         "matched_segment_end": None,
    #         "remaining_sentences": 2,
    #         "processed_sentences": 0
    #     }
    # ),
    # Trường hợp 3: Tất cả các câu đều khớp
    (
        [
            {"text": "Câu đầu tiên.", "end": 2, "start": 0, "words": [{"word": "Câu", "probability": 1.0}, {"word": "đầu", "probability": 1.0}, {"word": "tiên.", "probability": 1.0}]},
            {"text": "Câu tiếp theo.", "end": 4, "start": 3, "words": [{"word": "Câu", "probability": 1.0}, {"word": "tiếp", "probability": 1.0}, {"word": "theo.", "probability": 1.0}]},
            {"text": "Câu cuối.", "end": 6, "start": 5, "words": [{"word": "Câu", "probability": 1.0}, {"word": "cuối.", "probability": 1.0}]}
        ],
        [
            "Câu đầu tiên.",
            "Câu tiếp theo.",
            "Câu cuối."
        ],
        0.3,
        {
            "matched_segments": 3,
            "matched_segment_end": 6,
            "remaining_sentences": 0,
            "processed_sentences": 3
        }
    ),
    (
        segments,
        tokens_1,
        0.2,
        {
            "matched_segments": 4,
            "matched_segment_end": 20.22,
            "remaining_sentences": 1,
            "processed_sentences": 2
        }
    )
])
def test_find_best_segment_match(segments, sentences_texts, min_tolerance, expected):
    # Create an instance of SentenceMatcher
    matcher = SentenceMatcher(segments, sentences_texts)
    
    # Call the method
    matched_segments, matched_segment_end, remaining_sentences, processed_sentences = matcher.find_best_segment_match(min_tolerance)
    
    # Assertions
    print("\n\nMatched segments count: ", len(matched_segments))
    assert len(matched_segments) == expected["matched_segments"], "Matched segments không khớp với expected output."
    assert matched_segment_end == expected["matched_segment_end"], "Matched segment end does not match the expected output."
    assert len(remaining_sentences) == expected["remaining_sentences"], "Remaining sentences do not match the expected output."
    assert len(processed_sentences) == expected["processed_sentences"], "Processed sentences do not match the expected output."
