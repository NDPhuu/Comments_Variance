# design.md — Variance Workbench Demo Website

Phiên bản: v2.0 · cập nhật 17/10/2026

Tài liệu này là đặc tả giao diện cho website demo của khóa luận về hệ thống sinh giải trình chênh lệch ngân sách có thể kiểm chứng. Thiết kế không sử dụng tên, logo, hình ảnh hoặc dấu hiệu nhận diện của bất kỳ doanh nghiệp nào. Bảng màu navy–blue–cyan được giữ như một lựa chọn thẩm mỹ độc lập.

## 1. Mục tiêu trải nghiệm

Website phải giúp người xem hiểu hệ thống qua thao tác, không qua một trang giới thiệu dài. Luồng chính gồm ba bước:

1. Chọn kỳ và quét P&L để tìm các chênh lệch trọng yếu.
2. Mở một case để xem số liệu, contributors và tài liệu bằng chứng.
3. Sinh giải trình, xem kết quả kiểm chứng và lần ngược từng số hoặc trích dẫn về nguồn.

Màn hình so sánh M0–M1–M2 là phần bổ trợ cho nội dung nghiên cứu. Nó phải dùng đúng số liệu benchmark đã lưu, không tạo claim mới.

## 2. Nguyên tắc

- Chuyên nghiệp, rõ ràng, nhiều khoảng trắng.
- Giao diện phải giống một công cụ FP&A đang hoạt động, không giống slide trình chiếu.
- Mỗi màn hình có một nhiệm vụ chính và một hành động chính.
- Số liệu dùng font đơn cách và canh phải.
- Trạng thái không chỉ phân biệt bằng màu; luôn có nhãn hoặc biểu tượng đi kèm.
- Không dùng gradient, hiệu ứng kính mờ, emoji trang trí hoặc đổ bóng nặng.
- Chuyển động chỉ dùng để phản hồi thao tác, thời lượng 120–220 ms.
- Nội dung demo phải ghi rõ là dữ liệu mô phỏng.

## 3. Bảng màu

| Token | Hex | Vai trò |
|---|---|---|
| `ink-950` | `#081A36` | Thanh điều hướng, tiêu đề chính, nút chính |
| `blue-750` | `#004583` | Liên kết, nhãn đang chọn, tiêu đề phụ |
| `cyan-550` | `#01A7E5` | Focus ring, đường nhấn, trạng thái đang chạy |
| `blue-350` | `#789FD4` | Biểu đồ phụ, đường nối, nhãn ít quan trọng |
| `sky-200` | `#B2E2F9` | Nền lựa chọn và vùng thông tin |
| `cyan-100` | `#D8F7FC` | Nền provenance và bằng chứng |
| `slate-800` | `#303846` | Chữ nội dung chính |
| `slate-600` | `#5D6675` | Chữ mô tả |
| `slate-350` | `#B7BFCA` | Viền và đường phân cách |
| `slate-100` | `#F3F5F7` | Nền trang và nền bảng xen kẽ |
| `white` | `#FFFFFF` | Nền thẻ và chữ trên nền tối |
| `success-600` | `#23815A` | Đạt kiểm chứng, favorable |
| `success-100` | `#E8F5EF` | Nền trạng thái đạt |
| `warning-650` | `#A76500` | Cần xác nhận |
| `warning-100` | `#FFF3D6` | Nền cảnh báo |
| `danger-600` | `#C8404C` | Sai, unfavorable, từ chối |
| `danger-100` | `#FDECEE` | Nền lỗi và bẫy |

Tỷ lệ diện tích khuyến nghị: 72% trắng/xám nhạt, 18% navy, 10% cyan và màu trạng thái. Chữ thường phải đạt tương phản tối thiểu 4,5:1.

## 4. Kiểu chữ

- Tiêu đề: `Be Vietnam Pro`, dự phòng `Arial`, `sans-serif`.
- Nội dung: `Inter`, dự phòng `Arial`, `sans-serif`.
- Số và mã: `IBM Plex Mono`, dự phòng `Consolas`, `monospace`.

| Style | Cỡ chữ | Độ đậm | Line-height |
|---|---:|---:|---:|
| Page title | 28–34px | 650 | 1,2 |
| Section title | 16px | 650 | 1,3 |
| Card title | 14px | 650 | 1,35 |
| KPI | 28–36px | 650 | 1,1 |
| Body | 14px | 400 | 1,55 |
| Label | 11–12px | 650 | 1,3 |
| Code / number | 12–14px | 500 | 1,4 |

## 5. Lưới và khoảng cách

- Khung nội dung tối đa: 1.440px.
- Sidebar desktop: 232px; thu gọn thành top navigation khi dưới 900px.
- Lưới nội dung: 12 cột, gutter 20px.
- Thang khoảng cách: 4 / 8 / 12 / 16 / 24 / 32 / 48px.
- Bo góc: 6px cho control; 8px cho card và panel.
- Viền: 1px `slate-350`; trạng thái được chọn dùng 2px `cyan-550`.
- Bóng chỉ dùng cho modal: `0 18px 50px rgba(8,26,54,.18)`.

## 6. Cấu trúc ứng dụng

### 6.1. App shell

- Sidebar chứa tên sản phẩm dạng chữ: `Variance Workbench`.
- Navigation: `Hàng chờ`, `Điều tra`, `Soạn & kiểm`, `Kết quả nghiên cứu`.
- Footer sidebar hiển thị `dataset_v1`, model và trạng thái “Dữ liệu mô phỏng”.
- Header nội dung chứa breadcrumb, kỳ đang chọn và nút `Thiết lập ngưỡng`.

### 6.2. Hàng chờ chênh lệch

- Control đầu trang: kỳ, khu, nút `Quét P&L`.
- KPI: số case trọng yếu, verified, cần xác nhận, từ chối.
- Bảng: khu, dòng P&L, budget, actual, variance, %, trạng thái.
- Chọn một dòng phải mở được màn hình điều tra của chính case đó.
- Trong bản demo tĩnh, nút quét dùng dữ liệu nhúng và animation ngắn; không giả vờ gọi API thật.

### 6.3. Điều tra case

- KPI số liệu ở đầu màn hình.
- Bảng contributors ở trái; evidence panel ở phải.
- Khi chọn contributor, tài liệu liên quan được highlight.
- Hiển thị rõ tài liệu nào chỉ liên quan bề mặt và tài liệu nào được xem là liên kết.
- Có nút `Tạo giải trình` và `Xem JSON nguồn`.

### 6.4. Soạn và kiểm chứng

- Ba tab M0, M1 và M2; M2 được chọn mặc định.
- Bản giải trình dùng chip có thể bấm cho số và mã tài liệu.
- Panel kiểm chứng gồm: số liệu, trích dẫn, nhận định và từ chối.
- Khi bấm chip số, mở provenance cho biết trường engine và công thức.
- Khi bấm mã tài liệu, mở nội dung và metadata của tài liệu.
- Trạng thái cuối dùng ba nhãn: `Verified`, `Cần xác nhận`, `Từ chối`.

### 6.5. Kết quả nghiên cứu

- Hiển thị bảng mean ± SD được tính trên ba điểm trung bình theo lần chạy.
- Có ba thanh so sánh cho numeric accuracy, citation recall và unsupported-claim rate.
- Ghi rõ dữ liệu mô phỏng và cách tính SD.
- Không trình bày Cohen’s κ.

## 7. Thành phần giao diện

| Thành phần | Quy cách |
|---|---|
| Primary button | Nền `ink-950`, chữ trắng, cao 38px |
| Secondary button | Nền trắng, viền `slate-350`, chữ `ink-950` |
| Filter | Label trên, control cao 38px |
| Status badge | Pill nhỏ, có chấm/biểu tượng và chữ |
| KPI card | Nhãn nhỏ, số lớn, đường nhấn 3px ở cạnh trên |
| Data table | Header navy; hover nền `cyan-100`; số canh phải |
| Evidence card | Metadata đơn cách; phần hỗ trợ được highlight `sky-200` |
| Provenance chip | Nền `slate-100`, viền nét đứt `blue-750` |
| Citation chip | Nền trắng, viền `cyan-550`, chữ `blue-750` |
| Verification row | Tên cổng, kết quả, mô tả ngắn và trạng thái |
| Modal JSON | Nền trắng, mã trên nền `ink-950`, có nút đóng |
| Toast | Góc dưới phải; dùng cho quét, sinh và sao chép |

## 8. Trạng thái và hành vi

- `idle`: control sẵn sàng.
- `loading`: nút khóa, spinner và mô tả việc đang làm.
- `verified`: tất cả cổng bắt buộc đạt.
- `flagged`: ít nhất một cổng không đạt; chỉ rõ lỗi.
- `abstained`: thiếu bằng chứng liên kết; không nêu nguyên nhân.
- `empty`: không có case vượt ngưỡng.

Demo phải hỗ trợ bàn phím, focus ring rõ và `Escape` để đóng modal. Nếu người dùng bật `prefers-reduced-motion`, loại bỏ animation không cần thiết.

## 9. Nội dung và ngôn ngữ

- Tiếng Việt đơn giản; giữ thuật ngữ tiếng Anh chỉ khi nó là tên metric hoặc thành phần kỹ thuật.
- Dùng “khu” thay cho tên doanh nghiệp thật.
- Dùng mã giả lập `PROP-A…E`, `TEN-xxx`, `EV-xxx`.
- Ghi số theo định dạng Việt Nam trong nội dung trình bày.
- Mọi claim nghiên cứu phải khớp `app/backend/results/summary.csv`.
- Footer luôn ghi: `Dữ liệu mô phỏng · Không dùng cho báo cáo thực tế`.

## 10. Responsive và accessibility

- Dưới 900px: sidebar thành thanh tab; bảng cuộn ngang; evidence xuống dưới contributors.
- Dưới 640px: KPI chuyển thành hai cột; toolbar xếp dọc; modal dùng toàn màn hình.
- Mọi button có tên truy cập; bảng có caption ẩn; modal giữ focus cơ bản.
- Không dùng màu cyan cho chữ nhỏ trên nền trắng.

## 11. Phạm vi bản HTML demo

File `docs/variance_workbench_demo.html` là bản buildless, tự chứa CSS và JavaScript. File phải mở trực tiếp được, không cần cài thư viện. Dữ liệu được nhúng để minh họa giao diện và được ghi rõ là mô phỏng.

Bản HTML cần có các tương tác sau:

- Quét P&L và cập nhật hàng chờ.
- Chọn case bất kỳ trong bảng.
- Chọn contributor để xem evidence.
- Chuyển M0–M1–M2.
- Bấm số và trích dẫn để xem nguồn.
- Mở JSON thô.
- Thay đổi ngưỡng trọng yếu trong modal và quét lại.
- Xem bảng kết quả benchmark mới nhất.
