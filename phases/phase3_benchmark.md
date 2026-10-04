# Phase 3 — Benchmark & Evaluation (11–12/10/2026)

> **Gate M3 (tối 12/10):** `app/experiments/results/summary.csv` hoàn chỉnh + 4–6 hình trong `thesis/figures/` — Chương 4 có số thật để viết.
> **Trạng thái:** ☐ chưa bắt đầu / ☐ đang làm / ☐ XONG

## Mục tiêu
Sinh ra toàn bộ bằng chứng định lượng của khóa luận. Mọi bảng/hình Chương 4 xuất tự động từ đây — không chép tay số nào.

## Việc phải làm

### A. Chạy benchmark
- [ ] Freeze: test set, model_id, temperature, seed, prompt_version, dataset_version → ghi vào `results/run_config.json`.
- [ ] `run_benchmark.py`: 3 modes × toàn bộ material cases; lưu raw outputs + verdicts (raw vào `results/raw/` — gitignored; summary commit).

### B. Metrics (`metrics.py`)
- [ ] Numeric accuracy; traceability coverage; citation precision/recall vs gold; unsupported-claim rate; abstention accuracy (trên case missing-evidence); retrieval P@5 / R@5 / MRR.
- [ ] Kiểm tay 20% mẫu unsupported-claim flags (rule-based có thể sai) — ghi lại tỷ lệ đồng thuận người-máy.
- [ ] Slice kết quả theo kịch bản (robustness table).

### C. Xuất liệu cho Chương 4
- [ ] Bảng chính: 3 modes × metrics. Hình: bar chart theo metric, slice theo kịch bản, 1 ví dụ walkthrough.
- [ ] Lưu `thesis/figures/` (PNG + script sinh hình — tái lập được).

### D. Human test (CUT-ABLE — làm nếu còn thời gian)
- [ ] 2 người × ~8 cases: verify comment CÓ vs KHÔNG CÓ provenance link — đo thời gian kiểm, lỗi bắt được, 5 câu Likert (ease of verification, trust). Phân tích mô tả, không claim thống kê.

## Writing track
- [ ] `thesis/chuong4.md`: viết phần setup thí nghiệm + đổ kết quả, diễn giải từng bảng/hình (theo `prompts/thesis_writing.md`: mỗi hình một đoạn "hình này nói gì").

## Cut line nếu trễ
Bỏ human test (ghi vào hạn chế); giảm kiểm tay còn 10%. KHÔNG cắt: benchmark 3 modes đầy đủ case, run_config đóng băng.

## Ghi chú bàn giao (điền khi xong)
- Quyết định phát sinh:
- Vấn đề để lại:
