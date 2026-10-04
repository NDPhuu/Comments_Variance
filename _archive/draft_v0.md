# Research Review Brief: Evidence-Grounded FP&A Copilot

## Cách sử dụng tài liệu này

Gửi toàn bộ tài liệu này cho một AI khác và yêu cầu AI thực hiện phần **Nhiệm vụ phản biện** ở cuối. Tài liệu được thiết kế để AI có đủ bối cảnh nhưng không mặc định rằng ý tưởng hiện tại là đúng.

Không cung cấp dữ liệu, tên doanh nghiệp, tên khách hàng, nhà cung cấp, dự án hoặc số liệu tài chính mật cho AI bên ngoài khi chưa được doanh nghiệp cho phép.

---

## 1. Bối cảnh người thực hiện

Người thực hiện là sinh viên FinTech, có kiến thức về tài chính doanh nghiệp, econometrics và data analytics; kỹ năng Python và Excel ở mức trung cấp. Người thực hiện hiện có trải nghiệm thực tập FP&A trong lĩnh vực bất động sản công nghiệp.

Đây là đề tài thực tập tốt nghiệp. Sản phẩm phải đồng thời:

1. Có cơ sở nghiên cứu và phương pháp đánh giá rõ ràng.
2. Giải quyết một vấn đề FP&A thực tế.
3. Có thể xây dựng trong nguồn lực của một sinh viên.
4. Có bằng chứng về tính hữu ích, không chỉ là một bản demo AI.
5. Không phụ thuộc vào việc huấn luyện một foundation model mới.
6. Bảo vệ được dữ liệu và quy trình nội bộ của doanh nghiệp.

---

## 2. Tên đề tài dự kiến

### Tiếng Việt

**Thiết kế và Đánh giá Hệ thống FP&A Copilot dựa trên Hybrid RAG hỗ trợ Phân tích Chênh lệch Ngân sách–Thực tế: Nghiên cứu Tình huống tại Doanh nghiệp Bất động sản Công nghiệp**

### Tiếng Anh

**Designing and Evaluating a Hybrid RAG-based FP&A Copilot for Budget–Actual Variance Analysis: A Case Study in Industrial Real Estate**

Tên gọi thay thế có thể sử dụng nếu cần nhấn mạnh khả năng kiểm chứng:

**Designing and Evaluating an Evidence-Grounded FP&A Copilot for Budget–Actual Variance Analysis in Industrial Real Estate**

---

## 3. Vấn đề nghiên cứu dự kiến

Trong quy trình monthly performance review, FP&A thường phải:

1. Tổng hợp Budget, Actual và Forecast.
2. Tính toán chênh lệch.
3. Xác định các khoản mục trọng yếu.
4. Drill down theo property, cost center, GL account, vendor hoặc transaction.
5. Tìm invoice, purchase order, work order và supporting documents.
6. Trao đổi với business owner để xác nhận nguyên nhân.
7. Viết variance commentary.
8. Chỉnh sửa theo review của cấp quản lý.

Các pain point giả định gồm dữ liệu phân tán, công việc lặp lại, thời gian tìm evidence, commentary không nhất quán và khó truy ngược nhận định về nguồn. Tuy nhiên, đây mới là giả định. Nghiên cứu phải đo quy trình hiện tại để xác nhận hoặc bác bỏ những pain point này.

Vấn đề không được định nghĩa là “doanh nghiệp chưa có AI”. Vấn đề cần được định nghĩa bằng chi phí, thời gian, lỗi, rework, độ trễ hoặc chất lượng quyết định trong quy trình FP&A hiện tại.

---

## 4. Mục tiêu nghiên cứu

### Mục tiêu tổng quát

Thiết kế và đánh giá một hệ thống hỗ trợ FP&A trong việc phát hiện, điều tra và soạn thảo giải trình cho các chênh lệch Budget–Actual trọng yếu, kết hợp deterministic financial analytics với evidence-grounded generation.

### Mục tiêu cụ thể

1. Chẩn đoán quy trình Budget–Actual Variance Analysis hiện tại.
2. Xác định yêu cầu thiết kế và kiểm soát của hệ thống AI.
3. Thiết kế artifact theo Design Science Research Methodology.
4. Tách biệt calculation, evidence retrieval và language generation.
5. Xây dựng synthetic benchmark có thể công khai.
6. Đánh giá artifact trên tập dữ liệu doanh nghiệp đã được phép sử dụng và ẩn danh.
7. So sánh proposed system với quy trình thủ công, LLM-only và vanilla RAG.
8. Đánh giá technical performance, operational usefulness và Task–Technology Fit.

---

## 5. Scope dự kiến

### Trong scope

- Monthly Budget–Actual Variance Analysis.
- Operating expenses, gọi tắt là OPEX.
- Cấp phân tích: period × property/site × cost center × GL account.
- Materiality detection.
- Contribution analysis và drill-down.
- Retrieval supporting evidence từ tài liệu phi cấu trúc.
- Draft variance commentary có citation.
- Numeric verification, citation verification và human approval.
- Nghiên cứu tình huống trong bất động sản công nghiệp.

### Ngoài scope của MVP

- Toàn bộ P&L, balance sheet và cash flow.
- Financial forecasting.
- Tự động ra quyết định quản trị.
- Chatbot hỏi đáp mọi chủ đề tài chính.
- Fine-tuning một foundation model mới.
- Tự động gửi email hoặc làm việc thay business owner.
- Kết nối trực tiếp ERP ở phiên bản nghiên cứu ban đầu.
- Tự động phê duyệt hoặc đăng số liệu.
- Khẳng định quan hệ nhân quả khi không có evidence.

### Giả định scope cần được phản biện

OPEX hiện được chọn vì dữ liệu transaction-level và cost-center thường có khả năng tiếp cận hơn dữ liệu driver của doanh thu. Tuy nhiên, nếu doanh nghiệp không có supporting evidence hoặc root-cause labels, claim “giải thích nguyên nhân” có thể phải giảm xuống “phát hiện và hỗ trợ điều tra chênh lệch”.

---

## 6. Câu hỏi nghiên cứu dự kiến

**RQ1 — Problem diagnosis**  
Những hạn chế nào trong quy trình Budget–Actual Variance Analysis hiện tại tạo ra nhu cầu đối với một hệ thống AI hỗ trợ?

**RQ2 — Artifact design**  
Hệ thống cần được thiết kế như thế nào để kết hợp dữ liệu tài chính có cấu trúc và evidence phi cấu trúc một cách chính xác, có thể kiểm chứng và phù hợp với quy trình FP&A?

**RQ3 — Technical effectiveness**  
Hybrid analytical RAG có cải thiện factual accuracy, citation accuracy và unsupported-claim rate so với LLM-only và vanilla RAG không?

**RQ4 — Operational usefulness**  
Hệ thống có giảm thời gian và công sức thực hiện variance analysis mà không làm giảm chất lượng kết quả không?

**RQ5 — User and task fit**  
Người làm FP&A đánh giá như thế nào về Task–Technology Fit, trust, ease of verification và intention to use của hệ thống?

---

## 7. Nền tảng lý thuyết và nghiên cứu dự kiến

### Framework nghiên cứu chính

**Design Science Research Methodology — DSRM**

1. Problem identification and motivation.
2. Define objectives for a solution.
3. Design and development.
4. Demonstration.
5. Evaluation.
6. Communication.

### Framework đánh giá mức độ phù hợp với công việc

**Task–Technology Fit — TTF**

Công nghệ chỉ tạo ra performance impact khi khả năng của công nghệ phù hợp với yêu cầu của tác vụ và được người dùng thực sự sử dụng.

### Nền tảng AI dự kiến tham khảo

- Retrieval-Augmented Generation.
- Hybrid retrieval.
- Self-RAG như một nguồn design principle về retrieval-on-demand và self-reflection.
- Corrective RAG như một nguồn design principle về retrieval validation.
- RAGAS hoặc các framework tương tự để tham khảo đánh giá retrieval và generation.
- FinQA và TAT-QA để củng cố lập luận rằng numerical financial reasoning cần symbolic or programmatic execution.

Nghiên cứu không tuyên bố phát minh một mô hình RAG mới. Đóng góp dự kiến nằm ở domain-specific architecture, design principles, evaluation protocol và bằng chứng thực địa.

---

## 8. Product concept

Product được định vị là **Variance Investigation and Commentary Workbench**, không phải chatbot tài chính tổng quát.

Đối tượng trung tâm của hệ thống là một **Variance Case**:

