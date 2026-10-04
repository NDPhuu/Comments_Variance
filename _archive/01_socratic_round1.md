# Vòng 1 — Câu hỏi Socratic để sharpen đề tài

> **Cách dùng:** Trả lời trực tiếp dưới mỗi câu (dòng `**Trả lời:**`). Trả lời bằng sự thật quan sát được, không trả lời bằng "chắc là". Câu nào chưa biết → ghi "chưa biết, cách kiểm tra: …". Sau khi trả lời xong, Claude sẽ tổng hợp thành proposal v1.
>
> Nguyên tắc Socratic ở đây: mỗi câu hỏi nhắm vào một **giả định chưa kiểm chứng** của draft_v0. Câu trả lời của bạn sẽ quyết định scope, không phải ý kiến của AI nào.

---

## Nhóm A — Vấn đề có thật không, và nằm ở đâu?

### A1. Thời gian thực sự trôi đi đâu?
Trong chu kỳ tháng gần nhất, từ lúc có số Actual đến lúc bộ comments được duyệt xong: tổng mất bao nhiêu giờ-người, và phân bổ phần trăm giữa:
(a) chuẩn bị/đối chiếu số liệu — (b) tìm nguyên nhân chênh lệch — (c) chờ/hỏi người khác xác nhận — (d) viết comment — (e) sửa theo review?

*Vì sao hỏi:* draft_v0 mặc định bottleneck là "tìm evidence trong tài liệu" → mới cần RAG. Nếu bottleneck thật là (a) hoặc (e), kiến trúc phải khác hẳn. Đây là câu RQ1 phải trả lời bằng đo lường, nhưng bạn có thể ước lượng trước từ trải nghiệm.

**Trả lời:**

### A2. Review sửa cái gì?
Khi manager review comments (của bạn hoặc của skill v4/v5), họ sửa nhiều nhất vì: số sai? thiếu/sai driver? chọn sai khoản trọng yếu để nói? hay văn phong/cấu trúc? Bạn có giữ được các cặp bản-trước/bản-sau-sửa không?

*Vì sao hỏi:* lỗi mà người review phải sửa = định nghĩa vận hành của "chất lượng commentary" = chính là evaluation metrics của khóa luận. Cặp trước/sau còn là ground truth miễn phí.

**Trả lời:**

### A3. Skill v4/v5 hiện tại thiếu gì?
Bạn đã iterate rent-variance-comment đến v5. Điều gì khiến nó vẫn chưa "xong"? Nó sai ở đâu, khi nào bạn không dám tin output của nó?

*Vì sao hỏi:* khoảng cách giữa v5 và "đáng tin" chính là research gap thật của bạn — cụ thể và defensible hơn mọi gap trích từ literature.

**Trả lời:**

---

## Nhóm B — Input: evidence thật sự nằm ở đâu?

### B1. Truy vết 3 variance thật
Chọn 3 variance trọng yếu gần đây (đã ẩn danh). Với từng cái: nguyên nhân cuối cùng được xác nhận bằng **nguồn cụ thể nào** — file nào/cột nào (contract list? rent roll? GL?), email/tin nhắn, hay lời nói của ai? Trong 3 cái đó, bao nhiêu cái suy ra được **thuần từ dữ liệu có cấu trúc**, không cần đọc bất kỳ document nào?

*Vì sao hỏi:* đây là câu quyết định kiến trúc. Nếu ≥2/3 nguyên nhân suy từ structured data → vector RAG trên invoice/PO là "solution looking for a problem"; MVP chỉ cần structured evidence linking. Nếu ngược lại → RAG có chỗ đứng.

**Trả lời:**

### B2. Grain và mapping
Budget và Actual hiện có cùng grain không (property × account × tháng)? Mapping chart-of-accounts giữa Budget và GL đã tồn tại sẵn, hay mỗi tháng bạn/analyst phải tự khớp tay?

*Vì sao hỏi:* nếu phải khớp tay, thì "deterministic variance engine" không phải phần phụ — nó là nửa giá trị của sản phẩm, và là phần chắc chắn làm được.

**Trả lời:**

### B3. Quyền dùng dữ liệu
Đã hỏi ai ở công ty về việc dùng dữ liệu ẩn danh cho khóa luận chưa? Câu trả lời là gì / khi nào hỏi được? Nếu không được phép: bạn chấp nhận phương án synthetic benchmark + chỉ mô tả định tính case thực không?

*Vì sao hỏi:* điều kiện go/no-go số 1 của draft_v0, và là thứ phải chốt TRƯỚC khi thiết kế evaluation. Quyết định luôn việc được dùng cloud LLM API hay không.

**Trả lời:**

---

## Nhóm C — Output: sản phẩm dừng ở đâu, cho ai?

