# design_v3.md — Variance Workbench Rebuild

Phien ban: v3.0 · tao 23/10/2026
Huong da chon: **Luong kiem tra tung buoc (Guided Investigation)**
Nguoi dung chinh: chuyen vien FP&A. Nguoi thao tac demo: giang vien tu bam.

---

## 1. Cau hoi trung tam

> Case nay co the duoc giai thich bang bang chung hien co hay chua?

Moi man hinh, moi thanh phan giao dien phai phuc vu viec tra loi cau hoi nay.

---

## 2. Nguyen tac thiet ke

### Phai giu

- Quy trinh nghiep vu 10 buoc (da mo ta trong brief).
- Du lieu va so lieu benchmark tu repository (khong bia).
- Logic trang thai: case bat dau o "Chua xu ly", chuyen doi qua hanh dong.
- Kha nang truy nguon (provenance): bam vao so/claim/evidence → biet no den tu dau.
- Kha nang tu choi: case thieu bang chung → khong tu tao nguyen nhan.
- 4 cong kiem chung tat dinh: numeric, citation, claim, abstention.

### Co the thiet ke lai

- Cau truc dieu huong: tu 4 man hinh sidebar → luong tung buoc.
- So luong man hinh: tu 4 → 2 (danh sach + case investigation).
- Bo cuc desktop va mobile.
- Cach hien thi so lieu, evidence, ket qua kiem chung.
- Cach so sanh M0, M1, M2.
- Typography, mau sac, component.

---

## 3. Cau truc ung dung

### 3.1. Hai lop chinh

**Lop 1 — Danh sach case (Quet P&L)**
Nguoi dung chon ky bao cao + khu (hoac tat ca) + nguong trong yeu.
Bam "Quet P&L" → danh sach case vuot nguong hien ra.
Day la man hinh khoi dau duy nhat.

**Lop 2 — Dieu tra case (Guided Investigation)**
Khi chon mot case tu danh sach, nguoi dung vao luong 5 buoc.
Thanh tien trinh nam ngang o dau trang, luon hien.

### 3.2. Thanh tien trinh (Progress Bar)

```
[ Tong quan ] → [ Bang chung ] → [ Giai trinh ] → [ Kiem chung ] → [ Quyet dinh ]
```

Moi buoc la mot trang noi dung day du (khong phai tab nho).
Nguoi dung co the:
- Tien/lui bang nut "Tiep theo" / "Quay lai".
- Bam truc tiep len mot buoc bat ky da hoan thanh.
- Buoc chua mo khoa hien xam, giai thich ly do (vd: "Can tao giai trinh truoc").

Thanh tien trinh co indicator trang thai:
- Buoc hoan thanh: dau tick.
- Buoc dang lam: highlight.
- Buoc chua mo khoa: xam.

### 3.3. Header sticky

Khi dang trong luong dieu tra, header sticky gom:
- Nut quay lai danh sach (← Danh sach case).
- Ten case: [Property] · [P&L Line] · [Thang].
- So nhanh: Budget | Actual | Variance | % | Direction.
- Trang thai hien tai cua case.

Header nay khong thay doi khi chuyen buoc. Nguoi dung luon biet minh dang xem case nao.

---

## 4. Chi tiet tung buoc

### Buoc 1: Tong quan

**Cau hoi nguoi dung:** "Chenh lech nay lon bao nhieu va den tu dau?"

Hien thi:
- Budget, Actual, Variance, %, Direction (thuong loi/bat loi) — set lon, ro rang.
- Bang contributors:
  - Ma (GL-xxx hoac TEN-xxx).
  - Loai (giao dich / tenant).
  - Mo ta (memo).
  - Gia tri dong gop (delta).
  - Ty le dong gop (share).
  - Doi tac (party) neu co.
- Nguong trong yeu da ap dung.

**Provenance tai buoc nay:**
Bam vao Budget → tooltip/panel nho: "budget = tong budget_line theo property=X, pl_line=Y, month=Z".
Bam vao Variance → "variance = actual - budget = [so] - [so]".
Bam vao contributor delta → "tu gl.csv, txn_id=GL-xxx, amount=[so]".

**Hanh dong chinh:** "Tiep theo: Xem bang chung" (hoac bam buoc 2 tren thanh tien trinh).

### Buoc 2: Bang chung

**Cau hoi nguoi dung:** "Co tai lieu nao thuc su ho tro viec giai thich chenh lech nay khong?"

Hien thi:
- Danh sach tai lieu da truy xuat (tu evidence_packs), moi tai lieu gom:
  - Ma (EV-xxx).
  - Loai (termination_notice, work_order, vendor_invoice, v.v.).
  - Khu va ky.
  - Authority level (nhan 1/2/3, co giai thich).
  - Noi dung day du.
  - Trang thai lien ket (linked / khong lien ket) — giai thich tai sao.
  - Diem BM25 va RRF (cho nguoi muon biet ky thuat).
- Phan biet ro:
  - "Tai lieu lien ket" (linked=true) — co noi dung thuc su lien quan den case.
  - "Tai lieu truy xuat nhung khong lien ket" (linked=false) — chi trung metadata.
  - Distractor/ops_memo (authority=3) — hien thi nhung ghi ro "Khong co tac dong ngan sach".

**Truong hop khong co bang chung lien ket:**
- Hien thi thong bao ro: "Khong co tai lieu nao lien ket noi dung voi case nay."
- Van hien cac tai lieu truy xuat (neu co), nhung tat ca danh dau "Khong lien ket".
- Dong ghi chu: "Khi khong co bang chung, he thong se tu choi neu nguyen nhan."

**Hanh dong chinh:** "Tiep theo: Tao giai trinh".

### Buoc 3: Giai trinh

**Cau hoi nguoi dung:** "He thong giai thich chenh lech nay nhu the nao?"

Phan biet 2 che do hien thi:

**3a. Giai trinh M2 (mac dinh, luong nghiep vu)**
Hien thi cau truc output M2 thuc te tu records_full.jsonl:
- **Du kien quan sat** (observed_facts): cau mo ta variance bang so da kiem chung.
- **Nguyen nhan da xac nhan** (drivers_confirmed): moi driver co:
  - Noi dung claim.
  - Ma tai lieu trich dan [EV-xxx] — bam duoc, link sang buoc 2.
  - Trang thai ho tro (tu claim gate — hien o buoc 4).
- **Nguyen nhan chua chac chan** (drivers_possible): tuong tu, co ghi chu.
- **Tac dong bu tru** (offsets): neu co.
- **Ghi chu tiep theo** (forward_note): neu co.
- **Ban giai trinh hoan chinh** (draft_comment): van ban tong hop.

Nguoi dung co the chinh sua draft_comment. Khi chinh sua:
- Trang thai kiem chung cu mat hieu luc.
- Hien thi canh bao: "Noi dung da thay doi. Can kiem chung lai truoc khi su dung."
- Nut sao chep ban da kiem chung bi khoa cho den khi kiem chung lai thanh cong.

**3b. So sanh M0–M1–M2 (nut phu "So sanh 3 cau hinh")**
Khi bam, hien thi khu vuc mo rong hoac panel ben duoi, chia 3 cot (desktop) hoac 3 phan xep doc (mobile):

| M0 — LLM truc tiep | M1 — RAG khong kiem chung | M2 — Glass-box |
|---|---|---|
| Chi co draft_comment | Co draft_comment voi [EV-xxx] | Co cau truc day du |
| Khong co nguon | Co nguon nhung khong co cong kiem | Co nguon + 4 cong kiem |
| Khong co tu choi | Khong co tu choi | Tu choi khi thieu bang chung |

Moi cot hien thi output THUC TE cua mode do tu records_full.jsonl (rep=0 lam mac dinh, co the chon rep 0/1/2).
Khong mo ta chung chung ("M0 khong co nguon") — phai hien noi dung that.

**Truong hop abstain:**
- M2 ghi ro: "abstained: true".
- Phan drivers_confirmed trong.
- draft_comment chi neu du kien va ghi: "Chua du bang chung de xac dinh nguyen nhan. De nghi bo sung ho so."
- M0 va M1 van bja nguyen nhan (hien thi de doi chieu — day la diem M2 vuot troi).

**Hanh dong chinh:** "Tiep theo: Kiem chung" (chi mo khoa sau khi da xem giai trinh).

### Buoc 4: Kiem chung

**Cau hoi nguoi dung:** "Ban giai trinh nay co dang tin cay khong?"

Hien thi 4 cong kiem chung cua M2, moi cong la mot phan rieng:

**Cong 1: So lieu (Numeric Gate)**
- Bang: moi con so trong output, kem:
  - Gia tri tho (raw).
  - Gia tri da parse.
  - Truong engine khop (matched) hoac "Khong khop".
  - Ket qua: Dat / Khong dat.
