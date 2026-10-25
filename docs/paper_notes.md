# Paper notes — đọc từ nguồn gốc (PDF trong `materials/papers/`, 10/10/2026)

> Mỗi bài: bài nói gì → định nghĩa nguyên bản quan trọng → **ta lấy gì / đổi gì và vì sao**.
> Đây là spec cho `experiments/metrics.py` và là nguồn viết mục 2.2 + 3.3 của khóa luận.

## 1. ALCE — Gao, Yen, Yu, Chen (EMNLP 2023) · aclanthology.org/2023.emnlp-main.398

- Benchmark đầu tiên chấm tự động "LLM viết có trích dẫn"; 3 chiều: fluency, correctness, citation quality.
- **Citation recall**: mỗi statement được chấm 0/1 — bằng 1 khi *ghép toàn bộ* passages đã cite lại thì **entail** (suy ra được) statement đó; ALCE dùng NLI model TRUE (t5-xxl) để phán entail. Recall của bài = trung bình trên các statement.
- **Citation precision**: một citation là "thừa/irrelevant" nếu (a) một mình nó không đỡ được statement VÀ (b) bỏ nó đi, các citation còn lại vẫn đỡ được. Nếu recall của statement = 0 thì precision các citation của nó = 0.
- **Ta lấy:** cấu trúc statement-level + đúng logic recall/precision trên. **Ta đổi:** thay NLI model bằng so khớp **gold evidence ID** + quote-match (benchmark của ta có đáp án gắn sẵn) → tất định, tái lập, chặt hơn NLI. Khác biệt này khai rõ ở 3.3.

## 2. FActScore — Min và cộng sự (EMNLP 2023) · aclanthology.org/2023.emnlp-main.741

- Tách bài viết dài thành **atomic facts** (mỗi câu một thông tin), điểm = % atomic facts được nguồn tri thức đỡ; ChatGPT chỉ đạt ~58% trên tiểu sử người. Ghi nhận: model biết từ chối (abstain) thì factual precision cao hơn; lỗi dồn về phần sau của bài viết.
- **Ta lấy:** nguyên tắc chấm ở mức mệnh đề nguyên tử. Schema output của ta (mỗi driver/offset/note là một mục riêng, kèm citations) **đã atomic-by-construction** → unsupported-claim rate = % mục nhận định không có evidence hợp lệ, chấm bằng rule không cần LLM.

## 3. TAT-QA — Zhu và cộng sự (ACL 2021) · aclanthology.org/2021.acl-long.254

- QA trên bảng + văn bản tài chính; **họ phải sửa EM/F1 gốc vì bản gốc BỎ DẤU +/−**: "we keep the plus-minus of a value"; F1 = 0 nếu số × scale không khớp chính xác đáp án.
- **Ta lấy:** numeric gate parse **dấu** và **scale** ($530k ≠ $530m ≠ 530); sai dấu hoặc sai scale = sai hoàn toàn. Đây là căn cứ học thuật cho đúng bài học "$142/m²/kỳ hạn" của dự án.

## 4. FinQA — Chen và cộng sự (EMNLP 2021) · aclanthology.org/2021.emnlp-main.300

- QA số học trên báo cáo tài chính thật, có gold reasoning program; model tốt nhất 65% vs chuyên gia 91%. Lưu ý phương pháp: **execution accuracy có thể overestimate** (trúng đáp án do may), program accuracy có thể false negative.
- **Ta lấy:** (i) luận điểm "LLM không được tự tính số trong tài chính"; (ii) numeric gate khớp số với **TRƯỜNG engine cụ thể** (variance/budget/actual/contributor…), không chỉ khớp giá trị — tránh "trúng do may".

## 5. Selective QA — Kamath, Jia, Liang (ACL 2020) · aclanthology.org/2020.acl-main.503

- Khung **selective prediction**: hệ thống trả (answer, confidence); trả lời khi confidence ≥ ngưỡng, ngược lại từ chối. Đánh giá bằng **risk–coverage**: coverage = % câu dám trả lời; risk = tỷ lệ sai trên phần đã trả lời; model overconfident trên dữ liệu lạ → cần calibrator ngoài.
- **Ta lấy:** abstention của ta là rule tất định (LINKAGE nội dung — xem ghi chú 10/10 bên dưới; ngưỡng BM25 đã bỏ vì không tách được bẫy/thật) — đóng vai calibrator ngoài. Chương 4 báo: recall lớp phải-từ-chối trên trap cases + bảng coverage/risk cho cả 3 cấu hình (KHÔNG dùng tên 'abstention accuracy').

