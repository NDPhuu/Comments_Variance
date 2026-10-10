"""Cong kiem chung tat dinh — fail-closed, khong dung LLM.

- Numeric gate: boc moi con so trong comment, doi chieu TUNG TRUONG cua VarianceCase;
  GIU DAU va SCALE k/m (theo TAT-QA, xem docs/paper_notes.md §3; khop theo truong de
  tranh "trung do may" theo FinQA §4).
- Citation gate: [EV-x] phai ton tai + dung pham vi property + ky <= thang case.
- Claim gate: moi driver_confirmed phai co >=1 citation hop le (atomic theo FActScore).
- Abstention gate: evidence yeu -> output PHAI abstain (selective prediction, Kamath 2020).
"""

from __future__ import annotations

import re

from vwb import config

REL_TOL = 0.005  # 0.5% — cho phep viet 62,500 thanh $62.5k, KHONG cho lech scale/sign
PCT_TOL = 0.15   # diem phan tram

_NUM = re.compile(
    r"(?<![A-Za-z0-9-])([+\-−–~]?)\$?\s?(\d{1,3}(?:,\d{3})+|\d+(?:\.\d+)?)\s*(k|m|bn|%)?",
    re.I,
)
_EVID = re.compile(r"\[(EV-\d+)\]")
_SKIP_CTX = re.compile(r"(EV-|TEN-|GL-|VND-|PROP-|WO-|\d{4}-\d{2})")


def parse_numbers(text: str) -> list[dict]:
    """Tra [{raw, value(signed, USD), is_pct, approx}] — bo qua ma dinh danh/ngay."""
    out = []
    for m in _NUM.finditer(text):
        start = max(0, m.start() - 5)
        if _SKIP_CTX.search(text[start : m.end() + 3]):
            continue
        sign_s, num_s, suffix = m.group(1), m.group(2), (m.group(3) or "").lower()
        val = float(num_s.replace(",", ""))
        # So "tran" (khong $, dau, hau to, phay, thap phan): bo neu nho hoac giong nam —
        # "phase 2", "in 2026" khong phai so tai chinh
        bare = (
            "$" not in m.group(0) and suffix == "" and sign_s == ""
            and "," not in num_s and "." not in num_s
        )
        if bare and (val < 1000 or 1900 <= val <= 2100):
            continue
        if suffix == "k":
            val *= 1_000
        elif suffix == "m":
            val *= 1_000_000
        elif suffix == "bn":
            val *= 1_000_000_000
        sign = -1.0 if sign_s in ("-", "−", "–") else 1.0
        out.append(
            {
                "raw": m.group(0).strip(),
                "value": sign * val,
                "is_pct": suffix == "%",
                "approx": sign_s == "~",
            }
        )
    return out


def engine_fields(case: dict) -> dict[str, float]:
    """Cac gia tri duoc phep xuat hien trong comment, kem ten truong."""
    f = {
        "budget": case["budget"],
        "actual": case["actual"],
        "variance": case["variance"],
        "variance_abs": abs(case["variance"]),
    }
    for c in case.get("contributors", []):
        f[f"contributor:{c['key']}"] = c["delta"]
        f[f"contributor_abs:{c['key']}"] = abs(c["delta"])
    return f


def _match(value: float, approx: bool, fields: dict[str, float]) -> str | None:
    tol_rel = 0.05 if approx else REL_TOL
    for name, v in fields.items():
        if v == 0:
            continue
        if abs(value - v) <= max(1.0, tol_rel * abs(v)):
            return name
    return None


def numeric_gate(output: dict, case: dict) -> list[dict]:
    text_parts = [output.get("draft_comment", "")]
    for key in ("observed_facts", "drivers_confirmed", "drivers_possible", "offsets"):
        for item in output.get(key, []) or []:
            text_parts.append(item["text"] if isinstance(item, dict) else str(item))
    fields = engine_fields(case)
    pct = case.get("variance_pct")
    verdicts = []
    for n in parse_numbers(" \n ".join(text_parts)):
        if n["is_pct"]:
            ok = pct is not None and abs(abs(n["value"]) - abs(pct) * 100) <= PCT_TOL
            verdicts.append({**n, "matched": "variance_pct" if ok else None, "ok": ok})
        else:
            matched = _match(n["value"], n["approx"], fields)
            verdicts.append({**n, "matched": matched, "ok": matched is not None})
    return verdicts


def citation_gate(output: dict, docs_by_id: dict[str, dict], case: dict) -> list[dict]:
    ids: list[str] = _EVID.findall(output.get("draft_comment", ""))
    for key in ("drivers_confirmed", "drivers_possible", "offsets"):
        for item in output.get(key, []) or []:
            if isinstance(item, dict):
                ids += item.get("evidence_ids", [])
    verdicts = []
    for cid in dict.fromkeys(ids):  # giu thu tu, bo trung
        d = docs_by_id.get(cid)
        if d is None:
            verdicts.append({"id": cid, "ok": False, "reason": "khong ton tai"})
            continue
        scope_ok = d["property"] == case["property"] or (
            case["property"] == config.CORP and d["property"] == config.CORP
        )
        period_ok = d["period"] <= case["month"]
        ok = scope_ok and period_ok
        verdicts.append(
            {"id": cid, "ok": ok,
             "reason": "" if ok else ("sai property" if not scope_ok else "sau ky bao cao")}
        )
    return verdicts


def claim_gate(output: dict, citation_verdicts: list[dict]) -> list[dict]:
    ok_ids = {v["id"] for v in citation_verdicts if v["ok"]}
    verdicts = []
    for item in output.get("drivers_confirmed", []) or []:
        cited = item.get("evidence_ids", []) if isinstance(item, dict) else []
        supported = any(c in ok_ids for c in cited)
        verdicts.append(
            {"text": item["text"] if isinstance(item, dict) else str(item),
             "supported": supported}
        )
    return verdicts


def abstention_gate(output: dict, pack: dict) -> dict:
    """Evidence 'yeu' = khong doc nao LIEN KET noi dung voi case (xem retrieval.core.linked).

    Diem BM25 tho khong so sanh duoc giua cac case (IDF khac nhau) — da kiem chung
    tren dataset: case that co the diem thap hon case bay. Linkage tat dinh thay the.
    """
    docs = pack.get("docs") or []
    weak = not any(d.get("linked") for d in docs)
    abstained = bool(output.get("abstained"))
    has_confirmed = bool(output.get("drivers_confirmed"))
    ok = (abstained and not has_confirmed) if weak else True
    return {"evidence_weak": weak, "abstained": abstained, "ok": ok,
            "over_abstain": abstained and not weak}


def verify(output: dict, case: dict, docs: list[dict], pack: dict) -> dict:
    docs_by_id = {d["doc_id"]: d for d in docs}
    numbers = numeric_gate(output, case)
    citations = citation_gate(output, docs_by_id, case)
    claims = claim_gate(output, citations)
    abst = abstention_gate(output, pack)
    ok = (
        all(n["ok"] for n in numbers)
        and all(c["ok"] for c in citations)
        and all(c["supported"] for c in claims)
        and abst["ok"]
    )
    return {"numbers": numbers, "citations": citations, "claims": claims,
            "abstention": abst, "overall": "verified" if ok else "flagged"}
