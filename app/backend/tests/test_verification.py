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


def test_10_phan_tram_sai_bi_bat():
    v = gates.numeric_gate(out("variance of 62,500 (+45.0%)"), CASE)
    pct = [x for x in v if x["is_pct"]]
    assert pct and not pct[0]["ok"]  # 45% khac 52.1%
