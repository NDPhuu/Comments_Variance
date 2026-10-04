# Phase 4 — Web App & Deploy (13–15/10/2026)

> **Gate M4 (tối 15/10):** link public mở được từ máy khác, chạy trơn kịch bản demo 2 phút; screenshots đã vào `thesis/figures/`.
> **Trạng thái:** ☐ chưa bắt đầu / ☐ đang làm / ☐ XONG

## Mục tiêu
Lớp "hộp kính" nhìn thấy được: UI provenance + deploy công khai. Lưu ý: kết quả khoa học đã chốt ở Phase 3 — phase này là trình diễn, không phát sinh claim mới.

## Việc phải làm

### A0. Yêu cầu "ENGINE SỐNG" — app không được giống slide (phê bình đã tiếp thu 04/10)
- **Không có hộp giải thích/"Điểm demo" trong app** — phần dẫn dắt nằm ở slide và lời nói; app chỉ là công cụ.
- Demo phải có **hành động thật trước mắt hội đồng**: chọn kỳ → bấm "Quét P&L" (engine chạy thật, có trạng thái loading, số case hiện ra) → chọn **BẤT KỲ case nào** (không chỉ 1 case cứng) → bấm "Generate" gọi Gemini THẬT (spinner/stream vài giây) → cổng kiểm chạy, badge bật realtime.
- **Settings chỉnh được ngưỡng materiality** → bấm áp dụng → hàng chờ thay đổi ngay. Đây là thứ slide không giả được.
- Panel **"Xem JSON thô"** (engine output, retrieval scores, verdict) cho người kỹ thuật trong hội đồng mở ra xem — bằng chứng không có gì giấu.
- Mock hiện tại (`docs/ui_mockup.html`) chỉ là **wireframe chốt bố cục**, không phải demo cuối.

### A. Backend hoàn thiện
- [ ] Endpoints theo `docs/architecture.md` §4.6 + CORS + env (`ANTHROPIC_API_KEY`).
- [ ] `GET /api/meta` trả dataset_version/model_id/prompt_version (hiện ở footer UI — tính minh bạch).

### B. React UI — 3 màn hình (Vite + TS + Tailwind)
- [ ] **Variance Queue**: bảng case, filter property/period, badge material/direction.
- [ ] **Case Investigation**: con số bấm được → bảng GL contributors; driver bấm được → evidence panel highlight đoạn trích. *(Đây là màn hình ăn điểm nhất trước hội đồng.)*
- [ ] **Draft & Verify**: 3 modes side-by-side + verification badges (✅ verified / 🔴 số sai / 🟡 cần xác nhận / ⛔ abstained).

### C. Deploy
- [ ] Backend → Render/Railway (SQLite synthetic nằm trong repo — hợp lệ vì dữ liệu giả). Frontend → Vercel (`VITE_API_URL`).
- [ ] Viết `docs/demo_script.md`: kịch bản 2 phút — mở Queue → vào 1 case → bấm số ra GL → so 3 modes → chỉ vào badge đỏ của M0/M1.

## Writing track
- [ ] `thesis/chuong4.md` hoàn chỉnh: artifact walkthrough kèm screenshots.
- [ ] `thesis/chuong5.md` draft: đóng góp, hạn chế (nói thật: synthetic, 1 bối cảnh, n nhỏ), hướng phát triển (dữ liệu thật, tích hợp ERP).

## Cut line nếu trễ
Màn hình 3 rút còn 1 mode + badges (bỏ side-by-side); deploy rút xuống demo local + video quay sẵn. KHÔNG cắt: provenance click-through ở màn hình 2 (lý do tồn tại của UI).

## Ghi chú bàn giao (điền khi xong)
- Link deploy:
- Quyết định phát sinh:
- Vấn đề để lại:
