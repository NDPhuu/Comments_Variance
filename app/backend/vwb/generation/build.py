"""Lap context va goi LLM cho 3 che do M0/M1/M2 (dinh nghia: docs/architecture.md §2).

Fairness: cung mot client/model cho ca 3 modes; chi khac noi dung context va schema.
"""

from __future__ import annotations

import json
from pathlib import Path

from vwb import config
from vwb.generation.client import LLMClient, parse_json_output

PROMPT_DIR = Path(__file__).parent / "prompts_llm"
TAXONOMY = (
    "early_termination, handover_delay, new_lease_early, rent_escalation, "
    "timing_difference, one_off_event, rate_change, accounting_treatment, financing_event"
)


def _case_table(case: dict) -> str:
    rows = [
        f"P&L line: {case['pl_line']} | Property: {case['property']} | Month: {case['month']}",
        f"Budget: {case['budget']:,.0f} | Actual: {case['actual']:,.0f} | "
        f"Variance: {case['variance']:+,.0f}"
        + (f" ({case['variance_pct']:+.1%})" if case.get("variance_pct") is not None else ""),
        "Contributors:",
    ]
    for c in case.get("contributors", []):
        rows.append(
            f"  - {c.get('key')} | {c.get('memo', c.get('kind', ''))} | {c['delta']:+,.0f}"
        )
    return "\n".join(rows)


def _evidence_block(pack: dict) -> str:
    if not pack.get("docs"):
        return "(no documents retrieved)"
    return "\n".join(
        f"[{d['doc_id']}] ({d['type']}, {d['property']}, {d['period']}) {d['text']}"
        for d in pack["docs"]
    )


def build_prompt(mode: str, case: dict, pack: dict | None) -> str:
    tpl = (PROMPT_DIR / f"{mode}.txt").read_text(encoding="utf-8")
    return tpl.format(
        case_table=_case_table(case),
        evidence_block=_evidence_block(pack or {"docs": []}),
        facts_json=json.dumps(
            {k: case[k] for k in ("case_id", "pl_line", "property", "month", "budget",
                                   "actual", "variance", "variance_pct", "direction",
                                   "contributors")},
            indent=1,
        ),
        taxonomy=TAXONOMY,
    )


def generate(mode: str, case: dict, pack: dict | None, client: LLMClient) -> dict:
    """Tra output da chuan hoa: luon co draft_comment + abstained (+ cac truong M2)."""
    if mode not in ("m0", "m1", "m2"):
        raise ValueError(f"mode la m0/m1/m2, nhan duoc: {mode}")
    prompt = build_prompt(mode, case, pack if mode != "m0" else None)
    out = parse_json_output(client.generate(prompt))
    out.setdefault("draft_comment", "")
    out.setdefault("abstained", False)
    out["mode"] = mode
    out["case_id"] = case["case_id"]
    out["model_id"] = client.model_id
    out["prompt_version"] = config.PROMPT_VERSION
    return out
