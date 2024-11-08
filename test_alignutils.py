import pytest
from alignutils import calculate_similarity_ratio, find_best_segment_match
from hypothesis import given, strategies as st

@pytest.mark.parametrize("segment_text, candidate_text, expected_ratio", [
    (
        "This is a test segment with exactly ten words here.", 
        "Completely different text with no matching words. This is a test segment with, exactly  ten  words  here.", 
        0.99
    ),
    ("Short text.", "Short text.", 1.0),
    ("Short text.", "Different text.", 0.61),
    ("", "", 0.0),
    ("", "Non-empty text.", 0.0),
    ("Non-empty text.", "", 0.0)
])
def test_calculate_similarity_ratio(segment_text, candidate_text, expected_ratio):
    ratio = calculate_similarity_ratio(segment_text, candidate_text)
    assert ratio == pytest.approx(expected_ratio, rel=1e-2), f"Expected {expected_ratio}, but got {ratio}"
# 

@pytest.mark.parametrize("segments, sentences_texts, expected_matched_segments, expected_matched_segment_end, expected_remaining_sentences, expected_processed_sentences", [
    (
        [{"text": "This is a test segment.", "start": 5, "end": 10}, {"text": "Another segment here.", "start": 12, "end": 20}],
        ["This is a test segment.", "Completely different sentence."],
        [{"text": "This is a test segment.", "start": 5, "end": 10}],
        10,
        ["Completely different sentence."],
        ["This is a test segment."]
    ),
    (
        [{"text": "Short segment.", "start": 3, "end": 5}, {"text": "Another short segment.", "start": 8, "end": 15}],
        ["Short segment.", "Another short segment."],
        [{"text": "Short segment.", "start": 3, "end": 5}, {"text": "Another short segment.", "start": 8, "end": 15}],
        15, # end of the last matched segment
        [],
        ["Short segment.", "Another short segment."]
    ),
    (
        [{"text": "Short segment.", "start": 3, "end": 6}, {"text": "Another short segment.", "start": 8, "end": 15}],
        ["Short segment.", "Another short segment.", "Third short segment."],
        [{"text": "Short segment.", "start": 3, "end": 6}, {"text": "Another short segment.", "start": 8, "end": 15}],
        15,
        ["Third short segment."], 
        ["Short segment.", "Another short segment."]
    ),
    # (
    #     [{"text": "Segment one.", "start": 3, "end": 5}, {"text": "Segment two.", "start": 8, "end": 10}],
    #     ["No match here.", "Another non-matching sentence."],
    #     [],
    #     None,
    #     ["No match here.", "Another non-matching sentence."],
    #     []
    # ),
    (
        [{'start': 0.88, 'end': 1.4, 'text': ' Ngoài ra,'}, {'start': 1.88, 'end': 5.14, 'text': ' CompTIA còn đóng vai trò xây dựng các chính sách và tiêu chuẩn công nghiệp,'}, {'start': 6.22, 'end': 11.42, 'text': ' đồng thời cung cấp dữ liệu và nghiên cứu để giúp các công ty và tổ chức hiểu rõ xu hướng và yêu cầu công nghệ hiện đại.'}, {'start': 17.26, 'end': 20.16, 'text': '  2.'}, {'start': 29.34, 'end': 29.98, 'text': ' Các chứng chỉ nổi bật của CompTIA'}, {'start': 63.02, 'end': 66.7, 'text': '  CompTIA cung cấp một loạt chứng chỉ chuyên sâu phù hợp cho từng'}, {'start': 67.26, 'end': 70.72, 'text': ' giai đoạn phát triển trong sự nghiệp CNTT,'}, {'start': 70.72, 'end': 70.72, 'text': ' bao gồm từ cơ bản đến nâng cao:'}, {'start': 71.76, 'end': 75.54, 'text': '  CompTIA IT Fundamentals (ITF+): Dành'}, {'start': 76.48, 'end': 78.62, 'text': ' cho người mới bắt đầu,'}, {'start': 78.62, 'end': 79.66, 'text': ' giúp họ hiểu rõ các khái niệm cơ bản về CNTT'}, {'start': 80.54, 'end': 81.1, 'text': ' và'}, {'start': 84.08, 'end': 85.32, 'text': ' chuẩn bị cho các chứng chỉ cao cấp hơn.'}, {'start': 86.1, 'end': 86.78, 'text': '  CompTIA A+:'}, {'start': 87.3, 'end': 89.46, 'text': ' Một chứng chỉ căn bản nhưng quan trọng,'}, {'start': 89.64, 'end': 92.66, 'text': ' tập trung vào các kỹ năng hỗ trợ'}, {'start': 95.92, 'end': 97.4, 'text': ' kỹ thuật, xử lý sự cố,'}, {'start': 97.4, 'end': 97.4, 'text': ' và bảo trì hệ thống máy tính.'}, {'start': 102.48, 'end': 104.5, 'text': '  CompTIA Network'}, {'start': 106.82, 'end': 113.34, 'text': '+: Tập trung vào kiến thức mạng'}, {'start': 128.32, 'end': 131.28, 'text': ' máy tính,'}, {'start': 131.62, 'end': 132.38, 'text': ' hướng dẫn cách thiết lập,'}, {'start': 132.38, 'end': 134.14, 'text': ' quản lý và khắc phục sự cố mạng.'}, {'start': 136.0, 'end': 142.68, 'text': '  CompTIA Security+: Đây'}, {'start': 148.64, 'end': 151.42, 'text': ' là chứng chỉ về an ninh mạng phổ biến,'}, {'start': 151.42, 'end': 151.42, 'text': ' trang bị kiến thức nền tảng về bảo mật mạng,'}, {'start': 151.42, 'end': 151.42, 'text': ' kiểm soát truy cập,'}, {'start': 151.42, 'end': 151.8, 'text': ' và bảo vệ hệ thống khỏi các mối đe dọa bảo mật.'}, {'start': 152.68, 'end': 154.44, 'text': '  CompTIA CySA+ (Cybersecurity Analyst):'}, {'start': 156.2, 'end': 157.82, 'text': ' Chứng chỉ này tập trung vào phân tích an ninh mạng,'}, {'start': 157.82, 'end': 157.82, 'text': ' phát hiện các mối đe dọa và phòng chống tấn công.'}, {'start': 160.74, 'end': 161.52, 'text': '  CompTIA PenTest+:'}, {'start': 163.54, 'end': 169.44, 'text': ' Dành cho những người làm trong lĩnh vực kiểm thử xâm nhập, cung cấp'}, {'start': 170.28, 'end': 171.88, 'text': ' kiến'}, {'start': 172.56, 'end': 175.46, 'text': ' thức về các kỹ thuật tấn công và khai thác điểm yếu hệ thống.'}, {'start': 177.92, 'end': 182.6, 'text': '  CompTIA Advanced Security Practitioner (CASP+): Đây là chứng chỉ cao'}, {'start': 183.24, 'end': 184.22, 'text': ' cấp nhất trong lĩnh vực an ninh mạng của CompTIA,'}, {'start': 185.54, 'end': 185.54, 'text': ' tập trung vào việc thiết kế và triển khai các giải pháp an ninh mạng.'}, {'start': 185.54, 'end': 186.5, 'text': '  3.'}, {'start': 186.5, 'end': 189.9, 'text': ' Ưu điểm khi sở hữu chứng chỉ CompTIA  Được công nhận toàn cầu: Chứng chỉ của CompTIA được công nhận rộng rãi và đánh giá cao bởi các doanh nghiệp và tổ chức trên thế giới.'}, {'start': 190.08, 'end': 193.14, 'text': '  Không lệ thuộc nhà cung cấp (Vendor-neutral): CompTIA tập trung vào các khái niệm và kỹ năng cốt lõi,'}, {'start': 193.14, 'end': 193.76, 'text': ' không phụ thuộc vào bất kỳ công nghệ'}, {'start': 195.1, 'end': 195.1, 'text': ' nghệ hoặc nhà cung cấp cụ thể nào,'}, {'start': 195.1, 'end': 195.1, 'text': ' giúp người học linh hoạt trong nhiều môi trường làm việc khác nhau.'}, {'start': 195.1, 'end': 195.1, 'text': '  Cơ hội nghề nghiệp tốt hơn: Việc sở hữu các chứng chỉ của CompTIA có thể giúp các chuyên gia CNTT tăng cường kỹ năng,'}, {'start': 195.1, 'end': 195.1, 'text': ' nâng cao năng lực và có cơ hội được tuyển dụng hoặc thăng tiến trong ngành CNTT.'}, {'start': 195.1, 'end': 195.1, 'text': '  4.'}, {'start': 195.1, 'end': 195.1, 'text': ' Hình thức thi và đánh giá  Các kỳ thi của CompTIA được tổ chức theo tiêu chuẩn quốc tế,'}, {'start': 195.1, 'end': 195.1, 'text': ' với hình thức câu hỏi đa lựa chọn,'}, {'start': 195.1, 'end': 195.1, 'text': ' bài thực hành mô phỏng (performance-based),'}, {'start': 195.1, 'end': 195.1, 'text': ' và bài kiểm tra kỹ năng thực tế.'}, {'start': 195.1, 'end': 195.1, 'text': ' Thí sinh có thể đăng ký và tham gia thi trực tuyến hoặc tại các trung tâm thi được CompTIA ủy quyền.'}, {'start': 195.1, 'end': 195.1, 'text': '  5.'}, {'start': 195.1, 'end': 195.1, 'text': ' Tầm quan trọng trong ngành CNTT  Với uy tín và chất lượng đào tạo,'}, {'start': 195.1, 'end': 195.1, 'text': ' CompTIA đóng góp rất lớn trong việc chuẩn hóa kiến thức và kỹ năng cho những người làm việc trong ngành CNTT.'}, {'start': 195.1, 'end': 195.1, 'text': ' Các chứng chỉ của CompTIA không chỉ giúp cá nhân phát triển sự nghiệp mà còn hỗ trợ doanh nghiệp trong việc duy trì một lực lượng lao động CNTT chuyên nghiệp và đủ năng lực.'}, {'start': 195.1, 'end': 195.1, 'text': '  Tóm lại,'}, {'start': 195.1, 'end': 195.1, 'text': ' CompTIA là một tổ chức hàng đầu với mục tiêu nâng cao chuẩn mực và chất lượng nguồn nhân lực CNTT toàn cầu.'}, {'start': 195.1, 'end': 195.1, 'text': ' Các chứng chỉ của CompTIA giúp trang bị kiến thức chuyên sâu,'}, {'start': 195.1, 'end': 195.1, 'text': ' kỹ năng thực tiễn,'}, {'start': 195.1, 'end': 195.1, 'text': ' đồng thời mở rộng cơ hội cho người làm việc trong ngành công nghệ.'}],
        ['Ngoài ra, CompTIA còn đóng vai trò xây dựng các chính sách và tiêu chuẩn công nghiệp, đồng thời cung cấp dữ liệu và nghiên cứu để giúp các công ty và tổ chức hiểu rõ xu hướng và yêu cầu công nghệ hiện đại.', '2. Các chứng chỉ nổi bật của CompTIA', 'CompTIA cung cấp một loạt chứng chỉ chuyên sâu phù hợp cho từng giai đoạn phát triển trong sự nghiệp CNTT, bao gồm từ cơ bản đến nâng cao:', 'CompTIA IT Fundamentals (ITF+): Dành cho người mới bắt đầu, giúp họ hiểu rõ các khái niệm cơ bản về CNTT và chuẩn bị cho các chứng chỉ cao cấp hơn.', 'CompTIA A+: Một chứng chỉ căn bản nhưng quan trọng, tập trung vào các kỹ năng hỗ trợ kỹ thuật, xử lý sự cố, và bảo trì hệ thống máy tính.', 'CompTIA Network+: Tập trung vào kiến thức mạng máy tính, hướng dẫn cách thiết lập, quản lý và khắc phục sự cố mạng.', 'CompTIA Security+: Đây là chứng chỉ về an ninh mạng phổ biến, trang bị kiến thức nền tảng về bảo mật mạng, kiểm soát truy cập, và bảo vệ hệ thống khỏi các mối đe dọa bảo mật.', 'CompTIA CySA+ (Cybersecurity Analyst): Chứng chỉ này tập trung vào phân tích an ninh mạng, phát hiện các mối đe dọa và phòng chống tấn công.', 'CompTIA PenTest+: Dành cho những người làm trong lĩnh vực kiểm thử xâm nhập, cung cấp kiến thức về các kỹ thuật tấn công và khai thác điểm yếu hệ thống.', 'CompTIA Advanced Security Practitioner (CASP+): Đây là chứng chỉ cao cấp nhất trong lĩnh vực an ninh mạng của CompTIA, tập trung vào việc thiết kế và triển khai các giải pháp an ninh mạng.', '3. Ưu điểm khi sở hữu chứng chỉ CompTIA', 'Được công nhận toàn cầu: Chứng chỉ của CompTIA được công nhận rộng rãi và đánh giá cao bởi các doanh nghiệp và tổ chức trên thế giới.', 'Không lệ thuộc nhà cung cấp (Vendor-neutral): CompTIA tập trung vào các khái niệm và kỹ năng cốt lõi, không phụ thuộc vào bất kỳ công nghệ hoặc nhà cung cấp cụ thể nào, giúp người học linh hoạt trong nhiều môi trường làm việc khác nhau.', 'Cơ hội nghề nghiệp tốt hơn: Việc sở hữu các chứng chỉ của CompTIA có thể giúp các chuyên gia CNTT tăng cường kỹ năng, nâng cao năng lực và có cơ hội được tuyển dụng hoặc thăng tiến trong ngành CNTT.', '4. Hình thức thi và đánh giá', 'Các kỳ thi của CompTIA được tổ chức theo tiêu chuẩn quốc tế, với hình thức câu hỏi đa lựa chọn, bài thực hành mô phỏng (performance-based), và bài kiểm tra kỹ năng thực tế. Thí sinh có thể đăng ký và tham gia thi trực tuyến hoặc tại các trung tâm thi được CompTIA ủy quyền.', '5. Tầm quan trọng trong ngành CNTT', 'Với uy tín và chất lượng đào tạo, CompTIA đóng góp rất lớn trong việc chuẩn hóa kiến thức và kỹ năng cho những người làm việc trong ngành CNTT. Các chứng chỉ của CompTIA không chỉ giúp cá nhân phát triển sự nghiệp mà còn hỗ trợ doanh nghiệp trong việc duy trì một lực lượng lao động CNTT chuyên nghiệp và đủ năng lực.', 'Tóm lại, CompTIA là một tổ chức hàng đầu với mục tiêu nâng cao chuẩn mực và chất lượng nguồn nhân lực CNTT toàn cầu. Các chứng chỉ của CompTIA giúp trang bị kiến thức chuyên sâu, kỹ năng thực tiễn, đồng thời mở rộng cơ hội cho người làm việc trong ngành công nghệ.'],
        [{'end': 1.4, 'start': 0.88, 'text': ' Ngoài ra,'}, {'end': 5.14, 'start': 1.88, 'text': ' CompTIA còn đóng vai trò xây dựng các chính sách và tiêu chuẩn công nghiệp,'}, {'end': 11.42, 'start': 6.22, 'text': ' đồng thời cung cấp dữ liệu và nghiên cứu để giúp các công ty và tổ chức hiểu rõ xu hướng và yêu cầu công nghệ hiện đại.'}, {'end': 20.16, 'start': 17.26, 'text': '  2.'}, {'end': 29.98, 'start': 29.34, 'text': ' Các chứng chỉ nổi bật của CompTIA'}], # matched segments
        29.98, # end of the last matched segment
        [
            'CompTIA cung cấp một loạt chứng chỉ chuyên sâu phù hợp cho từng giai đoạn '
            'phát triển trong sự nghiệp CNTT, bao gồm từ cơ bản đến nâng cao:',
            'CompTIA IT Fundamentals (ITF+): Dành cho người mới bắt đầu, giúp họ hiểu '
            'rõ các khái niệm cơ bản về CNTT và chuẩn bị cho các chứng chỉ cao cấp '
            'hơn.',
            'CompTIA A+: Một chứng chỉ căn bản nhưng quan trọng, tập trung vào các kỹ '
            'năng hỗ trợ kỹ thuật, xử lý sự cố, và bảo trì hệ thống máy tính.',
            'CompTIA Network+: Tập trung vào kiến thức mạng máy tính, hướng dẫn cách '
            'thiết lập, quản lý và khắc phục sự cố mạng.',
            'CompTIA Security+: Đây là chứng chỉ về an ninh mạng phổ biến, trang bị '
            'kiến thức nền tảng về bảo mật mạng, kiểm soát truy cập, và bảo vệ hệ '
            'thống khỏi các mối đe dọa bảo mật.',
            'CompTIA CySA+ (Cybersecurity Analyst): Chứng chỉ này tập trung vào phân '
            'tích an ninh mạng, phát hiện các mối đe dọa và phòng chống tấn công.',
            'CompTIA PenTest+: Dành cho những người làm trong lĩnh vực kiểm thử xâm '
            'nhập, cung cấp kiến thức về các kỹ thuật tấn công và khai thác điểm yếu '
            'hệ thống.',
            'CompTIA Advanced Security Practitioner (CASP+): Đây là chứng chỉ cao cấp '
            'nhất trong lĩnh vực an ninh mạng của CompTIA, tập trung vào việc thiết kế '
            'và triển khai các giải pháp an ninh mạng.',
            '3. Ưu điểm khi sở hữu chứng chỉ CompTIA',
            'Được công nhận toàn cầu: Chứng chỉ của CompTIA được công nhận rộng rãi và '
            'đánh giá cao bởi các doanh nghiệp và tổ chức trên thế giới.',
            'Không lệ thuộc nhà cung cấp (Vendor-neutral): CompTIA tập trung vào các '
            'khái niệm và kỹ năng cốt lõi, không phụ thuộc vào bất kỳ công nghệ hoặc '
            'nhà cung cấp cụ thể nào, giúp người học linh hoạt trong nhiều môi trường '
            'làm việc khác nhau.',
            'Cơ hội nghề nghiệp tốt hơn: Việc sở hữu các chứng chỉ của CompTIA có thể '
            'giúp các chuyên gia CNTT tăng cường kỹ năng, nâng cao năng lực và có cơ '
            'hội được tuyển dụng hoặc thăng tiến trong ngành CNTT.',
            '4. Hình thức thi và đánh giá',
            'Các kỳ thi của CompTIA được tổ chức theo tiêu chuẩn quốc tế, với hình '
            'thức câu hỏi đa lựa chọn, bài thực hành mô phỏng (performance-based), và '
            'bài kiểm tra kỹ năng thực tế. Thí sinh có thể đăng ký và tham gia thi '
            'trực tuyến hoặc tại các trung tâm thi được CompTIA ủy quyền.',
            '5. Tầm quan trọng trong ngành CNTT',
            'Với uy tín và chất lượng đào tạo, CompTIA đóng góp rất lớn trong việc '
            'chuẩn hóa kiến thức và kỹ năng cho những người làm việc trong ngành CNTT. '
            'Các chứng chỉ của CompTIA không chỉ giúp cá nhân phát triển sự nghiệp mà '
            'còn hỗ trợ doanh nghiệp trong việc duy trì một lực lượng lao động CNTT '
            'chuyên nghiệp và đủ năng lực.',
            'Tóm lại, CompTIA là một tổ chức hàng đầu với mục tiêu nâng cao chuẩn mực '
            'và chất lượng nguồn nhân lực CNTT toàn cầu. Các chứng chỉ của CompTIA '
            'giúp trang bị kiến thức chuyên sâu, kỹ năng thực tiễn, đồng thời mở rộng '
            'cơ hội cho người làm việc trong ngành công nghệ.',
        ],
        [
            'Ngoài ra, CompTIA còn đóng vai trò xây dựng các chính sách và tiêu chuẩn '
            'công nghiệp, đồng thời cung cấp dữ liệu và nghiên cứu để giúp các công ty '
            'và tổ chức hiểu rõ xu hướng và yêu cầu công nghệ hiện đại.',
            '2. Các chứng chỉ nổi bật của CompTIA',
        ] # processed sentences
    ),
    (
        [{'start': 1.08, 'end': 2.22, 'text': ' 4.', 'words': [{'probability': 86600.14718770981}]}, {'start': 2.84, 'end': 7.46, 'text': ' Hình thức thi và đánh giá  Các kỳ thi của CompTIA được tổ chức theo tiêu chuẩn quốc tế,', 'words': [{'probability': 348800.59538409114}, {'probability': 7219455.298036337}, {'probability': 128957.45458081365}, {'probability': 19663.195416796952}, {'probability': 2159349.201247096}, {'probability': 1401757.076382637}, {'probability': 4472601.395315223}, {'probability': 23940942.952564605}, {'probability': 47906.956751830876}, {'probability': 3938092.291355133}, {'probability': 29161268.804455176}, {'probability': 174316.7988024652}, {'probability': 1180068.84586066}, {'probability': 388476.112857461}, {'probability': 21997.270232532173}, {'probability': 2064485.2193072438}, {'probability': 54614471.227978356}, {'probability': 3235547.404619865}, {'probability': 11890069.581568241}]}, {'start': 7.74, 'end': 9.38, 'text': ' với hình thức câu hỏi đa lựa chọn,', 'words': [{'probability': 530137.3545080423}, {'probability': 2560064.2897188663}, {'probability': 81734046.33998871}, {'probability': 45099914.90579069}, {'probability': 3159595.699980855}, {'probability': 1169365.9602315165}, {'probability': 30824757.398416597}, {'probability': 2437759.656459093}]}, {'start': 11.14, 'end': 11.47, 'text': ' bài bài thực hành mô phỏng (performance-based),', 'words': [{'probability': 814557.7739924192}, {'probability': 0.0}, {'probability': 0.0}, {'probability': 0.0}, {'probability': 0.0}, {'probability': 0.0}, {'probability': 0.0}, {'probability': 0.0}]}, {'start': 11.47, 'end': 11.47, 'text': ' và bài kiểm tra kỹ năng thực tế.', 'words': [{'probability': 0.0}, {'probability': 0.0}, {'probability': 0.0}, {'probability': 0.0}, {'probability': 0.0}, {'probability': 0.0}, {'probability': 0.0}, {'probability': 0.0}]}, {'start': 11.47, 'end': 11.47, 'text': ' Thí sinh có thể đăng ký và tham gia thi trực tuyến hoặc tại các trung tâm thi được CompTIA ủy quyền.', 'words': [{'probability': 0.0}, {'probability': 0.0}, {'probability': 0.0}, {'probability': 0.0}, {'probability': 0.0}, {'probability': 0.0}, {'probability': 0.0}, {'probability': 0.0}, {'probability': 0.0}, {'probability': 0.0}, {'probability': 0.0}, {'probability': 0.0}, {'probability': 0.0}, {'probability': 0.0}, {'probability': 0.0}, {'probability': 0.0}, {'probability': 0.0}, {'probability': 0.0}, {'probability': 0.0}, {'probability': 0.0}, {'probability': 0.0}, {'probability': 0.0}]}, {'start': 11.47, 'end': 11.47, 'text': '  5.', 'words': [{'probability': 0.0}]}, {'start': 11.47, 'end': 11.47, 'text': ' Tầm quan trọng trong ngành CNTT  Với uy tín và chất lượng đào tạo,', 'words': [{'probability': 0.0}, {'probability': 0.0}, {'probability': 0.0}, {'probability': 0.0}, {'probability': 0.0}, {'probability': 0.0}, {'probability': 0.0}, {'probability': 0.0}, {'probability': 0.0}, {'probability': 0.0}, {'probability': 0.0}, {'probability': 0.0}, {'probability': 0.0}, {'probability': 0.0}, {'probability': 0.0}]}, {'start': 11.47, 'end': 11.47, 'text': ' CompTIA đóng góp rất lớn trong việc chuẩn hóa kiến thức và kỹ năng cho những người làm việc trong ngành CNTT.', 'words': [{'probability': 0.0}, {'probability': 0.0}, {'probability': 0.0}, {'probability': 0.0}, {'probability': 0.0}, {'probability': 0.0}, {'probability': 0.0}, {'probability': 0.0}, {'probability': 0.0}, {'probability': 0.0}, {'probability': 0.0}, {'probability': 0.0}, {'probability': 0.0}, {'probability': 0.0}, {'probability': 0.0}, {'probability': 0.0}, {'probability': 0.0}, {'probability': 0.0}, {'probability': 0.0}, {'probability': 0.0}, {'probability': 0.0}, {'probability': 0.0}, {'probability': 0.0}]}, {'start': 11.47, 'end': 11.47, 'text': ' Các chứng chỉ của CompTIA không chỉ giúp cá nhân phát triển sự nghiệp mà còn hỗ trợ doanh nghiệp trong việc duy trì một lực lượng lao động CNTT chuyên nghiệp và đủ năng lực.', 'words': [{'probability': 0.0}, {'probability': 0.0}, {'probability': 0.0}, {'probability': 0.0}, {'probability': 0.0}, {'probability': 0.0}, {'probability': 0.0}, {'probability': 0.0}, {'probability': 0.0}, {'probability': 0.0}, {'probability': 0.0}, {'probability': 0.0}, {'probability': 0.0}, {'probability': 0.0}, {'probability': 0.0}, {'probability': 0.0}, {'probability': 0.0}, {'probability': 0.0}, {'probability': 0.0}, {'probability': 0.0}, {'probability': 0.0}, {'probability': 0.0}, {'probability': 0.0}, {'probability': 0.0}, {'probability': 0.0}, {'probability': 0.0}, {'probability': 0.0}, {'probability': 0.0}, {'probability': 0.0}, {'probability': 0.0}, {'probability': 0.0}, {'probability': 0.0}, {'probability': 0.0}, {'probability': 0.0}, {'probability': 0.0}, {'probability': 0.0}, {'probability': 0.0}]}, {'start': 11.47, 'end': 11.47, 'text': '  Tóm lại,', 'words': [{'probability': 0.0}, {'probability': 0.0}, {'probability': 0.0}, {'probability': 0.0}]}, {'start': 11.47, 'end': 11.47, 'text': ' CompTIA là một tổ chức hàng đầu với mục tiêu nâng cao chuẩn mực và chất lượng nguồn nhân lực CNTT toàn cầu.', 'words': [{'probability': 0.0}, {'probability': 0.0}, {'probability': 0.0}, {'probability': 0.0}, {'probability': 0.0}, {'probability': 0.0}, {'probability': 0.0}, {'probability': 0.0}, {'probability': 0.0}, {'probability': 0.0}, {'probability': 0.0}, {'probability': 0.0}, {'probability': 0.0}, {'probability': 0.0}, {'probability': 0.0}, {'probability': 0.0}, {'probability': 0.0}, {'probability': 0.0}, {'probability': 0.0}, {'probability': 0.0}, {'probability': 0.0}, {'probability': 0.0}, {'probability': 0.0}, {'probability': 0.0}]}, {'start': 11.47, 'end': 11.47, 'text': ' Các chứng chỉ của CompTIA giúp trang bị kiến thức chuyên sâu,', 'words': [{'probability': 0.0}, {'probability': 0.0}, {'probability': 0.0}, {'probability': 0.0}, {'probability': 0.0}, {'probability': 0.0}, {'probability': 0.0}, {'probability': 0.0}, {'probability': 0.0}, {'probability': 0.0}, {'probability': 0.0}, {'probability': 0.0}, {'probability': 0.0}]}, {'start': 11.47, 'end': 11.47, 'text': ' kỹ năng thực tiễn,', 'words': [{'probability': 0.0}, {'probability': 0.0}, {'probability': 0.0}, {'probability': 0.0}, {'probability': 0.0}]}, {'start': 11.47, 'end': 11.47, 'text': ' đồng thời mở rộng cơ hội cho người làm việc trong ngành công nghệ.', 'words': [{'probability': 0.0}, {'probability': 0.0}, {'probability': 0.0}, {'probability': 0.0}, {'probability': 0.0}, {'probability': 0.0}, {'probability': 0.0}, {'probability': 0.0}, {'probability': 0.0}, {'probability': 0.0}, {'probability': 0.0}, {'probability': 0.0}, {'probability': 0.0}, {'probability': 0.0}, {'probability': 0.0}]}],
        ['4. Hình thức thi và đánh giá', 'Các kỳ thi của CompTIA được tổ chức theo tiêu chuẩn quốc tế, với hình thức câu hỏi đa lựa chọn, bài thực hành mô phỏng (performance-based), và bài kiểm tra kỹ năng thực tế. Thí sinh có thể đăng ký và tham gia thi trực tuyến hoặc tại các trung tâm thi được CompTIA ủy quyền.', '5. Tầm quan trọng trong ngành CNTT', 'Với uy tín và chất lượng đào tạo, CompTIA đóng góp rất lớn trong việc chuẩn hóa kiến thức và kỹ năng cho những người làm việc trong ngành CNTT. Các chứng chỉ của CompTIA không chỉ giúp cá nhân phát triển sự nghiệp mà còn hỗ trợ doanh nghiệp trong việc duy trì một lực lượng lao động CNTT chuyên nghiệp và đủ năng lực.', 'Tóm lại, CompTIA là một tổ chức hàng đầu với mục tiêu nâng cao chuẩn mực và chất lượng nguồn nhân lực CNTT toàn cầu. Các chứng chỉ của CompTIA giúp trang bị kiến thức chuyên sâu, kỹ năng thực tiễn, đồng thời mở rộng cơ hội cho người làm việc trong ngành công nghệ.'],
        [],
        None,
        [
            '4. Hình thức thi và đánh giá',
            'Các kỳ thi của CompTIA được tổ chức theo tiêu chuẩn quốc tế, với hình '
            'thức câu hỏi đa lựa chọn, bài thực hành mô phỏng (performance-based), và '
            'bài kiểm tra kỹ năng thực tế. Thí sinh có thể đăng ký và tham gia thi '
            'trực tuyến hoặc tại các trung tâm thi được CompTIA ủy quyền.',
            '5. Tầm quan trọng trong ngành CNTT',
            'Với uy tín và chất lượng đào tạo, CompTIA đóng góp rất lớn trong việc '
            'chuẩn hóa kiến thức và kỹ năng cho những người làm việc trong ngành CNTT. '
            'Các chứng chỉ của CompTIA không chỉ giúp cá nhân phát triển sự nghiệp mà '
            'còn hỗ trợ doanh nghiệp trong việc duy trì một lực lượng lao động CNTT '
            'chuyên nghiệp và đủ năng lực.',
            'Tóm lại, CompTIA là một tổ chức hàng đầu với mục tiêu nâng cao chuẩn mực '
            'và chất lượng nguồn nhân lực CNTT toàn cầu. Các chứng chỉ của CompTIA '
            'giúp trang bị kiến thức chuyên sâu, kỹ năng thực tiễn, đồng thời mở rộng '
            'cơ hội cho người làm việc trong ngành công nghệ.',
        ],
        []
    )
])
def test_find_best_segment_match(segments, sentences_texts, expected_matched_segments, expected_matched_segment_end, expected_remaining_sentences, expected_processed_sentences):
    print(f"expected_processed_sentences: {expected_processed_sentences}")
    matched_segments, matched_segment_end, remaining_sentences, processed_sentences = find_best_segment_match(segments, sentences_texts)
    assert matched_segment_end == expected_matched_segment_end, f"Expected {expected_matched_segment_end}, but got {matched_segment_end}"
    assert matched_segments == expected_matched_segments, f"Expected {expected_matched_segments}, but got {matched_segments}"
    assert remaining_sentences == expected_remaining_sentences, f"Expected {expected_remaining_sentences}, but got {remaining_sentences}"
    assert processed_sentences == expected_processed_sentences, f"Expected {expected_processed_sentences}, but got {processed_sentences}"

# 
@given(st.text(), st.text())
def test_calculate_similarity_ratio_2(segment_text, candidate_text):
    ratio = calculate_similarity_ratio(segment_text, candidate_text)
    assert 0.0 <= ratio <= 1.0, "The similarity ratio should be between 0 and 1"

def test_calculate_similarity_ratio_exact_match():
    segment_text = "This is a test segment with exactly ten words here."
    candidate_text = "This is a test segment with exactly ten words here."
    ratio = calculate_similarity_ratio(segment_text, candidate_text)
    assert ratio == 1.0, "The similarity ratio should be 1.0 for exact matches"
