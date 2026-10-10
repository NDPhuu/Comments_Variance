"""Truy xuat bang chung: metadata filter -> BM25 (+ dense BGE-M3 neu co) -> fusion RRF.

Nguyen tac (docs/architecture.md 4.3): loc dung property/ky TRUOC khi so khop noi dung —
day la co che ne bay trung-tu-khoa (thiet ke bay theo SQuAD 2.0, xem docs/paper_notes.md §6).
Corpus va case co dinh -> evidence pack duoc PRECOMPUTE va luu file; runtime khong can model.
"""

from __future__ import annotations

import json
import re

from rank_bm25 import BM25Okapi

from vwb import config

try:  # dense retrieval la tuy chon (cut line: BM25 + metadata)
    from FlagEmbedding import BGEM3FlagModel  # type: ignore

    _HAS_DENSE = True
except ImportError:
    _HAS_DENSE = False


def _tokenize(text: str) -> list[str]:
    return re.findall(r"[a-z0-9]+", text.lower())


def load_evidence() -> list[dict]:
    return json.loads((config.DATA_DIR / "evidence.json").read_text(encoding="utf-8"))


def case_query(case: dict) -> str:
    """Query dung tu du lieu CO CAU TRUC cua case (khong can LLM)."""
    parts = [case["property"], case["pl_line"], case["month"]]
    for c in case.get("contributors", []):
        parts += [str(c.get("key", "")), str(c.get("party", "")), str(c.get("memo", ""))]
    return " ".join(parts)


def metadata_filter(docs: list[dict], case: dict) -> list[dict]:
    """Giu doc dung property (hoac CORP-level cho case CORP) va ky <= thang cua case."""
    out = []
    for d in docs:
        same_scope = d["property"] == case["property"]
        if case["property"] == config.CORP:
            same_scope = d["property"] == config.CORP
        if same_scope and d["period"] <= case["month"]:
            out.append(d)
    return out


_STOP = {
    "the", "at", "in", "of", "for", "and", "on", "to", "a", "an", "per", "with", "by",
    "from", "is", "are", "was", "be", "no", "not", "now", "under", "monthly", "month",
    "services", "service", "budget", "budgeted", "phasing", "unchanged", "impact",
    "expected", "completed",
}


def _informative_tokens(case: dict) -> tuple[set[str], set[str], set[str]]:
    """(id_tokens, memo_word_tokens, pl_line_tokens) — da tru stopword/property/thang-nam."""
    prop_toks = set(_tokenize(case["property"]))
    time_toks = set(_tokenize(case["month"]))
    line_toks = set(_tokenize(case["pl_line"])) - _STOP
    id_toks: set[str] = set()
    word_toks: set[str] = set()
    for c in case.get("contributors", []):
        for field in ("key", "party"):
            for t in _tokenize(str(c.get(field, ""))):
                if t.isdigit() and len(t) >= 3:
                    id_toks.add(t)
        for t in _tokenize(str(c.get("memo", ""))):
            if not t.isdigit():
                word_toks.add(t)
    word_toks -= _STOP | prop_toks | time_toks | line_toks
    return id_toks, word_toks, line_toks


def linked(doc: dict, case: dict) -> bool:
    """Doc co LIEN KET noi dung voi case khong — tin hieu abstention (thay nguong BM25 tho,
    vi diem BM25 khong so sanh duoc giua cac case; do dac 10/10/2026). Phien ban tat dinh
    cua y tuong 'retrieval evaluator' trong CRAG (docs/paper_notes.md §8):
    (1) nhac ma dinh danh cua contributor (TEN/VND/GL...), hoac
    (2) nhac ten dong P&L cua case, hoac
    (3) trung >=2 tu noi dung voi memo giao dich.
    """
    id_toks, word_toks, line_toks = _informative_tokens(case)
    d = set(_tokenize(doc["title"] + " " + doc["text"]))
    if id_toks & d:
        return True
    if line_toks & d:
        return True
    return len(word_toks & d) >= 2


def _rrf(rank_lists: list[list[str]], k: int = 60) -> dict[str, float]:
    scores: dict[str, float] = {}
    for ranks in rank_lists:
        for i, doc_id in enumerate(ranks):
            scores[doc_id] = scores.get(doc_id, 0.0) + 1.0 / (k + i + 1)
    return scores


class Retriever:
    def __init__(self, docs: list[dict] | None = None, use_dense: bool | None = None):
        self.docs = docs if docs is not None else load_evidence()
        self.use_dense = _HAS_DENSE if use_dense is None else (use_dense and _HAS_DENSE)
        self._dense = None
        if self.use_dense:
            self._dense = BGEM3FlagModel("BAAI/bge-m3", use_fp16=False)

    def retrieve(self, case: dict, top_k: int | None = None) -> dict:
        """Tra evidence pack: {case_id, docs: [{doc_id, bm25_score, ...}], best_bm25}."""
        top_k = top_k or config.TOP_K_EVIDENCE
        pool = metadata_filter(self.docs, case)
        if not pool:
            return {"case_id": case["case_id"], "docs": [], "best_bm25": 0.0,
                    "linked_any": False, "dense_used": self.use_dense}
        q = _tokenize(case_query(case))
        corpus = [_tokenize(d["title"] + " " + d["text"]) for d in pool]
        bm25 = BM25Okapi(corpus)
        scores = bm25.get_scores(q)
        order_bm25 = sorted(range(len(pool)), key=lambda i: -scores[i])
        rank_lists = [[pool[i]["doc_id"] for i in order_bm25]]

        if self.use_dense and self._dense is not None:
            emb_q = self._dense.encode([" ".join(q)])["dense_vecs"]
            emb_d = self._dense.encode([d["title"] + " " + d["text"] for d in pool])["dense_vecs"]
            sims = (emb_q @ emb_d.T)[0]
            order_dense = sorted(range(len(pool)), key=lambda i: -float(sims[i]))
            rank_lists.append([pool[i]["doc_id"] for i in order_dense])

        fused = _rrf(rank_lists)
        by_id = {d["doc_id"]: d for d in pool}
        bm25_by_id = {pool[i]["doc_id"]: float(scores[i]) for i in range(len(pool))}
        top = sorted(fused, key=lambda d: -fused[d])[:top_k]
        docs_out = [
            {**by_id[i], "bm25_score": round(bm25_by_id[i], 3), "rrf": round(fused[i], 4),
             "linked": linked(by_id[i], case)}
            for i in top
        ]
        return {
            "case_id": case["case_id"],
            "docs": docs_out,
            "best_bm25": round(max((bm25_by_id[i] for i in top), default=0.0), 3),
            "linked_any": any(d["linked"] for d in docs_out),
            "dense_used": self.use_dense,
        }


def precompute_packs() -> dict:
    """Chay 1 lan sau khi co dataset: luu evidence pack cho moi material case."""
    cases = json.loads((config.DATA_DIR / "cases.json").read_text(encoding="utf-8"))
    r = Retriever()
    packs = {c["case_id"]: r.retrieve(c) for c in cases}
    out = config.DATA_DIR / config.EVIDENCE_PACKS_FILE
    out.write_text(json.dumps(packs, indent=1), encoding="utf-8")
    return packs


def load_packs() -> dict:
    return json.loads(
        (config.DATA_DIR / config.EVIDENCE_PACKS_FILE).read_text(encoding="utf-8")
    )


if __name__ == "__main__":
    packs = precompute_packs()
    n_docs = sum(len(p["docs"]) for p in packs.values())
    print(f"precomputed {len(packs)} packs, {n_docs} doc slots, dense={_HAS_DENSE}")
