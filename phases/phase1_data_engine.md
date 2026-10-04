# Phase 1 — Dữ liệu & Variance Engine (04–07/10/2026)

> **Gate M1 (tối 07/10):** chạy 1 lệnh sinh ra danh sách VarianceCase JSON; đối chiếu tay ≥3 case khớp 100%; `dataset_v1` đóng băng + commit; `docs/house_style.md` chốt xong.
> **Trạng thái:** ☑ BUILD XONG 04/10 (sớm 3 ngày — gate M1 đạt: 34 case = 34 gold, khớp 100%, 0 noise; 5/5 test tay tính pass). Còn lại: writing track (C1 draft, C3 outline).
> **Lệnh chạy:** `cd app/backend && poetry run python -m vwb.data_synth.generate` · `poetry run pytest`

## Mục tiêu
Nền móng tất định: dữ liệu synthetic đóng băng được, engine tính đúng 100%, và output schema rút từ comments THẬT (T1–T8/2026).

## Việc phải làm

### A. Rút house style từ comments thật ✅ XONG 04/10
- [x] `app/tools/extract_comments.py` → 17 comments từ cột "Key Commentary" (sheet Output) → `local_data/comments_PL.csv` (không commit).
- [x] Phân tích: bullet điện tín $Xm/$Xk, "Partly offset by", forward note, carry-forward qua tháng.
- [x] Taxonomy thật: timing_difference (nhiều nhất) > one_off_event > financing_event > accounting_treatment > rate_change (+nhóm leasing).
- [x] `docs/house_style.md` đã chốt (ẩn danh 100%).

### B. Synthetic data ✅ XONG 04/10
- [x] `app/backend/vwb/data_synth/scenarios.yaml`: 12 kịch bản khớp taxonomy thật (doanh thu trước, timing nhiều nhất, 2 bẫy).
- [x] `generate.py`: 5 properties × 12 tháng, 60 tenants, 1,865 dòng GL, 55 evidence docs, **34 material cases + gold labels**, seed 26 idempotent.
- [x] `dataset_v1` đóng băng tại `app/backend/data/dataset_v1/` (CSV + JSON — chuyển SQLite khi cần ở Phase 4), commit.

### C. Variance engine ✅ XONG 04/10
- [x] `vwb/engine/core.py`: variance, materiality (từ `config.py`), revenue contributors theo tenant, txn drill-down, build_cases → đúng contract architecture §3.
- [x] pytest 5/5 pass: 4 test tay tính (gồm budget=0, favorable-cost) + 1 integration test (generator → engine khớp gold 100%).

## Writing track (song song, không chờ code)
- [ ] `thesis/chuong1.md` draft — lấy từ `objectives.md` (câu chuyện 5 đoạn + pitch), viết theo `prompts/thesis_writing.md`.
- [ ] `thesis/chuong3.md` outline (DSRM mapping + thiết kế dữ liệu + thiết kế đánh giá).

## Cut line nếu trễ
Giảm kịch bản còn 6, corpus còn 40 docs. KHÔNG cắt: tests engine, gold labels, house_style.md.

## Ghi chú bàn giao (điền khi xong)
- Quyết định phát sinh:
- Vấn đề để lại cho phase sau:
