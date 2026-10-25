# Phase 3 — Đánh giá thực nghiệm (11–12/10/2026)

> **Gate M3 (tối 12/10):** `results/summary.csv` + 4–6 hình cho C4; ngưỡng thành công đã đăng ký trước KHI chạy final run.
> **Trạng thái:** ☐ chưa bắt đầu / ☐ đang làm / ☐ XONG

## Mục tiêu
Sinh toàn bộ bằng chứng định lượng của Chương 4 — bằng **metric học thuật có nguồn trích dẫn** và một quy trình chấm **khách quan, kiểm chứng được**. Không có metric tự chế.

## A. Nguyên tắc khách quan (đọc trước khi làm bất kỳ việc gì)

1. **Đề thi và đáp án đóng băng TRƯỚC khi bất kỳ chế độ nào chạy.** Dataset + gold labels commit lên git trước final run — commit hash là bằng chứng thời gian, không sửa đáp án sau khi thấy kết quả.
2. **Script chấm KHÔNG sinh đề và KHÔNG chấm cảm tính.** Nó chỉ so khớp cơ học với đáp án có sẵn (số khớp/không, citation id có trong gold set không, câu có evidence đính kèm không) — vai trò giống thầy chấm trắc nghiệm bằng đáp án, không phải giám khảo tự nghĩ ra điểm. KHÔNG dùng LLM làm giám khảo chính (LLM-as-judge chỉ là số liệu phụ, nếu dùng phải nêu caveat theo Zheng et al., 2023).
3. **Ngưỡng thành công đăng ký trước (pre-registered):** ghi vào mục D dưới đây và chốt với GVHD TRƯỚC final run — tránh "thấy kết quả rồi mới đặt ngưỡng".
4. **Tái lập được:** seed, `run_config.json` (model, temperature, prompt_version, dataset_version), code công khai — người khác có thể chạy lại.

## B. Metric — tất cả theo chuẩn đã công bố (bảng mapping đầy đủ ở `docs/02_khung_khoaluan_APA7.md` §3.5)

| Đo cái gì | Metric học thuật | Nguồn |
|---|---|---|
| Số trong comment khớp sổ | **Numerical exact match (EM)** | FinQA; TAT-QA |
| Trích dẫn đúng tài liệu gold | **Citation precision / recall** | ALCE (Gao, Yen, et al., 2023) |
| Câu nguyên nhân có căn cứ | **Attribution (AIS)** / atomic-fact precision | Rashkin et al. (2023); FActScore |
| Tìm đúng tài liệu | **Precision@5, Recall@5, MRR** | IR chuẩn (Manning et al., 2008) |
| Từ chối đúng lúc trên case không trả lời được | **Answerability / selective prediction accuracy** | SQuAD 2.0; Kamath et al. (2020) |
| (Phụ, nếu kịp) faithfulness qua thư viện bên thứ ba | **RAGAS** | Es et al. (2024) — nêu caveat LLM-judge |

**Cách báo cáo kết quả — theo đúng convention của các bài RAG/NLP (ALCE, FinQA, RAGAS):** bảng metric theo từng chế độ; mỗi case × mỗi mode chạy **k = 3 lần** (temperature cố định) và báo **mean ± độ lệch chuẩn** để thể hiện độ dao động của LLM; kèm bảng slice theo kịch bản. **KHÔNG dùng kiểm định kinh tế lượng** (bootstrap CI / Wilcoxon / McNemar — đã bỏ theo quyết định của người thực hiện 04/10: đánh giá theo chuẩn mực của literature RAG, không phải chuẩn đề tài kinh tế lượng).

## C. Việc phải làm

- [ ] Freeze test set + gold labels → commit (ghi lại hash vào run_config).
- [ ] Viết `metrics.py` đúng định nghĩa các metric ở B (mỗi hàm ghi docstring kèm citation).
- [ ] Chạy batch 3 chế độ × toàn bộ case; lưu raw (`results/raw/` — gitignored) + summary (commit).
- [ ] Slice kết quả theo kịch bản (robustness) + xuất bảng/hình vào `thesis/figures/` (script sinh, không chép tay).

## D. Ngưỡng thành công đăng ký trước (đề xuất — CHỐT VỚI GVHD trước final run)

- M2: numerical EM ≥ 98%; citation precision ≥ 90%; tỷ lệ câu không căn cứ ≤ 5%; từ chối đúng ≥ 4/5 case bẫy.
- Thứ tự kỳ vọng M2 > M1 > M0 trên các chỉ số chính; nếu không đạt, báo cáo trung thực và phân tích vì sao — kết quả âm vẫn là kết quả.

## Cut line nếu trễ
Bỏ RAGAS phụ. KHÔNG cắt: đóng băng đáp án trước và công bố ngưỡng đánh giá trước khi chạy.

## Ghi chú bàn giao (điền khi xong)
- Ngưỡng đã chốt với GVHD ngày:
- Quyết định phát sinh: · Vấn đề để lại:
