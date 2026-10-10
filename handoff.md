# Handoff TỔNG — Khóa luận: Glass-Box Variance Commentary System

> **Cập nhật:** 2026-10-04 · **Deadline toàn bộ (code + deploy + 5 chương): 18/10/2026**
> **Trạng thái:** **Phase 1 BUILD XONG 04/10 (sớm 3 ngày)** — house style rút từ 17 comments thật; dataset_v1 đóng băng (34 case = 34 gold, khớp 100%); engine + 5/5 tests pass. Còn nợ Phase 1: writing track (C1 draft, C3 outline). Kế tiếp: **Phase 2** (`phases/phase2_rag_generation.md`).
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
│   ├── ui_mockup.html         # mock app theo luồng demo giảng viên (artifact Vfzk…)
│   ├── phases_mockup.html     # mock sản phẩm từng phase (artifact M1Zr…)
│   └── 02_khung_khoaluan_APA7.md  # khung chương + APA refs (còn nợ: sửa 6→5 chương)
├── design.md                  # style guide (palette BW pitchbook) — nguồn thiết kế web
├── README.md                  # cửa ngõ repo: vấn đề/giải pháp + bảng thuật ngữ
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
| 30 | **Phase 2 code xong 10/10** (18/18 tests): retrieval metadata+BM25+BGE-M3/RRF, 3 prompt templates, verification gates (giữ dấu+scale theo TAT-QA, khớp theo trường engine theo FinQA). **Abstention = rule LINKAGE tất định** (doc phải nhắc mã contributor/dòng P&L/≥2 từ memo) — thay ngưỡng BM25 thô vì đo được là không tách nổi bẫy/thật; = bản tất định của CRAG retrieval-evaluator. Thêm ref Wen và cộng sự 2025 (TACL, abstention survey); "abstention accuracy" phải định nghĩa tường minh trong C3. Benchmark thật chờ `GEMINI_API_KEY` | 10/10 |
| 29 | **KHUNG C3/C4 CHỐT (07/10, theo người thực hiện):** C3 = 3.1 Dữ liệu · 3.2 Mô hình & Kiến trúc · 3.3 Cơ chế đánh giá · 3.4 Thiết lập; C4 = 4.1 Kết quả chính · 4.2 Kiểm định tính vững (các kịch bản lỗi) · 4.3 Thảo luận. Bỏ mục "quy trình 4 bước" và "khảo sát hiện trạng" riêng — khảo sát 17 giải trình nằm trong 3.1; thống kê dataset ở 3.1; κ định nghĩa 3.3, giá trị báo 4.2; walkthrough trong 4.1. Chi tiết: `docs/02` bảng khung chương | 07/10 |
| 28 | **Xuất Word**: `thesis/chuong1.docx` tạo bằng `app/tools/export_docx.js` (format Viện: TNR, H1 16/H2 14, body 13 justify 1,5, lề chuẩn, số trang, Hình 1.1 PNG từ `gen_hinh_1_1.py`). ⚠ TÁC GIẢ SỬA TRỰC TIẾP TRÊN .DOCX → từ nay bản .docx là source of truth của C1; phiên sau muốn sửa C1 phải đọc .docx (pandoc/python-docx), KHÔNG ghi đè từ chuong1.md. Lưu ý: chuong1.md trên đĩa từng bị buffer cũ ghi đè về draft 1 — đã khôi phục draft 2 từ git | 04/10 |
| 27 | **Chương 1 draft 2**: văn phong formal; mở đầu kết hợp ngành BĐS KCN + làn sóng GenAI với **nguồn sơ cấp CBRE Figures Q2/2026** (2 PDF trong `materials/` — bản quyền, đã gitignore `materials/*.pdf`) + Gartner 2025; Hình 1.1 (mermaid, điểm đứt gãy kiểm chứng); 7 nguồn đã verify (docs/02 §3.7–3.8). Còn ⟦anecdote⟧ chờ tác giả | 04/10 |
| 26 | **BỎ DSRM/TTF hoàn toàn** — khóa luận định vị là **NGHIÊN CỨU ỨNG DỤNG** (giải quyết vấn đề doanh nghiệp bằng kiến thức RAG/NLP học ở trường); phương pháp C3 = quy trình 4 bước: khảo sát vấn đề → xác định yêu cầu → thiết kế & xây dựng → đánh giá thực nghiệm. Đã gỡ refs DSR/TTF/TAM khỏi kho nguồn; KHÔNG đề xuất lại | 04/10 |
| 25 | Đánh giá theo **convention của literature RAG/NLP**: bảng metric + mean ± SD trên k=3 lần chạy + Cohen's κ cho máy chấm. **BỎ kiểm định kinh tế lượng** (bootstrap/Wilcoxon/McNemar) — không thuộc chuẩn mực dòng bài này; xác nhận cách hiểu tiêu chí rubric với GVHD | 04/10 |
| 24 | **Chương 1 draft 1 đã viết** (`thesis/chuong1.md`, tiếng Việt, Harvard, có H1–H3) — còn 1 chỗ ⟦chờ anecdote⟧. Người thực hiện chọn BỎ QUA bước đề cương sơ bộ riêng (rủi ro ghi tại `docs/quy_dinh_vien.md` §5) | 04/10 |
| 23 | **Ngôn ngữ khóa luận: TIẾNG VIỆT** (không cần mẫu GĐK tiếng Anh). Quy định Viện tóm tắt tại `docs/quy_dinh_vien.md`: kết cấu 5 phần (khớp khung đã chốt), ~50 trang, TNR 12–13 giãn 1,5, bảng/hình có tên+ĐVT+nguồn, số kiểu VN. Rubric có mục "kiểm định thống kê 2đ" → phase 3 thêm bootstrap CI + Wilcoxon/McNemar + k=3 lần chạy/case | 04/10 |
| 22 | **Trích dẫn trong bản nộp = HARVARD theo Viện, KHÔNG phải APA 7th** (thay quyết định cũ): ≥4 tác giả dùng "cộng sự"; mẫu danh mục theo `docs/quy_dinh_vien.md` §3. Kho nguồn `docs/02_…` giữ APA để tra cứu/verify, reformat khi đưa vào luận | 04/10 |
| 21 | Demo = **engine sống**, không phải slide: app không chứa hộp giải thích; demo có hành động thật (quét P&L, generate gọi LLM thật, chỉnh ngưỡng materiality → queue đổi ngay, panel JSON thô); giảng viên chọn case bất kỳ. Mock chỉ là wireframe bố cục | 04/10 |
| 20 | Đánh giá dùng **metric học thuật có trích dẫn** (EM — FinQA/TAT-QA; citation P/R — ALCE; attribution — AIS/FActScore; P@k/MRR — IR chuẩn; abstention — SQuAD 2.0/selective prediction; Cohen's κ cho máy chấm) + quy trình khách quan: đáp án đóng băng trước, chấm mù, κ ≥ 0.7, ngưỡng đăng ký trước, 5 held-out case do người khác gieo. Chi tiết: `phases/phase3_benchmark.md` | 04/10 |
| 19 | Style web theo `design.md` (palette navy/cyan pitchbook, Be Vietnam Pro + Inter, không emoji/gradient) — KHÔNG gắn logo/tên công ty để giữ ẩn danh. 2 mock đã publish: app demo flow https://claude.ai/artifact/Vfzk4DSJLFJUDfzSocfCH9 · mock 5 phase https://claude.ai/artifact/M1ZrjDzkvKkwgq1mwLdngH | 04/10 |
| 18 | Chống buzzword: `README.md` là cửa ngõ repo (vấn đề/giải pháp tiếng Việt thường + bảng thuật ngữ); mọi tài liệu mới: thuật ngữ xuất hiện lần đầu phải kèm giải thích một dòng | 04/10 |
| 17 | LLM generation: **Gemini API (Google AI Studio, free tier)** qua wrapper trung lập provider (đổi model chỉ sửa config); model thống nhất cho cả 3 modes (đề xuất `gemini-2.5-flash`); CHỈ gửi dữ liệu synthetic lên API | 04/10 |
| 16 | **Scope: TOÀN BỘ P&L Act vs Budget** (line × property × tháng), trọng tâm kịch bản **leasing revenue** (contract events); chi phí R&M/SG&A vẫn trong scope — KHÔNG phải OPEX-only. Mock đã đổi ví dụ chính sang leasing revenue | 04/10 |
| 15 | Mock UI đã publish: https://claude.ai/artifact/Vfzk4DSJLFJUDfzSocfCH9 (nguồn: `docs/ui_mockup.html`) — tham chiếu thiết kế cho Phase 4 | 04/10 |
| 14 | Embeddings: **BGE-M3** chạy local (FlagEmbedding), KHÔNG dùng API trả phí; embed corpus + evidence pack per case PRECOMPUTE offline → runtime web không load model (Render free tier). LLM generation qua API ngoài — xem #17 | 04/10 |
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

1. ✅ ĐÃ CHỐT Gemini free tier (quyết định #17). Việc còn lại phía bạn: tạo API key tại Google AI Studio → đặt vào file `.env` trên máy (`GEMINI_API_KEY=...`) — file này đã bị gitignore, KHÔNG commit.
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
