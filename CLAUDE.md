# CLAUDE.md — Khóa luận: Glass-Box Variance Commentary System (repo: Comments_Variance)

Dự án khóa luận tốt nghiệp của người dùng (sinh viên FinTech, FP&A intern tại doanh nghiệp BĐS công nghiệp). Tách biệt hoàn toàn với công việc Dashboard ở `c:\Phu_Intern\Dashboard`. **Deadline toàn bộ: 18/10/2026.**

## Quy trình mỗi phiên

1. **Đầu phiên:** đọc `handoff.md` (trạng thái tổng + timeline + quyết định) → mở file phase đang chạy trong `phases/` → làm việc trong phạm vi phase đó.
2. **Khi code:** tuân thủ `prompts/clean_code.md`. **Khi viết luận** (file trong `thesis/`): tuân thủ `prompts/thesis_writing.md`.
3. **Cuối phiên:** tick checklist + điền "Ghi chú bàn giao" trong file phase; quyết định mới → bảng mục 4 của `handoff.md`. Không để phiên sau hỏi lại điều đã chốt.

## Ràng buộc đã chốt (không hỏi lại)

- **Trục giá trị:** verifiability/trust — "từ hộp đen đến hộp kính". TUYỆT ĐỐI không dùng luận điểm "tiết kiệm thời gian" (thực tế: quy trình có AI chỉ ~1h/tháng).
- **Kiến trúc** (`docs/architecture.md`): engine tất định tính số (LLM không tính số) + hybrid retrieval (RAG) + generation theo schema có citation + verification gates + abstention. 3 modes so sánh: M0 LLM-only / M1 vanilla RAG / M2 glass-box — cùng model, chỉ khác machinery.
- **Stack:** FastAPI + React, backend-first; React UI = provenance viewer. Dữ liệu: synthetic 5 properties (PROP-A…E), schema theo `Sample_FP&A/`.
- **Khóa luận:** 5 chương chuẩn nghiên cứu (C1 Mở đầu, C2 Cơ sở LT & tổng quan, C3 Phương pháp, C4 Kết quả & thảo luận, C5 Kết luận), DSRM, APA 7th — mọi citation phải verify trước khi chốt.
- **Cấu trúc thư mục** cố định trong `handoff.md` mục 2 — không tạo file ngoài cấu trúc, không file rác (file tạm → scratchpad hoặc `local_data/`).

## Git (BẮT BUỘC)

- Remote: https://github.com/NDPhuu/Comments_Variance.git — commit nhỏ, message `feat:/fix:/test:/docs:/data:`.
- **Trước mọi commit chạy `git status`**: thấy `Sample_FP&A/`, `local_data/`, `.env`, hay bất kỳ `.xls*` → DỪNG. Đó là dữ liệu thật của doanh nghiệp.
- Không commit `results/raw/` (output LLM thô), chỉ commit summary.

## Phong cách làm việc người dùng yêu cầu

- Brainstorm kiểu Socratic khi bàn ý tưởng: hỏi để sharpen, nêu rõ vì sao hỏi.
- Phân biệt rành mạch fact / inference / recommendation.
- Ngôn ngữ làm việc: tiếng Việt (thuật ngữ kỹ thuật giữ tiếng Anh). Văn khóa luận: đơn giản, dễ hiểu — chuẩn trong `prompts/thesis_writing.md`.

## Bảo mật (nghiêm ngặt)

- `Sample_FP&A/` chứa dữ liệu THẬT: chỉ dùng làm khuôn cấu trúc sheet/cột. Trích xuất (vd comments T1–T8) chỉ lưu `local_data/` (gitignored).
- `docs/house_style.md` và mọi file tracked: chỉ mô tả ẩn danh — không nguyên văn comment thật, không số thật, không tên công ty/khách hàng/vendor/dự án.
- Mọi thứ công bố được: schema ẩn danh, synthetic data, phương pháp, kết quả tổng hợp.
