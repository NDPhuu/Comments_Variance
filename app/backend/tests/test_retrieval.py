"""Sanity retrieval tren dataset that: gold evidence phai nam trong top-5 (BM25+metadata)."""

import json

import pytest

from vwb import config
from vwb.retrieval import core


@pytest.fixture(scope="module")
def data():
    cases = json.loads((config.DATA_DIR / "cases.json").read_text(encoding="utf-8"))
    gold = json.loads((config.DATA_DIR / "gold_labels.json").read_text(encoding="utf-8"))
    return cases, gold


def test_gold_evidence_in_top5(data):
    cases, gold = data
    r = core.Retriever(use_dense=False)  # test nhanh, khong can model dense
    hit, total = 0, 0
    misses = []
    for c in cases:
        g = gold.get(c["case_id"])
        if not g or not g["gold_evidence"]:
            continue
        total += 1
        got = {d["doc_id"] for d in r.retrieve(c)["docs"]}
        if set(g["gold_evidence"]) & got:
            hit += 1
        else:
            misses.append(c["case_id"])
    assert total > 0
    assert hit / total >= 0.8, f"recall@5 {hit}/{total}; miss: {misses[:5]}"


def test_metadata_filter_chan_bay_sai_property(data):
    cases, gold = data
    docs = core.load_evidence()
    for c in cases:
        pool = core.metadata_filter(docs, c)
        assert all(
            d["property"] == c["property"] or
            (c["property"] == config.CORP and d["property"] == config.CORP)
            for d in pool
        )
        assert all(d["period"] <= c["month"] for d in pool)


def test_linkage_tach_dung_abstain_va_case_that(data):
    """Tin hieu abstention = linked_any: case bay phai KHONG linked, case that phai CO."""
    cases, gold = data
    r = core.Retriever(use_dense=False)
    bad = []
    for c in cases:
        g = gold.get(c["case_id"])
        if not g:
            continue
        p = r.retrieve(c)
        if g["abstain"] and p["linked_any"]:
            bad.append((c["case_id"], "bay nhung linked"))
        if (not g["abstain"]) and g["gold_evidence"] and not p["linked_any"]:
            bad.append((c["case_id"], "that nhung khong linked"))
    assert not bad, bad
