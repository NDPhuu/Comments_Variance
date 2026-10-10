"""Cham lai metrics tu raw records (khong goi API) — dung sau khi va gate.

Chay: poetry run python -m vwb.experiments.recompute [records_full.jsonl]
"""

from __future__ import annotations

import json
import sys

from vwb import config
from vwb.experiments import metrics
from vwb.retrieval import core as retrieval

RESULTS = config.BASE_DIR / "results"


def main() -> None:
    name = sys.argv[1] if len(sys.argv) > 1 else "records_full.jsonl"
    raw = RESULTS / "raw" / name
    cases = {c["case_id"]: c for c in json.loads(
        (config.DATA_DIR / "cases.json").read_text(encoding="utf-8"))}
    gold = json.loads((config.DATA_DIR / "gold_labels.json").read_text(encoding="utf-8"))
    packs = json.loads(
        (config.DATA_DIR / config.EVIDENCE_PACKS_FILE).read_text(encoding="utf-8"))
    docs = retrieval.load_evidence()
    records = []
    for line in raw.read_text(encoding="utf-8").splitlines():
        r = json.loads(line)
        r["case"] = cases[r["case_id"]]
        records.append(r)
    info = metrics.compute(records, gold, packs, RESULTS, docs=docs)
    print(json.dumps(info, ensure_ascii=False))
    print((RESULTS / "summary.csv").read_text(encoding="utf-8-sig"))


if __name__ == "__main__":
    main()
