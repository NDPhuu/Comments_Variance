"""Bo 10 loi gieo co y — tieu chi gate M2: cong kiem bat du 10/10 (phan loai dung ca pass lan fail)."""

from vwb.verification import gates

CASE = {
    "case_id": "2026-07_PROP-X_RM", "month": "2026-07", "property": "PROP-X",
    "pl_line": "Repair & Maintenance", "budget": 120_000.0, "actual": 182_500.0,
    "variance": 62_500.0, "variance_pct": 0.5208, "direction": "unfavorable",
    "contributors": [
        {"key": "GL-88412", "memo": "roof repair phase 2", "delta": 48_200.0},
        {"key": "GL-88503", "memo": "chiller maintenance", "delta": 9_800.0},
    ],
}
DOCS = [
    {"doc_id": "EV-301", "type": "work_order", "property": "PROP-X", "period": "2026-07",
     "title": "WO roof", "text": "roof repair phase 2, value $48.2k"},
    {"doc_id": "EV-302", "type": "memo", "property": "PROP-Y", "period": "2026-07",
     "title": "trap", "text": "roof inspection elsewhere"},
    {"doc_id": "EV-303", "type": "memo", "property": "PROP-X", "period": "2026-09",
     "title": "late doc", "text": "phat sinh sau ky"},
]
PACK_OK = {"docs": [{**DOCS[0], "linked": True}], "best_bm25": 5.0, "linked_any": True}
PACK_EMPTY = {"docs": [], "best_bm25": 0.0, "linked_any": False}


def out(comment: str, confirmed=None, abstained=False) -> dict:
    return {"draft_comment": comment, "drivers_confirmed": confirmed or [],
            "abstained": abstained}


def test_01_so_sai_bi_bat():
    v = gates.numeric_gate(out("Variance of 58,000 due to roof"), CASE)
    assert any(not x["ok"] for x in v)  # 58,000 khong khop truong nao


def test_02_sai_dau_bi_bat():
    v = gates.numeric_gate(out("Variance of -62,500 this month"), CASE)
    assert any(not x["ok"] for x in v)  # -62,500 khac +62,500 (giu dau theo TAT-QA)


def test_03_sai_scale_bi_bat():
    v = gates.numeric_gate(out("Impact of $62.5m from repairs"), CASE)
    assert any(not x["ok"] for x in v)  # m thay vi k


def test_04_citation_ma_bi_bat():
    v = gates.citation_gate(out("due to roof [EV-999]"), {d["doc_id"]: d for d in DOCS}, CASE)
    assert v and not v[0]["ok"] and v[0]["reason"] == "khong ton tai"


def test_05_citation_sai_property_bi_bat():
    v = gates.citation_gate(out("roof work [EV-302]"), {d["doc_id"]: d for d in DOCS}, CASE)
    assert v and not v[0]["ok"] and v[0]["reason"] == "sai property"


def test_06_citation_sau_ky_bi_bat():
    v = gates.citation_gate(out("confirmed [EV-303]"), {d["doc_id"]: d for d in DOCS}, CASE)
    assert v and not v[0]["ok"] and v[0]["reason"] == "sau ky bao cao"


def test_07_claim_khong_citation_bi_bat():
    o = out("roof repair drove the variance",
            confirmed=[{"text": "roof repair phase 2 drove overspend", "evidence_ids": []}])
    r = gates.verify(o, CASE, DOCS, PACK_OK)
    assert r["claims"] and not r["claims"][0]["supported"] and r["overall"] == "flagged"


def test_08_thieu_bang_chung_ma_van_ket_luan_bi_bat():
    o = out("cause: marketing push",
            confirmed=[{"text": "marketing push", "evidence_ids": ["EV-301"]}], abstained=False)
    r = gates.abstention_gate(o, PACK_EMPTY)
    assert not r["ok"] and r["evidence_weak"]


