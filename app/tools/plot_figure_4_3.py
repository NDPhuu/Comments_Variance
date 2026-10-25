"""Vẽ Hình 4.3 từ kết quả benchmark theo nhóm tình huống.

Ví dụ:
    python app/tools/plot_figure_4_3.py

Script chỉ sử dụng các dòng mode=m2 trong by_scenario.csv và xuất đồng thời
PNG 300 dpi cùng SVG để có thể chèn vào luận văn.
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


SCENARIO_LABELS = {
    "accounting_treatment": "Xử lý kế toán",
    "early_termination": "Chấm dứt hợp đồng trước hạn",
    "financing_event": "Sự kiện tài trợ",
    "handover_delay": "Chậm bàn giao",
    "missing_evidence": "Thiếu bằng chứng",
    "new_lease_early": "Hợp đồng mới bắt đầu sớm",
    "one_off_event": "Sự kiện một lần",
    "rate_change": "Thay đổi đơn giá",
    "timing_difference": "Khác biệt thời điểm",
}

COLORS = {
    "navy": "#081A36",
    "blue": "#004583",
    "cyan": "#01A7E5",
    "slate": "#5D6675",
    "grid": "#D9DEE5",
    "light": "#F3F5F7",
    "danger": "#C8404C",
}


def parse_mean(value: str) -> float | None:
    """Lấy giá trị trung bình từ chuỗi dạng '0.970±0.009'."""
    value = value.strip().lower()
    if value in {"n/a", "na", ""}:
        return None
    return float(value.split("±", maxsplit=1)[0]) * 100


def load_m2_rows(csv_path: Path) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    with csv_path.open("r", encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            if row["mode"].strip().lower() != "m2":
                continue
            scenario = row["scenario"].strip()
            if scenario not in SCENARIO_LABELS:
                raise ValueError(f"Chưa có nhãn tiếng Việt cho scenario: {scenario}")
            rows.append(
                {
                    "scenario": scenario,
                    "label": SCENARIO_LABELS[scenario],
                    "n": int(row["n"]),
                    "numeric_accuracy": parse_mean(row["numeric_accuracy"]),
                    "unsupported_rate": parse_mean(row["unsupported_rate"]),
                }
            )
    if not rows:
        raise ValueError("Không tìm thấy dòng mode=m2 trong file dữ liệu.")
    return rows


def format_percent(value: float) -> str:
    return f"{value:.1f}%".replace(".", ",")


def draw_figure(rows: list[dict[str, object]], output_png: Path) -> None:
    labels = [f"{row['label']}  (n={row['n']})" for row in rows]
    numeric = np.array([float(row["numeric_accuracy"]) for row in rows])
    unsupported = [row["unsupported_rate"] for row in rows]
    y = np.arange(len(rows))

    plt.rcParams.update(
        {
            "font.family": "Times New Roman",
            "font.size": 9.5,
            "axes.titlesize": 11,
            "axes.titleweight": "bold",
            "axes.labelcolor": COLORS["slate"],
            "xtick.color": COLORS["slate"],
            "ytick.color": COLORS["navy"],
        }
    )

    fig, (ax_num, ax_unsup) = plt.subplots(
        1,
        2,
        figsize=(12.2, 6.2),
        sharey=True,
        gridspec_kw={"width_ratios": [1.05, 1.0], "wspace": 0.13},
    )
    fig.patch.set_facecolor("white")

    # Panel A: dùng trục 95–100% để các khác biệt nhỏ vẫn nhìn thấy được.
    ax_num.hlines(y, 95, numeric, color="#B2E2F9", linewidth=6, zorder=1)
    ax_num.scatter(numeric, y, s=48, color=COLORS["blue"], zorder=2)
    for yi, value in zip(y, numeric):
        is_at_ceiling = value >= 99.9
        ax_num.text(
            value - 0.18 if is_at_ceiling else value + 0.10,
            yi,
            format_percent(value),
            va="center",
            ha="right" if is_at_ceiling else "left",
            color=COLORS["navy"],
            fontweight="bold",
        )
    ax_num.set_xlim(95, 100.5)
    ax_num.set_xticks(np.arange(95, 101, 1))
    ax_num.set_xlabel("Tỷ lệ (%)")
    ax_num.set_title("A. Độ chính xác số liệu", loc="left", color=COLORS["navy"], pad=12)
    ax_num.set_yticks(y, labels)
    ax_num.tick_params(axis="y", length=0, pad=8)

    # Panel B: N/A được biểu diễn riêng, tuyệt đối không thay bằng 0%.
    for yi, value in zip(y, unsupported):
        if value is None:
            ax_unsup.scatter(0, yi, marker="x", s=48, color=COLORS["slate"], zorder=2)
            ax_unsup.text(1.4, yi, "Không áp dụng", va="center", color=COLORS["slate"])
            continue
        value = float(value)
        ax_unsup.hlines(yi, 0, value, color="#F7CDD1", linewidth=6, zorder=1)
        ax_unsup.scatter(value, yi, s=48, color=COLORS["danger"], zorder=2)
        ax_unsup.text(
            value + 1.2,
            yi,
            format_percent(value),
            va="center",
            color=COLORS["navy"],
            fontweight="bold",
        )
    ax_unsup.set_xlim(0, 56)
    ax_unsup.set_xticks(np.arange(0, 51, 10))
    ax_unsup.set_xlabel("Tỷ lệ (%) · thấp hơn là tốt hơn")
    ax_unsup.set_title(
        "B. Tỷ lệ nhận định thiếu căn cứ",
        loc="left",
        color=COLORS["navy"],
        pad=12,
    )
    ax_unsup.tick_params(axis="y", left=False, labelleft=False)

    for ax in (ax_num, ax_unsup):
        ax.set_facecolor("white")
        ax.grid(axis="x", color=COLORS["grid"], linewidth=0.7, alpha=0.9)
        ax.set_axisbelow(True)
        ax.spines[["top", "right", "left"]].set_visible(False)
        ax.spines["bottom"].set_color(COLORS["grid"])

    ax_num.invert_yaxis()
    fig.suptitle(
        "Kết quả của M2 theo nhóm tình huống",
        x=0.06,
        y=0.985,
        ha="left",
        fontsize=14,
        fontweight="bold",
        color=COLORS["navy"],
    )
    fig.text(
        0.06,
        0.018,
        "Ghi chú: n là số case; mỗi case được chạy 3 lần. Panel A dùng trục 95–100%. "
        "Nhóm thiếu bằng chứng không có nhận định để chấm nên được ghi là ‘Không áp dụng’.",
        ha="left",
        va="bottom",
        fontsize=8.5,
        color=COLORS["slate"],
    )
    fig.subplots_adjust(left=0.30, right=0.98, top=0.88, bottom=0.15)

    output_png.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_png, dpi=300, bbox_inches="tight", facecolor="white")
    fig.savefig(output_png.with_suffix(".svg"), bbox_inches="tight", facecolor="white")
    plt.close(fig)


def main() -> None:
    repo_root = Path(__file__).resolve().parents[2]
    parser = argparse.ArgumentParser(description="Vẽ Hình 4.3 của khóa luận.")
    parser.add_argument(
        "--input",
        type=Path,
        default=repo_root / "app/backend/results/by_scenario.csv",
        help="Đường dẫn đến by_scenario.csv.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=repo_root / "thesis/figures/hinh_4_3.png",
        help="Đường dẫn file PNG đầu ra; SVG được tạo cùng thư mục.",
    )
    args = parser.parse_args()
    draw_figure(load_m2_rows(args.input.resolve()), args.output.resolve())
    print(args.output.resolve())
    print(args.output.resolve().with_suffix(".svg"))


if __name__ == "__main__":
    main()