- Tong ket: X/Y so lieu dat.

**Cong 2: Trich dan (Citation Gate)**
- Bang: moi [EV-xxx], kem:
  - Ma tai lieu.
  - Ton tai? Dung property? Dung ky?
  - Ket qua: Dat / Khong dat.
  - Ly do neu khong dat.
- Tong ket: X/Y trich dan dat.

**Cong 3: Nhan dinh (Claim Gate)**
- Bang: moi driver_confirmed, kem:
  - Noi dung claim.
  - Co citation hop le di kem?
  - Ket qua: Co ho tro / Khong co ho tro.
- Tong ket: X/Y nhan dinh co nguon.

**Cong 4: Tu choi (Abstention Gate)**
- Hien thi:
  - Bang chung co yeu khong? (evidence_weak: true/false).
  - Mo hinh da tu choi chua? (abstained: true/false).
  - Ket qua: Dat / Khong dat.
  - Giai thich: vd "Bang chung yeu va mo hinh da tu choi — dung."
  - Hoac: "Bang chung yeu nhung mo hinh van neu nguyen nhan — SAI."

**Tong hop:**
- Tat ca cong dat → Trang thai: "Da kiem tra".
- Bat ky cong nao khong dat → Trang thai: "Can xac minh". Chi ro cong nao va muc nao co van de.

**Hanh dong chinh:** "Tiep theo: Quyet dinh".

### Buoc 5: Quyet dinh

**Cau hoi nguoi dung:** "Toi ket luan gi ve case nay?"

Hien thi tom tat:
- So lieu case (tu buoc 1).
- So cong dat / khong dat (tu buoc 4).
- Trang thai de xuat:
  - "Da kiem tra" — tat ca cong dat.
  - "Can xac minh" — co cong khong dat nhung van co bang chung.
  - "Khong du bang chung" — case thieu bang chung, M2 da abstain.

Nguoi dung bam xac nhan trang thai. Trang thai cap nhat tren danh sach case.

Co nut "Sao chep giai trinh" (chi mo khi trang thai la "Da kiem tra").
Co nut "Quay lai danh sach" de tiep tuc case khac.

---

## 5. Trang ket qua nghien cuu (tach rieng)

Truy cap tu danh sach case, qua nut/link "Ket qua nghien cuu" o header hoac footer.
Khong nam trong luong dieu tra case.

### 5.1. Bang tong hop

Hien thi 5 thuoc do chinh:

| Thuoc do | M0 | M1 | M2 |
|---|---|---|---|
| Do chinh xac so lieu (Numeric accuracy) | 0.901 +- 0.026 | 0.960 +- 0.012 | 0.984 +- 0.004 |
| Do chinh xac trich dan (Citation precision) | Khong ap dung | 0.935 +- 0.001 | 1.000 +- 0.000 |
| Do bao phu trich dan (Citation recall) | 0.000 +- 0.000 | 0.914 +- 0.019 | 0.952 +- 0.016 |
| Ty le nhan dinh thieu can cu (Unsupported claim rate) | 1.000 +- 0.000 | 0.293 +- 0.026 | 0.054 +- 0.019 |
| Ty le tu choi dung (Abstain recall — trap) | 0.111 +- 0.192 | 0.000 +- 0.000 | 1.000 +- 0.000 |

Ghi chu duoi bang:
- "Mean +- SD tinh tu 3 diem trung binh cua 3 lan chay."
- "Citation precision cua M0 la 'Khong ap dung' vi M0 khong tao trich dan."

### 5.2. Chi so bo sung

| Thuoc do | M0 | M1 | M2 |
|---|---|---|---|
| Coverage | 0.843 +- 0.034 | 0.922 +- 0.034 | 0.912 +- 0.000 |
| Risk on asserted | 0.093 +- 0.019 | 0.096 +- 0.004 | 0.000 +- 0.000 |
| Retrieval P@5 | 0.338 | — | — |
| Retrieval R@5 | 1.000 | — | — |

### 5.3. Ket qua theo kich ban

Hien thi bang by_scenario.csv: mode x scenario, voi n, unsupported_rate va numeric_accuracy.
De nguoi xem thay hieu suat M2 theo tung loai tinh huong.

### 5.4. Quy tac

- Moi so phai khop file summary.csv, summary_by_rep.csv, by_scenario.csv.
- Khong trinh bay Cohen's kappa.
- Khong tu tao ket luan nghien cuu moi.
- Ghi ro: "Du lieu mo phong · Khong dung cho bao cao thuc te".

---

## 6. Trang thai case

Trang thai la KET QUA HANH DONG, khong phai thuoc tinh gan san.

| Trang thai | Dieu kien | Hien thi |
|---|---|---|
| Chua xu ly | Case vua duoc quet, chua ai mo | Nhan xam |
| Dang tao | Dang sinh giai trinh (animation) | Spinner + mo ta |
| Da kiem tra | Tat ca 4 cong dat + nguoi dung xac nhan | Nhan xanh la + chu |
| Can xac minh | Co cong khong dat | Nhan vang + chu + chi tiet |
| Khong du bang chung | M2 abstain + nguoi dung xac nhan | Nhan do nhat + chu |
| Khong co ket qua | Quet nhung khong co case vuot nguong | Thong bao rieng |
| Loi xu ly | Loi bat ngo | Nhan do + chi tiet loi |

Trang thai luon co CHU di kem mau, khong chi dung mau.

---

## 7. Bang mau

Giu tinh than chuyen nghiep, it mau, ro thu bac. Mau chi dung cho trang thai va du lieu can chu y.

| Token | Hex | Vai tro |
|---|---|---|
| --ink | #0F1A2E | Tieu de, chu chinh, nut chinh |
| --ink-secondary | #4A5468 | Chu mo ta, nhan phu |
| --ink-tertiary | #8B95A5 | Chu bo sung, placeholder |
| --surface | #FFFFFF | Nen chinh |
| --surface-raised | #F6F7F9 | Nen phan, nen bang xen ke |
| --surface-sunken | #ECEEF2 | Nen input, nen vung thong tin |
| --border | #D5D9E0 | Vien mac dinh |
| --border-focus | #2563EB | Focus ring (blue-600) |
| --accent | #2563EB | Hanh dong chinh, lien ket |
| --accent-subtle | #EFF4FF | Nen vung chon, highlight nhe |
| --status-pass | #166534 | Dat kiem chung |
| --status-pass-bg | #F0FDF4 | Nen trang thai dat |
| --status-warn | #92400E | Can xac minh |
| --status-warn-bg | #FFFBEB | Nen canh bao |
| --status-fail | #991B1B | Khong dat, bat loi |
| --status-fail-bg | #FEF2F2 | Nen loi |
| --status-neutral | #6B7280 | Chua xu ly |
| --favorable | #166534 | Chenh lech thuan loi |
| --unfavorable | #991B1B | Chenh lech bat loi |

Ty le dien tich: ~80% surface/surface-raised, ~15% ink cho header va nut, ~5% mau trang thai.
Tuong phan toi thieu: 4.5:1 cho chu thuong, 3:1 cho chu lon.

---

## 8. Kieu chu

| Vai tro | Font | Co | Do dam | Line-height |
|---|---|---|---|---|
| Page title | Inter | 22px | 600 | 1.3 |
| Section title | Inter | 16px | 600 | 1.35 |
| Body | Inter | 14px | 400 | 1.55 |
| Label | Inter | 12px | 500 | 1.3 |
| So va ma | JetBrains Mono | 13px | 450 | 1.4 |
| KPI (so lon) | JetBrains Mono | 28px | 600 | 1.1 |

- So canh phai, dung tabular figures (font-variant-numeric: tabular-nums).
- 2 font toi da: Inter (noi dung) + JetBrains Mono (so, ma).
- Fallback: system-ui, -apple-system, sans-serif / Consolas, monospace.

---

## 9. Luoi va khoang cach

- Khung noi dung toi da: 1200px (khong can 1440 cho app screen).
- Khong co sidebar co dinh. Navigation nam trong header va thanh tien trinh.
- Gutter: 16px (mobile), 24px (tablet), 32px (desktop).
- Khoang cach giua cac phan: 32px (mobile), 48px (desktop).
- Bo goc: 6px cho control, 8px cho panel/card.
- Vien: 1px --border. Trang thai chon: 2px --border-focus.
- Bong: chi dung cho modal va dropdown: 0 8px 30px rgba(0,0,0,0.12).

---

## 10. Thanh phan giao dien

| Thanh phan | Quy cach |
|---|---|
| Nut chinh (Primary) | Nen --ink, chu trang, cao 36px, bo goc 6px |
| Nut phu (Secondary) | Nen trang, vien --border, chu --ink, cao 36px |
| Nut ghost | Khong nen, khong vien, chu --accent |
| Filter/Select | Label tren, control cao 36px, vien --border |
| Status label | Chu + cham mau (dot), nen nhe tuong ung, khong dung pill tron |
| Bang du lieu | Header nen --surface-raised, khong mau dam. Hover hang nen --accent-subtle. So canh phai. |
| Evidence card | Vien trai 3px mau theo authority. Noi dung day du. Trang thai linked/khong lien ket. |
| Provenance panel | Nen --surface-sunken, vien --border, mo rong inline |
| Verification row | Ten cong, ket qua (dat/khong dat), giai thich, mau trang thai |
| Progress bar | 5 buoc ngang, indicator trang thai, bam duoc |
| Modal | Nen trang, bong, dong bang Escape, giu focus |
| Toast | Goc duoi phai, 3 giay, cho quet/tao/sao chep |

---

## 11. Responsive

### Desktop (>= 1024px)
- Thanh tien trinh nam ngang.
- Bang contributor va so lieu hien day du.
- So sanh M0-M1-M2: 3 cot.
- Verification: 4 cong xep doc.

### Tablet (640px — 1023px)
- Thanh tien trinh van ngang, nhan rut gon.
- Bang cuon ngang neu can.
- So sanh M0-M1-M2: 2 cot hoac accordion.

### Mobile (< 640px)
- Thanh tien trinh chuyen thanh indicator nho (buoc X/5 + ten buoc).
- KPI xep 2 cot.
- So sanh M0-M1-M2: accordion (bam mo tung mode).
- Evidence card toan chieu rong.
- Modal toan man hinh.

### Accessibility
- Ban phim: Tab di chuyen, Enter/Space hanh dong, Escape dong modal.
- Focus ring 2px --border-focus, offset 2px.
- prefers-reduced-motion: loai bo animation, giu noi dung.
- aria-label cho nut, aria-current cho buoc hien tai.
- Table co caption (co the an).

---

## 12. Du lieu va tinh trung thuc

- Moi case demo doi chieu voi cases.json.
- Moi output M0/M1/M2 lay tu records_full.jsonl (rep=0 mac dinh).
- Moi so benchmark doi chieu voi summary.csv, summary_by_rep.csv, by_scenario.csv.
- Evidence lay tu evidence.json va evidence_packs.json.
- Khong bia case, so lieu, tai lieu, trang thai kiem chung.
- Footer moi trang: "Du lieu mo phong · Khong dung cho bao cao thuc te".

---

## 13. Case dien hinh de demo

Trong 34 case, danh dau 4 case dien hinh de giang vien de theo doi:

1. **2026-05 / PROP-D / Repair & Maintenance** — Co work order + invoice, evidence manh, M2 verified.
2. **2026-05 / PROP-B / Marketing** — Trap case, khong co evidence lien ket, M2 abstain.
3. **2026-08 / PROP-C / Leasing revenue** — 2 contributor (termination + escalation), nhieu tai lieu.
4. **2026-08 / CORP / Other income** — CORP-level, insurance compensation, variance rat lon (+498%).

---

## 14. Ky thuat

- File moi: `Comments_Variance/docs/variance_workbench_v3.html` (hoac thu muc rieng).
- Buildless: HTML + CSS + JS, mo truc tiep tu file system.
- Du lieu nhung trong JS (mot object duy nhat), khong nhap lai o nhieu noi.
- Trang thai va tong so tinh tu du lieu, khong hard-code.
- Khong ghi de file cu.
- Khong gia voi goi API, khong hien thi tien trinh AI gia.

---

## 15. Doi chieu voi design.md v2

| Muc | v2 (design.md) | v3 (file nay) |
|---|---|---|
| Dieu huong | 4 man hinh sidebar | 2 lop: danh sach + luong 5 buoc |
| Case flow | Cat ngang qua Dieu tra / Soan & kiem | Mot luong lien tuc tren cung case |
| Evidence vs Claim | Tach 2 man hinh | Lien ket: claim chi sang evidence |
| M0-M1-M2 | 3 tab cung format | 3 cot voi output thuc te, khac biet hien thi |
| Provenance | Chip nho, popover | Inline expansion hoac panel ben |
| Trang thai | KPI san co | Ket qua hanh dong cua nguoi dung |
| Mau sac | Navy-cyan dominant | Trung tinh, mau chi cho trang thai |
| Sidebar | 232px co dinh | Khong co sidebar |
