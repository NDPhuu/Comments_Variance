# Khung trình bày khóa luận + Danh mục tài liệu tham khảo (APA 7th)

> **Trạng thái:** cập nhật 04/10 — khung 5 chương (quyết định #7), bổ sung metric học thuật và dòng trust/XAI.
> **⚠ CHUẨN TRÍCH DẪN TRONG BẢN NỘP = HARVARD THEO VIỆN** (xem `docs/quy_dinh_vien.md` mục 3), KHÔNG phải APA. Danh mục dưới đây giữ định dạng APA làm **kho tra cứu nguồn** (đầy đủ DOI để verify); khi đưa vào khóa luận phải reformat sang mẫu Harvard của Viện, và "et al." đổi thành "cộng sự".
> **Cảnh báo trích dẫn:** các mục tham khảo dưới đây được ghi từ trí nhớ của Claude — các bài kinh điển có độ tin cao, nhưng **bắt buộc đối chiếu lại DOI/số trang/năm trên Google Scholar hoặc trang nhà xuất bản trước khi đưa vào khóa luận**. Tuyệt đối không cite bài chưa tự mở ra đọc ít nhất abstract + phần liên quan.

---

## 1. Khung chương khóa luận (mapping với DSRM)

Khóa luận dạng Design Science Research trình bày theo 6 hoạt động của DSRM (Peffers et al., 2007), gói trong **khung 5 chương chuẩn nghiên cứu** (đã chốt — quyết định #7):

| Chương | Nội dung | Hoạt động DSRM tương ứng | Viết draft ở |
|---|---|---|---|
| **1. Mở đầu** | Bối cảnh FP&A; vấn đề (hộp đen — theo `objectives.md`); mục tiêu; câu hỏi nghiên cứu; phạm vi; đóng góp; cấu trúc khóa luận | Problem identification & motivation | Phase 1 |
| **2. Cơ sở lý thuyết & Tổng quan nghiên cứu** | (a) Variance analysis & quy trình FP&A; (b) LLM, hallucination, RAG, numerical reasoning tài chính; (c) DSR, TTF, trust in automation/XAI; (d) **gap statement** 1 đoạn kết chương | (nền cho mọi bước) | Phase 2 |
| **3. Phương pháp nghiên cứu** | DSRM 6 bước → hoạt động cụ thể; thiết kế hệ thống (từ `docs/architecture.md`); thiết kế dữ liệu synthetic + gold labels; **evaluation protocol với metric học thuật có trích dẫn** (xem §3.5) + quy trình khách quan (chấm mù, Cohen's κ, ngưỡng đăng ký trước); đạo đức & bảo mật | Objectives + Design & development | Phase 1–2 |
| **4. Kết quả & Thảo luận** | Artifact hoàn chỉnh (walkthrough + screenshots); kết quả thực nghiệm 3 chế độ (bảng/hình sinh tự động); robustness theo kịch bản; thảo luận đối chiếu RQ và literature | Demonstration + Evaluation | Phase 3–4 |
| **5. Kết luận & Khuyến nghị** | Trả lời từng RQ; đóng góp học thuật & thực tiễn; hạn chế nói thật (synthetic, một bối cảnh, n nhỏ); khuyến nghị triển khai (gom kho bằng chứng); hướng phát triển | Communication | Phase 4–5 |

Nguyên tắc trình bày quan trọng với hội đồng:
- **Mỗi claim trong chương 5–6 phải trace về một con số hoặc một quan sát ở chương 5.** Khóa luận về "hệ thống chống unsupported claim" mà tự mình overclaim là tự bắn vào chân.
- Phân biệt rõ trong văn bản: *fact quan sát được* / *kết quả đo* / *suy luận* / *khuyến nghị* — đúng tinh thần evidence policy của chính artifact.
- Chương 2 viết theo luận điểm (argument-driven), không viết theo kiểu liệt kê từng bài báo.

## 2. Quy tắc trích dẫn APA 7th — tóm tắt thực dụng

**In-text:**
- 1 tác giả: (Davis, 1989) hoặc "Davis (1989) cho rằng…"
- 2 tác giả: (Goodhue & Thompson, 1995)
- ≥3 tác giả: (Peffers et al., 2007) — dùng "et al." ngay từ lần cite đầu
- Trích dẫn trực tiếp phải kèm số trang: (Hevner et al., 2004, p. 83)

**Reference list:** xếp alphabet theo họ tác giả đầu; hanging indent; tên journal và volume in nghiêng; có DOI thì luôn ghi dạng `https://doi.org/...`; bài arXiv chưa qua peer review ghi rõ là arXiv (và cân nhắc tìm bản đã công bố ở hội nghị để cite thay).

**Mẫu định dạng:**
- *Journal:* Họ, A. B., & Họ, C. D. (Năm). Tên bài viết thường. *Tên Journal, Volume*(Issue), trang–trang. https://doi.org/xxx
- *Hội nghị:* Họ, A. B. (Năm). Tên bài. In *Proceedings of …* (pp. xx–xx). Nhà xuất bản/ACL/IEEE. DOI
- *arXiv:* Họ, A. B. (Năm). *Tên bài* (arXiv:xxxx.xxxxx). arXiv. https://doi.org/10.48550/arXiv.xxxx.xxxxx
- *Sách:* Họ, A. B. (Năm). *Tên sách* (ấn bản thứ x). Nhà xuất bản.

## 3. Danh mục tài liệu khởi điểm (APA 7th) — theo dòng literature

### 3.1. Phương pháp — Design Science Research
- Gregor, S., & Hevner, A. R. (2013). Positioning and presenting design science research for maximum impact. *MIS Quarterly, 37*(2), 337–355. https://doi.org/10.25300/MISQ/2013/37.2.01
- Hevner, A. R., March, S. T., Park, J., & Ram, S. (2004). Design science in information systems research. *MIS Quarterly, 28*(1), 75–105. https://doi.org/10.2307/25148625
- Peffers, K., Tuunanen, T., Rothenberger, M. A., & Chatterjee, S. (2007). A design science research methodology for information systems research. *Journal of Management Information Systems, 24*(3), 45–77. https://doi.org/10.2753/MIS0742-1222240302
- Venable, J., Pries-Heje, J., & Baskerville, R. (2016). FEDS: A framework for evaluation in design science research. *European Journal of Information Systems, 25*(1), 77–89. https://doi.org/10.1057/ejis.2014.36

### 3.2. Khung chấp nhận & phù hợp công nghệ–tác vụ
- Davis, F. D. (1989). Perceived usefulness, perceived ease of use, and user acceptance of information technology. *MIS Quarterly, 13*(3), 319–340. https://doi.org/10.2307/249008
- Goodhue, D. L., & Thompson, R. L. (1995). Task-technology fit and individual performance. *MIS Quarterly, 19*(2), 213–236. https://doi.org/10.2307/249689
- Venkatesh, V., Morris, M. G., Davis, G. B., & Davis, F. D. (2003). User acceptance of information technology: Toward a unified view. *MIS Quarterly, 27*(3), 425–478. https://doi.org/10.2307/30036540

### 3.2b. Trust, automation và XAI (trục "hộp đen → hộp kính")
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
- Gao, T., Yen, H., Yu, J., & Chen, D. (2023). Enabling large language models to generate text with citations. In *Proceedings of EMNLP 2023* (pp. 6465–6488). Association for Computational Linguistics.
- Kamath, A., Jia, R., & Liang, P. (2020). Selective question answering under domain shift. In *Proceedings of ACL 2020* (pp. 5684–5696). Association for Computational Linguistics.
- Manning, C. D., Raghavan, P., & Schütze, H. (2008). *Introduction to information retrieval*. Cambridge University Press.
- Rajpurkar, P., Jia, R., & Liang, P. (2018). Know what you don't know: Unanswerable questions for SQuAD. In *Proceedings of ACL 2018* (pp. 784–789). Association for Computational Linguistics.
- Rashkin, H., Nikolaev, D., Lamm, M., Aroyo, L., Collins, M., Das, D., Petrov, S., Tomar, G. S., Turc, I., & Reitter, D. (2023). Measuring attribution in natural language generation models. *Computational Linguistics, 49*(4), 777–840. https://doi.org/10.1162/coli_a_00486
- Es, S., James, J., Espinosa-Anke, L., & Schockaert, S. (2024). RAGAs: Automated evaluation of retrieval augmented generation. In *Proceedings of the 18th Conference of the European Chapter of the Association for Computational Linguistics: System Demonstrations* (pp. 150–158). Association for Computational Linguistics.
- Min, S., Krishna, K., Lyu, X., Lewis, M., Yih, W., Koh, P. W., Iyyer, M., Zettlemoyer, L., & Hajishirzi, H. (2023). FActScore: Fine-grained atomic evaluation of factual precision in long form text generation. In *Proceedings of EMNLP 2023* (pp. 12076–12100). Association for Computational Linguistics.
- Zheng, L., Chiang, W.-L., Sheng, Y., Zhuang, S., Wu, Z., Zhuang, Y., Lin, Z., Li, Z., Li, D., Xing, E. P., Zhang, H., Gonzalez, J. E., & Stoica, I. (2023). Judging LLM-as-a-judge with MT-Bench and Chatbot Arena. In *Advances in Neural Information Processing Systems 36*.
- (Nếu đo workload) Hart, S. G., & Staveland, L. E. (1988). Development of NASA-TLX (Task Load Index): Results of empirical and theoretical research. In P. A. Hancock & N. Meshkati (Eds.), *Human mental workload* (pp. 139–183). North-Holland. https://doi.org/10.1016/S0166-4115(08)62386-9

### 3.6. Domain — kế toán quản trị, FP&A, variance analysis
- Datar, S. M., & Rajan, M. V. (2021). *Horngren's cost accounting: A managerial emphasis* (17th ed.). Pearson. [các chương flexible budgets & variance analysis — nền định nghĩa variance chuẩn]
- Robertson, S., & Zaragoza, H. (2009). The probabilistic relevance framework: BM25 and beyond. *Foundations and Trends in Information Retrieval, 3*(4), 333–389. https://doi.org/10.1561/1500000019 [chỉ cần nếu giữ retrieval phi cấu trúc]

### 3.7. Cần tự tìm thêm (chưa có citation đáng tin từ trí nhớ — tìm trên Google Scholar)
- AI/automation trong kế toán quản trị và FP&A: tìm từ khóa `"generative AI" management accounting`, `LLM "variance analysis"`, `AI "financial reporting" narrative` trong *Journal of Management Accounting Research*, *Accounting Horizons*, *International Journal of Accounting Information Systems* (nhóm Vasarhelyi về continuous auditing/automation là một mạch đáng xem).
- Narrative/commentary generation từ dữ liệu bảng: từ khóa `data-to-text generation financial`, `table-to-text faithfulness`.
- Nếu giữ hướng trust/verification: `human-AI trust verification`, `appropriate reliance on AI`.

## 4. Chiến lược review literature (3 dòng, mỗi dòng trả lời 1 câu)

1. **Dòng domain (FP&A/variance):** variance analysis là bài toán gì, quy trình chuẩn ra sao, đã được tự động hóa đến đâu → để chứng minh vấn đề có thật và gap nằm ở khâu giải trình.
2. **Dòng kỹ thuật (LLM/RAG/numerical reasoning):** vì sao LLM thuần không đáng tin với số liệu tài chính (FinQA/TAT-QA/PoT), các cơ chế grounding hiện có và hạn chế → để biện minh kiến trúc calculate-then-narrate + verification.
3. **Dòng phương pháp & đánh giá (DSR/TTF/evaluation):** cách xây và đánh giá một artifact IS cho nghiêm túc → để khóa luận có xương sống học thuật thay vì chỉ là build log.

Research gap được phát biểu ở GIAO của 3 dòng: *các cơ chế grounding tổng quát chưa được thiết kế/đánh giá cho tác vụ sinh giải trình variance trong quy trình FP&A thực, nơi mọi con số phải khớp tuyệt đối với sổ sách và mọi nhận định nguyên nhân phải truy vết được về bằng chứng.*
