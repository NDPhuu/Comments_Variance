"""Variance engine — tat dinh, pandas thuan. LLM khong bao gio duoc dung de tinh cac so o day.

Quy uoc dau: moi amount luu duong (cost cung duong). variance = actual - budget.
Favorable: dong thu nhap co variance > 0; dong chi phi co variance < 0.
"""

from __future__ import annotations

import pandas as pd

from vwb import config

INCOME_LIKE = config.REVENUE_LINES | {"Financial income", "Other income"}


def _direction(pl_line: str, variance: float) -> str:
    if variance == 0:
        return "flat"
    income = pl_line in INCOME_LIKE
    fav = variance > 0 if income else variance < 0
    return "favorable" if fav else "unfavorable"


def variance_table(
    budget_line: pd.DataFrame,
    actual_line: pd.DataFrame,
    month: str,
    materiality: dict | None = None,
) -> pd.DataFrame:
    """Bang variance theo property x pl_line cho mot thang.

    Input: 2 DataFrame cot [property, pl_line, month, amount].
    Output cot: property, pl_line, budget, actual, variance, variance_pct,
                direction, side, material, materiality_rule.
    """
    materiality = materiality or config.MATERIALITY
    b = (
        budget_line[budget_line["month"] == month]
        .groupby(["property", "pl_line"], as_index=False)["amount"]
        .sum()
        .rename(columns={"amount": "budget"})
    )
    a = (
        actual_line[actual_line["month"] == month]
        .groupby(["property", "pl_line"], as_index=False)["amount"]
        .sum()
        .rename(columns={"amount": "actual"})
    )
    t = b.merge(a, on=["property", "pl_line"], how="outer").fillna(0.0)
    t["variance"] = t["actual"] - t["budget"]
    t["variance_pct"] = t.apply(
        lambda r: (r["variance"] / abs(r["budget"])) if r["budget"] != 0 else None, axis=1
    )
    t["direction"] = t.apply(lambda r: _direction(r["pl_line"], r["variance"]), axis=1)
    t["side"] = t.apply(lambda r: config.line_side(r["pl_line"], r["property"]), axis=1)

    def _material(r) -> bool:
        rule = materiality[r["side"]]
        if abs(r["variance"]) >= rule["abs"]:
            return True
        return r["variance_pct"] is not None and abs(r["variance_pct"]) >= rule["pct"]

    t["material"] = t.apply(_material, axis=1)
    t["materiality_rule"] = t["side"].map(
        lambda s: f"|var|>={materiality[s]['abs']:,.0f} OR |pct|>={materiality[s]['pct']:.0%}"
    )
    t["month"] = month
    return t.sort_values("variance", key=abs, ascending=False).reset_index(drop=True)


def revenue_contributors(
    budget_rent: pd.DataFrame,
    actual_rent: pd.DataFrame,
    prop: str,
    month: str,
    top_n: int | None = None,
) -> list[dict]:
    """Phan ra variance dong doanh thu theo tenant (budget_rent/actual_rent:
    cot [property, tenant, month, amount])."""
    top_n = top_n or config.TOP_CONTRIBUTORS
    b = budget_rent.query("property == @prop and month == @month").set_index("tenant")["amount"]
    a = actual_rent.query("property == @prop and month == @month").set_index("tenant")["amount"]
    delta = a.reindex(b.index.union(a.index), fill_value=0.0) - b.reindex(
        b.index.union(a.index), fill_value=0.0
    )
    delta = delta[delta != 0].sort_values(key=lambda s: s.abs(), ascending=False)
    total = delta.sum()
    out = []
    for ten, d in delta.head(top_n).items():
        out.append(
            {
                "key": str(ten),
                "kind": "tenant",
                "delta": round(float(d), 2),
                "share_of_variance": round(float(d / total), 4) if total != 0 else None,
            }
        )
    return out


def txn_contributors(
    gl: pd.DataFrame, prop: str, pl_line: str, month: str, top_n: int | None = None
) -> list[dict]:
    """Top giao dich GL theo |amount| cho mot case chi phi
    (gl: cot [txn_id, month, property, pl_line, party, memo, amount])."""
    top_n = top_n or config.TOP_CONTRIBUTORS
    g = gl.query("property == @prop and pl_line == @pl_line and month == @month")
    g = g.reindex(g["amount"].abs().sort_values(ascending=False).index)
    total = g["amount"].sum()
    out = []
    for _, r in g.head(top_n).iterrows():
        out.append(
            {
                "key": str(r["txn_id"]),
                "kind": "transaction",
                "party": str(r["party"]),
                "memo": str(r["memo"]),
                "delta": round(float(r["amount"]), 2),
                "share_of_actual": round(float(r["amount"] / total), 4) if total != 0 else None,
            }
        )
    return out


def case_id(month: str, prop: str, pl_line: str) -> str:
    return f"{month}_{prop}_{pl_line.replace(' ', '_').replace('&', 'and')}"


def build_cases(
    budget_line: pd.DataFrame,
    actual_line: pd.DataFrame,
    budget_rent: pd.DataFrame,
    actual_rent: pd.DataFrame,
    gl: pd.DataFrame,
    month: str,
    materiality: dict | None = None,
) -> list[dict]:
    """Danh sach VarianceCase (chi case material) cho mot thang — nguon su that duy nhat ve SO."""
    vt = variance_table(budget_line, actual_line, month, materiality)
    cases = []
    for _, r in vt[vt["material"]].iterrows():
        prop, line = r["property"], r["pl_line"]
        if line in config.REVENUE_LINES and line == "Leasing revenue":
            contributors = revenue_contributors(budget_rent, actual_rent, prop, month)
        else:
            contributors = txn_contributors(gl, prop, line, month)
        cases.append(
            {
                "case_id": case_id(month, prop, line),
                "month": month,
                "property": prop,
                "pl_line": line,
                "side": r["side"],
                "budget": round(float(r["budget"]), 2),
                "actual": round(float(r["actual"]), 2),
                "variance": round(float(r["variance"]), 2),
                "variance_pct": (
                    round(float(r["variance_pct"]), 4) if r["variance_pct"] is not None else None
                ),
                "direction": r["direction"],
                "material": True,
                "materiality_rule": r["materiality_rule"],
                "contributors": contributors,
            }
        )
    return cases
