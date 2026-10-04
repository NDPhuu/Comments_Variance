"""Sinh dataset_v1 — du lieu gia lap co DAP AN (gold labels) gan san.

Chay:  poetry run python -m vwb.data_synth.generate
Output: app/backend/data/dataset_v1/ (CSV + evidence.json + gold_labels.json + cases.json)

Nguyen tac:
- Seed co dinh -> tai lap duoc 100%.
- Moi kich ban gieo tuong ung mot loai nguyen nhan CO THAT (scenarios.yaml / house_style.md).
- Gold facts duoc tinh lai tu bang so lieu CUOI CUNG -> luon khop voi engine.
"""

from __future__ import annotations

import json
import random
from collections import defaultdict
from datetime import datetime, timezone

import pandas as pd

from vwb import config
from vwb.engine import core

R = random.Random(config.SEED)
M = config.MONTHS  # "2026-01".."2026-12"


def _mi(month: str) -> int:
    return int(month[5:]) - 1


def _next(month: str) -> str:
    return M[min(_mi(month) + 1, 11)]


# ----------------------------------------------------------------------------- masters
def build_tenants() -> list[dict]:
    tenants, k = [], 1
    for prop in config.PROPERTIES:
        for _ in range(R.randint(10, 13)):
            tenants.append(
                {"tenant": f"TEN-{k:03d}", "property": prop, "base_rent": R.randrange(12, 62) * 1000}
            )
            k += 1
    return tenants


COST_BASE = {
    "Repair & Maintenance": (90, 150),
    "Utilities": (80, 120),
    "Security & cleaning": (40, 70),
    "Marketing": (30, 60),
    "Insurance": (20, 30),
    "Management fee": (50, 80),
}
CORP_BASE = {"Financial expenses": 5400, "Financial income": 150, "Other income": 60}


# ----------------------------------------------------------------------------- events
class World:
    """Trang thai du lieu + nhat ky su kien gieo."""

    def __init__(self) -> None:
        self.tenants = build_tenants()
        self.b_rent: dict[tuple, float] = {}  # (prop, tenant, month) -> amount
        self.a_rent: dict[tuple, float] = {}
        for t in self.tenants:
            for m in M:
                self.b_rent[(t["property"], t["tenant"], m)] = float(t["base_rent"])
                self.a_rent[(t["property"], t["tenant"], m)] = float(t["base_rent"])
        self.b_cost: dict[tuple, float] = {}  # (prop, line, month)
        self.a_cost: dict[tuple, float] = {}
        for prop in config.PROPERTIES:
            for line, (lo, hi) in COST_BASE.items():
                base = R.randrange(lo, hi) * 1000
                for m in M:
                    bud = base * (1 + 0.04 * ((_mi(m) % 6) - 3) / 3) * (1 + R.uniform(-0.01, 0.01))
                    self.b_cost[(prop, line, m)] = round(bud, 0)
                    self.a_cost[(prop, line, m)] = round(bud * (1 + R.uniform(-0.03, 0.03)), 0)
        for line, base_k in CORP_BASE.items():
            for m in M:
                bud = base_k * 1000 * (1 + R.uniform(-0.005, 0.005))
                self.b_cost[(config.CORP, line, m)] = round(bud, 0)
                self.a_cost[(config.CORP, line, m)] = round(bud * (1 + R.uniform(-0.008, 0.008)), 0)
        self.docs: list[dict] = []
        self.gold = defaultdict(
            lambda: {"causes": [], "evidence": [], "prohibited": [], "abstain": False, "notes": []}
        )
        self.event_txns: list[dict] = []
        self.terminated: set[tuple] = set()  # (prop, tenant) da cham dut -> khong tai su dung
        self._doc_n = 100
        self._used: set[tuple] = set()

    # -- helpers ---------------------------------------------------------
    def doc(self, dtype: str, prop: str, period: str, authority: int, title: str, text: str) -> str:
        self._doc_n += 1
        d = {
            "doc_id": f"EV-{self._doc_n}",
            "type": dtype,
            "property": prop,
            "period": period,
            "authority": authority,
            "title": title,
            "text": text,
        }
        self.docs.append(d)
        return d["doc_id"]

    def mark(self, prop: str, line: str, months: list[str], cause: str, ev: list[str],
             prohibited: list[str], note: str | None = None, abstain: bool = False) -> None:
        for m in months:
            g = self.gold[core.case_id(m, prop, line)]
            g["month"], g["property"], g["pl_line"] = m, prop, line
            if cause not in g["causes"]:
                g["causes"].append(cause)
            g["evidence"] += [e for e in ev if e not in g["evidence"]]
            g["prohibited"] += [p for p in prohibited if p not in g["prohibited"]]
            g["abstain"] = g["abstain"] or abstain
            if note:
                g["notes"].append(note)

    def pick_slot(self, lines: list[str], months: range) -> tuple[str, str, str]:
        while True:
            prop = R.choice(config.PROPERTIES)
            line = R.choice(lines)
            m = M[R.choice(list(months))]
            if (prop, line, m) not in self._used:
                self._used.add((prop, line, m))
                return prop, line, m

    def big_tenant(self, prop: str, min_rent: int = 40000) -> dict:
        ok = [t for t in self.tenants
              if t["property"] == prop and (prop, t["tenant"]) not in self.terminated]
        cands = [t for t in ok if t["base_rent"] >= min_rent]
        return R.choice(cands) if cands else max(ok, key=lambda t: t["base_rent"])


