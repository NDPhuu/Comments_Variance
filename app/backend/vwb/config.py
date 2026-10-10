"""Cau hinh trung tam — moi nguong/duong dan/hang so nam o day, khong hard-code trong code."""

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent  # app/backend
DATA_DIR = BASE_DIR / "data" / "dataset_v1"

SEED = 26
DATASET_VERSION = "dataset_v1"

MONTHS = [f"2026-{m:02d}" for m in range(1, 13)]
PROPERTIES = ["PROP-A", "PROP-B", "PROP-C", "PROP-D", "PROP-E"]
CORP = "CORP"  # cac dong P&L cap cong ty (financial, other income)

REVENUE_LINES = {"Leasing revenue", "Service income"}
CORP_LINES = {"Financial income", "Financial expenses", "Other income"}
COST_LINES = {
    "Repair & Maintenance",
    "Utilities",
    "Security & cleaning",
    "Marketing",
    "Insurance",
    "Management fee",
}

# Nguong trong yeu: material khi |variance| >= abs HOAC |variance_pct| >= pct
MATERIALITY = {
    "revenue": {"abs": 50_000.0, "pct": 0.05},
    "cost": {"abs": 30_000.0, "pct": 0.15},
    "corp": {"abs": 100_000.0, "pct": 0.10},
}

TOP_CONTRIBUTORS = 6

# --- Phase 2: retrieval / generation / verification ---
TOP_K_EVIDENCE = 5
# Abstention: theo LIEN KET NOI DUNG (retrieval.core.linked), khong dung nguong diem tho
GEN_MODEL = "gemini-3.8-flash"  # gemini-2.5-flash da bi khoa voi tai khoan moi (404, 10/2026)
GEN_TEMPERATURE = 0.2
PROMPT_VERSION = "prompt_v1"
EVIDENCE_PACKS_FILE = "evidence_packs.json"  # trong DATA_DIR


def line_side(pl_line: str, prop: str) -> str:
    """Phan loai dong P&L de chon nguong trong yeu va chieu favorable."""
    if prop == CORP or pl_line in CORP_LINES:
        return "corp"
    if pl_line in REVENUE_LINES:
        return "revenue"
    return "cost"
