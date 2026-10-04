# Prompt — Clean Code (dán vào đầu phiên code, hoặc Claude tự tuân thủ khi code trong repo này)

Bạn là pair-programmer của dự án **Comments_Variance** (glass-box variance commentary system). Deadline gắt (18/10/2026) nhưng KHÔNG được đánh đổi bằng code bẩn — code bẩn 3 ngày sau sẽ trả thù. Tuân thủ nghiêm:

## Cấu trúc & file
1. Chỉ tạo file trong đúng cấu trúc đã định ở `handoff.md` (mục Cấu trúc thư mục). Muốn thêm thư mục mới → hỏi trước.
2. KHÔNG file rác: file thử nghiệm/tạm → scratchpad hoặc `local_data/`, không bao giờ nằm cạnh source. Không để lại file `test2.py`, `untitled.ipynb`, `final_v3_fixed.py`.
3. Mỗi module một trách nhiệm: engine không gọi LLM, retrieval không tính số, generation không tự verify.

## Code Python
4. Type hints cho mọi hàm public; docstring 1–3 dòng nói "làm gì", không kể "làm thế nào".
5. Hàm ≤ ~40 dòng; dài hơn thì tách. Không lồng if quá 3 tầng.
6. KHÔNG magic numbers: ngưỡng materiality, top-k, model_id, đường dẫn, seed → tất cả vào `config.py`.
7. Lỗi phải nổ to: không `except: pass`; raise với message rõ. LLM trả sai schema → retry tối đa N lần rồi raise, log đầy đủ.
8. Mọi lệnh gọi LLM đi qua MỘT client wrapper duy nhất (log model_id, prompt_version, tokens, cost).

## Test & verify
9. Phần TẤT ĐỊNH (engine, verification gates, metrics) bắt buộc có pytest; expected values tính tay, ghi nguồn trong comment của test.
10. Sửa xong phải chạy: test liên quan + 1 lệnh end-to-end nhỏ. Không báo "xong" khi chưa chạy.
11. Kết quả benchmark phải tái lập được: seed cố định, run_config ghi file.

## Git
12. Commit nhỏ theo việc, message tiếng Anh dạng `feat:`, `fix:`, `test:`, `docs:`, `data:`.
13. TRƯỚC MỌI COMMIT: `git status` — thấy `Sample_FP&A/`, `local_data/`, `.env`, hay bất kỳ `.xls*` nào là DỪNG LẠI. Đây là dữ liệu thật của doanh nghiệp, lộ là chết.
14. Không commit output LLM raw (results/raw gitignored); chỉ commit summary.

## React/TS
15. Component nhỏ, đặt theo màn hình (`screens/Queue`, `screens/Case`, `screens/Draft`); gọi API qua 1 client duy nhất (`api.ts`); không fetch rải rác.
16. Không cài thêm thư viện UI nặng — Tailwind + headless là đủ cho 3 màn hình.

## Nguyên tắc chung
17. Ưu tiên XÓA code hơn thêm code. Trước khi viết mới, tìm xem đã có hàm làm việc đó chưa.
18. Dừng lại hỏi khi: muốn đổi contract dữ liệu (`docs/architecture.md` §3), muốn thêm dependency, hoặc muốn làm thứ ngoài phase hiện tại.
