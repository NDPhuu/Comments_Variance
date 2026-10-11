# Khung trình bày khóa luận + Danh mục tài liệu tham khảo (APA 7th)

> **Trạng thái:** cập nhật 04/10 — khung 5 chương (quyết định #7), bổ sung metric học thuật và dòng trust/XAI.
> **⚠ CHUẨN TRÍCH DẪN TRONG BẢN NỘP = HARVARD THEO VIỆN** (xem `docs/quy_dinh_vien.md` mục 3), KHÔNG phải APA. Danh mục dưới đây giữ định dạng APA làm **kho tra cứu nguồn** (đầy đủ DOI để verify); khi đưa vào khóa luận phải reformat sang mẫu Harvard của Viện, và "et al." đổi thành "cộng sự".
> **Cảnh báo trích dẫn:** các mục tham khảo dưới đây được ghi từ trí nhớ của Claude — các bài kinh điển có độ tin cao, nhưng **bắt buộc đối chiếu lại DOI/số trang/năm trên Google Scholar hoặc trang nhà xuất bản trước khi đưa vào khóa luận**. Tuyệt đối không cite bài chưa tự mở ra đọc ít nhất abstract + phần liên quan.

---

## 1. Khung chương khóa luận

Khóa luận là **nghiên cứu ứng dụng**: vận dụng kiến thức RAG/NLP để giải quyết vấn đề của doanh nghiệp, theo quy trình 4 bước (khảo sát vấn đề → xác định yêu cầu → thiết kế & xây dựng → đánh giá thực nghiệm), trình bày trong **khung 5 chương** theo kết cấu bắt buộc của Viện:

| Chương | Nội dung | Viết draft ở |
|---|---|---|
| **1. Giới thiệu** | Bối cảnh FP&A; vấn đề (hộp đen — theo `objectives.md`); mục tiêu; câu hỏi nghiên cứu + giả thuyết; phạm vi; đóng góp; cấu trúc khóa luận | Phase 1 ✔ |
| **2. Tổng quan nghiên cứu** | (a) Variance analysis & quy trình FP&A; (b) LLM, hallucination, RAG, numerical reasoning tài chính; (c) trust in automation & XAI; (d) **gap statement** 1 đoạn kết chương | Phase 2 |
| **3. Phương pháp nghiên cứu** | **3.1 Dữ liệu** (phân tích 17 giải trình thật → các loại nguyên nhân + khuôn viết; bộ dữ liệu giả lập 5 khu × 12 tháng, 12 loại tình huống gieo sẵn, mỗi tình huống có đáp án: nguyên nhân thật, tài liệu chứng minh, các câu giải thích sai AI hay bịa; bảng mô tả bộ dữ liệu) · **3.2 Mô hình & Kiến trúc** (bài toán vào/ra; 4 khối: tính số bằng code thường → tìm tài liệu đúng khu đúng kỳ, theo từ khóa + theo nghĩa → AI viết theo khuôn kèm trích dẫn → máy soát từng số/trích dẫn, thiếu bằng chứng thì từ chối) · **3.3 Cơ chế đánh giá** (5 thước đo theo chuẩn nghiên cứu trước — §3.5; chấm công bằng: đáp án chốt trước khi AI làm bài, người chấm không biết bài của cấu hình nào, so máy chấm với người chấm tay, mức đạt thống nhất trước với GVHD) · **3.4 Thiết lập** (3 cấu hình cùng model; mỗi tình huống chạy 3 lần lấy trung bình; dữ liệu sinh lại được y hệt; FastAPI + React) — KHUNG CHỐT 07/10 theo người thực hiện | Phase 1–2 |
| **4. Kết quả nghiên cứu** | **4.1 Kết quả chính** (bảng điểm 3 cấu hình × 5 thước đo + hình; đi trọn một tình huống làm ví dụ) · **4.2 Kiểm định tính vững** (tách kết quả theo loại tình huống; các tình huống cố tình làm khó: không có tài liệu liên quan — xem có dám từ chối không, tài liệu nhiễu trùng từ khóa sai khu, bộ lỗi gieo cố ý; kết quả so máy chấm với người chấm) · **4.3 Thảo luận** (kết quả nói gì về 3 giả thuyết; giống/khác nghiên cứu trước; hạn chế) — KHUNG CHỐT 07/10 | Phase 3–4 |
| **5. Kết luận & Khuyến nghị** | Trả lời từng RQ; đóng góp học thuật & thực tiễn; hạn chế nói thật (synthetic, một bối cảnh, n nhỏ); khuyến nghị triển khai cho doanh nghiệp (gom kho bằng chứng); hướng phát triển | Phase 4–5 |

Nguyên tắc trình bày quan trọng với hội đồng:
- **Mỗi claim trong chương 5–6 phải trace về một con số hoặc một quan sát ở chương 5.** Khóa luận về "hệ thống chống unsupported claim" mà tự mình overclaim là tự bắn vào chân.
- Phân biệt rõ trong văn bản: *fact quan sát được* / *kết quả đo* / *suy luận* / *khuyến nghị* — đúng tinh thần evidence policy của chính artifact.
- Chương 2 viết theo luận điểm (argument-driven), không viết theo kiểu liệt kê từng bài báo.

## 2. Quy tắc trích dẫn APA 7th — tóm tắt thực dụng

**In-text:**
- 1 tác giả: (Cohen, 1960) hoặc "Cohen (1960) cho rằng…"
- 2 tác giả: (Lee & See, 2004)
- ≥3 tác giả: (Chen et al., 2021) — dùng "et al." ngay từ lần cite đầu
- Trích dẫn trực tiếp phải kèm số trang: (Lee & See, 2004, p. 53)
- ⚠ Trong BẢN NỘP tiếng Việt dùng mẫu Harvard của Viện: "và cộng sự" thay "et al.", "và" thay "&" (xem `docs/quy_dinh_vien.md` §3)

**Reference list:** xếp alphabet theo họ tác giả đầu; hanging indent; tên journal và volume in nghiêng; có DOI thì luôn ghi dạng `https://doi.org/...`; bài arXiv chưa qua peer review ghi rõ là arXiv (và cân nhắc tìm bản đã công bố ở hội nghị để cite thay).

**Mẫu định dạng:**
- *Journal:* Họ, A. B., & Họ, C. D. (Năm). Tên bài viết thường. *Tên Journal, Volume*(Issue), trang–trang. https://doi.org/xxx
- *Hội nghị:* Họ, A. B. (Năm). Tên bài. In *Proceedings of …* (pp. xx–xx). Nhà xuất bản/ACL/IEEE. DOI
- *arXiv:* Họ, A. B. (Năm). *Tên bài* (arXiv:xxxx.xxxxx). arXiv. https://doi.org/10.48550/arXiv.xxxx.xxxxx
- *Sách:* Họ, A. B. (Năm). *Tên sách* (ấn bản thứ x). Nhà xuất bản.

## 3. Danh mục tài liệu khởi điểm (APA 7th) — theo dòng literature

### 3.1. Trust, automation và XAI (trục "hộp đen → hộp kính")
- Doshi-Velez, F., & Kim, B. (2017). *Towards a rigorous science of interpretable machine learning* (arXiv:1702.08608). arXiv. https://doi.org/10.48550/arXiv.1702.08608
- Lee, J. D., & See, K. A. (2004). Trust in automation: Designing for appropriate reliance. *Human Factors, 46*(1), 50–80. https://doi.org/10.1518/hfes.46.1.50_30392
- Parasuraman, R., & Riley, V. (1997). Humans and automation: Use, misuse, disuse, abuse. *Human Factors, 39*(2), 230–253. https://doi.org/10.1518/001872097778543886

### 3.3. LLM, RAG và grounding
- Asai, A., Wu, Z., Wang, Y., Sil, A., & Hajishirzi, H. (2024). Self-RAG: Learning to retrieve, generate, and critique through self-reflection. In *The Twelfth International Conference on Learning Representations (ICLR)*. (bản arXiv:2310.11511)
- Gao, Y., Xiong, Y., Gao, X., Jia, K., Pan, J., Bi, Y., Dai, Y., Sun, J., Wang, M., & Wang, H. (2023). *Retrieval-augmented generation for large language models: A survey* (arXiv:2312.10997). arXiv. https://doi.org/10.48550/arXiv.2312.10997
- Ji, Z., Lee, N., Frieske, R., Yu, T., Su, D., Xu, Y., Ishii, E., Bang, Y. J., Madotto, A., & Fung, P. (2023). Survey of hallucination in natural language generation. *ACM Computing Surveys, 55*(12), Article 248. https://doi.org/10.1145/3571730
- Lewis, P., Perez, E., Piktus, A., Petroni, F., Karpukhin, V., Goyal, N., Küttler, H., Lewis, M., Yih, W., Rocktäschel, T., Riedel, S., & Kiela, D. (2020). Retrieval-augmented generation for knowledge-intensive NLP tasks. *Advances in Neural Information Processing Systems, 33*, 9459–9474.
- Yan, S.-Q., Gu, J.-C., Zhu, Y., & Ling, Z.-H. (2024). *Corrective retrieval augmented generation* (arXiv:2401.15884). arXiv. https://doi.org/10.48550/arXiv.2401.15884

### 3.4. Numerical reasoning trên dữ liệu tài chính (lập luận "LLM không được tự tính số")
- Chen, W., Ma, X., Wang, X., & Cohen, W. W. (2023). Program of thoughts prompting: Disentangling computation from reasoning for numerical reasoning tasks. *Transactions on Machine Learning Research*. (bản arXiv:2211.12588)
- Chen, Z., Chen, W., Smiley, C., Shah, S., Borova, I., Langdon, D., Moussa, R., Beane, M., Huang, T.-H., Routledge, B., & Wang, W. Y. (2021). FinQA: A dataset of numerical reasoning over financial data. In *Proceedings of the 2021 Conference on Empirical Methods in Natural Language Processing* (pp. 3697–3711). Association for Computational Linguistics. https://doi.org/10.18653/v1/2021.emnlp-main.300
- Zhu, F., Lei, W., Huang, Y., Wang, C., Zhang, S., Lv, J., Feng, F., & Chua, T.-S. (2021). TAT-QA: A question answering benchmark on a hybrid of tabular and textual content in finance. In *Proceedings of ACL-IJCNLP 2021* (pp. 3277–3287). Association for Computational Linguistics. https://doi.org/10.18653/v1/2021.acl-long.254

### 3.5. Đánh giá hệ thống sinh văn bản — METRIC HỌC THUẬT CHO CHƯƠNG ĐÁNH GIÁ

> Mỗi chỉ số của đề tài phải được định nghĩa theo một chuẩn đã công bố, KHÔNG tự chế. Bảng mapping:
>
> | Chỉ số của đề tài | Tên học thuật | Nguồn định nghĩa |
> |---|---|---|
> | Số khớp sổ | Numerical exact match (EM) | FinQA (Chen et al., 2021); TAT-QA (Zhu et al., 2021) |
> | Trích dẫn đúng tài liệu | Citation precision / citation recall | ALCE (Gao, Yen, et al., 2023) |
> | Câu có căn cứ | Attribution / AIS; faithfulness; atomic-fact precision | Rashkin et al. (2023); RAGAS (Es et al., 2024); FActScore (Min et al., 2023) |
> | Tìm đúng tài liệu | Precision@k, Recall@k, MRR, nDCG | Manning et al. (2008) |
> | Từ chối đúng lúc | Answerability / selective prediction | SQuAD 2.0 (Rajpurkar et al., 2018); Kamath et al. (2020) |
> | Độ tin của máy chấm | Cohen's κ (đồng thuận máy–người) | Cohen (1960) |

- Cohen, J. (1960). A coefficient of agreement for nominal scales. *Educational and Psychological Measurement, 20*(1), 37–46. https://doi.org/10.1177/001316446002000104
- Gao, T., Yen, H., Yu, J., & Chen, D. (2023). Enabling large language models to generate text with citations. In *Proceedings of EMNLP 2023*. Association for Computational Linguistics. ✓ <https://aclanthology.org/2023.emnlp-main.398> · arXiv: <https://arxiv.org/abs/2305.14627>
- Kamath, A., Jia, R., & Liang, P. (2020). Selective question answering under domain shift. In *Proceedings of ACL 2020* (pp. 5684–5696). Association for Computational Linguistics. ✓ <https://aclanthology.org/2020.acl-main.503>
- Manning, C. D., Raghavan, P., & Schütze, H. (2008). *Introduction to information retrieval*. Cambridge University Press.
- Rajpurkar, P., Jia, R., & Liang, P. (2018). Know what you don't know: Unanswerable questions for SQuAD. In *Proceedings of ACL 2018* (pp. 784–789). Association for Computational Linguistics.
- Rashkin, H., Nikolaev, D., Lamm, M., Aroyo, L., Collins, M., Das, D., Petrov, S., Tomar, G. S., Turc, I., & Reitter, D. (2023). Measuring attribution in natural language generation models. *Computational Linguistics, 49*(4), 777–840. https://doi.org/10.1162/coli_a_00486
- Wen, B., Yao, J., Feng, S., Xu, C., Tsvetkov, Y., Howe, B., & Wang, L. L. (2025). Know your limits: A survey of abstention in large language models. *Transactions of the Association for Computational Linguistics, 13*. https://doi.org/10.1162/tacl_a_00754 ✓ <https://aclanthology.org/2025.tacl-1.26> — tổng quan đánh giá abstention; "abstention accuracy" của đề tài = recall của lớp phải-từ-chối (tên do đề tài đặt, định nghĩa tường minh ở 3.3), báo kèm coverage–risk
- Es, S., James, J., Espinosa-Anke, L., & Schockaert, S. (2024). RAGAs: Automated evaluation of retrieval augmented generation. In *Proceedings of the 18th Conference of the European Chapter of the Association for Computational Linguistics: System Demonstrations* (pp. 150–158). Association for Computational Linguistics.
- Min, S., Krishna, K., Lyu, X., Lewis, M., Yih, W., Koh, P. W., Iyyer, M., Zettlemoyer, L., & Hajishirzi, H. (2023). FActScore: Fine-grained atomic evaluation of factual precision in long form text generation. In *Proceedings of EMNLP 2023*. Association for Computational Linguistics. ✓ <https://aclanthology.org/2023.emnlp-main.741> · arXiv: <https://arxiv.org/abs/2305.14251>
- Zheng, L., Chiang, W.-L., Sheng, Y., Zhuang, S., Wu, Z., Zhuang, Y., Lin, Z., Li, Z., Li, D., Xing, E. P., Zhang, H., Gonzalez, J. E., & Stoica, I. (2023). Judging LLM-as-a-judge with MT-Bench and Chatbot Arena. In *Advances in Neural Information Processing Systems 36*.
- (Nếu đo workload) Hart, S. G., & Staveland, L. E. (1988). Development of NASA-TLX (Task Load Index): Results of empirical and theoretical research. In P. A. Hancock & N. Meshkati (Eds.), *Human mental workload* (pp. 139–183). North-Holland. https://doi.org/10.1016/S0166-4115(08)62386-9

### 3.6. Domain — kế toán quản trị, FP&A, variance analysis
- Datar, S. M., & Rajan, M. V. (2021). *Horngren's cost accounting: A managerial emphasis* (17th ed.). Pearson. [các chương flexible budgets & variance analysis — nền định nghĩa variance chuẩn]
- Robertson, S., & Zaragoza, H. (2009). The probabilistic relevance framework: BM25 and beyond. *Foundations and Trends in Information Retrieval, 3*(4), 333–389. https://doi.org/10.1561/1500000019 [chỉ cần nếu giữ retrieval phi cấu trúc]

### 3.7. Cần tự tìm thêm (chưa có citation đáng tin từ trí nhớ — tìm trên Google Scholar)
- AI/automation trong kế toán quản trị và FP&A: tìm từ khóa `"generative AI" management accounting`, `LLM "variance analysis"`, `AI "financial reporting" narrative` trong *Journal of Management Accounting Research*, *Accounting Horizons*, *International Journal of Accounting Information Systems* (nhóm Vasarhelyi về continuous auditing/automation là một mạch đáng xem).
- Narrative/commentary generation từ dữ liệu bảng: từ khóa `data-to-text generation financial`, `table-to-text faithfulness`.
- Nếu giữ hướng trust/verification: `human-AI trust verification`, `appropriate reliance on AI`.

### 3.7. Nguồn số liệu thực tiễn cho Chương 1 (✓ = đã verify 04/10/2026; khi đưa vào luận reformat theo mẫu Harvard điện tử của Viện)
- ✓ CBRE Việt Nam (2026), *Hanoi Real Estate Market Figures Q2 2026*, CBRE Research — **nguồn sơ cấp**, bản PDF trong `materials/` (bản quyền CBRE, không công bố lại file). Số dùng: GDP 6T/2026 +8,18%; FDI 34,65 tỷ USD (+61%); hấp thụ đất KCN miền Bắc 217 ha Q2; lấp đầy 81,3%; RBF 82,7%, 5,1 USD/m²/tháng.
- ✓ CBRE Việt Nam (2026), *Ho Chi Minh City Real Estate Market Figures Q2 2026*, CBRE Research — nguồn sơ cấp, PDF trong `materials/`. Số dùng: hấp thụ đất KCN miền Nam H1 124 ha (+125% y-o-y); RBF 91%, 5,2 USD/m²/tháng.
- ✓ Gartner (2025), *Gartner Survey Shows Finance AI Adoption Remains Steady in 2025*, truy cập ngày 04/10/2026, <https://www.gartner.com/en/newsroom/press-releases/2025-11-18-gartner-survey-shows-finance-ai-adoption-remains-steady-in-2025>. Số dùng: 59% (2025) ← 58% (2024) ← 37% (2023), n = 183 CFO.
- (Dự phòng) McKinsey & Company (2025), *The state of AI*, truy cập ngày 04/10/2026, <https://www.mckinsey.com/featured-insights/charts/ai-at-work-but-not-at-scale>.
- ✓ Gartner (2024), *Gartner Survey Shows 66% of Finance Leaders Think Generative AI Will Have Most Immediate Impact on Explaining Forecast and Budget Variances*, công bố 27/06/2024, truy cập ngày 11/10/2026, <https://www.gartner.com/en/newsroom/press-releases/2024-06-27-gartner-survey-shows-66-of-finance-leaders-think-generative-ai-will-have-most-immediate-impact-on-explaining-forecast-and-budget-variances1>. Số dùng (C2 §2.1): 66% xếp "giải trình chênh lệch dự báo/ngân sách" vào **top-3** use case GenAI tác động nhất (26% xếp hạng NHẤT — không viết quá thành "đa số chọn hàng đầu"); kế tiếp: phân loại dữ liệu thu/chi 44%, báo cáo quản trị 34%; n = 100 finance leaders, khảo sát 11/2023. Verify 11/10/2026: trang gốc chặn bot (Cloudflare) — xác nhận bằng tiêu đề/URL trên gartner.com + 2 nguồn thứ cấp khớp số (CDO Magazine 28/06/2024; CFO Brew 27/06/2024). Trước khi nộp: tác giả mở link bằng browser đối chiếu nguyên văn lần cuối.

### 3.8. Trạng thái verify 4 nguồn học thuật đang dùng ở Chương 1 (04/10/2026)
- ✓ Parasuraman & Riley (1997) — *Human Factors*, 39(2), 230–253.
- ✓ Lee & See (2004) — *Human Factors*, 46(1), 50–80, <https://journals.sagepub.com/doi/10.1518/hfes.46.1.50_30392>.
- ✓ Chen et al. (2021) FinQA — <https://aclanthology.org/2021.emnlp-main.300>.
- ✓ Zhu et al. (2021) TAT-QA — <https://aclanthology.org/2021.acl-long.254>.

## 4. Chiến lược review literature (3 dòng, mỗi dòng trả lời 1 câu)

1. **Dòng domain (FP&A/variance):** variance analysis là bài toán gì, quy trình chuẩn ra sao, đã được tự động hóa đến đâu → để chứng minh vấn đề có thật và gap nằm ở khâu giải trình.
2. **Dòng kỹ thuật (LLM/RAG/numerical reasoning):** vì sao LLM thuần không đáng tin với số liệu tài chính (FinQA/TAT-QA/PoT), các cơ chế grounding hiện có và hạn chế → để biện minh kiến trúc calculate-then-narrate + verification.
3. **Dòng đánh giá hệ thống sinh văn bản (evaluation):** cách literature RAG/NLP đo grounding, citation và abstention (AIS, ALCE, FActScore; abstention: SQuAD 2.0, Kamath, Wen) → để chương phương pháp và chương kết quả có chuẩn mực đo lường được thừa nhận, thay vì chỉ là build log. (RAGAS đã BỎ khỏi C2 theo quyết định 11/10 — không nhắc trong luận; ref Es et al. giữ trong kho làm tư liệu.)

Research gap được phát biểu ở GIAO của 3 dòng: *các cơ chế grounding tổng quát chưa được thiết kế/đánh giá cho tác vụ sinh giải trình variance trong quy trình FP&A thực, nơi mọi con số phải khớp tuyệt đối với sổ sách và mọi nhận định nguyên nhân phải truy vết được về bằng chứng.*
