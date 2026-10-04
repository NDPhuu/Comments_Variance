# Handoff TỔNG — Khóa luận: Glass-Box Variance Commentary System

> **Cập nhật:** 2026-10-04 · **Deadline toàn bộ (code + deploy + 5 chương): 18/10/2026**
> **Trạng thái:** Kiến trúc + kế hoạch 5 phase đã chốt. Đang ở **Phase 1** (`phases/phase1_data_engine.md`).
> **Repo:** https://github.com/NDPhuu/Comments_Variance.git
> **Phiên mới:** đọc `CLAUDE.md` → file này → file phase đang mở.

---

## 1. Đề tài (tóm tắt 3 dòng)

Hệ thống "hộp kính" sinh giải trình chênh lệch Budget–Actual cho FP&A: engine tất định tính số, RAG truy bằng chứng, comment sinh theo schema có citation, cổng kiểm chứng + abstention, web UI provenance. Trục giá trị: **verifiability/trust — KHÔNG phải tiết kiệm thời gian**. Câu chuyện đầy đủ: `objectives.md`. Kiến trúc: `docs/architecture.md`.

## 2. Cấu trúc thư mục (CỐ ĐỊNH — không tạo file ngoài cấu trúc này)

```
KhoaLuan/  (= repo Comments_Variance)
├── CLAUDE.md                  # bootstrap phiên Claude
├── handoff.md                 # file này — trạng thái tổng + timeline
├── objectives.md              # câu chuyện đề tài v2 (nguồn cho Chương 1)
├── docs/
│   ├── architecture.md        # kiến trúc hệ thống + data contracts
│   ├── house_style.md         # (Phase 1 tạo) output schema + cause taxonomy, ẨN DANH
│   ├── demo_script.md         # (Phase 4 tạo) kịch bản demo 2 phút
│   └── 02_khung_khoaluan_APA7.md  # khung chương + APA refs (còn nợ: sửa 6→5 chương)
├── phases/                    # handoff riêng từng phase (trạng thái + checklist + bàn giao)
│   ├── phase1_data_engine.md      04–07/10
│   ├── phase2_rag_generation.md   08–10/10
│   ├── phase3_benchmark.md        11–12/10
│   ├── phase4_webapp_deploy.md    13–15/10
│   └── phase5_thesis.md           15–18/10
├── prompts/
│   ├── clean_code.md          # chuẩn code — mọi phiên code phải theo
│   └── thesis_writing.md      # chuẩn viết luận — mọi phiên viết phải theo
├── app/                       # (Phase 1 tạo) backend/ · data_synth/ · experiments/ · frontend/
├── thesis/                    # chuong1..5.md + figures/
├── _archive/                  # draft_v0, socratic round 1 — xong vai trò, giữ tham khảo
├── local_data/                # (gitignored) MỌI trích xuất từ dữ liệu thật
└── Sample_FP&A/               # (gitignored) dữ liệu THẬT — chỉ làm khuôn schema
```

## 3. Timeline 14 ngày — mốc nào phải xong gì

| Mốc | Hạn | Build phải xong | Viết phải xong |
|---|---|---|---|
| **M1** | tối 07/10 | House style + taxonomy từ comments thật T1–T8; synthetic dataset_v1 đóng băng; variance engine + tests khớp tay tính | C1 draft; C3 outline |
| **M2** | tối 10/10 | Hybrid retrieval; generation 3 modes đúng schema; verification gates bắt 100% lỗi gieo | C2 draft; C3 đầy đủ |
| **M3** | tối 12/10 | Benchmark 3 modes toàn bộ cases; `summary.csv` + 4–6 hình cho C4 | C4 có số thật |
| **M4** | tối 15/10 | Web app 3 màn hình + deploy public + demo script | C4 hoàn chỉnh; C5 draft |
| **M5** | **18/10** | Repo tag `v1.0` + link web sống | PDF toàn văn + citations verified + slide |

**Cut lines toàn cục (cắt theo thứ tự khi trễ):** human test (P3) → side-by-side UI (P4) → dense embeddings (P2, giữ BM25+metadata) → deploy public (thay bằng local + video). **KHÔNG BAO GIỜ cắt:** engine tests, verification gates, benchmark 3 modes, 2 lượt rà toàn văn.

## 4. Quyết định đã chốt (mới nhất trên cùng)

| # | Quyết định | Ngày |
|---|---|---|
| 16 | **Scope: TOÀN BỘ P&L Act vs Budget** (line × property × tháng), trọng tâm kịch bản **leasing revenue** (contract events); chi phí R&M/SG&A vẫn trong scope — KHÔNG phải OPEX-only. Mock đã đổi ví dụ chính sang leasing revenue | 04/10 |
| 15 | Mock UI đã publish: https://claude.ai/artifact/Vfzk4DSJLFJUDfzSocfCH9 (nguồn: `docs/ui_mockup.html`) — tham chiếu thiết kế cho Phase 4 | 04/10 |
| 14 | Embeddings: **BGE-M3** chạy local (FlagEmbedding), KHÔNG dùng API trả phí; embed corpus + evidence pack per case PRECOMPUTE offline → runtime web không load model (Render free tier). LLM generation vẫn là Anthropic API | 04/10 |
| 13 | Quản lý thư viện backend bằng **Poetry** (máy đã có v2.4.1); commit `poetry.lock` | 04/10 |
| 12 | Quản lý mã nguồn GitHub (`NDPhuu/Comments_Variance`); `.gitignore` chặn `Sample_FP&A/`, `local_data/`, mọi `.xls*`, `.env` | 04/10 |
| 11 | Deadline 18/10/2026 cho TOÀN BỘ (deploy + 5 chương); user có kinh nghiệm RAG + deploy → giữ stack FastAPI+React | 04/10 |
| 10 | Cấu trúc 5 phase + handoff riêng từng phase; 2 prompt chuẩn (clean code, thesis writing) | 04/10 |
| 9 | Comments thật T1–T8/2026 (trong 8 file `PL_Act vs budget_*.xlsb`) = nguồn house style + cause taxonomy; trích xuất chỉ lưu `local_data/` | 04/10 |
| 8 | Câu chuyện v2: verifiability/trust ("hộp đen → hộp kính"), KHÔNG claim tiết kiệm thời gian | 04/10 |
| 7 | Khung 5 chương chuẩn nghiên cứu; phương pháp DSRM; APA 7th | 04/10 |
| 6 | RAG = module + trục so sánh (M0 LLM-only / M1 vanilla RAG / M2 glass-box) | 04/10 |
| 5 | Mock data 5 properties × 12 tháng, schema theo `Sample_FP&A/` | 04/10 |
| 4 | FastAPI + React, backend-first; UI = provenance viewer | 04/10 |
| 1–3 | (xem lịch sử: tách khỏi Dashboard; bỏ draft_v0; chuyển workspace riêng) | 03–04/10 |

## 5. Việc user cần làm / xác nhận NGAY

1. ⚠️ **LLM API cho generation** (embeddings đã chốt BGE-M3 local, không tốn phí): cần Anthropic API key + budget cho benchmark (~25 cases × 3 modes × vài lần chạy — ước lượng nhỏ, vài USD). Model đề xuất: 1 model thống nhất (`claude-sonnet-5-5`).
2. ⚠️ Xác nhận 18/10 là hạn **toàn văn nộp** hay còn buffer sau đó (ảnh hưởng cut lines).
3. Deploy: Render + Vercel ổn không, hay bạn có hạ tầng quen tay khác?
4. (Khi rảnh) 1 anecdote AI-comment-sai cụ thể cho mở đầu Chương 1.

## 6. Nợ tồn đọng (không chặn Phase 1)

- `docs/02_khung_khoaluan_APA7.md`: sửa khung 6 chương → 5 chương + thêm 3 refs trust (cuối `objectives.md`). Làm trong Phase 2 writing track.
- `_archive/01_socratic_round1.md`: không cập nhật nữa — câu chưa trả lời đã được chuyển vào mục 5 ở trên.

## 7. Bảo mật (đọc mỗi lần định commit)

- `Sample_FP&A/` và `local_data/` là dữ liệu THẬT: gitignored, không bao giờ commit, không copy nội dung vào bất kỳ file tracked nào.
- `docs/house_style.md` chỉ chứa mô tả ẩn danh (cấu trúc, taxonomy) — không chép nguyên văn comment thật.
- Trước mọi commit: `git status` soát `.xls*`, `.env`, `local_data`.
