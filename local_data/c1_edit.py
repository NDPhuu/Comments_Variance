# -*- coding: utf-8 -*-
"""Ap cac sua nhom A + D vao chuong1.docx (da unpack + merge runs).
Moi replacement assert tim thay dung 1 lan — fail to thi dung lai, khong ghi file."""
import io, re, sys

P = "c1_unpacked/word/document.xml"
xml = io.open(P, encoding="utf-8").read()

def rep(old, new, n=1):
    global xml
    c = xml.count(old)
    assert c == n, f"FOUND {c} (expect {n}): {old[:80]}..."
    xml = xml.replace(old, new)

# ---- A2: cau claim khong nguon + dau cham giua cau (Gartner 2024)
rep("nhóm ba tác vụ hàng đầu. trên cả phân loại dữ liệu thu chi (44%) và soạn báo cáo quản trị (34%) (Gartner, 2024). Điều này có nghĩa AI đã chạm vào báo cáo quản trị trước khi các cơ chế kiểm soát dành riêng cho nó kịp hình thành.",
    "nhóm ba tác vụ hàng đầu, trên cả phân loại dữ liệu thu chi (44%) và soạn báo cáo quản trị (34%) (Gartner, 2024). Kỳ vọng ứng dụng vì vậy dồn đúng vào khâu mà một sai sót đi thẳng tới quyết định quản trị, trong khi — như mục 2.2 sẽ cho thấy — việc bảo đảm văn bản sinh ra có căn cứ vẫn là bài toán nghiên cứu đang mở.")

# ---- A1: 50 -> 17 giai trinh (so thuc te da phan tich)
rep("đặc điểm này được xác nhận khi phân tích 50 giải trình đã phê duyệt tại doanh nghiệp quan sát giai đoạn 2025-2026.",
    "đặc điểm này được xác nhận khi phân tích 17 giải trình đã phê duyệt tại doanh nghiệp quan sát (trình bày ở mục 3.1).")

# ---- A4: vanilla RAG -> RAG khong kiem chung (RQ2 + H2)
rep("So với cách sử dụng LLM trực tiếp và cách kết hợp truy xuất tài liệu thông thường (vanilla RAG), kiến trúc đề xuất cải thiện ra sao",
    "So với cách sử dụng LLM trực tiếp và cách RAG không kiểm chứng (dùng cùng bộ bằng chứng truy xuất nhưng không kiểm số, không kiểm trích dẫn), kiến trúc đề xuất cải thiện ra sao")
rep("Hệ thống đề xuất có độ chính xác trích dẫn cao hơn phương án vanilla RAG.",
    "Hệ thống đề xuất có độ chính xác trích dẫn cao hơn phương án RAG không kiểm chứng.")

# ---- A5: gap #3 — bo RAGAS, 'kiem toan' -> 'soat xet'
rep("Thứ ba, các cơ chế kiểm chứng hiện hành chủ yếu dùng mô hình học làm giám khảo (NLI trong ALCE, mô hình ngôn ngữ trong RAGAS và FActScore tự động), trong khi bối cảnh kiểm toán đòi hỏi phương án tất định, giải thích được từng quyết định.",
    "Thứ ba, ở khâu phán định “câu này có được tài liệu xác nhận không”, các cơ chế chấm hiện hành (ALCE, FActScore) đều dùng một mô hình học làm giám khảo — giám khảo đó có thể phán sai và không nêu được lý do chấm, trong khi quy trình soát xét báo cáo quản trị đòi hỏi phương án tất định: người phê duyệt lần lại được vì sao từng câu đạt hay không đạt.")

# ---- A6: 'mo hinh sau khi duoc dieu chinh' -> 'he thong de xuat'
rep("để đánh giá khả năng truy xuất và độ chính xác của mô hình sau khi được điều chỉnh.",
    "để đánh giá khả năng truy xuất và độ chính xác của hệ thống đề xuất.")

# ---- A7: automation bias -> misuse (dung thuat ngu cua Parasuraman & Riley)
rep("Nghiên cứu về tự động hóa đã chỉ ra hiện tượng automation bias, khi đầu ra của hệ thống",
    "Nghiên cứu kinh điển về tự động hóa đã chỉ ra hiện tượng lạm dụng tự động hóa (misuse): khi đầu ra của hệ thống")

# ---- B2: pham vi — them cac dong chi phi
rep("ở mức dòng P&amp;L theo từng khu công nghiệp, với trọng tâm là doanh thu cho thuê, mảng có các sự kiện nguyên nhân",
    "ở mức dòng P&amp;L theo từng khu công nghiệp, trên các dòng doanh thu và chi phí vận hành chính, với trọng tâm là doanh thu cho thuê — mảng có các sự kiện nguyên nhân")

# ---- D: chinh ta / cau trung / thuat ngu
rep("một câu hỏi khác lại được đặt ra: Làm thế nào để kiểm chứng được những gì AI viết ra, và bằng cách nào.",
    "một câu hỏi khác lại được đặt ra: làm thế nào để kiểm chứng được những gì AI viết ra.")
rep("quy trình hiện tại phụ thuộc vào rất lớn vào khả năng",
    "quy trình hiện tại phụ thuộc rất lớn vào khả năng")
rep("Vấn đề này đã tồn tại ra từ trước khi có mô hình ngôn ngữ lớn, trong nghiên cứu về  khả năng đọc hiểu",
    "Vấn đề này đã tồn tại từ trước khi có mô hình ngôn ngữ lớn, trong nghiên cứu về khả năng đọc hiểu")
rep("SQuAD là một trong những bộ đề phổ biến nhất cho bài toán này nằm, và đến năm 2018",
    "SQuAD là một trong những bộ đề phổ biến nhất cho bài toán này, và đến năm 2018")
rep("FactScore giải quyết vấn đề này", "FActScore giải quyết vấn đề này")
rep("<w:t>*sinh*</w:t>", "<w:t>sinh</w:t>")
# NLI gloss (chong buzzword)
rep("thay người đọc bằng một mô hình NLI để xét xem",
    "thay người đọc bằng một mô hình NLI (Natural Language Inference — mô hình học chuyên phán định đoạn văn A có suy ra được câu B hay không) để xét xem")
# Harvard >=4 tac gia + tach 2023a/2023b cho hai nhom Gao
rep("Theo khảo sát của Gao và cộng sự (2023) chỉ ra hai điểm yếu",
    "Khảo sát của Gao và cộng sự (2023a) chỉ ra hai điểm yếu")
rep("(Gao, Yen, Yu và Chen, 2023)", "(Gao và cộng sự, 2023b)")

# ---- A8b: dao thu tu 'Nguon:' va caption 'Hinh 1.1'
paras = re.findall(r"<w:p[ >].*?</w:p>", xml, flags=re.S)
i_src = next(i for i, p in enumerate(paras) if "Nguồn: Tác giả đề xuất." in p)
i_cap = next(i for i, p in enumerate(paras) if "Quy trình giải trình hàng tháng tại doanh nghiệp quan sát" in p)
assert i_cap == i_src + 1, f"vi tri khong lien ke: src={i_src}, cap={i_cap}"
block = paras[i_src] + paras[i_cap]
assert xml.count(block) == 1
xml = xml.replace(block, paras[i_cap] + paras[i_src])

# ---- A3: chen lai muc 'Niem tin' truoc 'Khoang trong', doi so 2.3->2.4
paras = re.findall(r"<w:p[ >].*?</w:p>", xml, flags=re.S)
gap_head = next(p for p in paras if ".3. Khoảng trống nghiên cứu" in p)
body_tpl = next(p for p in paras if "Đặt ba dòng nghiên cứu cạnh nhau" in p)

def clone_para(tpl, text):
    m = re.match(r"(<w:p[ >].*?<w:pPr>.*?</w:pPr>)", tpl, flags=re.S)
    assert m, "khong tach duoc pPr"
    return (m.group(1)
            + '<w:r><w:t xml:space="preserve">' + text + "</w:t></w:r></w:p>")

trust_head = clone_para(gap_head, "2.3. Niềm tin và kiểm soát đối với hệ thống tự động")
trust_p1 = clone_para(body_tpl,
    "Dòng nghiên cứu thứ ba giải thích vì sao “hệ thống viết đúng” chưa đủ — còn cần “con người kiểm được”. Hiện tượng lạm dụng (misuse) đã nêu ở mục 1.2 là điểm xuất phát: khi đầu ra của máy có hình thức đáng tin và việc kiểm tra tốn công, con người chuyển sang phê duyệt mà không kiểm chứng, kể cả khi máy sai (Parasuraman và Riley, 1997). Lee và See (2004) bổ sung khái niệm hiệu chỉnh niềm tin: niềm tin phù hợp chỉ hình thành khi người dùng có thông tin để đánh giá đúng năng lực thật của hệ thống — thiếu thông tin đó, niềm tin hoặc thừa hoặc thiếu, và cả hai đều gây hại. Ở góc độ thiết kế, Doshi-Velez và Kim (2017) lập luận rằng khả năng giải thích trở thành yêu cầu bắt buộc khi hệ quả của sai sót lớn và việc đánh giá trực tiếp đầu ra khó khăn.")
trust_p2 = clone_para(body_tpl,
    "Áp vào bối cảnh tài chính, ba kết luận trên hội tụ thành một yêu cầu kiến trúc: cơ chế kiểm chứng phải được thiết kế sẵn trong hệ thống, thay vì trông đợi vào sự cảnh giác của người dùng. Nguyên tắc kiểm soát nội bộ của kế toán cũng vận hành đúng theo logic này — chứng từ, đối chiếu và phê duyệt tồn tại cho thiểu số trường hợp sai, không phải cho đa số trường hợp đúng. Một hệ thống AI tham gia báo cáo tài chính vì vậy cần được đối xử như một quy trình kế toán: mọi đầu ra truy vết được về nguồn, và dấu vết đó do cơ chế tất định tạo ra.")

assert xml.count(gap_head) == 1
xml = xml.replace(gap_head, trust_head + trust_p1 + trust_p2 + gap_head)
rep("<w:t>.3. Khoảng trống nghiên cứu</w:t>", "<w:t>.4. Khoảng trống nghiên cứu</w:t>")

io.open(P, "w", encoding="utf-8", newline="").write(xml)
print("ALL EDITS APPLIED")
