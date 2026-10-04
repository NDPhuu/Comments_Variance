# Khung trình bày khóa luận + Danh mục tài liệu tham khảo (APA 7th)

> **Trạng thái:** bản khởi điểm, sẽ tinh chỉnh sau khi chốt scope ở Round 1–2.
> **Cảnh báo trích dẫn:** các mục tham khảo dưới đây được ghi từ trí nhớ của Claude — các bài kinh điển có độ tin cao, nhưng **bắt buộc đối chiếu lại DOI/số trang/năm trên Google Scholar hoặc trang nhà xuất bản trước khi đưa vào khóa luận**. Tuyệt đối không cite bài chưa tự mở ra đọc ít nhất abstract + phần liên quan.

---

## 1. Khung chương khóa luận (mapping với DSRM)

Khóa luận dạng Design Science Research trình bày tự nhiên theo 6 hoạt động của DSRM (Peffers et al., 2007). Khung 6 chương chuẩn:

| Chương | Nội dung | Hoạt động DSRM tương ứng |
|---|---|---|
| **1. Giới thiệu** | Bối cảnh FP&A; vấn đề nghiên cứu (định nghĩa bằng chi phí/thời gian/lỗi, không phải "chưa có AI"); mục tiêu; câu hỏi nghiên cứu; phạm vi; đóng góp dự kiến; cấu trúc khóa luận | Problem identification & motivation |
| **2. Cơ sở lý thuyết & Tổng quan nghiên cứu** | (a) Variance analysis trong kế toán quản trị & quy trình FP&A; (b) LLM, grounding, hallucination; RAG và các biến thể; numerical reasoning trên dữ liệu tài chính; (c) DSR và TTF làm khung; (d) **research gap** — kết thúc chương bằng gap statement 1 đoạn | (nền cho mọi bước) |
| **3. Phương pháp nghiên cứu** | DSRM 6 bước → mapping sang hoạt động cụ thể của đề tài; chiến lược đánh giá (FEDS — Venable et al., 2016); thiết kế dữ liệu (synthetic + doanh nghiệp ẩn danh); đạo đức & bảo mật dữ liệu | Objectives of a solution |
| **4. Thiết kế và xây dựng Artifact** | Yêu cầu thiết kế (từ chẩn đoán quy trình); kiến trúc; design principles (dạng "nếu muốn X trong bối cảnh Y thì thiết kế Z vì W"); implementation; ví dụ walkthrough một Variance Case | Design & development + Demonstration |
| **5. Đánh giá** | Technical evaluation (benchmark, metrics tự động); expert evaluation (chấm mù); kết quả case study; phân tích robustness; thảo luận — đối chiếu lại RQ và literature | Evaluation |
| **6. Kết luận** | Đóng góp học thuật & thực tiễn; hạn chế (nói thật: n nhỏ, một doanh nghiệp, synthetic bias); hướng phát triển | Communication |

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

### 3.5. Đánh giá hệ thống sinh văn bản
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
