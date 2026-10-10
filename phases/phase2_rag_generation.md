# Phase 2 — RAG + Generation + Verification (08–10/10/2026)

> **Gate M2 (tối 10/10):** cả 3 modes chạy batch không vỡ schema; verifier bắt được 100% lỗi gieo cố ý trong bộ test nhỏ (~10 câu lỗi nhân tạo: số sai, citation ma, claim không evidence).
> **Trạng thái:** ☑ CODE XONG 10/10 — 18/18 tests pass; verifier bắt đủ bộ lỗi gieo (số sai/sai dấu/sai scale/citation ma/sai khu/sau kỳ/claim trống/abstain-vi-phạm/%sai); retrieval gold-in-top5 đạt; **abstention đổi sang rule LINKAGE** (ngưỡng BM25 thô thất bại khi đo — xem `docs/paper_notes.md` ghi chú 10/10). Còn lại: precompute packs (đang chạy nền) + lượt gọi Gemini thật (chờ `GEMINI_API_KEY`). Writing track (C2 draft, C3 đầy đủ) chưa làm.

## Mục tiêu
Pipeline sinh–kiểm hoàn chỉnh: evidence retrieval hybrid, generation theo schema, verification gates + abstention. Đây là lõi kỹ thuật của khóa luận.

## Việc phải làm

### A. Retrieval (module RAG)
- [ ] Index corpus: metadata filter (property, period, doc type) + BM25 + dense embeddings → fusion top-k, trả `retrieval_score`.
- [ ] Sanity check: với 5 case bất kỳ, gold evidence nằm trong top-5 — nếu không, chỉnh chunking/metadata trước khi đi tiếp.

### B. Generation
- [ ] Context package builder (engine facts + evidence pack + taxonomy + house-style schema).
- [ ] 3 prompt templates versioned (`prompts_llm/m0.txt`, `m1.txt`, `m2.txt`) — đúng định nghĩa modes trong `docs/architecture.md` §2. Cùng model, cùng temperature.
- [ ] Structured output parse + retry; log mọi call (model_id, prompt_version, tokens).

### C. Verification gates (tất định — có pytest)
- [ ] Numeric gate: bóc mọi số trong comment, đối chiếu VarianceCase.
- [ ] Citation gate: evidence_id tồn tại + quote match.
- [ ] Unsupported-claim flag; abstention rule (missing-evidence case phải ra `abstained`).
- [ ] Test bằng bộ lỗi gieo cố ý (fixtures) — đây chính là tiêu chí gate M2.

### D. Walkthrough
- [ ] 1 case chạy end-to-end cả 3 modes, lưu output làm ví dụ minh họa Chương 4.

## Writing track
- [ ] `thesis/chuong2.md` draft — 3 dòng literature (domain FP&A / LLM-grounding / trust & XAI) theo `docs/02_khung_khoaluan_APA7.md`; kết chương bằng gap statement.
- [ ] `thesis/chuong3.md` hoàn thiện phần thiết kế hệ thống (lấy từ `docs/architecture.md`).

## Cut line nếu trễ
Bỏ dense embeddings, giữ BM25 + metadata (vẫn là "hybrid" ở mức filter+lexical — ghi rõ hạn chế). KHÔNG cắt: verification gates, 3 modes, abstention.

## Ghi chú bàn giao (điền khi xong)
- Quyết định phát sinh:
- Vấn đề để lại:
