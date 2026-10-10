# Câu chuyện & bối cảnh đề tài — v2

> **v2 (2026-10-04) thay v1** sau khi xác nhận hai thực tế từ người thực hiện:
> 1. Quy trình comments hiện tại ĐÃ có AI hỗ trợ, chỉ tốn **~1 giờ/tháng** → luận điểm "tiết kiệm thời gian" CHẾT, không được dùng làm tính cấp thiết.
> 2. Pain thật: với người dùng **non-tech**, AI là **hộp đen** đúng nghĩa — không biết nó làm thế nào, lấy số liệu ở đâu, suy luận ra sao.
>
> Neo thực tế: bộ file tháng nào cũng có trong `Sample_FP&A/` — `GL Full`, `PL_Act vs budget`, `SG&A PL`, `Leasing YTD` (có sheet `Act vs Budget` và `Comment`).

---

## Pitch 30 giây

*"Ở đơn vị em thực tập, AI đã giúp viết variance comments trong khoảng một giờ mỗi tháng — nhanh thì nhanh rồi. Nhưng với người làm tài chính không biết lập trình, nó là một hộp đen: không ai biết con số trong comment được lấy từ đâu, nguyên nhân được suy ra bằng cách nào, và khi nào AI đang đoán. Khóa luận của em biến hộp đen thành hộp kính: mọi con số trong comment bấm vào là truy về dòng sổ cái, mọi nhận định nguyên nhân phải kèm bằng chứng, thiếu chứng cứ thì hệ thống phải tự khai là thiếu — và em đo lường xem sự minh bạch đó chặn được bao nhiêu nhận định vô căn cứ, giảm bao nhiêu công kiểm tra, và thay đổi niềm tin của người dùng tài chính ra sao."*

## Câu chuyện 5 đoạn (xương sống Chương 1)

**Đoạn 1 — Nghi thức tháng nào cũng lặp lại.** Sau chốt sổ hàng tháng, FP&A phải giải trình vì sao thực tế lệch ngân sách. Con số trả lời "lệch bao nhiêu"; commentary trả lời "vì sao" — và là phần ban lãnh đạo thực sự đọc để ra quyết định. Tại doanh nghiệp nghiên cứu tình huống, nghi thức này chạy trên một bộ file cố định: sổ cái đầy đủ (GL Full), bảng đối chiếu P&L Actual vs Budget, gói SG&A, và báo cáo Leasing YTD có sheet Act vs Budget + Comment.

**Đoạn 2 — Twist: AI đã ở trong quy trình rồi.** Khác với 95% đề tài "ứng dụng AI" (xuất phát từ "doanh nghiệp chưa có AI"), ở đây AI **đã** được dùng để soạn comments — cả chu trình chỉ còn ~1 giờ. Nhưng sự hiệu quả đó đứng trên hai chân rất yếu: (1) nó phụ thuộc vào MỘT người biết điều khiển AI (bus factor — người đó đi thì quy trình sập); (2) với các thành viên non-tech còn lại, toàn bộ bước sinh comment là hộp đen: không nhìn được số lấy từ đâu, logic suy nguyên nhân thế nào, chỗ nào AI đang đoán. Niềm tin hiện tại là **niềm tin theo thói quen**, không phải **niềm tin có cấu trúc**.

**Đoạn 3 — Vì sao hộp đen trong tài chính là nguy hiểm.** Khi output trôi chảy mà công cụ kiểm tra không có, người review dễ rơi vào automation bias — duyệt cho qua thứ mình không thể kiểm chứng (Parasuraman & Riley, 1997; Lee & See, 2004). Một con số không khớp sổ hoặc một nguyên nhân bịa có thể lọt thẳng vào báo cáo quản trị; audit trail đứt gãy đúng ở khâu sinh văn bản. Bản chất công việc analyst đã đổi: từ **người viết** thành **người kiểm** — nhưng toolchain hiện tại chỉ hỗ trợ viết, không hỗ trợ kiểm.

**Đoạn 4 — Khoảng trống.** Nghiên cứu và sản phẩm đổ dồn vào năng lực *sinh* (generation): RAG, prompt, benchmark QA tổng quát. Năng lực *kiểm chứng cho người dùng tài chính non-tech* — truy vết số về sổ, truy vết claim về bằng chứng, biết từ chối khi thiếu chứng cứ, và giao diện làm được việc đó bằng một cú bấm — gần như bỏ trống. FinQA/TAT-QA đã chứng minh LLM yếu khi tự tính số; công cụ thương mại thì không công bố kiến trúc lẫn bằng chứng grounding. Gap: chưa có nghiên cứu thiết kế – đánh giá đầu-cuối một hệ thống variance commentary **có thể kiểm chứng được** đặt trong quy trình FP&A thực. *(Cần literature search xác nhận trước khi viết Chương 2.)*

**Đoạn 5 — Đề tài.** Nghiên cứu ứng dụng: vận dụng kiến thức RAG/NLP để xây dựng và đánh giá một hệ thống "hộp kính" giải quyết vấn đề trên của doanh nghiệp: engine tất định tính toàn bộ số (LLM không được tính số); truy xuất bằng chứng hybrid (RAG — module + trục so sánh); sinh comment theo schema bắt buộc kèm citation; cổng kiểm chứng số học + citation + cơ chế từ chối; và web UI (FastAPI + React) nơi **mỗi con số bấm vào là thấy dòng GL nguồn, mỗi nguyên nhân bấm vào là thấy bằng chứng** — UI không phải trang trí, nó chính là cơ chế minh bạch. Đánh giá trên benchmark synthetic 5 properties mô phỏng đúng cấu trúc bộ file tháng thật (ẩn danh), so với LLM-only và RAG không kiểm chứng (cùng bằng chứng, không cổng kiểm).

