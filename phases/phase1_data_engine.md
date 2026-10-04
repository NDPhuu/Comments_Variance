# Phase 1 — Dữ liệu & Variance Engine (04–07/10/2026)

> **Gate M1 (tối 07/10):** chạy 1 lệnh sinh ra danh sách VarianceCase JSON; đối chiếu tay ≥3 case khớp 100%; `dataset_v1` đóng băng + commit; `docs/house_style.md` chốt xong.
> **Trạng thái:** ☐ chưa bắt đầu / ☐ đang làm / ☐ XONG (cập nhật khi làm)

## Mục tiêu
Nền móng tất định: dữ liệu synthetic đóng băng được, engine tính đúng 100%, và output schema rút từ comments THẬT (T1–T8/2026).

## Việc phải làm

### A. Rút house style từ comments thật (làm TRƯỚC — quyết định mọi thứ phía sau)
- [ ] Script trích comments từ 8 file `Sample_FP&A/PL_Act vs budget_*.xlsb` (pyxlsb) → output vào `local_data/` (**gitignored — tuyệt đối không commit**).
- [ ] Phân tích: cấu trúc câu, độ dài, con số bắt buộc xuất hiện, ngôn ngữ, định dạng.
- [ ] Rút **cause taxonomy** (~8–12 loại nguyên nhân thực tế xuất hiện trong 8 tháng).
- [ ] Viết `docs/house_style.md`: mô tả schema + taxonomy ở dạng ẨN DANH (không chép nguyên văn comment thật, không số thật, không tên dự án/vendor).

### B. Synthetic data
- [ ] `app/data_synth/scenarios.yaml`: 8–10 kịch bản, **doanh thu leasing trước** (new lease sớm/trễ, early termination, dời bàn giao, escalation, FX) + vài kịch bản chi phí (one-off repair, timing, reversal) + 2 bẫy (missing evidence, trùng từ khóa sai property). Đối chiếu taxonomy ở A — kịch bản phải giống loại nguyên nhân thật.
- [ ] `generator.py`: 5 properties × 12 tháng × ~10 PL lines, GL transaction-level, budget, mapping, ~25 material cases, evidence corpus 60–100 docs + gold labels. Seed cố định.
- [ ] Freeze `dataset_v1`, commit (SQLite + evidence docs).

### C. Variance engine
- [ ] `engine/`: variance, materiality (đọc từ `config.py`), contribution, txn drill-down → VarianceCase JSON (contract trong `docs/architecture.md` §3).
- [ ] pytest: tay tính 3–5 case làm expected values; test edge: budget=0, actual âm.

## Writing track (song song, không chờ code)
- [ ] `thesis/chuong1.md` draft — lấy từ `objectives.md` (câu chuyện 5 đoạn + pitch), viết theo `prompts/thesis_writing.md`.
- [ ] `thesis/chuong3.md` outline (DSRM mapping + thiết kế dữ liệu + thiết kế đánh giá).

## Cut line nếu trễ
Giảm kịch bản còn 6, corpus còn 40 docs. KHÔNG cắt: tests engine, gold labels, house_style.md.

## Ghi chú bàn giao (điền khi xong)
- Quyết định phát sinh:
- Vấn đề để lại cho phase sau:
