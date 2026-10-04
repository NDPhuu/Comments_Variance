# design.md — Slides hướng dẫn Leasing Dashboard (BW Industrial)

Phiên bản: v1.0 · chốt 01/10/2026 · demo trực quan: https://claude.ai/artifact/CGXMQ2pzoRubiqJiJm2B7C
Nguồn: BW_Pitchbook_VSIP_NgheAn.pdf (màu, font) · logo BW Industrial · dashboard `Leasing dashboard_01_10.pbip`.

## 1. Nguyên tắc
- Chuyên nghiệp, tối giản, nhiều khoảng trắng — theo tinh thần pitchbook BW.
- Navy là màu chủ đạo, cyan chỉ để nhấn. Không gradient, không emoji, không đổ bóng nặng.
- Mỗi slide một ý. Slide hướng dẫn ưu tiên **ảnh dashboard + số chú thích**.
- Tối đa ~6 dòng nội dung / slide, mỗi dòng ≤ ~12 từ. Phần giải thích dài đưa vào speaker notes.

## 2. Màu sắc
| Token | Hex | Dùng cho |
|---|---|---|
| `navy-900` | `#081A36` | Tiêu đề, nền cover / section, header bảng |
| `blue-700` | `#004583` | Tiêu đề phụ, số liệu nhấn, icon |
| `cyan-500` | `#01A7E5` | Số chú thích, gạch nhấn, highlight — chữ chỉ khi ≥ 24px |
| `blue-300` | `#789FD4` | Đường trang trí, biểu đồ phụ — không dùng cho chữ |
| `sky-200` | `#B2E2F9` | Nền thẻ, khối phụ; chữ phụ trên nền navy |
| `cyan-100` | `#D8F7FC` | Nền ô **Lưu ý** |
| `gray-700` | `#4B4B4B` | Chữ nội dung |
| `gray-400` | `#AEB4C2` | Viền, đường phân cách |
| `gray-100` | `#F3F4F6` | Nền khối |
| `white` | `#FFFFFF` | Nền slide nội dung; chữ trên nền navy |
| `green-500` | `#2E9E6B` | Chỉ cho **Nên / Do**, ▲ tốt hơn |
| `red-500` | `#EC5D69` | Chỉ cho **Không nên / Don't**, **Bẫy**, ▼ kém hơn |
| `red-100` | `#FDECEE` | Nền ô **Bẫy dễ đọc sai** |

- Slide nội dung: nền trắng · tiêu đề `navy-900` · nội dung `gray-700`.
- Cover / Section: nền `navy-900` · chữ trắng · nhấn `cyan-500`.
- Tỷ lệ diện tích ~ 70% trắng/xám nhạt · 20% navy · 10% cyan.
- Tương phản chữ ≥ 4.5:1.

## 3. Font
- Tiêu đề: **Be Vietnam Pro SemiBold** (thay Headlines SemiBold của pitchbook).
- Nội dung: **Inter** 400 / 500 / 600.
- Dự phòng khi xuất .pptx: **Arial**.

## 4. Cỡ chữ (khung 1920×1080; pt ≈ px × 0.5 trên slide 13.33″)
| Style | Font | px | ≈ pt | Đậm | Màu |
|---|---|---|---|---|---|
| Cover title | Heading | 88 | 44 | 600 | trắng |
| Section title | Heading | 64 | 32 | 600 | trắng |
| Slide title (H1) | Heading | 48 | 24 | 600 | navy-900 |
| Subtitle (H2) | Inter | 32 | 16 | 600 | blue-700 |
| KPI lớn | Heading | 72 | 36 | 600 | navy-900 / cyan-500 |
| Body | Inter | 24 | 12 | 400 | gray-700 |
| Callout / bullet nhỏ | Inter | 20 | 10 | 400 | gray-700 |
| Caption | Inter | 18 | 9 | 400 | gray-700 |
| Footer | Inter | 14 | 7 | 400 | gray-400 |

- Trên deck Slides thực tế: **không chữ nào < 24px** (kể cả caption, footer) để đọc rõ khi chiếu và khi xuất .pptx — các cỡ 20/18/14 ở trên nâng lên 24. Line-height 1.4 (body) · 1.15 (tiêu đề).

## 5. Lưới & khoảng cách
- Lề trái/phải 96px · trên 80px · dưới 64px · lưới 12 cột, gutter 24px.
- Thang khoảng cách: 8 / 16 / 24 / 40 / 64.
- Bo góc: 4px (thẻ) · tròn (số chú thích, chip).
- Footer slide nội dung: logo màu trái · "Hướng dẫn Power BI cho Sales" giữa · số trang phải · kẻ mảnh `gray-400` phía trên.

## 6. Thành phần lặp lại
| Thành phần | Quy cách |
|---|---|
| Số chú thích | Tròn `cyan-500` Ø40px, số trắng 20px; đặt trên ảnh, chú thích cùng số ở cột phải |
| Ô Lưu ý | Nền `cyan-100`, tiêu đề "Lưu ý" navy đậm |
| Ô Bẫy dễ đọc sai | Nền `red-100`, viền 1px `red-500` bao quanh, tiêu đề "⚠ Bẫy dễ đọc sai" |
| Do / Don't | 2 cột, viền `gray-400`, icon tròn ✓ green / ✕ red |
| Bước thao tác | Số `01…` lớn cyan, kẻ trên navy 4px, tiêu đề ngắn + 1 dòng mô tả |
| Chip nhịp số liệu | `YTD` = nền `navy-900` chữ trắng · `Cuối tháng` = viền `navy-900` chữ navy; cao 24px, chữ 14px 600, đặt ngay sau tên chỉ số |
| Tên chỉ số / visual | Giữ nguyên tiếng Anh như trên dashboard, IN HOA, Inter 600 navy |
| Thẻ ▶ DEMO | Góc trên phải, nền `cyan-500`, chữ navy 600 "▶ DEMO", chỉ trên slide có demo live |
| Khung ảnh dashboard | Viền 1px `gray-400`, không đổ bóng; khi chưa có ảnh: khung mô phỏng + nhãn "Thay ảnh chụp" |

## 7. Kiểu layout slide
Cover · Agenda · Section · Lưới thẻ · 3 cột · So sánh 2 cột · Dashboard tour (ảnh 8 cột + chú thích 4 cột) · Step-by-step · Do/Don't · Bảng · Kết.

## 8. Logo
- Nền navy: logo trắng (cắt từ `Images/logo.jpeg`).
- Nền trắng: logo màu (`StaticResources/RegisteredResources/logo-color-fix-done….png`).
- Khoảng trống quanh logo ≥ chiều cao chữ "B".

## 9. Nội dung
- Deck gửi Sales **không** chứa: mục "⚠ Cần thử trên Desktop", Phụ lục C, Phụ lục D, giọng nội bộ.
- Phụ lục A (Thuật ngữ) và B (Tình huống) là slide dự phòng cuối deck.
