# Bảng thuật ngữ

Dành cho người đọc không chuyên về kỹ thuật. Tách ra từ `README.md`.

| Thuật ngữ | Nghĩa |
|---|---|
| **Variance** | Chênh lệch giữa thực tế và kế hoạch (Actual − Budget) |
| **Materiality** | Ngưỡng trọng yếu: lệch nhỏ bỏ qua, lệch lớn phải giải trình |
| **RAG** | "Tìm trước rồi mới viết": trước khi mô hình viết, hệ thống đi tìm tài liệu liên quan đưa kèm, để viết có căn cứ thay vì viết từ trí nhớ |
| **RAG không kiểm chứng** | RAG có tìm tài liệu đưa kèm nhưng để mô hình viết tự do, không kiểm số, không kiểm trích dẫn. Trong đề tài, M1 dùng chung bộ truy xuất với M2 nên so sánh M1–M2 cô lập được giá trị của khâu kiểm chứng |
| **Glass-box** | Hộp kính, ngược với hộp đen: mọi số bấm ra được dòng sổ, mọi nguyên nhân bấm ra được tài liệu |
| **Provenance** | Gốc gác của một con số hay một câu: nó đến từ dòng sổ nào, tài liệu nào |
| **Abstention** | Từ chối có chủ đích: thiếu bằng chứng thì báo thiếu, không suy đoán |
| **Mệnh đề nguyên tử** | Khẳng định nhỏ nhất chỉ nói một điều, kiểm chứng được độc lập. Tách câu dài thành các mệnh đề như vậy mới biết tin phần nào, sai phần nào (gốc: FActScore) |
| **Benchmark** | Bộ đề chuẩn kèm cách chấm tự động, để các hệ thống khác nhau thi cùng một đề và so được điểm |
| **Rà soát / người duyệt** | Rà soát: cấp quản lý đọc và kiểm tra lại báo cáo trước khi dùng. Người duyệt: người làm việc đó. Khác "kiểm toán" là cuộc kiểm tra độc lập theo chuẩn mực để đưa ra ý kiến xác nhận. Không dùng "soát xét" vì trong kế toán Việt Nam từ này gắn với dịch vụ có chuẩn mực riêng. "Phê duyệt" chỉ dùng cho bước ký chấp thuận cuối |
| **Evidence corpus** | Kho bằng chứng: tập tài liệu số hóa (hợp đồng, biên bản, email duyệt) mà hệ thống tìm kiếm trong đó |
| **BM25** | Thuật toán tìm theo từ khóa, như Ctrl+F có xếp hạng |
| **Embedding / BGE-M3** | Cách máy biểu diễn nghĩa để tìm tài liệu gần nghĩa dù khác từ. BGE-M3 là mô hình mã nguồn mở, chạy được trên máy cá nhân |
| **RRF** | Reciprocal Rank Fusion: cách hợp nhất hai bảng xếp hạng (BM25 và vector) thành một |
| **Gold label** | Đáp án chuẩn gắn sẵn trong dữ liệu mô phỏng, dùng để chấm điểm hệ thống |