def test_09_output_dung_phai_duoc_pass():
    o = out("R&M exceeded budget by 62,500 (+52.1%), mainly roof repair $48.2k [EV-301]",
            confirmed=[{"text": "roof repair phase 2, $48.2k in 2026-07",
                        "evidence_ids": ["EV-301"]}])
    r = gates.verify(o, CASE, DOCS, PACK_OK)
    assert r["overall"] == "verified", r


def test_11_phan_so_chep_tu_facts_duoc_pass():
    # model chep variance_pct dang phan so (0.5208) tu FACTS — khong phai bia
    v = gates.numeric_gate(out("unfavorable variance of 62,500 (0.5208)"), CASE)
    assert all(x["ok"] for x in v), v


def test_12_gia_tri_zero_duoc_pass():
    v = gates.numeric_gate(out("actual of $0.0k after termination"), CASE)
    assert all(x["ok"] for x in v), v


def test_13_so_quote_tu_tai_lieu_da_cite():
    # 48.2k co trong EV-301; duoc pass KHI cite, FAIL khi khong cite
    doc = DOCS[0]
    ok = gates.numeric_gate(out("contract value $48.2k [EV-301]"),
                            {**CASE, "contributors": []}, cited_docs=[doc])
    assert all(x["ok"] for x in ok), ok
    no = gates.numeric_gate(out("contract value $48.2k"), {**CASE, "contributors": []})
    assert any(not x["ok"] for x in no), no


def test_14_dau_cong_tren_variance_am_bi_bat():
    # case favorable: variance = -62,500. Model viet "+62,500" -> mau thuan dau (TAT-QA).
    fav = {**CASE, "actual": 57_500.0, "variance": -62_500.0, "variance_pct": -0.5208,
           "direction": "favorable", "contributors": []}
    v = gates.numeric_gate(out("favorable variance of +62,500 (+52.1%)"), fav)
    assert all(not x["ok"] for x in v), v  # ca so tien lan % deu sai dau
    # khong dau: do lon hop le (huong da neu bang chu "favorable") -> pass
    v2 = gates.numeric_gate(out("favorable variance of 62,500 (52.1%)"), fav)
    assert all(x["ok"] for x in v2), v2
    # dau am dung -> pass
    v3 = gates.numeric_gate(out("variance of -62,500 (-52.1%)"), fav)
    assert all(x["ok"] for x in v3), v3


def test_15_bullet_markdown_khong_phai_dau_am():
    # "- 48,200" sau xuong dong la gach dau dong, KHONG phai -48,200
    v = gates.numeric_gate(out("drivers:\n- 48,200 roof repair\n- 9,800 chiller"), CASE)
    assert all(x["ok"] for x in v), v


def test_16_variance_pct_am_100_chep_tu_facts():
    z = {**CASE, "actual": 0.0, "variance": -120_000.0, "variance_pct": -1.0,
         "direction": "favorable", "contributors": []}
    v = gates.numeric_gate(out("actual 0.0 vs budget 120,000, variance -120,000 (-1.0)"), z)
    assert all(x["ok"] for x in v), v
    # nhung dan nhan % cho phan so van bi bat: -1.0% khac -100%
    v2 = gates.numeric_gate(out("favorable variance of -1.0%"), z)
    assert any(not x["ok"] for x in v2), v2


def test_17_phan_tram_quote_tu_tai_lieu_da_cite():
    doc = {**DOCS[0], "text": "22% temporary tariff surcharge applied"}
    ok = gates.numeric_gate(out("22% tariff surcharge drove overspend [EV-301]"),
                            {**CASE, "contributors": []}, cited_docs=[doc])
    assert all(x["ok"] for x in ok), ok
    no = gates.numeric_gate(out("22% tariff surcharge drove overspend"),
                            {**CASE, "contributors": []})
    assert any(not x["ok"] for x in no), no


def test_10_phan_tram_sai_bi_bat():
    v = gates.numeric_gate(out("variance of 62,500 (+45.0%)"), CASE)
    pct = [x for x in v if x["is_pct"]]
    assert pct and not pct[0]["ok"]  # 45% khac 52.1%