PROHIB_REV = ["leasing market slowdown", "tenant payment default"]
PROHIB_COST = ["general inflation", "market price increase"]


def seed_events(w: World) -> None:
    rev_line = "Leasing revenue"
    term_slots = []

    # 1) early_termination x3 (thang 7-9 de gioi han so case YTD)
    for _ in range(3):
        prop = R.choice(config.PROPERTIES)
        t = w.big_tenant(prop)
        w.terminated.add((prop, t["tenant"]))
        m = M[R.randint(6, 8)]
        for mm in M[_mi(m):]:
            w.a_rent[(prop, t["tenant"], mm)] = 0.0
        fee = round(t["base_rent"] * 0.5 / 1000) * 1000
        ev = w.doc(
            "termination_notice", prop, m, 1,
            f"Termination notice {t['tenant']}",
            f"Termination of lease {t['tenant']} at {prop}: effective end of {M[_mi(m)-1]} under "
            f"clause 8.2. Termination fee ${fee/1000:.0f}k payable by tenant, to be recorded in "
            f"{_next(m)} under Other income. Budgeted rent ${t['base_rent']/1000:.0f}k/month ceases from {m}.",
        )
        w.mark(prop, rev_line, M[_mi(m):], "early_termination", [ev], PROHIB_REV,
               note=f"termination fee ${fee/1000:.0f}k expected in {_next(m)} (Other income)")
        term_slots.append((prop, m))

    # 2) handover_delay x2 (lease moi trong budget tu thang m, thuc te m+2)
    for _ in range(2):
        prop = R.choice(config.PROPERTIES)
        m_i = R.randint(4, 6)
        rent = R.randrange(28, 38) * 1000
        k = len(w.tenants) + 1
        ten = f"TEN-{k:03d}"
        w.tenants.append({"tenant": ten, "property": prop, "base_rent": rent})
        for j, mm in enumerate(M):
            w.b_rent[(prop, ten, mm)] = float(rent) if j >= m_i else 0.0
            w.a_rent[(prop, ten, mm)] = float(rent) if j >= m_i + 2 else 0.0
        ev = w.doc(
            "handover_minutes", prop, M[m_i], 2,
            f"Handover minutes {ten}",
            f"{ten} at {prop}: handover postponed from {M[m_i]} to {M[m_i+2]} due to delayed M&E "
            f"completion. Rent (${rent/1000:.0f}k/month) accrues from actual handover date.",
        )
        w.mark(prop, rev_line, [M[m_i], M[m_i + 1]], "handover_delay", [ev], PROHIB_REV)

    # 3) rent_escalation_unbudgeted x2 — offset trong cung case termination
    for prop, m in term_slots[:2]:
        t = w.big_tenant(prop, 30000)
        pct = R.choice([5, 6, 8])
        for mm in M[_mi(m):]:
            key = (prop, t["tenant"], mm)
            if w.a_rent[key] > 0:
                w.a_rent[key] = round(w.a_rent[key] * (1 + pct / 100), 0)
        ev = w.doc(
            "contract_annex", prop, m, 2,
            f"Escalation annex {t['tenant']}",
            f"Annex to lease {t['tenant']} at {prop}: rental escalation {pct}% effective {m} per "
            f"contract schedule; budget was prepared at pre-escalation rate.",
        )
        w.mark(prop, rev_line, M[_mi(m):], "rent_escalation", [ev], PROHIB_REV)

    # 4) new_lease_early x1 (favorable thang m-1)
    prop = R.choice(config.PROPERTIES)
    m_i = R.randint(5, 7)
    rent = R.randrange(30, 40) * 1000
    ten = f"TEN-{len(w.tenants)+1:03d}"
    w.tenants.append({"tenant": ten, "property": prop, "base_rent": rent})
    for j, mm in enumerate(M):
        w.b_rent[(prop, ten, mm)] = float(rent) if j >= m_i else 0.0
        w.a_rent[(prop, ten, mm)] = float(rent) if j >= m_i - 1 else 0.0
    ev = w.doc(
        "handover_minutes", prop, M[m_i - 1], 2, f"Early handover {ten}",
        f"{ten} at {prop}: early handover completed in {M[m_i-1]}, one month ahead of budget; "
        f"rent ${rent/1000:.0f}k/month starts immediately.",
    )
    w.mark(prop, rev_line, [M[m_i - 1]], "new_lease_early", [ev], PROHIB_REV)

    # 5) timing_fee_delay x3 (favorable: phi chua book)
    for _ in range(3):
        prop, line, m = w.pick_slot(["Marketing", "Management fee"], range(2, 9))
        amt = R.randrange(20, 45) * 1000
        w.a_cost[(prop, line, m)] = max(0.0, w.a_cost[(prop, line, m)] - amt)
        ev = w.doc(
            "approval_email", prop, m, 2, f"Fee rescheduled {prop} {m}",
            f"Approved: consultancy fee ${amt/1000:.0f}k budgeted under {line} at {prop} for {m} "
            f"is rescheduled; vendor will invoice in {_next(m)}. Budget phasing unchanged.",
        )
        w.mark(prop, line, [m], "timing_difference", [ev], PROHIB_COST,
               note=f"${amt/1000:.0f}k to be recorded in {_next(m)}")

    # 6) one_off_repair x3 (unfavorable)
    for _ in range(3):
        prop, line, m = w.pick_slot(["Repair & Maintenance"], range(2, 10))
        amt = R.randrange(45, 90) * 1000
        vnd = f"VND-{R.randint(10, 60):03d}"
        desc = R.choice(["roof repair phase 2", "fire pump overhaul", "road surface repair"])
        w.a_cost[(prop, line, m)] += amt
        w.event_txns.append(
            {"month": m, "property": prop, "pl_line": line, "party": vnd,
             "memo": f"{desc} - {prop}", "amount": float(amt)}
        )
        ev1 = w.doc("work_order", prop, m, 1, f"Work order {desc}",
                    f"Work order WO-{R.randint(2000, 2999)} approved: {desc} at {prop}, contractor "
                    f"{vnd}, contract value ${amt/1000:.0f}k, execution {m}.")
        ev2 = w.doc("vendor_invoice", prop, m, 2, f"Invoice {vnd} {desc}",
                    f"Invoice {vnd}: {desc} at {prop}, amount ${amt/1000:.0f}k, service period {m}.")
        w.mark(prop, line, [m], "one_off_event", [ev1, ev2], PROHIB_COST)

    # 7) utilities_rate_change x2 (surcharge 1 thang)
    for _ in range(2):
        prop, line, m = w.pick_slot(["Utilities"], range(3, 10))
        pct = R.choice([22, 25, 30])
        add = round(w.a_cost[(prop, line, m)] * pct / 100, 0)
        w.a_cost[(prop, line, m)] += add
        ev = w.doc("rate_notice", prop, m, 2, f"Tariff surcharge {m}",
                   f"Utility provider notice: temporary tariff surcharge {pct}% applied to {prop} "
                   f"consumption in {m} (approx ${add/1000:.0f}k impact).")
        w.mark(prop, line, [m], "rate_change", [ev], PROHIB_COST)

    # 8) accounting_capitalization x1 (favorable)
    prop, line, m = w.pick_slot(["Repair & Maintenance"], range(3, 9))
    amt = R.randrange(35, 45) * 1000
    w.a_cost[(prop, line, m)] = max(0.0, w.a_cost[(prop, line, m)] - amt)
    ev = w.doc("accounting_memo", prop, m, 2, f"Capitalization memo {prop}",
               f"Accounting memo: ${amt/1000:.0f}k of improvement works at {prop} qualifies for "
               f"capitalization from {m}; {line} expense reduced accordingly vs budget.")
    w.mark(prop, line, [m], "accounting_treatment", [ev], PROHIB_COST)

    # 9) refinancing_gap_interest x2 (CORP, unfavorable)
    for _ in range(2):
        m = M[R.randint(4, 9)]
        while (config.CORP, "Financial expenses", m) in w._used:
            m = M[R.randint(4, 9)]
        w._used.add((config.CORP, "Financial expenses", m))
        amt = R.randrange(150, 250) * 1000
        w.a_cost[(config.CORP, "Financial expenses", m)] += amt
        ev = w.doc("loan_memo", config.CORP, m, 2, f"Refinancing gap {m}",
                   f"Treasury memo: repayment-to-refinancing gap on project facilities in {m}; "
                   f"interest saving assumed in budget (~${amt/1000:.0f}k) does not materialize "
                   f"until new facility drawdown.")
        w.mark(config.CORP, "Financial expenses", [m], "financing_event", [ev],
               ["base rate increase"])

    # 10) one_off_insurance_gain x1 (CORP Other income, favorable)
    m = M[R.randint(5, 8)]
    amt = 300000
    w.a_cost[(config.CORP, "Other income", m)] += amt
    ev = w.doc("insurance_letter", config.CORP, m, 1, "Insurance compensation",
               f"Insurer confirmation: compensation ${amt/1000:.0f}k for storm damage approved; "
               f"recognized under Other income in {m}.")
    w.mark(config.CORP, "Other income", [m], "one_off_event", [ev], ["revaluation gain"])

    # 11) missing_evidence x3 (TRAP: vuot nguong nhung khong co tai lieu)
    for _ in range(3):
        prop, line, m = w.pick_slot(["Marketing", "Security & cleaning"], range(2, 10))
        amt = R.randrange(18, 30) * 1000
        vnd = f"VND-{R.randint(61, 90):03d}"
        w.a_cost[(prop, line, m)] += amt
        w.event_txns.append(
            {"month": m, "property": prop, "pl_line": line, "party": vnd,
             "memo": "sundry services", "amount": float(amt)}
        )
        w.mark(prop, line, [m], "unknown", [], PROHIB_COST + ["one-off campaign"], abstain=True)

    # 12) keyword_trap x2 — chi them tai lieu nhieu (sai property)
    for prop, m in term_slots[:2]:
        other = R.choice([p for p in config.PROPERTIES if p != prop])
        w.doc("distractor_memo", other, m, 3, f"Marketing tour {other}",
              f"Ops memo: marketing tour for prospective tenants at {other} in {m}; discussion of "
              f"lease termination clauses and handover standards for the showcase unit.")

    # distractor chung ~30 doc
    topics = ["routine fire-safety inspection", "landscaping schedule", "quarterly pest control",
              "parking line repainting", "CCTV maintenance visit", "tenant satisfaction survey"]
    for _ in range(30):
        prop = R.choice(config.PROPERTIES)
        m = M[R.randint(0, 11)]
        tp = R.choice(topics)
        w.doc("ops_memo", prop, m, 3, f"{tp} {prop} {m}",
              f"Ops memo: {tp} at {prop} completed in {m}; no budget impact expected.")


