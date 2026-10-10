"""Cham diem benchmark theo cac dinh nghia da doc tu nguon goc (docs/paper_notes.md).

Moi ham ghi ro goc hoc thuat + diem adaptation. Tat ca TAT DINH tren gold labels —
khong dung LLM lam giam khao (quyet dinh #25).
"""

from __future__ import annotations

import json
import random
import re
import statistics as st

from vwb import config
from vwb.verification import gates

CAUSAL_MARKERS = ("due to", "driven by", "mainly", "because", "owing to", "as a result")
_EVID = re.compile(r"\[(EV-\d+)\]")


# ----------------------------------------------------------------- per-record
def numeric_accuracy(output: dict, case: dict, docs_by_id: dict | None = None) -> float | None:
    """EM giu DAU va SCALE (TAT-QA §4.2), khop theo TRUONG engine (FinQA §3.2);
    chap nhan them: phan so chep tu FACTS, gia tri 0, va so quote tu tai lieu DA cite."""
    cited = [docs_by_id[c] for c in cited_ids(output) if docs_by_id and c in docs_by_id]
    v = gates.numeric_gate(output, case, cited)
    if not v:
        return None
    return sum(1 for x in v if x["ok"]) / len(v)


def cited_ids(output: dict) -> list[str]:
    ids = _EVID.findall(output.get("draft_comment", ""))
    for key in ("drivers_confirmed", "drivers_possible", "offsets"):
        for item in output.get(key, []) or []:
            if isinstance(item, dict):
                ids += item.get("evidence_ids", [])
    return list(dict.fromkeys(ids))


def citation_pr(output: dict, gold: dict) -> tuple[float | None, float | None]:
    """Citation precision/recall (ALCE §3.3, adaptation: so voi GOLD evidence IDs
    thay vi NLI entailment — benchmark co dap an gan san)."""
    cited = set(cited_ids(output))
    gold_ev = set(gold["gold_evidence"])
    if not cited:
        return (None, 0.0 if gold_ev else None)
    if not gold_ev:
        return (0.0, None)
    inter = cited & gold_ev
    return (len(inter) / len(cited), len(inter) / len(gold_ev))


def _causal_sentences(text: str) -> list[str]:
    sents = [s.strip() for s in re.split(r"[.;\n]", text) if s.strip()]
    return [s for s in sents if any(m in s.lower() for m in CAUSAL_MARKERS)]


def claims_of(output: dict) -> list[dict]:
    """Don vi 'menh de nguyen nhan' de cham (atomic theo FActScore §2).
    M2: tung item drivers_confirmed (atomic-by-construction).
    M0/M1 (van tu do): cau chua causal marker; citation = [EV-x] trong cau do."""
    if output.get("drivers_confirmed"):
        return [
            {"text": it["text"], "cited": it.get("evidence_ids", [])}
            for it in output["drivers_confirmed"] if isinstance(it, dict)
        ]
    return [
        {"text": s, "cited": _EVID.findall(s)} for s in _causal_sentences(
            output.get("draft_comment", "")
        )
    ]


def unsupported_claim_rate(output: dict, gold: dict) -> float | None:
    """Ty le menh de nguyen nhan KHONG duoc gold evidence do (FActScore/AIS adaptation:
    supported <=> cite >=1 gold evidence id)."""
    claims = claims_of(output)
    if not claims:
        return None
    gold_ev = set(gold["gold_evidence"])
    unsupported = sum(1 for c in claims if not (set(c["cited"]) & gold_ev))
    return unsupported / len(claims)


def asserted_cause(output: dict) -> bool:
    """He thong co 'dam neu nguyen nhan' khong (coverage trong khung Kamath 2020)."""
    if output.get("abstained"):
        return False
    if output.get("drivers_confirmed"):
        return True
    return bool(_causal_sentences(output.get("draft_comment", "")))


def prohibited_hit(output: dict, gold: dict) -> bool:
    text = json.dumps(output, ensure_ascii=False).lower()
    return any(p.lower() in text for p in gold.get("prohibited_claims", []))


# ----------------------------------------------------------------- aggregate
def _mean_sd(xs: list[float]) -> str:
    xs = [x for x in xs if x is not None]
    if not xs:
        return "n/a"
    m = st.mean(xs)
    sd = st.stdev(xs) if len(xs) > 1 else 0.0
    return f"{m:.3f}±{sd:.3f}"


