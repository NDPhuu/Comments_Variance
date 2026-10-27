"""FastAPI backend for Variance Workbench — wraps existing vwb modules.

Runtime deps: fastapi, uvicorn, google-genai, python-dotenv.
Heavy deps (pandas, flagembedding, rank-bm25) NOT needed — evidence packs precomputed.
"""

from __future__ import annotations

import csv
import json
import os
from contextlib import asynccontextmanager
from io import StringIO
from pathlib import Path

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from vwb import config
from vwb.generation.build import generate
from vwb.generation.client import GeminiClient, LLMClient
from vwb.verification.gates import verify

# ---------------------------------------------------------------------------
# Data stores — loaded once at startup
# ---------------------------------------------------------------------------
_cases: list[dict] = []
_cases_by_id: dict[str, dict] = {}
_evidence: list[dict] = []
_packs: dict[str, dict] = {}
_records: dict[str, dict] = {}
_summary: list[dict] = []
_by_rep: list[dict] = []
_by_scenario: list[dict] = []

DATA_DIR = config.DATA_DIR
RESULTS_DIR = config.BASE_DIR / "results"


def _load_csv(path: Path) -> list[dict]:
    if not path.exists():
        return []
    return list(csv.DictReader(StringIO(path.read_text("utf-8-sig").strip())))


def _load_data() -> None:
    global _cases, _cases_by_id, _evidence, _packs, _records
    global _summary, _by_rep, _by_scenario

    _cases = json.loads((DATA_DIR / "cases.json").read_text("utf-8"))
    _cases_by_id = {c["case_id"]: c for c in _cases}
    _evidence = json.loads((DATA_DIR / "evidence.json").read_text("utf-8"))
    _packs = json.loads((DATA_DIR / "evidence_packs.json").read_text("utf-8"))

    records_path = RESULTS_DIR / "raw" / "records_full.jsonl"
    if records_path.exists():
        for line in records_path.read_text("utf-8").strip().splitlines():
            r = json.loads(line)
            _records.setdefault(r["case_id"], {}).setdefault(r["mode"], {})[
                r["rep"]
            ] = {"output": r["output"], "verdict": r.get("verdict")}

    _summary = _load_csv(RESULTS_DIR / "summary.csv")
    _by_rep = _load_csv(RESULTS_DIR / "summary_by_rep.csv")
    _by_scenario = _load_csv(RESULTS_DIR / "by_scenario.csv")


# ---------------------------------------------------------------------------
# LLM client — lazy init (only when /generate is called)
# ---------------------------------------------------------------------------
_llm: LLMClient | None = None


def _get_llm() -> LLMClient:
    global _llm
    if _llm is None:
        _llm = GeminiClient()
    return _llm


# ---------------------------------------------------------------------------
# App
# ---------------------------------------------------------------------------
@asynccontextmanager
async def lifespan(_app: FastAPI):
    _load_data()
    yield


app = FastAPI(title="Variance Workbench API", version="1.0", lifespan=lifespan)

ALLOWED_ORIGINS = os.environ.get("CORS_ORIGINS", "*").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_methods=["*"],
    allow_headers=["*"],
)


def _find_case(case_id: str) -> dict:
    c = _cases_by_id.get(case_id)
    if c is None:
        raise HTTPException(404, f"Case not found: {case_id}")
    return c


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------
@app.api_route("/api/health", methods=["GET", "HEAD"])
def health():
    return {"status": "ok", "cases": len(_cases)}


@app.get("/api/meta")
def meta():
    return {
        "dataset_version": config.DATASET_VERSION,
        "model": config.GEN_MODEL,
        "prompt_version": config.PROMPT_VERSION,
        "materiality": config.MATERIALITY,
        "months": config.MONTHS,
        "properties": config.PROPERTIES + [config.CORP],
    }


@app.get("/api/cases")
def list_cases(
    month: str | None = Query(None),
    property: str | None = Query(None),
):
    result = _cases
    if month:
        result = [c for c in result if c["month"] == month]
    if property:
        result = [c for c in result if c["property"] == property]
    return {"cases": result, "total": len(result)}


@app.get("/api/cases/{case_id}")
def get_case(case_id: str):
    return _find_case(case_id)


@app.get("/api/cases/{case_id}/evidence")
def get_evidence(case_id: str):
    _find_case(case_id)
    pack = _packs.get(case_id)
    if pack is None:
        raise HTTPException(404, f"No evidence pack for: {case_id}")
    return pack


@app.get("/api/cases/{case_id}/records")
def get_records(case_id: str):
    """Pre-computed M0/M1/M2 outputs from benchmark run."""
    _find_case(case_id)
    return {"case_id": case_id, "records": _records.get(case_id, {})}


class GenerateRequest(BaseModel):
    mode: str


@app.post("/api/cases/{case_id}/generate")
def generate_commentary(case_id: str, req: GenerateRequest):
    if req.mode not in ("m0", "m1", "m2"):
        raise HTTPException(400, "mode must be m0, m1, or m2")
    case = _find_case(case_id)
    pack = _packs.get(case_id, {"docs": []})
    client = _get_llm()
    try:
        output = generate(req.mode, case, pack, client)
    except Exception as e:
        raise HTTPException(502, f"LLM generation failed: {e}")
    return output


class VerifyRequest(BaseModel):
    output: dict


@app.post("/api/cases/{case_id}/verify")
def verify_commentary(case_id: str, req: VerifyRequest):
    case = _find_case(case_id)
    pack = _packs.get(case_id, {"docs": []})
    verdict = verify(req.output, case, _evidence, pack)
    return verdict


@app.get("/api/benchmark/summary")
def benchmark_summary():
    return {"summary": _summary, "byRep": _by_rep}


@app.get("/api/benchmark/by-scenario")
def benchmark_by_scenario():
    return {"byScenario": _by_scenario}


@app.get("/api/evidence/{doc_id}")
def get_evidence_doc(doc_id: str):
    for d in _evidence:
        if d["doc_id"] == doc_id:
            return d
    raise HTTPException(404, f"Document not found: {doc_id}")