```text
Reporting cutoff
+ Property / site
+ Cost center
+ GL account
+ Budget and Actual
+ Materiality status
+ Contributing transactions
+ Retrieved evidence
+ Confirmed and possible drivers
+ Missing information
+ Draft commentary
+ Review and approval status
```

Một Variance Case phải có trạng thái rõ ràng và audit trail. AI không được âm thầm ghi đè dữ liệu hoặc coi inference là fact.

---

## 9. Product architecture dự kiến

### Layer 1 — Data sources

Structured data:

- Budget and Forecast.
- General Ledger and Actual transactions.
- Chart of accounts.
- Property and cost-center master data.
- Vendor and currency data.

Unstructured evidence:

- Invoices.
- Purchase orders.
- Work orders.
- Contracts.
- Approval notes.
- Operations reports.
- Historical commentaries.
- Business-owner confirmations.

### Layer 2 — Data governance and preparation

- Immutable reporting-cutoff snapshot.
- Budget-version control.
- Schema validation.
- Reconciliation.
- Duplicate and missing-data checks.
- Canonical financial data model.
- Document parsing and metadata extraction.
- Access control and data masking.

### Layer 3 — Deterministic financial intelligence

- Absolute and percentage variance.
- Monthly and YTD variance.
- Favorable/unfavorable classification.
- Materiality rules.
- Contribution analysis.
- Transaction drill-down.
- Driver decomposition nếu có driver data.
- Unexplained residual phải được giữ lại.

LLM không được sử dụng để tính các chỉ tiêu tài chính chính thức.

### Layer 4 — Evidence intelligence

Structured retrieval:

- SQL or semantic queries đối với GL và master data.

Unstructured retrieval:

- Metadata filtering.
- Keyword or BM25 retrieval.
- Vector retrieval.
- Reranking.
- Evidence relevance and sufficiency checking.

Raw GL transactions không nên được vector hóa và dùng như nguồn duy nhất để LLM tự tính toán.

### Layer 5 — AI orchestration

Orchestrator tạo một context package có cấu trúc:

1. Verified financial facts.
2. Materiality result.
3. Top contributors.
4. Retrieved evidence.
5. Evidence authority level.
6. Missing information.
7. Permitted cause taxonomy.
8. Required output schema.

LLM tạo structured output gồm:

- Observed facts.
- Confirmed drivers.
- Possible drivers.
- Unknowns.
- Required follow-ups.
- Draft commentary.
- Evidence citations.
- Confidence level.

### Layer 6 — Verification and control gates

- Numeric verification.
- Citation existence and citation-entailment checks.
- Unsupported-claim detection.
- Reporting-cutoff validation.
- Permission validation.
- Confidence calibration.
- Abstention khi evidence không đủ.

### Layer 7 — FP&A workflow

1. Data and Control Center.
2. Material Variance Queue.
3. Investigation Workspace.
4. Commentary Review.
5. Manager Approval.
6. Export to management report.

### Layer 8 — Evaluation and observability

- Model, prompt, index and rule versions.
- Retrieval traces.
- Generated outputs.
- Verification results.
- User edits.
- Completion time.
- Approval outcome.
- Expert scores.

---

## 10. Evidence policy dự kiến

Nguồn thông tin được phân cấp:

| Cấp | Nguồn | Vai trò dự kiến |
|---|---|---|
| 1 | Xác nhận chính thức, approved work order | Có thể hỗ trợ confirmed cause |
| 2 | Invoice, PO, contract, accounting record | Evidence giao dịch mạnh |
| 3 | Operations report | Evidence nghiệp vụ cần kiểm tra |
| 4 | Historical commentary | Nguồn tham khảo, không mặc định đúng |
| 5 | LLM inference | Không được xem là evidence |

Hệ thống phải phân biệt:

- Observed fact.
- Calculated fact.
- Confirmed explanation.
- Possible explanation.
- Missing evidence.

---

## 11. Thiết kế dữ liệu dự kiến

### Bộ dữ liệu public/synthetic

Mục đích:

- Phát triển prototype.
- Reproducible technical testing.
- Demo mà không lộ dữ liệu doanh nghiệp.
- Tạo adversarial and edge cases có gold answer.

Thành phần:

- Synthetic Budget.
- Synthetic Actual transactions.
- Master data.
- Synthetic invoices, work orders và commentaries.
- Gold materiality labels.
- Gold evidence IDs.
- Gold cause labels.
- Gold facts and prohibited claims.

### Bộ dữ liệu doanh nghiệp

Mục đích:

- Real-world case study.
- External validity.
- Operational usefulness evaluation.
- Manual-versus-Copilot comparison.

Dữ liệu dự kiến:

- Transaction-level OPEX.
- Budget cùng mức chi tiết.
- Supporting documents.
- Historical variance cases.
- Expert-validated ground truth.

Chỉ công bố schema, phương pháp chọn mẫu, evaluation protocol, synthetic benchmark và kết quả tổng hợp. Không công bố dữ liệu mật.

### Đơn vị quan sát

Một material variance tại một tổ hợp:

```text
Reporting period × property × cost center × GL account
```

kèm contributing transactions và supporting evidence.

---

## 12. Phương pháp tạo ground truth

1. Recompute bằng script.
2. Reconcile với nguồn báo cáo chính thức.
3. FP&A analyst xác định relevant evidence và cause label.
4. Reviewer thứ hai kiểm tra một phần hoặc toàn bộ test set.
5. Business owner xác nhận khi nguyên nhân không thể suy ra từ accounting data.
6. Bất đồng được adjudicate.
7. Cho phép nhãn `unknown` hoặc `insufficient evidence`.

Historical commentary không được mặc định là ground truth.

---

## 13. Baseline và phương án so sánh

Tất cả các phương án phải được chạy trên cùng một frozen test set:

### Baseline 0 — Manual process

FP&A analyst thực hiện theo quy trình hiện tại.

### Baseline 1 — LLM-only

LLM nhận case data nhưng không có retrieval pipeline có kiểm soát.

### Baseline 2 — Vanilla RAG

LLM nhận retrieved context nhưng không có đầy đủ deterministic financial engine và verification gates.

### Proposed system — Hybrid analytical RAG

- Deterministic calculations.
- Structured and unstructured retrieval.
- Evidence validation.
- Controlled generation.
- Numeric and citation verification.
- Human approval.

---

## 14. Evaluation protocol dự kiến

### Technical evaluation

Calculation:

- Numerical exact match.
- Formula execution accuracy.
- Reconciliation difference.

Retrieval:

- Precision@k.
- Recall@k.
- Mean Reciprocal Rank.
- nDCG nếu phù hợp.

Generation and grounding:

- Factual accuracy.
- Citation accuracy.
- Unsupported-claim rate.
- Explanation coverage.
- Cause-classification accuracy.
- Abstention accuracy.

### Business evaluation

- Completion time.
- Number of manual searches.
- Correction rate.
- Manager acceptance rate.
- Number of follow-up cycles.
- Perceived usefulness.
- Ease of verification.
- Cognitive workload.
- Task–Technology Fit.
- Trust and intention to use.

### User-study design dự kiến

Crossover hoặc paired-task design:

```text
Analyst A: Case group 1 manual, case group 2 with Copilot
Analyst B: Case group 1 with Copilot, case group 2 manual
```

Commentary quality nên được chuyên gia chấm mù nếu khả thi.

### Robustness cases

- Missing evidence.
- Irrelevant evidence có cùng từ khóa.
- Conflicting documents.
- Budget bằng zero.
- Negative Actual do reversal.
- Timing differences.
- One large transaction.
- Wrong currency.
- Historical commentary sai.
- Tài liệu phát sinh sau reporting cutoff.

---

## 15. Các giả thuyết hoặc propositions dự kiến

**H1:** Hybrid analytical RAG có unsupported-claim rate thấp hơn LLM-only.

**H2:** Hybrid analytical RAG có citation accuracy cao hơn vanilla RAG.

**H3:** FP&A analysts sử dụng proposed system hoàn thành variance analysis nhanh hơn quy trình thủ công.

**H4:** Proposed system duy trì hoặc cải thiện độ chính xác của analysis so với quy trình thủ công.

Nếu số lượng người dùng nhỏ, TTF, trust và intention to use sẽ được phân tích mô tả hoặc định tính thay vì xây dựng mô hình hồi quy không đủ statistical power.

---

## 16. Scope MVP dự kiến

MVP nên bao gồm:

- Import Budget và Actual từ Excel/CSV.
- Một hoặc một nhóm OPEX accounts.
- Property × account × period analysis.
- Configurable materiality rules.
- Contribution analysis.
- Supporting-document retrieval.
- Structured draft commentary có citation.
- Numeric verification.
- Analyst review and edit.
- Audit log.
- Baseline experiment modes.

MVP chưa cần:

- ERP integration.
- Forecasting.
- General-purpose chatbot.
- Multi-agent workflow.
- Fine-tuning.
- Automated management decisions.

---

## 17. Những điểm chưa chắc chắn

AI phản biện không được giả định rằng các điều kiện sau đã được đáp ứng:

1. Chưa xác nhận quyền sử dụng dữ liệu doanh nghiệp cho nghiên cứu.
2. Chưa xác nhận có transaction-level OPEX đủ sạch.
3. Chưa xác nhận Budget và Actual có cùng grain.
4. Chưa xác nhận supporting documents có thể liên kết với giao dịch.
5. Chưa xác nhận historical commentary có chất lượng.
6. Chưa xác nhận có đủ FP&A analysts tham gia user study.
7. Chưa xác nhận deployment phải local hay được dùng cloud API.
8. Chưa xác nhận pain point lớn nhất là calculation, retrieval, follow-up hay writing.
9. Chưa xác nhận số variance cases đủ lớn để kiểm định thống kê.
10. Chưa xác nhận OPEX là scope tạo giá trị cao nhất.

---

## 18. Điều kiện go/no-go dự kiến

Nghiên cứu chỉ nên tiếp tục với claim “explanation” nếu có:

1. Evidence có thể liên kết với variance cases.
2. Chuyên gia có thể xác nhận ground truth.
3. Có thể đo baseline process.

Nếu thiếu evidence, scope phải giảm xuống detection, prioritization và investigation support.

Nếu thiếu user-study participants, không được đưa ra kết luận mạnh về adoption hoặc organizational impact.

Nếu không được phép sử dụng dữ liệu thực, nghiên cứu chỉ có thể chứng minh technical feasibility trên synthetic data.

---

# Nhiệm vụ phản biện dành cho AI

Bạn là một hội đồng phản biện gồm ba vai trò độc lập:

1. **Giảng viên nghiên cứu hệ thống thông tin và Design Science Research.**
2. **FP&A Director trong lĩnh vực bất động sản công nghiệp.**
3. **Machine Learning/RAG Engineer chuyên về hệ thống AI có yêu cầu accuracy và auditability cao.**

Hãy phản biện proposal trên một cách nghiêm khắc. Không mặc định rằng RAG, GenAI hoặc product hiện tại là cần thiết. Không khen chung chung. Mọi phê bình phải chỉ rõ:

- Vấn đề cụ thể.
- Vì sao vấn đề đó quan trọng.
- Bằng chứng hoặc kiểm tra nào cần thực hiện.
- Cách sửa khả thi trong phạm vi đề tài tốt nghiệp.

## Phần A — Tóm tắt và kiểm tra logic

1. Tóm tắt problem, artifact, users, inputs, outputs và claimed contribution trong tối đa 250 từ.
2. Viết lại problem statement theo dạng có thể đo lường.
3. Xác định liệu problem–solution fit hiện tại có hợp lý không.
4. Chỉ ra bất kỳ trường hợp “solution looking for a problem” nào.

## Phần B — Phản biện học thuật

1. Research gap có thật sự là gap hay chỉ là thiếu implementation trong một domain?
2. DSRM và TTF có phù hợp không? Có framework nào thừa hoặc thiếu?
3. RQ có trùng lặp, quá rộng hoặc không thể trả lời không?
4. Hypotheses có đo lường được với sample dự kiến không?
5. Contribution nào có thể bảo vệ được và contribution nào đang overclaim?
6. Đề xuất phiên bản research questions và hypotheses tốt hơn.
7. Đề xuất literature streams cần review, phân biệt foundational papers, evaluation papers và domain papers.

## Phần C — Phản biện FP&A và business value