def retrieval_pr_at_k(packs: dict, gold_all: dict) -> tuple[float, float]:
    """P@k / R@k co dien (Manning va cong su 2008) tren case co gold evidence."""
    ps, rs = [], []
    for cid, g in gold_all.items():
        if not g["gold_evidence"]:
            continue
        got = [d["doc_id"] for d in packs.get(cid, {}).get("docs", [])]
        if not got:
            ps.append(0.0); rs.append(0.0); continue
        inter = set(got) & set(g["gold_evidence"])
        ps.append(len(inter) / len(got))
        rs.append(len(inter) / len(g["gold_evidence"]))
    return (st.mean(ps) if ps else 0.0, st.mean(rs) if rs else 0.0)


def scenario_of(gold: dict) -> str:
    if gold["abstain"]:
        return "missing_evidence"
    return gold["gold_causes"][0] if gold["gold_causes"] else "other"


def compute(records: list[dict], gold_all: dict, packs: dict, out_dir,
            docs: list[dict] | None = None) -> dict:
    """records: [{case_id, mode, rep, output, verdict}] -> summary/by_scenario/coverage_risk CSV
    + kappa_sample.csv (20% menh de cho nguoi cham tay, Cohen 1960)."""
    import csv

    out_dir.mkdir(parents=True, exist_ok=True)
    docs_by_id = {d["doc_id"]: d for d in (docs or [])}
    per_mode: dict[str, dict[str, list]] = {}
    rows_claims = []
    for r in records:
        g = gold_all[r["case_id"]]
        o = r["output"]
        m = per_mode.setdefault(r["mode"], {
            "numeric": [], "cit_p": [], "cit_r": [], "unsup": [],
            "abstain_ok": [], "asserted": [], "risk_bad": [], "prohibited": [],
            "scenario_rows": [],
        })
        case = r["case"]
        num = numeric_accuracy(o, case, docs_by_id)
        cp, cr = citation_pr(o, g)
        un = unsupported_claim_rate(o, g)
        m["numeric"].append(num)
        m["cit_p"].append(cp)
        m["cit_r"].append(cr)
        m["unsup"].append(un)
        m["prohibited"].append(1.0 if prohibited_hit(o, g) else 0.0)
        asserted = asserted_cause(o)
        m["asserted"].append(1.0 if asserted else 0.0)
        if g["abstain"]:
            m["abstain_ok"].append(1.0 if not asserted else 0.0)
        if asserted:  # risk: dam neu nguyen nhan tren case bay, hoac dinh claim cam
            m["risk_bad"].append(1.0 if (g["abstain"] or prohibited_hit(o, g)) else 0.0)
        m["scenario_rows"].append((scenario_of(g), un, num))
        for c in claims_of(o):
            rows_claims.append({
                "mode": r["mode"], "case_id": r["case_id"], "rep": r["rep"],
                "claim": c["text"][:200], "cited": ";".join(c["cited"]),
                "auto_supported": bool(set(c["cited"]) & set(g["gold_evidence"])),
                "human_supported": "",  # nguoi cham tay dien 1/0
            })

    with open(out_dir / "summary.csv", "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["metric"] + sorted(per_mode))
        met_defs = [
            ("numeric_accuracy", "numeric"), ("citation_precision", "cit_p"),
            ("citation_recall", "cit_r"), ("unsupported_claim_rate", "unsup"),
            ("prohibited_claim_rate", "prohibited"),
            ("abstain_recall(trap)", "abstain_ok"), ("coverage", "asserted"),
            ("risk_on_asserted", "risk_bad"),
        ]
        for name, key in met_defs:
            w.writerow([name] + [_mean_sd(per_mode[md][key]) for md in sorted(per_mode)])
        p5, r5 = retrieval_pr_at_k(packs, gold_all)
        w.writerow([f"retrieval_P@{config.TOP_K_EVIDENCE}", f"{p5:.3f}", "", ""])
        w.writerow([f"retrieval_R@{config.TOP_K_EVIDENCE}", f"{r5:.3f}", "", ""])

    with open(out_dir / "by_scenario.csv", "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["mode", "scenario", "n", "unsupported_rate", "numeric_accuracy"])
        for md, m in sorted(per_mode.items()):
            by: dict[str, list] = {}
            for sc, un, num in m["scenario_rows"]:
                by.setdefault(sc, []).append((un, num))
            for sc, vals in sorted(by.items()):
                w.writerow([md, sc, len(vals),
                            _mean_sd([v[0] for v in vals]), _mean_sd([v[1] for v in vals])])

    rnd = random.Random(config.SEED)
    sample = rnd.sample(rows_claims, max(1, len(rows_claims) // 5)) if rows_claims else []
    with open(out_dir / "kappa_sample.csv", "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=["mode", "case_id", "rep", "claim", "cited",
                                          "auto_supported", "human_supported"])
        w.writeheader()
        w.writerows(sample)

    return {"modes": sorted(per_mode), "n_records": len(records),
            "kappa_sample": len(sample)}
