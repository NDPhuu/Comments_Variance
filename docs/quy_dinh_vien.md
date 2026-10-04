# Quy định của Viện ĐMST (UEH) — tóm tắt từ `materials/` (nguồn chuẩn khi mâu thuẫn)

> Nguồn: `UII - HUONG DAN VIET KHOA LUAN TOT NGHIEP.docx`, `Mau08.MauDanhGiaKLTN-GV.docx`. Đã chốt: viết **tiếng Việt** (không cần mẫu GĐK tiếng Anh).

## 1. Kết cấu bắt buộc (khớp khung 5 chương đã chốt)

Tóm tắt (Abstract) + từ khóa (≤5) → **1. Giới thiệu** → **2. Tổng quan các kết quả nghiên cứu trước đây** → **3. Phương pháp nghiên cứu (Methodology and data)** → **4. Nội dung và các kết quả nghiên cứu** → **5. Kết luận** → Tài liệu tham khảo → Phụ lục.
Trang phụ trợ theo thứ tự: bìa chính (có SĐT, email SV) · bìa phụ · lời cảm ơn · xác nhận đơn vị thực tập (khuyến khích) · nhận xét GVHD · mục lục (≤2 trang) · danh mục từ viết tắt · danh mục bảng · danh mục hình.

## 2. Định dạng

- A4 · **Times New Roman, Unicode** · body 12–13, justify · line spacing 1,5 · spacing before/after 6pt.
- Lề: top 1–1,5cm; bottom/left/right 2–2,5cm. Số trang: cuối trang, canh phải (trang phụ trợ đánh i, ii…; nội dung đánh 1, 2…).
- Heading: C1 cỡ 16 HOA đậm giữa · 1.1 cỡ 14 đậm trái · 1.1.1 cỡ 12–13 nghiêng trái · tối đa 4 cấp, số Ả Rập.
- **Nội dung ~50 trang** (linh hoạt theo GVHD).
- Bảng/hình: đánh số theo chương (Bảng 2.1), **bắt buộc có tên (trên, đậm) + ĐVT + Nguồn (dưới, nghiêng, phải)**; số canh phải, cùng số thập phân; **phân cách nghìn bằng dấu chấm, thập phân bằng dấu phẩy (1.007.845,25)**; không để bảng vắt 2 trang.

## 3. Trích dẫn: chuẩn HARVARD của Viện (KHÔNG phải APA 7th — thay quyết định cũ)

**In-text:** `(Nguyễn Văn A, 2009)` hoặc `Nguyễn Văn A (2009) cho rằng…`; trích nguyên văn thêm trang `(…, 2009, tr.19)`.
**Tác giả:** 2–3 tác giả ghi đủ; **≥4 tác giả: tác giả đầu + "cộng sự"** (không dùng "et al." trong bản tiếng Việt).
**Danh mục cuối bài:** xếp ABC theo họ, KHÔNG đánh số. Mẫu:
- Sách: `Họ tên (năm), Tên sách, NXB, nơi XB.`
- Bài tạp chí: `Họ tên (năm), "Tên bài", Tên tạp chí, số X, tr. Y–Z.`
- Ấn phẩm điện tử: `Họ tên (năm), Tên tài liệu, tổ chức XB, truy cập ngày … , <link>.`
- Kỷ yếu hội thảo: `Họ tên (năm), 'tên bài', tên kỷ yếu, NXB, nơi XB, tr. Y–Z.`
→ Kho nguồn trong `docs/02_khung_khoaluan_APA7.md` giữ nguyên làm danh mục tra cứu; khi đưa vào luận phải **reformat sang mẫu Harvard trên**.
**Đạo văn = 0 điểm.** Mọi số liệu phải có nguồn.

## 4. Rubric GVHD (thang 10) — và cách đề tài ăn điểm từng mục

| Tiêu chí (điểm) | Đề tài đáp ứng bằng |
|---|---|
| Mục tiêu, đề cương đúng hạn (1) | objectives.md + kế hoạch 5 phase; liên hệ GVHD đều đặn (⚠ không liên hệ = GVHD có quyền từ chối → 0 điểm) |
| Tính mới, độ khó cao (1,5) | Hệ thống verifiable AI + benchmark gold-label đầu tiên cho variance commentary; khớp chủ đề gợi ý "ứng dụng công nghệ mới (AI) — case study doanh nghiệp" |
| Khung lý thuyết + bằng chứng thực nghiệm (1,5) | 3 dòng literature (FP&A · LLM/RAG/grounding · DSR/TTF/trust) + gap statement |
| Số liệu mẫu đủ lớn, tin cậy (1) | 34 case × 3 chế độ × **k lần chạy lặp** (xem phase 3); dataset đóng băng, seed, tái lập |
| **Mô hình NC + kiểm định thống kê phù hợp (2)** | DSRM làm khung; metric học thuật; **bootstrap CI + kiểm định ghép cặp (Wilcoxon/McNemar) khi so M0/M1/M2; Cohen's κ máy–người** |
| Phân tích gắn giả thuyết (2) | Giả thuyết H1–H3 phát biểu trước (C1/C3), C4 đối chiếu từng giả thuyết |
| Văn phong + bảng biểu (1) | prompts/thesis_writing.md + quy định bảng/hình mục 2 |

## 5. Quy trình với GVHD

Bước bắt buộc theo hướng dẫn: đề cương sơ bộ → GVHD duyệt → bản thảo 1 → sửa → bản thảo 2 → nộp (kèm xác nhận đơn vị thực tập — khuyến khích). *Người thực hiện đã chọn bỏ qua bước đề cương riêng và viết draft trực tiếp (quyết định 04/10) — lưu ý rủi ro: nếu GVHD yêu cầu đề cương, trích từ objectives.md + C1 ra là có ngay.*