## Input / Output (neo theo file thật)

**INPUT** — synthetic, mô phỏng đúng cấu trúc `Sample_FP&A/`:
1. **GL Full**: dump giao dịch (ngày, GL account, entity/project, vendor, memo, amount) — khuôn từ `GL Full Jul'26.xlsb`.
2. **Budget P&L** theo line × project × tháng — khuôn từ sheet `PL_26B` / `Budget for Monthly Package`.
3. **Master & mapping**: GL account → PL line; danh mục 5 properties (PROP-A…PROP-E), vendor, cost center.
4. **Evidence corpus** cho RAG: hợp đồng, email phê duyệt, memo nghiệp vụ (synthetic, có gold label: evidence nào giải thích variance nào).

**OUTPUT** — với mỗi material variance (PL line × project, MTD/YTD):
- Comment theo house style (khuôn từ sheet `Comment` của Leasing YTD), trong đó:
  - mọi con số mang **provenance link** về dòng GL / ô budget;
  - mọi câu nguyên nhân có **citation** tới evidence, hoặc nhãn "chưa xác nhận — cần hỏi [ai]";
  - trạng thái case: `verified` / `cần bổ sung chứng cứ` / `abstained`.

## Tên đề tài gợi ý (v2)

- **EN:** *From Black Box to Glass Box: Design and Evaluation of a Verifiable AI System for Budget-Variance Commentary in FP&A, Combining Deterministic Analytics and Retrieval-Augmented Generation*
- **VN:** *Từ hộp đen đến hộp kính: Thiết kế và đánh giá hệ thống AI có thể kiểm chứng cho giải trình chênh lệch ngân sách–thực tế trong FP&A, kết hợp phân tích tất định và sinh ngôn ngữ tăng cường truy xuất (RAG)*

## Thuyết phục giảng viên — map vào thang chấm

- **Tính cấp thiết:** GenAI đang vào quy trình tài chính nhanh hơn khả năng kiểm chứng nó — quan sát trực tiếp tại doanh nghiệp, cộng hưởng với mạch AI governance. KHÔNG dựa vào "tiết kiệm thời gian".
- **Tính khoa học:** quy trình nghiên cứu ứng dụng rõ ràng (khảo sát vấn đề → yêu cầu → xây dựng → đánh giá); RQ + giả thuyết + metrics chuẩn của literature RAG/NLP (unsupported-claim rate, citation precision/recall, numeric accuracy, abstention); baseline so sánh trên cùng frozen case set.
- **Tính mới (thành thật):** (1) kiến trúc + design principles cho *verifiable* financial commentary; (2) benchmark công khai có gold label cho tác vụ này (khả năng cao là đầu tiên); (3) bằng chứng định lượng về giá trị của verification machinery so với LLM thuần/RAG không kiểm chứng. Đóng góp dạng "hệ thống ứng dụng + bộ dữ liệu đánh giá + bằng chứng định lượng" — đúng khuôn một nghiên cứu ứng dụng giải quyết vấn đề doanh nghiệp.
- **Tính khả thi:** lived experience (đã vận hành AI comments thật, iterate đến v5), bộ file khuôn sẵn có, synthetic data né bảo mật, 20 ngày với kế hoạch cắt lớp.
- **Tính hữu ích:** claim trung thực — không hứa nhanh hơn, hứa **kiểm chứng được**: giảm rủi ro số sai/claim bịa vào báo cáo quản trị, giảm chi phí kiểm tra, biến trust cá nhân thành trust quy trình. **Demo 2 phút trước hội đồng:** cùng một variance, ba output đặt cạnh nhau (LLM-only / RAG không kiểm chứng / glass-box), bấm một con số → hiện dòng GL nguồn. Hội đồng *nhìn thấy* sự khác biệt, không cần tin lời.

## Câu hỏi hội đồng sẽ hỏi — và lời đáp

1. *"AI làm được trong 1 tiếng rồi, em còn giải quyết gì?"* — Một giờ đó tồn tại nhờ một cá nhân khéo dùng AI: không chuyển giao được, không kiểm toán được, không ai khác kiểm chứng được. Em không làm nó nhanh hơn; em làm nó **tin được và chuyển giao được** — thể chế hóa từ "người khéo prompt" thành "quy trình có kiểm soát".
2. *"Dữ liệu giả thì kết luận có giá trị gì?"* — Benchmark có gold label tự nó là đóng góp (chuẩn mực NLP); schema mô phỏng 1:1 bộ file thật; validation trên dữ liệu thật là future work nêu thẳng ở hạn chế.
3. *"RAG cũ rồi, em có gì mới?"* — Em không nghiên cứu RAG; em nghiên cứu điều kiện để tin được AI trong giải trình tài chính. RAG là một module và một trục so sánh.
4. *"Sao không dùng Copilot thương mại?"* — Hộp đen, không bảo đảm kiểm chứng, không công bố đánh giá cho tác vụ này; khóa luận cung cấp chính thước đo mà các công cụ đó thiếu.

## Literature hooks bổ sung cho trục trust/verification (verify trước khi cite)

- Lee, J. D., & See, K. A. (2004). Trust in automation: Designing for appropriate reliance. *Human Factors, 46*(1), 50–80.
- Parasuraman, R., & Riley, V. (1997). Humans and automation: Use, misuse, disuse, abuse. *Human Factors, 39*(2), 230–253.
- Doshi-Velez, F., & Kim, B. (2017). *Towards a rigorous science of interpretable machine learning* (arXiv:1702.08608). arXiv.

→ Cần đưa vào `02_khung_khoaluan_APA7.md` (mục 3.2 hoặc mục mới "Trust & XAI") ở lần cập nhật tới, cùng với việc đổi khung 6 chương → 5 chương.
