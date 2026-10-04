"""Trich Key Commentary tu cac file PL_Act vs budget_*.xlsb (sheet Output).

Output: local_data/comments_PL.csv (KHONG commit - du lieu that).
Chay:   python app/tools/extract_comments.py
"""
import csv
import glob
import os
import re

from pyxlsb import open_workbook

SRC_GLOB = os.path.join("Sample_FP&A", "PL_Act vs budget_*.xlsb")
OUT_CSV = os.path.join("local_data", "comments_PL.csv")


def month_tag(path: str) -> str:
    m = re.search(r"_([A-Za-z]{3})'?26", os.path.basename(path))
    return (m.group(1) if m else "?") + "-26"


def extract_file(path: str) -> list[dict]:
    rows_out: list[dict] = []
    with open_workbook(path) as wb:
        with wb.get_sheet("Output") as sh:
            grid = [[c.v for c in row] for row in sh.rows()]
    # tim hang header co "Key Commentary"
    hdr_i, com_j = None, None
    for i, row in enumerate(grid[:15]):
        for j, v in enumerate(row):
            if isinstance(v, str) and "commentary" in v.lower():
                hdr_i, com_j = i, j
                break
        if hdr_i is not None:
            break
    if hdr_i is None:
        print(f"  !! khong thay cot Commentary trong {path}")
        return rows_out
    for row in grid[hdr_i + 1 :]:
        if not row or len(row) <= com_j:
            continue
        line = row[0] if row and isinstance(row[0], str) else None
        com = row[com_j]
        if line and isinstance(com, str) and com.strip():
            rows_out.append(
                {"month": month_tag(path), "pl_line": line.strip(), "comment": com.strip()}
            )
    return rows_out


def main() -> None:
    all_rows: list[dict] = []
    for path in sorted(glob.glob(SRC_GLOB)):
        rows = extract_file(path)
        print(f"{os.path.basename(path)}: {len(rows)} comments")
        all_rows.extend(rows)
    os.makedirs("local_data", exist_ok=True)
    with open(OUT_CSV, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=["month", "pl_line", "comment"])
        w.writeheader()
        w.writerows(all_rows)
    print(f"\nTong: {len(all_rows)} comments -> {OUT_CSV}")
    lens = [len(r["comment"]) for r in all_rows] or [0]
    print(f"Do dai: min {min(lens)} / median {sorted(lens)[len(lens)//2]} / max {max(lens)} ky tu")


if __name__ == "__main__":
    main()
