"""Cham diem benchmark theo cac dinh nghia da doc tu nguon goc (docs/paper_notes.md).

Moi ham ghi ro goc hoc thuat + diem adaptation. Tat ca TAT DINH tren gold labels —
khong dung LLM lam giam khao (quyet dinh #25).
"""

from __future__ import annotations

import json
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


def _mean_or_none(xs: list[float | None]) -> float | None:
    """Trung bình trong một lần chạy, bỏ các quan sát không áp dụng."""
    valid = [x for x in xs if x is not None]
    return st.mean(valid) if valid else None


def _across_repetitions(rows: list[dict], key: str) -> str:
    """Tính mean ± SD từ các trung bình theo rep, không trộn case dễ/khó với độ dao động LLM."""
    by_rep: dict[int, list[float | None]] = {}
    for row in rows:
        by_rep.setdefault(row["rep"], []).append(row[key])
    rep_means = [_mean_or_none(by_rep[rep]) for rep in sorted(by_rep)]
    return _mean_sd(rep_means)


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
    ."""
    import csv

    out_dir.mkdir(parents=True, exist_ok=True)
    docs_by_id = {d["doc_id"]: d for d in (docs or [])}
    per_mode: dict[str, dict[str, list]] = {}
    for r in records:
        g = gold_all[r["case_id"]]
        o = r["output"]
        m = per_mode.setdefault(r["mode"], {
            "numeric": [], "cit_p": [], "cit_r": [], "unsup": [],
            "abstain_ok": [], "asserted": [], "risk_bad": [], "prohibited": [],
            "scenario_rows": [], "rep_rows": [],
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
        m["scenario_rows"].append((scenario_of(g), r["case_id"], r["rep"], un, num))
        m["rep_rows"].append({
            "rep": r["rep"], "numeric": num, "cit_p": cp, "cit_r": cr,
            "unsup": un, "prohibited": 1.0 if prohibited_hit(o, g) else 0.0,
            "abstain_ok": (1.0 if not asserted else 0.0) if g["abstain"] else None,
            "asserted": 1.0 if asserted else 0.0,
            "risk_bad": (1.0 if (g["abstain"] or prohibited_hit(o, g)) else 0.0)
                        if asserted else None,
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
            w.writerow([name] + [
                _across_repetitions(per_mode[md]["rep_rows"], key)
                for md in sorted(per_mode)
            ])
        p5, r5 = retrieval_pr_at_k(packs, gold_all)
        w.writerow([f"retrieval_P@{config.TOP_K_EVIDENCE}", f"{p5:.3f}", "", ""])
        w.writerow([f"retrieval_R@{config.TOP_K_EVIDENCE}", f"{r5:.3f}", "", ""])

    with open(out_dir / "summary_by_rep.csv", "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["mode", "rep", "numeric_accuracy", "citation_precision",
                    "citation_recall", "unsupported_claim_rate", "prohibited_claim_rate",
                    "abstain_recall(trap)", "coverage", "risk_on_asserted"])
        keys = ["numeric", "cit_p", "cit_r", "unsup", "prohibited",
                "abstain_ok", "asserted", "risk_bad"]
        for md, m in sorted(per_mode.items()):
            reps = sorted({row["rep"] for row in m["rep_rows"]})
            for rep in reps:
                rows = [row for row in m["rep_rows"] if row["rep"] == rep]
                vals = [_mean_or_none([row[key] for row in rows]) for key in keys]
                w.writerow([md, rep] + ["n/a" if v is None else f"{v:.6f}" for v in vals])

    with open(out_dir / "by_scenario.csv", "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["mode", "scenario", "n", "unsupported_rate", "numeric_accuracy"])
        for md, m in sorted(per_mode.items()):
            by: dict[str, list] = {}
            for sc, cid, rep, un, num in m["scenario_rows"]:
                by.setdefault(sc, []).append((cid, rep, un, num))
            for sc, vals in sorted(by.items()):
                reps = sorted({v[1] for v in vals})
                unsup_rep = [_mean_or_none([v[2] for v in vals if v[1] == rep]) for rep in reps]
                numeric_rep = [_mean_or_none([v[3] for v in vals if v[1] == rep]) for rep in reps]
                w.writerow([md, sc, len({v[0] for v in vals}),
                            _mean_sd(unsup_rep), _mean_sd(numeric_rep)])

    return {"modes": sorted(per_mode), "n_records": len(records)}
