"""Chay benchmark 3 che do tren frozen case set.

Chay:
  poetry run python -m vwb.experiments.run_benchmark --smoke        # 2 case x 3 mode x 1 rep (Gemini that)
  poetry run python -m vwb.experiments.run_benchmark                # full 34 case x 3 mode x k=3
  poetry run python -m vwb.experiments.run_benchmark --mock         # khong goi API (kiem tra pipeline)

Nguyen tac khach quan (phases/phase3): run_config dong bang + ghi git HEAD; raw luu
results/raw/ (gitignored); summary commit duoc. Free tier rate limit -> sleep giua cac call.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path

from vwb import config
from vwb.experiments import metrics
from vwb.generation.build import generate
from vwb.generation.client import GeminiClient, MockClient
from vwb.retrieval import core as retrieval
from vwb.verification import gates

RESULTS = config.BASE_DIR / "results"
SLEEP_BETWEEN_CALLS = 5.0  # giay — ton trong rate limit free tier


def load_inputs() -> tuple[list[dict], dict, list[dict], dict]:
    cases = json.loads((config.DATA_DIR / "cases.json").read_text(encoding="utf-8"))
    gold = json.loads((config.DATA_DIR / "gold_labels.json").read_text(encoding="utf-8"))
    docs = retrieval.load_evidence()
    packs_file = config.DATA_DIR / config.EVIDENCE_PACKS_FILE
    if packs_file.exists():
        packs = json.loads(packs_file.read_text(encoding="utf-8"))
    else:  # fallback: BM25+metadata (dense precompute chua xong)
        print("! evidence_packs.json chua co -> tinh tam bang BM25+metadata")
        r = retrieval.Retriever(docs, use_dense=False)
        packs = {c["case_id"]: r.retrieve(c) for c in cases}
    return cases, gold, docs, packs


def pick_smoke(cases: list[dict], gold: dict) -> list[dict]:
    normal = next(c for c in cases if not gold[c["case_id"]]["abstain"])
    trap = next(c for c in cases if gold[c["case_id"]]["abstain"])
    return [normal, trap]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--mock", action="store_true")
    ap.add_argument("--k", type=int, default=3)
    args = ap.parse_args()

    cases, gold, docs, packs = load_inputs()
    if args.smoke:
        cases, k = pick_smoke(cases, gold), 1
    else:
        k = args.k
    client = MockClient() if args.mock else GeminiClient()

    head = subprocess.run(["git", "rev-parse", "--short", "HEAD"],
                          capture_output=True, text=True).stdout.strip()
    run_config = {
        "model": client.model_id, "temperature": config.GEN_TEMPERATURE,
        "prompt_version": config.PROMPT_VERSION, "dataset_version": config.DATASET_VERSION,
        "k": k, "n_cases": len(cases), "git_head": head,
        "started_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "smoke": args.smoke, "mock": args.mock,
        "dense_in_packs": any(p.get("dense_used") for p in packs.values()),
    }
    raw_dir = RESULTS / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)
    (RESULTS / "run_config.json").write_text(json.dumps(run_config, indent=1), encoding="utf-8")

    tag = "smoke" if args.smoke else "full"
    raw_path = raw_dir / f"records_{tag}.jsonl"
    records: list[dict] = []
    total = len(cases) * 3 * k
    done = 0
    with open(raw_path, "w", encoding="utf-8") as f:
        for case in cases:
            pack = packs[case["case_id"]]
            for mode in ("m0", "m1", "m2"):
                for rep in range(k):
                    try:
                        output = generate(mode, case, pack, client)
                    except Exception as e:  # ghi loi, khong dung ca run
                        output = {"draft_comment": "", "abstained": False,
                                  "error": str(e)[:300], "mode": mode,
                                  "case_id": case["case_id"]}
                    verdict = gates.verify(output, case, docs, pack)
                    rec = {"case_id": case["case_id"], "mode": mode, "rep": rep,
                           "case": case, "output": output, "verdict": verdict}
                    records.append(rec)
                    f.write(json.dumps({k2: v for k2, v in rec.items() if k2 != "case"},
                                       ensure_ascii=False) + "\n")
                    done += 1
                    if done % 10 == 0 or args.smoke:
                        print(f"[{done}/{total}] {case['case_id']} {mode} rep{rep} "
                              f"-> {verdict['overall']}")
                    if not args.mock:
                        time.sleep(SLEEP_BETWEEN_CALLS)

    info = metrics.compute(records, gold, packs, RESULTS)
    n_err = sum(1 for r in records if r["output"].get("error"))
    print(json.dumps({**info, "errors": n_err, "raw": str(raw_path)}, ensure_ascii=False))
    print((RESULTS / "summary.csv").read_text(encoding="utf-8-sig"))


if __name__ == "__main__":
    main()