# ----------------------------------------------------------------------------- frames
def to_frames(w: World):
    b_rent = pd.DataFrame(
        [{"property": p, "tenant": t, "month": m, "amount": v} for (p, t, m), v in w.b_rent.items()]
    )
    a_rent = pd.DataFrame(
        [{"property": p, "tenant": t, "month": m, "amount": v} for (p, t, m), v in w.a_rent.items()]
    )
    rev_b = b_rent.groupby(["property", "month"], as_index=False)["amount"].sum()
    rev_b["pl_line"] = "Leasing revenue"
    rev_a = a_rent.groupby(["property", "month"], as_index=False)["amount"].sum()
    rev_a["pl_line"] = "Leasing revenue"
    cost_b = pd.DataFrame(
        [{"property": p, "pl_line": l, "month": m, "amount": v} for (p, l, m), v in w.b_cost.items()]
    )
    cost_a = pd.DataFrame(
        [{"property": p, "pl_line": l, "month": m, "amount": v} for (p, l, m), v in w.a_cost.items()]
    )
    budget_line = pd.concat([rev_b, cost_b], ignore_index=True)
    actual_line = pd.concat([rev_a, cost_a], ignore_index=True)

    # GL: rent 1 txn/tenant-thang; cost chia 2-4 txn, event txns giu nguyen memo rieng
    rows, n = [], 1
    for (p, t, m), v in w.a_rent.items():
        if v > 0:
            rows.append({"txn_id": f"GL-{n:05d}", "month": m, "property": p,
                         "pl_line": "Leasing revenue", "party": t, "memo": f"Rent {m}", "amount": v})
            n += 1
    ev_by_key = defaultdict(list)
    for e in w.event_txns:
        ev_by_key[(e["property"], e["pl_line"], e["month"])].append(e)
    for (p, l, m), total in w.a_cost.items():
        evs = ev_by_key.get((p, l, m), [])
        rest = total - sum(e["amount"] for e in evs)
        for e in evs:
            rows.append({"txn_id": f"GL-{n:05d}", "month": m, "property": p, "pl_line": l,
                         "party": e["party"], "memo": e["memo"], "amount": e["amount"]})
            n += 1
        parts = R.randint(2, 4)
        for i in range(parts):
            amt = round(rest / parts, 0)
            rows.append({"txn_id": f"GL-{n:05d}", "month": m, "property": p, "pl_line": l,
                         "party": f"VND-{R.randint(100, 180):03d}",
                         "memo": f"{l} services {m}", "amount": amt})
            n += 1
    gl = pd.DataFrame(rows)
    return b_rent, a_rent, budget_line, actual_line, gl


