"""Test engine bang so TINH TAY — expected values ghi ro phep tinh trong comment."""

import json

import pandas as pd
import pytest

from vwb import config
from vwb.data_synth import generate
from vwb.engine import core

MAT = {"revenue": {"abs": 50_000.0, "pct": 0.05},
       "cost": {"abs": 30_000.0, "pct": 0.15},
       "corp": {"abs": 100_000.0, "pct": 0.10}}


def _line_df(rows):
    return pd.DataFrame(rows, columns=["property", "pl_line", "month", "amount"])


def test_variance_revenue_unfavorable_material():
    # tay tinh: actual 1,165,000 - budget 1,250,000 = -85,000; pct = -85,000/1,250,000 = -6.8%
    b = _line_df([("PROP-C", "Leasing revenue", "2026-07", 1_250_000.0)])
    a = _line_df([("PROP-C", "Leasing revenue", "2026-07", 1_165_000.0)])
    r = core.variance_table(b, a, "2026-07", MAT).iloc[0]
    assert r["variance"] == -85_000.0
    assert r["variance_pct"] == pytest.approx(-0.068)
    assert r["direction"] == "unfavorable"  # thu nhap thap hon ke hoach
    assert bool(r["material"])  # 85k >= 50k va 6.8% >= 5%


def test_variance_cost_lower_is_favorable_but_timing_still_material():
    # cost: actual 30,000 < budget 55,000 -> favorable; pct = -25,000/55,000 = -45% >= 15%
    b = _line_df([("PROP-A", "Marketing", "2026-05", 55_000.0)])
    a = _line_df([("PROP-A", "Marketing", "2026-05", 30_000.0)])
    r = core.variance_table(b, a, "2026-05", MAT).iloc[0]
    assert r["variance"] == -25_000.0
    assert r["direction"] == "favorable"
    assert bool(r["material"])  # favorable van phai giai trinh (timing!)


def test_budget_zero_pct_none_material_by_abs():
    b = _line_df([("PROP-B", "Repair & Maintenance", "2026-03", 0.0)])
    a = _line_df([("PROP-B", "Repair & Maintenance", "2026-03", 40_000.0)])
    r = core.variance_table(b, a, "2026-03", MAT).iloc[0]
    assert r["variance_pct"] is None  # chia cho 0 -> khong co pct
    assert bool(r["material"])  # 40k >= 30k (abs rule)
    assert r["direction"] == "unfavorable"


def test_revenue_contributors_order_and_sum():
    # tay tinh: TEN-1: 0-60,000=-60,000; TEN-2: 0-32,000=-32,000; TEN-3: 147,000-140,000=+7,000
    cols = ["property", "tenant", "month", "amount"]
    b = pd.DataFrame([("P", "TEN-1", "m", 60_000.0), ("P", "TEN-2", "m", 32_000.0),
                      ("P", "TEN-3", "m", 140_000.0)], columns=cols)
    a = pd.DataFrame([("P", "TEN-1", "m", 0.0), ("P", "TEN-2", "m", 0.0),
                      ("P", "TEN-3", "m", 147_000.0)], columns=cols)
    out = core.revenue_contributors(b, a, "P", "m")
    assert [c["key"] for c in out] == ["TEN-1", "TEN-2", "TEN-3"]  # sap theo |delta|
    assert [c["delta"] for c in out] == [-60_000.0, -32_000.0, 7_000.0]
    assert sum(c["delta"] for c in out) == -85_000.0  # tong contributor = variance


def test_dataset_integration(tmp_path, monkeypatch):
    """Chay generator that vao thu muc tam: gold material nao cung phai duoc engine tim ra."""
    monkeypatch.setattr(config, "DATA_DIR", tmp_path)
    generate.main()
    gold = json.loads((tmp_path / "gold_labels.json").read_text(encoding="utf-8"))
    cases = json.loads((tmp_path / "cases.json").read_text(encoding="utf-8"))
    engine_ids = {c["case_id"] for c in cases}
    assert len(gold) >= 20
    for cid, g in gold.items():
        if g["material"]:
            assert cid in engine_ids, cid
    # case khop so: facts trong gold = so cua engine
    by_id = {c["case_id"]: c for c in cases}
    for cid, g in gold.items():
        if g["material"]:
            assert by_id[cid]["variance"] == pytest.approx(g["facts"]["variance"])
    # moi case abstain khong co evidence
    assert all(not g["gold_evidence"] for g in gold.values() if g["abstain"])
