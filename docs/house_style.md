# House style — rút từ 17 comments thật (P&L, T1–T8/2026)

> Nguồn: cột "Key Commentary" trong sheet Output của 8 file `PL_Act vs budget_*.xlsb`, trích bằng `app/tools/extract_comments.py` → `local_data/comments_PL.csv` (KHÔNG commit).
> File này chỉ chứa MÔ TẢ ẨN DANH: mọi tên dự án/đối tác/sự kiện thật đã thay bằng placeholder. Không câu nào dưới đây là trích nguyên văn.

## 1. Thống kê nhanh

- 17 comments / 8 tháng → mỗi tháng chỉ **0–4 dòng P&L có comment** (chỉ comment dòng có chênh lệch đáng kể; Revenue sát budget thì không comment).
- Comment tập trung ở: Selling expenses, G&A, Financial income/expenses, Other profits — và **Leasing revenue có hệ comment riêng** trong file Leasing YTD (sheet `Comment`).
- Độ dài: ~100–400 ký tự; dạng **bullet điện tín**, không phải văn xuôi.
- Ngôn ngữ: **tiếng Anh**, đơn vị `$Xm` / `$Xk`, dấu `+`/`−` đặt trước số theo hướng tác động.

## 2. Khuôn mẫu cấu trúc (pattern thật, đã ẩn danh)

```
[Câu định hướng]  Favorable/Unfavorable amount mainly due to <nguyên nhân nhóm>:
[Driver bullet]   - <sự kiện> +$Xk <tại đơn vị Y> delayed to <kỳ Z>
[Driver bullet]   - $Xk for <dịch vụ/khoản mục cụ thể>
[Offset]          Partly offset by: +$Xm from <yếu tố ngược chiều>; +$Xk from <…>
[YTD context]     YTD <chỉ tiêu>: $Xm, ~$Xm unfavorable vs. budget, due to <…>
[Forward note]    will be paid and recorded in <tháng tới> / to be recorded once finalized
```

Đặc điểm quan trọng:
1. **Mỗi driver = 1 bullet = số + thực thể + mốc thời gian.** Không có bullet nào thiếu số.
2. **"Partly offset by"** là một khối riêng, liệt kê yếu tố ngược chiều có số.
3. **Forward-looking note** gần như luôn có khi nguyên nhân là timing: nói rõ khoản sẽ rơi vào kỳ nào.
4. **Carry-forward**: khi driver YTD không đổi, comment được lặp gần nguyên văn qua các tháng (3 tháng liên tiếp giống hệt nhau trong mẫu). → Hệ thống nên hỗ trợ "kế thừa comment kỳ trước + cập nhật số".
5. Comment ở mức **dòng P&L hợp nhất**, trong thân bài mới nhắc đến dự án/đơn vị cụ thể. → Case của hệ thống (line × property) là mức ĐIỀU TRA; mức TRÌNH BÀY cần gom về line.

## 3. Cause taxonomy thực tế (đếm trên 17 comments)

| Nhóm nguyên nhân | Tần suất | Ví dụ dạng ẩn danh |
|---|---|---|
| **timing_difference** | ~8/17 — PHỔ BIẾN NHẤT | phí/penalty chưa book, dời sang kỳ sau; "sẽ ghi nhận tháng tới" |
| **one_off_event** | ~6/17 | lãi thoái vốn; bồi thường bảo hiểm thiên tai; xóa sổ khoản đặt cọc; penalty chấm dứt HĐ từ tenant |
| **financing_event** | ~4/17 | khoảng trống giữa trả nợ và tái cấp vốn làm mất khoản tiết kiệm lãi |
| **accounting_treatment** | ~3/17 | phí được vốn hóa thay vì chi phí; thay đổi cách phân bổ phí |
| **rate_change** | ~1/17 | lãi suất cơ sở mới chưa được áp dụng |
| (riêng cột) **fx_impact** | cột riêng trong file | tách sẵn khỏi commentary |
| (từ mảng leasing — file Leasing YTD) | — | early termination, handover delay, escalation |

## 4. Hệ quả thiết kế (ràng buộc cho generator + prompt + verifier)

1. **Output schema đổi theo khuôn thật**: `{headline, driver_bullets[], offsets[], ytd_context, forward_note}` — KHÔNG sinh đoạn văn trơn.
2. **Numeric gate phải parse đơn vị** `$1.5m`, `$530k`, `~$2m`, dấu `+/−` — so khớp sau khi quy đổi, chấp nhận prefix `~` với sai số khai báo.
3. **Kịch bản synthetic phải phủ taxonomy thật**: timing (nhiều nhất), one-off, accounting treatment, rate — cộng nhóm leasing (termination, handover, escalation).
4. **Abstention khớp hành vi thật**: dòng không trọng yếu thì KHÔNG comment (im lặng cũng là hành vi chuẩn).
5. Tính năng nên có (ghi vào backlog, không bắt buộc MVP): carry-forward comment kỳ trước.