def main() -> None:
    R.seed(config.SEED)  # idempotent: goi nhieu lan van ra cung mot dataset
    out = config.DATA_DIR
    out.mkdir(parents=True, exist_ok=True)
    w = World()
    seed_events(w)
    b_rent, a_rent, budget_line, actual_line, gl = to_frames(w)

    # gold facts tinh tu bang CUOI CUNG -> khop engine
    gold = {}
    vt_cache: dict[str, pd.DataFrame] = {}
    for cid, g in w.gold.items():
        m, prop, line = g["month"], g["property"], g["pl_line"]
        if m not in vt_cache:
            vt_cache[m] = core.variance_table(budget_line, actual_line, m)
        vt = vt_cache[m]
        row = vt[(vt["property"] == prop) & (vt["pl_line"] == line)]
        if row.empty:
            raise RuntimeError(f"gold case khong co trong data: {cid}")
        r = row.iloc[0]
        gold[cid] = {
            "case_id": cid, "month": m, "property": prop, "pl_line": line,
            "facts": {"budget": float(r["budget"]), "actual": float(r["actual"]),
                      "variance": float(r["variance"])},
            "material": bool(r["material"]),
            "gold_causes": g["causes"], "gold_evidence": g["evidence"],
            "prohibited_claims": g["prohibited"], "abstain": g["abstain"], "notes": g["notes"],
        }

    for name, df in [("tenants", pd.DataFrame(w.tenants)), ("budget_rent", b_rent),
                     ("actual_rent", a_rent), ("budget_line", budget_line),
                     ("actual_line", actual_line), ("gl", gl)]:
        df.to_csv(out / f"{name}.csv", index=False)
    (out / "evidence.json").write_text(json.dumps(w.docs, indent=1), encoding="utf-8")
    (out / "gold_labels.json").write_text(json.dumps(gold, indent=1), encoding="utf-8")

    # engine chay toan bo 12 thang -> cases.json
    all_cases = []
    for m in M:
        all_cases += core.build_cases(budget_line, actual_line, b_rent, a_rent, gl, m)
    (out / "cases.json").write_text(json.dumps(all_cases, indent=1), encoding="utf-8")

    manifest = {
        "dataset_version": config.DATASET_VERSION, "seed": config.SEED,
        "created_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "tenants": len(w.tenants), "evidence_docs": len(w.docs),
        "gl_rows": len(gl), "material_cases_engine": len(all_cases),
        "gold_cases": len(gold),
    }
    (out / "manifest.json").write_text(json.dumps(manifest, indent=1), encoding="utf-8")

    # kiem tra cheo: moi gold case material phai duoc engine tim ra
    engine_ids = {c["case_id"] for c in all_cases}
    missing = [cid for cid, g in gold.items() if g["material"] and cid not in engine_ids]
    extra = sorted(engine_ids - set(gold))
    print(json.dumps(manifest, indent=1))
    print(f"gold material thieu trong engine: {missing}")
    print(f"case engine tim ra ngoai gold (nhieu/noise): {len(extra)} -> {extra[:8]}")
    if missing:
        raise SystemExit("FAIL: gold/engine lech nhau")


if __name__ == "__main__":
    main()
