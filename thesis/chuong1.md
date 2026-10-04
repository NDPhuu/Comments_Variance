# PHẦN 1: GIỚI THIỆU

> **Trạng thái: DRAFT 1 — 04/10/2026.** Viết theo `prompts/thesis_writing.md`; trích dẫn Harvard theo `docs/quy_dinh_vien.md`. Còn một chỗ chờ tác giả bổ sung (đánh dấu ⟦…⟧).

## 1.1. Bối cảnh nghiên cứu

Mỗi tháng, sau khi chốt sổ kế toán, bộ phận FP&A (Financial Planning & Analysis — hoạch định và phân tích tài chính) của doanh nghiệp phải trả lời một câu hỏi lặp lại: vì sao kết quả thực tế lệch so với ngân sách? Phần trả lời bằng văn bản cho câu hỏi này được gọi là *variance commentary* (giải trình chênh lệch). Các bảng số cho ban lãnh đạo biết lệch bao nhiêu. Giải trình cho họ biết vì sao lệch, và đó là phần được đọc kỹ nhất trước khi ra quyết định.

Nghiên cứu này xuất phát từ quan sát trực tiếp của tác giả trong kỳ thực tập FP&A tại một doanh nghiệp bất động sản công nghiệp (thông tin doanh nghiệp được ẩn danh theo cam kết bảo mật). Quy trình giải trình hàng tháng tại đây chạy trên một bộ tệp cố định: sổ cái tổng hợp, bảng so sánh kết quả kinh doanh thực tế với ngân sách, và báo cáo hoạt động cho thuê. Phân tích 17 giải trình đã được phê duyệt trong 8 tháng liên tiếp cho thấy giải trình có chuẩn mực riêng: viết ngắn, mỗi nguyên nhân phải gắn một con số và một mốc thời gian, phần bù trừ ngược chiều được tách riêng, và thường kèm ghi chú về khoản sẽ phát sinh ở kỳ tới.

Một thực tế quan trọng khác: trí tuệ nhân tạo tạo sinh đã có mặt trong chính quy trình này. Với sự hỗ trợ của *mô hình ngôn ngữ lớn* (Large Language Model — LLM, loại mô hình AI có khả năng đọc và viết văn bản), toàn bộ phần soạn giải trình tháng tại đơn vị quan sát chỉ còn khoảng một giờ. Nói cách khác, bài toán "AI có viết được giải trình hay không" đã được thực tế trả lời. Câu hỏi còn lại khó hơn nhiều.

## 1.2. Vấn đề nghiên cứu

Vấn đề không nằm ở tốc độ, mà nằm ở khả năng kiểm chứng. Với người làm tài chính không có nền tảng lập trình, bước AI soạn giải trình là một *hộp đen (black box)*: họ không biết con số trong giải trình được lấy từ đâu, nguyên nhân được suy ra bằng cách nào, và khi nào mô hình đang suy đoán thay vì dựa trên dữ liệu. Niềm tin vào kết quả, nếu có, là niềm tin theo thói quen — không phải niềm tin dựa trên khả năng truy vết.

Một văn bản trôi chảy nhưng không kiểm chứng được tạo ra rủi ro thực. Nghiên cứu về tự động hóa đã chỉ ra hiện tượng *automation bias* (thiên lệch do tự động hóa): khi đầu ra của máy trông đáng tin và việc kiểm tra tốn công, con người có xu hướng phê duyệt mà không kiểm chứng (Parasuraman và Riley, 1997). Niềm tin phù hợp chỉ hình thành khi con người có phương tiện để đánh giá đúng năng lực của hệ thống (Lee và See, 2004). Trong bối cảnh tài chính, một con số không khớp sổ hoặc một nguyên nhân do mô hình tự nghĩ ra có thể đi thẳng vào báo cáo quản trị, trong khi dấu vết kiểm toán bị đứt đúng tại khâu sinh văn bản. Thêm vào đó, quy trình hiện tại phụ thuộc vào một cá nhân biết điều khiển AI; tri thức đó không được thể chế hóa.

⟦Chờ tác giả bổ sung: một tình huống thực tế (đã ẩn danh) trong đó giải trình do AI soạn nghe hợp lý nhưng chứa con số hoặc nguyên nhân không có căn cứ, và cách sai sót được phát hiện.⟧

Vấn đề nghiên cứu được phát biểu như sau: **làm thế nào để thiết kế một hệ thống sinh giải trình chênh lệch ngân sách trong đó mọi con số truy vết được về sổ sách, mọi nhận định nguyên nhân truy vết được về bằng chứng, và hệ thống từ chối kết luận khi bằng chứng không đủ?**

Khoảng trống nghiên cứu sẽ được phân tích chi tiết ở Phần 2, nhưng có thể tóm tắt: các nghiên cứu về LLM tập trung chủ yếu vào năng lực sinh văn bản; riêng với dữ liệu tài chính, các bộ dữ liệu chuẩn cho thấy LLM dễ sai khi tự thực hiện phép tính (Chen và cộng sự, 2021; Zhu và cộng sự, 2021). Trong khi đó, nhu cầu của người dùng tài chính lại nằm ở chiều ngược lại: không cần máy viết hay hơn, mà cần kiểm tra được từng câu máy viết.

## 1.3. Mục tiêu, câu hỏi và giả thuyết nghiên cứu

Mục tiêu tổng quát của khóa luận là xây dựng và đánh giá một hệ thống sinh giải trình chênh lệch ngân sách **có thể kiểm chứng** — gọi là hệ thống *hộp kính (glass-box)*, đối lập với hộp đen. Khóa luận thuộc dạng nghiên cứu ứng dụng: vận dụng kiến thức về xử lý ngôn ngữ tự nhiên (NLP) và kỹ thuật sinh văn bản tăng cường truy xuất (RAG) để giải quyết một vấn đề cụ thể của doanh nghiệp, theo quy trình bốn bước — khảo sát vấn đề tại doanh nghiệp, xác định yêu cầu hệ thống, thiết kế và xây dựng, đánh giá thực nghiệm.

Mục tiêu cụ thể gồm ba phần: (i) thiết kế kiến trúc tách phần tính toán (do chương trình tất định thực hiện) khỏi phần diễn đạt (do LLM thực hiện), trong đó nguyên nhân phải gắn với bằng chứng được truy xuất; (ii) xây dựng bộ dữ liệu mô phỏng có đáp án chuẩn để đánh giá khách quan; (iii) so sánh định lượng hệ thống đề xuất với hai cách dùng AI phổ biến hiện nay.

Ba câu hỏi nghiên cứu tương ứng:

- **RQ1.** Hệ thống cần được thiết kế như thế nào để mọi con số và nhận định trong giải trình đều truy vết được về nguồn?
- **RQ2.** So với cách dùng LLM trực tiếp và cách kết hợp truy xuất tài liệu thông thường (vanilla RAG), kiến trúc đề xuất cải thiện ra sao về độ chính xác số liệu, độ chính xác trích dẫn và tỷ lệ nhận định thiếu căn cứ?
- **RQ3.** Hệ thống có từ chối kết luận đúng lúc khi bằng chứng không đủ hay không?

Từ RQ2 và RQ3, khóa luận kiểm định ba giả thuyết: **H1** — hệ thống đề xuất có tỷ lệ nhận định thiếu căn cứ thấp hơn hai phương án đối chứng; **H2** — hệ thống đề xuất có độ chính xác trích dẫn cao hơn phương án vanilla RAG; **H3** — hệ thống đề xuất từ chối đúng trên các tình huống thiếu bằng chứng với tỷ lệ cao hơn hai phương án đối chứng. Phương pháp kiểm định được trình bày ở Phần 3; kết quả đối chiếu từng giả thuyết ở Phần 4.

## 1.4. Đối tượng và phạm vi nghiên cứu

Đối tượng nghiên cứu là quy trình giải trình chênh lệch giữa thực tế và ngân sách trên báo cáo kết quả kinh doanh (P&L) hàng tháng, ở mức dòng P&L theo từng khu công nghiệp, với trọng tâm là doanh thu cho thuê — mảng có các sự kiện nguyên nhân rõ ràng như chấm dứt hợp đồng sớm, dời ngày bàn giao, hay điều chỉnh đơn giá theo hợp đồng.

Về dữ liệu, khóa luận sử dụng bộ dữ liệu **mô phỏng có đáp án chuẩn**, được xây dựng theo đúng cấu trúc bộ tệp hàng tháng của doanh nghiệp quan sát nhưng không chứa bất kỳ số liệu hay danh tính thật nào. Lựa chọn này xuất phát từ hai lý do: cam kết bảo mật dữ liệu doanh nghiệp, và yêu cầu phương pháp — việc chấm điểm khách quan đòi hỏi biết trước nguyên nhân thật của từng chênh lệch, điều dữ liệu thật không cung cấp. Chi tiết được trình bày ở Phần 3.

Ngoài phạm vi nghiên cứu: dự báo tài chính, tự động ra quyết định quản trị, tích hợp trực tiếp với hệ thống ERP, tinh chỉnh (fine-tune) mô hình ngôn ngữ, và kiểm chứng trên dữ liệu thật — các nội dung này được bàn ở phần hạn chế và hướng phát triển.

## 1.5. Đóng góp dự kiến

Về học thuật, khóa luận đóng góp: (i) một kiến trúc hệ thống cùng các nguyên tắc thiết kế cho bài toán sinh giải trình tài chính kiểm chứng được; (ii) một bộ dữ liệu đánh giá công khai có đáp án chuẩn cho tác vụ giải trình chênh lệch ngân sách — theo khảo sát của tác giả, chưa có bộ tương tự được công bố; (iii) bằng chứng định lượng về mức cải thiện của cơ chế kiểm chứng so với hai cách dùng AI phổ biến.

Về thực tiễn, khung đánh giá của khóa luận chính là công cụ một doanh nghiệp cần khi quyết định có nên cho AI tham gia quy trình báo cáo quản trị hay không: thay vì tin hay không tin theo cảm tính, doanh nghiệp đo được tỷ lệ sai số, tỷ lệ trích dẫn sai và khả năng từ chối của hệ thống trước khi sử dụng.

## 1.6. Cấu trúc khóa luận

Phần còn lại của khóa luận gồm bốn phần. Phần 2 tổng quan ba dòng nghiên cứu liên quan — giải trình chênh lệch trong FP&A, mô hình ngôn ngữ lớn và cơ chế gắn kết bằng chứng, các khung đánh giá hệ thống thông tin — và chỉ ra khoảng trống. Phần 3 trình bày phương pháp: quy trình nghiên cứu ứng dụng bốn bước, thiết kế hệ thống, thiết kế dữ liệu mô phỏng và giao thức đánh giá. Phần 4 trình bày hệ thống hoàn chỉnh và kết quả thực nghiệm, đối chiếu với từng giả thuyết. Phần 5 kết luận, nêu đóng góp, hạn chế và hướng phát triển.

---

*Ghi chú biên tập (xóa trước khi nộp):* nguồn nội dung 1.1–1.2 lấy từ `objectives.md` và quan sát Phase 1; trích dẫn trong bài theo mẫu Harvard của Viện, bản đầy đủ của các nguồn nằm trong `docs/02_khung_khoaluan_APA7.md` và sẽ reformat ở bước ghép toàn văn; tư liệu kỹ thuật (dataset, engine) thuộc Phần 3–4, không đưa vào Phần 1.