1. Use case này có thực sự quan trọng với FP&A hay không?
2. Bottleneck thực có thể nằm ở calculation, evidence retrieval, business-owner response hay governance?
3. OPEX có phải scope phù hợp nhất không?
4. Commentary tốt có thực sự cải thiện decision quality hay chỉ tiết kiệm thời gian viết?
5. Doanh nghiệp sẽ từ chối sử dụng product vì lý do nào?
6. Metric nào phản ánh business value tốt hơn completion time?
7. Hãy đề xuất một minimum business case và go/no-go thresholds.

## Phần D — Phản biện dữ liệu

1. Data schema hiện thiếu những trường nào?
2. Một Variance Case nên được định nghĩa chính xác như thế nào?
3. Làm sao tạo gold evidence và gold cause mà không dùng historical commentary như đáp án mặc định?
4. Những loại leakage nào có thể xảy ra?
5. Temporal split có đủ không?
6. Synthetic data có thể gây sai lệch kết luận như thế nào?
7. Đề xuất minimum viable dataset và ideal dataset.

## Phần E — Phản biện architecture

1. RAG có thực sự cần thiết ở từng layer không?
2. Thành phần nào nên dùng deterministic rules, SQL, information retrieval hoặc LLM?
3. Kiến trúc có quá phức tạp cho một sinh viên không?
4. Điểm failure nghiêm trọng nhất là gì?
5. Verification gates hiện có thực sự phát hiện hallucination hay chỉ tạo thêm một LLM judge?
6. Làm sao kiểm soát document-level prompt injection và permission leakage?
7. Hãy đề xuất architecture MVP đơn giản hơn và architecture target dài hạn.

## Phần F — Phản biện evaluation

1. Các baselines có công bằng không?
2. Unit of analysis và unit of inference nên là gì?
3. Metrics nào là primary, secondary và diagnostic?
4. Có nên dùng RAGAS hoặc LLM-as-a-judge làm metric chính không?
5. Cách thiết kế blind expert evaluation?
6. Với số analyst nhỏ, statistical analysis nào phù hợp?
7. Làm sao tránh pseudo-replication khi một analyst xử lý nhiều cases?
8. Đề xuất acceptance criteria trước khi chạy final test.

## Phần G — Phản biện bảo mật và governance

1. Những dữ liệu nào tuyệt đối không nên đưa ra external API?
2. Cần những access-control và audit requirements nào?
3. Có rủi ro nào từ việc index documents vào vector database?
4. Làm sao xử lý right-to-delete, retention và model-provider logging?
5. Điều kiện nào buộc deployment phải local hoặc private cloud?

## Phần H — Redesign proposal

Sau khi phản biện, hãy đưa ra một proposal đã sharpen, gồm:

1. Tên đề tài tiếng Việt và tiếng Anh.
2. Problem statement.
3. Một primary research question và tối đa ba secondary questions.
4. Scope in và scope out.
5. Artifact definition.
6. Kiến trúc MVP.
7. Dataset strategy.
8. Evaluation strategy.
9. Academic contribution.
10. Business contribution.
11. Các giả định cần xác nhận trước khi build.
12. Kế hoạch thực hiện theo tuần phù hợp với một đề tài tốt nghiệp.

## Phần I — Decision memo

Kết luận bằng một decision memo ngắn với một trong bốn lựa chọn:

- **Proceed as proposed.**
- **Proceed with major narrowing.**
- **Pivot the use case.**
- **Stop because the study cannot support its claims.**

Decision memo phải chỉ rõ:

- Ba rủi ro lớn nhất.
- Ba điều cần xác minh ngay.
- Scope được khuyến nghị cuối cùng.
- Mức contribution có thể bảo vệ một cách trung thực.

## Yêu cầu trình bày

- Phân biệt rõ fact, inference và recommendation.
- Không tự bịa thông tin về doanh nghiệp hoặc dữ liệu.
- Đánh dấu mọi giả định chưa được xác nhận.
- Ưu tiên những thay đổi làm đề tài nhỏ hơn nhưng kiểm chứng tốt hơn.
- Không đề xuất công nghệ chỉ vì công nghệ đó phổ biến.
- Nếu cho rằng RAG không cần thiết, hãy nói rõ và đề xuất phương án thay thế.
- Chấm proposal từ 1 đến 5 theo: research rigor, data feasibility, technical feasibility, business value, evaluability và scope control.
- Kết thúc bằng danh sách tối đa 10 câu hỏi mà người thực hiện phải trả lời trước khi bắt đầu xây dựng.