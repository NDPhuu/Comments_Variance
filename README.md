# Comments_Variance — Giải trình chênh lệch ngân sách mà kiểm tra được từng câu

Khóa luận tốt nghiệp: web app demo + bộ thí nghiệm + khóa luận 5 chương. Hạn: **18/10/2026**.

## Vấn đề (nói bằng tiếng người)

Mỗi tháng sau khi chốt sổ, người làm FP&A phải viết phần **giải trình**: vì sao doanh thu, chi phí lệch so với kế hoạch. Đây là phần ban lãnh đạo thực sự đọc.

AI viết phần này rất nhanh và rất trôi chảy. Nhưng với người làm tài chính không biết lập trình, AI là một cái hộp đen: **không biết con số nó viết lấy từ đâu, nguyên nhân nó nêu có giấy tờ gì chứng minh không, hay nó đang đoán.** Nếu AI bịa mà không ai phát hiện, cái sai đi thẳng vào báo cáo cho ban lãnh đạo — và không ai truy lại được.

Câu hỏi của đề tài: **làm sao dùng AI viết giải trình mà vẫn kiểm tra được từng con số, từng câu nguyên nhân?**

## Giải pháp trong 4 câu

1. **Số do code thường tính** (cộng trừ nhân chia bằng Python) — AI không được tính số.
2. **Nguyên nhân phải có giấy tờ**: hệ thống tự tìm tài liệu liên quan (hợp đồng, biên bản thanh lý, email phê duyệt…) và đưa cho AI.
3. **AI chỉ được viết văn** từ hai nguồn trên; viết xong, code thường soát lại từng số, từng trích dẫn.
4. **Thiếu bằng chứng thì nói thiếu** — hệ thống từ chối nêu nguyên nhân thay vì đoán.

Kết quả là một "hộp kính": trên màn hình, bấm vào con số thì hiện ra dòng sổ gốc, bấm vào nguyên nhân thì hiện ra tài liệu chứng minh.

👉 **Xem mock giao diện:** https://claude.ai/artifact/Vfzk4DSJLFJUDfzSocfCH9

## Chứng minh nó tốt hơn bằng cách nào

Tạo một bộ tình huống giả lập **có đáp án gắn sẵn**, rồi cho 3 cách cùng làm bài:

| Cách | Là gì |
|---|---|
| M0 — AI trần | Đưa số thô cho AI tự viết (cách nhiều người đang dùng) |
| M1 — RAG không kiểm chứng | AI + đúng bộ tài liệu hệ thống tìm được (như M2), nhưng viết tự do, không ai soát |
| M2 — Hệ thống này | Đủ cả 4 nguyên tắc ở trên |

Chấm điểm tự động: bao nhiêu **số sai**, bao nhiêu **trích dẫn ma**, bao nhiêu **câu nói không có căn cứ**, và có **biết từ chối** đúng lúc không.

## Cấu trúc repo

| Đường dẫn | Nội dung |
|---|---|
| `README.md` | File này — đọc đầu tiên |
| `handoff.md` | Trạng thái dự án, timeline 5 mốc, nhật ký quyết định |
| `objectives.md` | Câu chuyện đề tài (nguồn cho Chương 1) |
| `docs/architecture.md` | Kiến trúc chi tiết (có sơ đồ mermaid) + hợp đồng dữ liệu |
| `phases/` | 5 giai đoạn, mỗi giai đoạn một file checklist |
| `prompts/` | Chuẩn viết code sạch + chuẩn viết khóa luận |
| `app/` | Code (backend, sinh dữ liệu, thí nghiệm, frontend) |
| `thesis/` | Bản thảo 5 chương + hình |
| `Sample_FP&A/`, `local_data/` | Dữ liệu thật của doanh nghiệp — **không bao giờ commit** |

## Bảng thuật ngữ (đọc một lần là xong)

| Thuật ngữ | Nghĩa dễ hiểu |
|---|---|
| **Variance** | Chênh lệch giữa thực tế và kế hoạch (Actual − Budget) |
| **Materiality** | Ngưỡng trọng yếu: lệch nhỏ bỏ qua, lệch lớn phải giải trình |
| **RAG** | "Tìm trước rồi mới viết": trước khi AI viết, hệ thống đi tìm tài liệu liên quan đưa kèm, để AI viết có căn cứ thay vì viết từ trí nhớ |
| **RAG không kiểm chứng** (unverified RAG) | RAG có tìm tài liệu đưa kèm nhưng để AI viết tự do — không ai kiểm số, không ai kiểm trích dẫn. Trong đề tài, M1 dùng chung bộ truy xuất với M2 nên so sánh M1↔M2 cô lập được giá trị của khâu kiểm chứng |
| **Glass-box** | "Hộp kính", ngược với hộp đen: nhìn xuyên được vào trong — mọi số bấm ra sổ, mọi nguyên nhân bấm ra tài liệu |
| **Provenance** | Gốc gác của một con số hay một câu: nó đến từ dòng sổ nào, tài liệu nào |
| **Abstention** | Sự từ chối có chủ đích: thiếu bằng chứng thì nói thiếu, không bịa |
| **Evidence corpus** | Kho bằng chứng: tập tài liệu số hóa (hợp đồng, biên bản, email duyệt…) mà hệ thống tìm kiếm trong đó |
| **BM25** | Thuật toán tìm theo từ khóa — như Ctrl+F thông minh |
| **Embedding / BGE-M3** | Cách máy "hiểu nghĩa" để tìm tài liệu gần nghĩa dù khác từ; BGE-M3 là model mã nguồn mở, miễn phí, chạy trên máy mình |
| **Gold label** | Đáp án chuẩn gắn sẵn trong dữ liệu giả lập, dùng để chấm điểm hệ thống |

## Dữ liệu

100% dữ liệu trong repo là **giả lập** (5 khu công nghiệp PROP-A…E, 12 tháng), mô phỏng đúng *cấu trúc* bộ file tháng thật nhưng không chứa bất kỳ số liệu hay tên thật nào. Quy tắc chi tiết: xem `CLAUDE.md` mục Bảo mật.