### C1. Một comment "đạt chuẩn" trông như thế nào?
Dán vào đây 2–3 comment thật đã được duyệt (ẩn danh số nhạy cảm): độ dài, cấu trúc, bắt buộc nêu con số nào, ngôn ngữ (Anh/Việt), văn phong nhà (house style) có quy tắc ngầm nào?

*Vì sao hỏi:* output schema của hệ thống phải mirror chuẩn này, không phải chuẩn tưởng tượng. Đây cũng là reference corpus cho đánh giá.

**Trả lời:**

### C2. Mức độ "xong" của output
Hệ thống nên dừng ở mức nào để hữu ích nhất mà vẫn an toàn:
(a) bảng variance đã xếp hạng trọng yếu — (b) variance case kèm evidence đã liên kết — (c) draft comment có citation — (d) comment đã qua verify số học, sẵn sàng cho manager?
Và ai là NGƯỜI DÙNG CHÍNH: analyst (viết) hay manager (review)?

*Vì sao hỏi:* mỗi mức là một claim khác nhau phải chứng minh. Mức (d) đòi verification gates; mức (b) thì không cần LLM nhiều. Chọn mức = chọn độ khó của khóa luận.

**Trả lời:**

### C3. Thế nào là "thắng"?
Hoàn thành khóa luận xong, điều gì ĐO ĐƯỢC xảy ra thì bạn coi là thành công? (vd: unsupported-claim rate < x%; thời gian làm comments giảm y%; manager chấp nhận z% draft không sửa nội dung; hay đơn giản: hệ thống được team dùng thật 2 tháng liên tiếp?)

*Vì sao hỏi:* acceptance criteria phải có TRƯỚC khi build, nếu không evaluation sẽ bị fit theo kết quả.

**Trả lời:**

---

## Nhóm D — Ràng buộc khóa luận

### D1. Khuôn khổ học thuật
Trường/khoa/GVHD của bạn: chấp nhận dạng đề tài nào (Design Science artifact? nghiên cứu thực nghiệm? "xây dựng hệ thống thông tin"?), yêu cầu độ dài/ngôn ngữ khóa luận, deadline nộp, và có yêu cầu gì về "tính mới"?

**Trả lời:**

### D2. Nguồn lực
Bạn có bao nhiêu giờ/tuần cho đề tài (ngoài giờ thực tập), trong bao nhiêu tuần? Có bao nhiêu FP&A analyst/manager thực sự có thể tham gia đánh giá (kể cả chỉ 30 phút chấm điểm mù)?

**Trả lời:**

### D3. Hạ tầng được phép
Với dữ liệu đã ẩn danh: được dùng cloud LLM API (Claude/GPT) không, hay bắt buộc local model? Công ty có ràng buộc nào thành văn về AI chưa?

**Trả lời:**

---

## Giả thuyết làm việc của Claude (để bạn bác bỏ hoặc xác nhận)

Dựa trên bằng chứng trong workspace (chưa được bạn xác nhận), tôi đặt cược như sau — **trả lời Round 1 sẽ xác nhận hoặc bác bỏ**:

1. **Scope**: pivot từ OPEX → **leasing revenue/NOI variance** (hoặc cả hai nếu dữ liệu OPEX thật sự sẵn). Lý do: dữ liệu, domain knowledge, ground truth và reviewer đều đang nằm trong tay bạn.
2. **Kiến trúc**: "calculate-then-narrate" —
   - *Input*: Budget workbook + Actual (GL/rent roll/contract list) cùng grain `property × account × tháng`;
   - *Engine tất định*: tính variance, materiality, phân rã theo driver có cấu trúc (contract events: new lease, termination, escalation, FX, timing, one-off);
   - *LLM*: chỉ nhận "context package" đã verify (facts + drivers + residual chưa giải thích được) và viết comment theo house-style schema, mọi con số phải trace về engine;
   - *Verifier*: regex/parser đối chiếu mọi số trong comment với engine output; claim không có nguồn → chặn hoặc gắn nhãn "cần xác nhận".
   - **Không có vector DB trong MVP** trừ khi B1 chứng minh ngược lại.
3. **Baselines khả thi**: (0) comment người viết trong lịch sử; (1) prompt-only skill kiểu v5; (2) proposed pipeline. Bỏ crossover user study; thay bằng blind expert scoring trên n case + đo unsupported-claim/citation accuracy tự động.
4. **Contribution thành thật**: design principles + evaluation protocol cho "grounded variance commentary" trong FP&A, kèm case study thực + synthetic benchmark công khai. Không claim phát minh RAG mới, không claim organizational impact.

> Nếu bạn xác nhận ≥3/4 giả thuyết này, đề tài đổi tên theo hướng: *"Thiết kế và đánh giá hệ thống sinh giải trình chênh lệch ngân sách có kiểm chứng số liệu (verified variance commentary) cho FP&A: nghiên cứu tình huống bất động sản công nghiệp"* — và RAG chỉ còn là một thành phần tùy chọn, không phải tên đề tài.