## 6. SQuAD 2.0 — Rajpurkar, Jia, Liang (ACL 2018) · aclanthology.org/P18-2124

- Thêm >50k câu hỏi **không trả lời được, viết adversarial cho GIỐNG câu trả lời được** (có "plausible answer" sai); hệ thống mạnh rớt từ 86% xuống 66% F1.
- **Ta lấy:** căn cứ thiết kế 2 loại bẫy của dataset: case thiếu bằng chứng (unanswerable) và tài liệu nhiễu trùng từ khóa sai khu (plausible-but-wrong) — đo đúng năng lực "biết mình không biết".

## 7. RAGAS — Es và cộng sự (EACL 2024) · arXiv:2309.15217

- Bộ đo reference-free cho RAG: **Faithfulness** (câu trả lời phải bám context), Answer Relevance, Context Relevance — ước lượng bằng LLM prompting.
- **Ta lấy:** chỉ làm **metric phụ** nếu kịp, kèm caveat LLM-judge (chính RAGAS thừa nhận các model dò hallucination bằng prompt chuẩn còn yếu — dẫn Li 2023, Azaria & Mitchell 2023). Metric chính của ta là tất định trên gold.

## 8. Self-RAG — Asai và cộng sự (ICLR 2024) · arXiv:2310.11511 · CRAG — Yan và cộng sự (2024) · arXiv:2401.15884

- Self-RAG: model tự sinh reflection tokens quyết định khi nào truy xuất và tự phê bình output. CRAG: thêm bộ **đánh giá chất lượng retrieval** trước khi sinh, kém thì sửa/truy xuất lại.
- **Ta lấy:** cảm hứng kiến trúc, KHÔNG lấy cơ chế (cả hai cần model/huấn luyện riêng): nguyên tắc "kiểm tra chất lượng bằng chứng trước khi viết" của ta nằm ở metadata filter + ngưỡng retrieval_score (tất định); nguyên tắc "tự phê bình" được thay bằng verification gates NGOÀI model — phù hợp yêu cầu kiểm toán được.

## 9. Know Your Limits — Wen và cộng sự (TACL 13, 2025) · DOI 10.1162/tacl_a_00754

- Survey chuyên về abstention trong LLM: hệ thống hóa phương pháp, benchmark, metric theo 3 góc nhìn (query–model–giá trị con người).
- **Ta lấy:** chỗ dựa thuật ngữ cho đánh giá từ chối. Lưu ý quan trọng: "abstention accuracy" KHÔNG phải tên metric chuẩn hóa — trong luận phải định nghĩa tường minh = recall của lớp 'phải-từ-chối' trên các case gieo không bằng chứng, neo vào Kamath 2020 + SQuAD 2.0 + Wen 2025, luôn báo kèm cặp coverage–risk.

## Ghi chú thiết kế phát sinh khi build (10/10) — abstention bằng LINKAGE

Phương án ngưỡng điểm BM25 thô THẤT BẠI khi đo trên dataset (case thật CORP: −2,35…1,96 < case bẫy: 2,16–3,97 — điểm BM25 không so sánh được giữa các case vì pool/IDF khác nhau). Thay bằng **rule liên kết nội dung tất định** (`retrieval.core.linked`): doc phải nhắc mã contributor (TEN/VND/GL), tên dòng P&L, hoặc ≥2 từ nội dung memo. Đây là phiên bản tất định của "retrieval evaluator" (CRAG); bản thân phát hiện này đưa vào mục Thảo luận C4.

## Bảng chốt: metric của khóa luận ↔ gốc học thuật ↔ điểm đổi

| Metric của ta | Gốc | Đổi gì |
|---|---|---|
| Numerical EM (giữ dấu + scale, khớp theo trường engine) | TAT-QA + FinQA | gold = output engine thay vì đáp án người |
| Citation precision/recall (statement-level) | ALCE | gold-ID + quote-match thay NLI |
| Unsupported-claim rate (mục nhận định) | FActScore + AIS | atomic theo schema, chấm rule |
| Abstain recall (lớp phải-từ-chối, tên do đề tài đặt) + coverage/risk | SQuAD 2.0 + Kamath + Wen 2025 | abstain bằng rule linkage tất định |
| Retrieval P@5/R@5 | IR chuẩn (Manning 2008) | giữ nguyên |
| (Phụ) RAGAS faithfulness | RAGAS | chỉ tham khảo, caveat LLM-judge |
