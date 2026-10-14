# Mô tả đề tài + Mục lục + Brief Chương 1–4 (bản gọn gửi GVHD, 07/10/2026)

## MỤC LỤC

```
TÓM TẮT — TỪ KHÓA

PHẦN 1: GIỚI THIỆU
  1.1  Bối cảnh nghiên cứu
  1.2  Vấn đề nghiên cứu
  1.3  Mục tiêu, câu hỏi và giả thuyết nghiên cứu
  1.4  Đối tượng và phạm vi nghiên cứu
  1.5  Đóng góp của khóa luận
  1.6  Cấu trúc khóa luận

PHẦN 2: TỔNG QUAN NGHIÊN CỨU
  2.1  Giải trình chênh lệch ngân sách trong FP&A
  2.2  Mô hình ngôn ngữ lớn, RAG và bài toán viết có căn cứ
  2.3  Niềm tin và kiểm soát đối với hệ thống tự động
  2.4  Khoảng trống nghiên cứu

PHẦN 3: PHƯƠNG PHÁP NGHIÊN CỨU
  3.1  Dữ liệu
       3.1.1  Khảo sát giải trình thực tế tại doanh nghiệp (17 bản, đã ẩn danh)
       3.1.2  Xây dựng bộ dữ liệu mô phỏng có đáp án (12 loại tình huống chênh lệch)
       3.1.3  Thống kê mô tả bộ dữ liệu
  3.2  Mô hình và kiến trúc
       3.2.1  Bài toán: đầu vào, đầu ra và yêu cầu kiểm chứng
       3.2.2  Khối tính toán chênh lệch (variance engine)
       3.2.3  Khối truy xuất bằng chứng (retrieval)
       3.2.4  Khối sinh giải trình theo khuôn, kèm trích dẫn
       3.2.5  Khối kiểm chứng và cơ chế từ chối
  3.3  Cơ chế đánh giá
       3.3.1  Năm thước đo và nguồn gốc của từng thước đo
       3.3.2  Quy trình chấm khách quan (đáp án chốt trước, chấm mù,
              đối chiếu máy chấm với người chấm)
  3.4  Thiết lập thực nghiệm
       3.4.1  Ba cấu hình so sánh trên cùng một mô hình ngôn ngữ
       3.4.2  Tham số chạy và hiện thực hóa hệ thống (web)

PHẦN 4: KẾT QUẢ NGHIÊN CỨU
  4.1  Kết quả chính
       4.1.1  So sánh ba cấu hình trên năm thước đo
       4.1.2  Minh họa một tình huống hoàn chỉnh: từ số liệu đến giải trình
  4.2  Kiểm định tính vững
       4.2.1  Kết quả theo từng loại tình huống
       4.2.2  Các tình huống làm khó: không có tài liệu liên quan,
              tài liệu gây nhiễu, lỗi gieo cố ý
       4.2.3  Độ tin cậy của máy chấm so với người chấm
  4.3  Thảo luận
       4.3.1  Đối chiếu ba giả thuyết nghiên cứu
       4.3.2  So sánh với nghiên cứu trước và hạn chế

PHẦN 5: KẾT LUẬN
  5.1  Kết luận
  5.2  Đóng góp và khuyến nghị
  5.3  Hạn chế và hướng phát triển

TÀI LIỆU THAM KHẢO
PHỤ LỤC
```

## TÓM TẮT (ABSTRACT)

Hàng tháng, bộ phận FP&A của doanh nghiệp phải giải trình chênh lệch giữa kết quả thực tế và ngân sách. AI tạo sinh giúp soạn phần này nhanh, nhưng người dùng tài chính không kiểm tra được con số và nhận định trong đó lấy từ đâu; sai sót vì vậy khó bị phát hiện trước khi đi vào báo cáo quản trị.

Khóa luận đề xuất một hệ thống sinh giải trình có thể kiểm tra được: chương trình thông thường tính toàn bộ số liệu; mô hình ngôn ngữ lớn chỉ viết văn theo khuôn của doanh nghiệp và phải kèm trích dẫn tới tài liệu bằng chứng; một lớp kiểm tra tự động đối chiếu lại từng con số, từng trích dẫn, và từ chối nêu nguyên nhân khi không đủ bằng chứng. Hệ thống được đánh giá trên bộ dữ liệu mô phỏng có đáp án sẵn, so sánh với hai cách dùng AI phổ biến bằng năm thước đo kế thừa từ các nghiên cứu NLP trước. ⟦Kết quả chính — điền sau khi chạy thực nghiệm.⟧

**Từ khóa:** giải trình chênh lệch ngân sách; mô hình ngôn ngữ lớn; truy xuất tăng cường (RAG); khả năng kiểm chứng; FP&A.

## MÔ TẢ ĐỀ TÀI

**Tên (đề xuất):** Xây dựng hệ thống sinh giải trình chênh lệch ngân sách có thể kiểm chứng bằng mô hình ngôn ngữ lớn và truy xuất tăng cường (RAG): nghiên cứu tình huống tại doanh nghiệp bất động sản khu công nghiệp.
*(EN: Developing a Verifiable Budget Variance Commentary System Using Large Language Models and Retrieval-Augmented Generation: A Case Study at an Industrial Real Estate Company.)*
*(Phương án thay thế nếu GVHD muốn theo khuôn chủ đề của Viện: "Ứng dụng mô hình ngôn ngữ lớn và truy xuất tăng cường (RAG) xây dựng hệ thống giải trình chênh lệch ngân sách có thể kiểm chứng: case study tại doanh nghiệp bất động sản khu công nghiệp.")*

**Tóm tắt:** AI đã được dùng để soạn giải trình chênh lệch ngân sách rất nhanh, nhưng với người làm tài chính, kết quả là một "hộp đen" — không kiểm tra được số lấy từ đâu, nhận định dựa trên căn cứ nào. Khóa luận xây dựng hệ thống trong đó: code thường tính số, AI chỉ viết văn theo khuôn kèm trích dẫn, máy tự soát lại từng số và từng trích dẫn, thiếu bằng chứng thì từ chối. Hệ thống được so với hai cách dùng AI phổ biến trên bộ dữ liệu mô phỏng có đáp án, chấm bằng các thước đo chuẩn của nghiên cứu NLP.

## BRIEF 4 CHƯƠNG

**Chương 1 — Giới thiệu** *(đã có bản thảo)*
Ngành BĐS KCN tăng trưởng, AI vào bộ phận tài chính (Gartner: 37%→59%); tại doanh nghiệp quan sát, AI soạn giải trình chỉ ~1 giờ. Vấn đề không phải tốc độ mà là không kiểm chứng được → rủi ro duyệt mà không kiểm tra, đứt dấu vết kiểm toán. Nêu 3 câu hỏi nghiên cứu, 3 giả thuyết, phạm vi (P&L theo khu, trọng tâm doanh thu cho thuê; dữ liệu mô phỏng vì bảo mật + cần đáp án để chấm), đóng góp.

**Chương 2 — Tổng quan nghiên cứu**
(2.1) Giải trình là khâu nối số liệu với quyết định quản trị. (2.2) LLM viết trôi chảy nhưng hay bịa và yếu tính số trên dữ liệu tài chính (FinQA, TAT-QA) → RAG giúp viết có tài liệu kèm (Lewis và cộng sự, 2020) → các thước đo "viết có căn cứ" đã có (ALCE, FActScore) nhưng mới thử trên hỏi–đáp tổng quát. (2.3) Khi kiểm tra tốn công, con người có xu hướng duyệt không kiểm (Parasuraman và Riley, 1997; Lee và See, 2004). (2.4) Khoảng trống: chưa ai thiết kế và đánh giá trọn vẹn cho giải trình ngân sách trong FP&A.

**Chương 3 — Phương pháp nghiên cứu**
(3.1) Dữ liệu: phân tích 17 giải trình thật → rút khuôn viết + các loại nguyên nhân; sinh bộ dữ liệu mô phỏng 5 khu × 12 tháng với 12 loại tình huống, mỗi tình huống có sẵn đáp án. (3.2) Mô hình & kiến trúc: 4 khối — tính số, tìm tài liệu, viết theo khuôn kèm trích dẫn, soát lại và từ chối khi thiếu bằng chứng. (3.3) Cơ chế đánh giá: 5 thước đo theo chuẩn nghiên cứu trước; đáp án chốt trước khi AI làm bài; so máy chấm với người chấm. (3.4) Thiết lập: 3 cấu hình cùng một model; mỗi tình huống chạy 3 lần lấy trung bình; web FastAPI + React.

**Năm thước đo dùng trong 3.3 và Chương 4** *(mỗi thước đo chạy 3 lần/tình huống, lấy trung bình ± độ lệch chuẩn)*

| # | Thước đo | Câu hỏi nó trả lời | Chuẩn lấy từ |
|---|---|---|---|
| 1 | Độ chính xác số liệu (numerical exact match) | Các con số trong giải trình có khớp sổ không? | FinQA (Chen và cộng sự, 2021); TAT-QA (Zhu và cộng sự, 2021) |
| 2 | Độ chính xác trích dẫn (citation precision/recall) | Trích dẫn có chỉ đúng tài liệu không, có trích đủ không? | ALCE (Gao, Yen và cộng sự, 2023) |
| 3 | Tỷ lệ nhận định thiếu căn cứ (unsupported-claim rate) | Câu nguyên nhân nào viết ra mà không có bằng chứng đỡ? | Rashkin và cộng sự (2023); Min và cộng sự (2023) |
| 4 | Từ chối đúng lúc (abstention accuracy) | Không có tài liệu, nó có dám nói "chưa đủ bằng chứng" không? | Rajpurkar, Jia và Liang (2018); Kamath, Jia và Liang (2020) |
| 5 | Độ trúng khâu tìm tài liệu (precision@k / recall@k) | Bước tìm bằng chứng có lấy đúng tài liệu không? | Manning và cộng sự (2008) |

**Chương 4 — Kết quả nghiên cứu**
(4.1) Bảng điểm 3 cấu hình trên 5 thước đo + một tình huống đi trọn từ số liệu đến giải trình. (4.2) Kiểm định tính vững: tách theo loại tình huống; các tình huống cố tình làm khó — không có tài liệu liên quan (có dám từ chối không), tài liệu nhiễu trùng từ khóa, lỗi gieo cố ý; so máy chấm với người chấm. (4.3) Thảo luận: kết quả nói gì về 3 giả thuyết, giống/khác nghiên cứu trước, hạn chế.
