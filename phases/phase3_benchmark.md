# Phase 3 — Đánh giá thực nghiệm (11–12/10/2026)

> **Gate M3 (tối 12/10):** `results/summary.csv` + 4–6 hình cho C4; Cohen's κ máy–người ≥ 0.7 trên mẫu kiểm tay; ngưỡng thành công đã đăng ký trước KHI chạy final run.
> **Trạng thái:** ☐ chưa bắt đầu / ☐ đang làm / ☐ XONG

## Mục tiêu
Sinh toàn bộ bằng chứng định lượng của Chương 4 — bằng **metric học thuật có nguồn trích dẫn** và một quy trình chấm **khách quan, kiểm chứng được**. Không có metric tự chế.

## A. Nguyên tắc khách quan (đọc trước khi làm bất kỳ việc gì)

1. **Đề thi và đáp án đóng băng TRƯỚC khi bất kỳ chế độ nào chạy.** Dataset + gold labels commit lên git trước final run — commit hash là bằng chứng thời gian, không sửa đáp án sau khi thấy kết quả.
2. **Script chấm KHÔNG sinh đề và KHÔNG chấm cảm tính.** Nó chỉ so khớp cơ học với đáp án có sẵn (số khớp/không, citation id có trong gold set không, câu có evidence đính kèm không) — vai trò giống thầy chấm trắc nghiệm bằng đáp án, không phải giám khảo tự nghĩ ra điểm. KHÔNG dùng LLM làm giám khảo chính (LLM-as-judge chỉ là số liệu phụ, nếu dùng phải nêu caveat theo Zheng et al., 2023).
3. **Máy chấm phải được người kiểm chứng:** 2 người chấm tay độc lập 20–30% mẫu (mục "câu có căn cứ" là chỗ máy dễ sai nhất) → tính **Cohen's κ** giữa máy và người; κ ≥ 0.7 mới được dùng máy chấm cho phần còn lại, ngược lại phải sửa rule chấm và làm lại.
4. **Chấm mù (blind):** với đánh giá chất lượng tổng thể, xáo trộn output 3 chế độ, che nhãn, nhờ 2–3 người làm FP&A chấm theo rubric cố định (số đúng? có căn cứ? dùng được ngay?). Người chấm không biết output nào của chế độ nào.
5. **Ngưỡng thành công đăng ký trước (pre-registered):** ghi vào mục D dưới đây và chốt với GVHD TRƯỚC final run — tránh "thấy kết quả rồi mới đặt ngưỡng".
6. **Held-out set do người khác gieo:** nhờ GVHD hoặc 1 analyst chọn tham số 5 case bí mật (mình không biết đáp án trước khi chạy) — chống thiên vị "người ra đề tự đi thi".
7. **Tái lập được:** seed, `run_config.json` (model, temperature, prompt_version, dataset_version), code công khai — người khác chạy lại ra đúng số.

## B. Metric — tất cả theo chuẩn đã công bố (bảng mapping đầy đủ ở `docs/02_khung_khoaluan_APA7.md` §3.5)

| Đo cái gì | Metric học thuật | Nguồn |
|---|---|---|
| Số trong comment khớp sổ | **Numerical exact match (EM)** | FinQA; TAT-QA |
| Trích dẫn đúng tài liệu gold | **Citation precision / recall** | ALCE (Gao, Yen, et al., 2023) |
| Câu nguyên nhân có căn cứ | **Attribution (AIS)** / atomic-fact precision | Rashkin et al. (2023); FActScore |
| Tìm đúng tài liệu | **Precision@5, Recall@5, MRR** | IR chuẩn (Manning et al., 2008) |
| Từ chối đúng lúc trên case không trả lời được | **Answerability / selective prediction accuracy** | SQuAD 2.0; Kamath et al. (2020) |
| Máy chấm đáng tin không | **Cohen's κ** máy vs. người | Cohen (1960) |
| (Phụ, nếu kịp) faithfulness qua thư viện bên thứ ba | **RAGAS** | Es et al. (2024) — nêu caveat LLM-judge |
| So sánh M0/M1/M2 có ý nghĩa thống kê không | **Bootstrap CI (95%) + kiểm định ghép cặp** (Wilcoxon signed-rank cho metric liên tục; McNemar cho đúng/sai theo case) | đáp ứng tiêu chí rubric "kiểm định thống kê phù hợp" (2đ) — xem `docs/quy_dinh_vien.md` §4 |

**Tăng cỡ mẫu quan sát:** mỗi case × mỗi mode chạy **k = 3 lần** (temperature cố định, ghi cả 3 output) → 34 case × 3 mode × 3 lần = 306 quan sát; vừa đo được độ dao động của LLM, vừa đủ n cho kiểm định ghép cặp theo case.

## C. Việc phải làm

- [ ] Freeze test set + gold labels → commit (ghi lại hash vào run_config).
- [ ] Nhờ GVHD/analyst gieo 5 held-out cases (mình không xem đáp án).
- [ ] Viết `metrics.py` đúng định nghĩa các metric ở B (mỗi hàm ghi docstring kèm citation).
- [ ] Chạy batch 3 chế độ × toàn bộ case; lưu raw (`results/raw/` — gitignored) + summary (commit).
- [ ] Chấm tay 20–30% mẫu attribution (2 người, độc lập) → tính κ; κ < 0.7 thì sửa rule và chấm lại.
- [ ] Blind scoring: 2–3 người FP&A × ~8 case xáo trộn, rubric 3 tiêu chí.
- [ ] Slice kết quả theo kịch bản (robustness) + xuất bảng/hình vào `thesis/figures/` (script sinh, không chép tay).

## D. Ngưỡng thành công đăng ký trước (đề xuất — CHỐT VỚI GVHD trước final run)

- M2: numerical EM ≥ 98%; citation precision ≥ 90%; tỷ lệ câu không căn cứ ≤ 5%; từ chối đúng ≥ 4/5 case bẫy.
- Thứ tự kỳ vọng M2 > M1 > M0 trên các chỉ số chính; nếu không đạt, báo cáo trung thực và phân tích vì sao — kết quả âm vẫn là kết quả.

## Cut line nếu trễ
Bỏ RAGAS phụ; blind scoring giảm còn 2 người × 5 case. KHÔNG cắt: đóng băng trước, κ check, pre-registered thresholds — đó là phần "khách quan" của khóa luận.

## Ghi chú bàn giao (điền khi xong)
- κ đạt được: · Ngưỡng đã chốt với GVHD ngày:
- Quyết định phát sinh: · Vấn đề để lại:
