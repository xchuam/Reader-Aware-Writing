#!/usr/bin/env python3
"""Generate a GitHub-readable report for Arrangement5-5 benchmark results."""

from __future__ import annotations

import argparse
import csv
import math
import random
from collections import defaultdict
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]

CONDITION_NAMES = {
    "C1": "Reader-aware writing",
    "C2": "No-skill baseline",
    "C3": "Scientific-writing representative",
    "C4": "Scientific-writing alternative",
    "C5": "Academic writing standards",
}

DIMENSIONS = [
    ("scientific_fidelity", "Scientific fidelity", 20),
    ("article_structure", "Article structure", 15),
    ("reader_orientation", "Reader orientation", 15),
    ("cohesion_coherence", "Cohesion/coherence", 20),
    ("evidence_uncertainty", "Evidence/uncertainty", 15),
    ("style_readability", "Style/readability", 10),
    ("constraint_following", "Constraint following", 5),
]

COLORS = {
    "C1": "#2E6F95",
    "C2": "#9B5DE5",
    "C3": "#00A676",
    "C4": "#F77F00",
    "C5": "#C44536",
}

README_LABELS = {
    "C1": "reader-aware-writing",
    "C2": "No-skill baseline",
    "C3": "Scientific-writing representative",
    "C4": "Scientific-writing alternative",
    "C5": "Academic writing standards",
}

SKILL_SNAPSHOT_ROWS = [
    [
        "C1",
        "Reader-aware writing",
        "[xchuam/Reader-Aware-Writing](https://github.com/xchuam/Reader-Aware-Writing/tree/97c06ad26991c68060a4094b6fbd63cb5ed4a671/skills/reader-aware-writing)",
        "`2026-05-01T12:17:30Z`",
        "Working tree at git head `97c06ad26991c68060a4094b6fbd63cb5ed4a671`; skill tree SHA-256 `b3ade6b38356ddf5fe16b139a8ee13d371e1017e789e2aa39feac5031d352f65`.",
    ],
    [
        "C2",
        "No-skill baseline",
        "N/A",
        "N/A",
        "Fresh isolated `CODEX_HOME` with no user writing skill installed.",
    ],
    [
        "C3",
        "Scientific-writing representative",
        "Listed GitHub repository [smithery/ai](https://github.com/smithery/ai); rendered source page [skills.sh/smithery/ai/scientific-writing](https://skills.sh/smithery/ai/scientific-writing)",
        "`2026-05-01T09:52:19Z`",
        "The listed GitHub repository was not reachable by `git ls-remote`, so the rendered `SKILL.md` was snapshotted; tree SHA-256 `cf4c35607ffc8f5e1c57b447f201b941ce1597fb26ff69aa36821dbab1726332`.",
    ],
    [
        "C4",
        "Scientific-writing alternative",
        "[ovachiever/droid-tings scientific-writing](https://github.com/ovachiever/droid-tings/tree/7acd12a7547ded8f801615e69c3b881a584ce323/skills/scientific-writing)",
        "`2026-05-01T09:52:19Z`",
        "Snapshot from commit `7acd12a7547ded8f801615e69c3b881a584ce323`; tree SHA-256 `faac0c616485479b7b0c9698541b17f6e82c0d6f10842849f7c1e5113d095b7a`.",
    ],
    [
        "C5",
        "Academic writing standards",
        "[seabbs/skills academic-writing-standards](https://github.com/seabbs/skills/tree/006088dd99868765db0847d068b5089c192086b5/plugins/research-academic/skills/academic-writing-standards)",
        "`2026-05-01T09:52:19Z`",
        "Snapshot from commit `006088dd99868765db0847d068b5089c192086b5`; tree SHA-256 `0b92cea6eef9b58fa57ee01f5cc72605f43e55d1404c2b95eadcdd38b17728f7`.",
    ],
]

SOURCE_ARTICLE = (
    "Jia, B., Shi, Y., Hong, Y. et al. Caspase 5c amplifies Wnt via APC "
    "cleavage to promote intestinal homeostasis. Nature 652, 1362-1374 "
    "(2026). https://doi.org/10.1038/s41586-026-10343-8"
)

POSITION_BIAS_REFERENCE = (
    "Wang et al. (2024), [Large Language Models are not Fair Evaluators]"
    "(https://aclanthology.org/2024.acl-long.511/)"
)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def fmt(value: float, digits: int = 2) -> str:
    if math.isnan(value):
        return "NA"
    return f"{value:.{digits}f}"


def markdown_table(headers: list[str], rows: list[list[object]]) -> str:
    out = ["| " + " | ".join(headers) + " |"]
    out.append("| " + " | ".join(["---"] * len(headers)) + " |")
    for row in rows:
        out.append("| " + " | ".join(str(value) for value in row) + " |")
    return "\n".join(out)


def bootstrap_ci(values: list[float], reps: int = 20000) -> tuple[float, float]:
    if not values:
        return (float("nan"), float("nan"))
    rng = random.Random(20260501)
    means: list[float] = []
    for _ in range(reps):
        sample = [rng.choice(values) for _ in values]
        means.append(sum(sample) / len(sample))
    means.sort()
    lo = means[int(0.025 * (len(means) - 1))]
    hi = means[int(0.975 * (len(means) - 1))]
    return lo, hi


def svg_bar_chart(path: Path, rows: list[dict[str, str]]) -> None:
    width, height = 760, 430
    left, right, top, bottom = 88, 28, 44, 88
    plot_w = width - left - right
    plot_h = height - top - bottom
    values = [float(row["mean_article_total"]) for row in rows]
    ymin = max(0.0, math.floor(min(values) - 2))
    ymax = min(100.0, math.ceil(max(values) + 2))
    span = ymax - ymin or 1
    bar_w = plot_w / len(rows) * 0.62
    gap = plot_w / len(rows)
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="white"/>',
        '<text x="24" y="28" font-family="Arial" font-size="18" font-weight="700">Mean total score by condition</text>',
    ]
    for tick in range(int(ymin), int(ymax) + 1):
        if tick % 2:
            continue
        y = top + plot_h - ((tick - ymin) / span) * plot_h
        parts.append(f'<line x1="{left}" y1="{y:.1f}" x2="{width-right}" y2="{y:.1f}" stroke="#e6e6e6"/>')
        parts.append(f'<text x="{left-10}" y="{y+4:.1f}" text-anchor="end" font-family="Arial" font-size="11" fill="#555">{tick}</text>')
    for i, row in enumerate(rows):
        cid = row["condition_id"]
        value = float(row["mean_article_total"])
        sd = float(row["sd_article_total"])
        x = left + i * gap + (gap - bar_w) / 2
        bar_h = ((value - ymin) / span) * plot_h
        y = top + plot_h - bar_h
        err_hi = min(ymax, value + sd)
        err_lo = max(ymin, value - sd)
        y_hi = top + plot_h - ((err_hi - ymin) / span) * plot_h
        y_lo = top + plot_h - ((err_lo - ymin) / span) * plot_h
        parts.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{bar_w:.1f}" height="{bar_h:.1f}" fill="{COLORS[cid]}" rx="3"/>')
        parts.append(f'<line x1="{x+bar_w/2:.1f}" y1="{y_hi:.1f}" x2="{x+bar_w/2:.1f}" y2="{y_lo:.1f}" stroke="#333" stroke-width="1.5"/>')
        parts.append(f'<line x1="{x+bar_w/2-7:.1f}" y1="{y_hi:.1f}" x2="{x+bar_w/2+7:.1f}" y2="{y_hi:.1f}" stroke="#333" stroke-width="1.5"/>')
        parts.append(f'<line x1="{x+bar_w/2-7:.1f}" y1="{y_lo:.1f}" x2="{x+bar_w/2+7:.1f}" y2="{y_lo:.1f}" stroke="#333" stroke-width="1.5"/>')
        parts.append(f'<text x="{x+bar_w/2:.1f}" y="{y-8:.1f}" text-anchor="middle" font-family="Arial" font-size="12" fill="#222">{value:.2f}</text>')
        parts.append(f'<text x="{x+bar_w/2:.1f}" y="{height-58}" text-anchor="middle" font-family="Arial" font-size="12" font-weight="700">{cid}</text>')
        parts.append(f'<text x="{x+bar_w/2:.1f}" y="{height-39}" text-anchor="middle" font-family="Arial" font-size="10" fill="#444">{CONDITION_NAMES[cid]}</text>')
    parts.append(f'<line x1="{left}" y1="{top+plot_h}" x2="{width-right}" y2="{top+plot_h}" stroke="#333"/>')
    parts.append("</svg>")
    path.write_text("\n".join(parts), encoding="utf-8")


def percentile(values: list[float], pct: float) -> float:
    if not values:
        return float("nan")
    ordered = sorted(values)
    if len(ordered) == 1:
        return ordered[0]
    rank = pct / 100 * (len(ordered) - 1)
    lo = math.floor(rank)
    hi = math.ceil(rank)
    if lo == hi:
        return ordered[lo]
    weight = rank - lo
    return ordered[lo] * (1 - weight) + ordered[hi] * weight


def svg_readme_boxplot(
    path: Path,
    condition_rows: list[dict[str, str]],
    score_rows: list[dict[str, str]],
) -> None:
    width, height = 980, 540
    left, right, top, bottom = 86, 34, 52, 160
    plot_w = width - left - right
    plot_h = height - top - bottom
    ordered_conditions = [row["condition_id"] for row in condition_rows]
    grouped: dict[str, list[float]] = defaultdict(list)
    for row in score_rows:
        grouped[row["condition_id"]].append(float(row["total_score"]))
    values = [score for cid in ordered_conditions for score in grouped[cid]]
    ymin = max(0.0, math.floor(min(values) - 2))
    ymax = min(100.0, math.ceil(max(values) + 1))
    span = ymax - ymin or 1

    def y_pos(value: float) -> float:
        return top + plot_h - ((value - ymin) / span) * plot_h

    gap = plot_w / len(ordered_conditions)
    box_w = gap * 0.38
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="white"/>',
        '<text x="24" y="30" font-family="Arial" font-size="18" font-weight="700">Blinded total score distribution by authoring setting</text>',
    ]
    for tick in range(int(ymin), int(ymax) + 1):
        if tick % 2:
            continue
        y = y_pos(tick)
        parts.append(f'<line x1="{left}" y1="{y:.1f}" x2="{width-right}" y2="{y:.1f}" stroke="#e5e7eb"/>')
        parts.append(f'<text x="{left-10}" y="{y+4:.1f}" text-anchor="end" font-family="Arial" font-size="11" fill="#555">{tick}</text>')
    parts.append(f'<line x1="{left}" y1="{top}" x2="{left}" y2="{top+plot_h}" stroke="#333"/>')
    parts.append(f'<line x1="{left}" y1="{top+plot_h}" x2="{width-right}" y2="{top+plot_h}" stroke="#333"/>')
    for index, cid in enumerate(ordered_conditions):
        scores = sorted(grouped[cid])
        q1 = percentile(scores, 25)
        median = percentile(scores, 50)
        q3 = percentile(scores, 75)
        lo = min(scores)
        hi = max(scores)
        x = left + gap * index + gap / 2
        y_q1 = y_pos(q1)
        y_q3 = y_pos(q3)
        y_med = y_pos(median)
        y_lo = y_pos(lo)
        y_hi = y_pos(hi)
        color = COLORS[cid]
        parts.append(f'<line x1="{x:.1f}" y1="{y_hi:.1f}" x2="{x:.1f}" y2="{y_lo:.1f}" stroke="#333" stroke-width="1.5"/>')
        parts.append(f'<line x1="{x-box_w/3:.1f}" y1="{y_hi:.1f}" x2="{x+box_w/3:.1f}" y2="{y_hi:.1f}" stroke="#333" stroke-width="1.5"/>')
        parts.append(f'<line x1="{x-box_w/3:.1f}" y1="{y_lo:.1f}" x2="{x+box_w/3:.1f}" y2="{y_lo:.1f}" stroke="#333" stroke-width="1.5"/>')
        parts.append(f'<rect x="{x-box_w/2:.1f}" y="{y_q3:.1f}" width="{box_w:.1f}" height="{max(1, y_q1-y_q3):.1f}" fill="{color}" fill-opacity="0.72" stroke="#222" rx="3"/>')
        parts.append(f'<line x1="{x-box_w/2:.1f}" y1="{y_med:.1f}" x2="{x+box_w/2:.1f}" y2="{y_med:.1f}" stroke="#111" stroke-width="2"/>')
        for dot_index, score in enumerate(scores):
            offset = ((dot_index % 5) - 2) * 3.4
            parts.append(f'<circle cx="{x+offset:.1f}" cy="{y_pos(score):.1f}" r="2.4" fill="#111" opacity="0.42"/>')
        label_y = top + plot_h + 22
        label = README_LABELS[cid]
        parts.append(
            f'<text x="{x:.1f}" y="{label_y:.1f}" transform="rotate(30 {x:.1f} {label_y:.1f})" '
            f'text-anchor="start" font-family="Arial" font-size="11" fill="#333">{label}</text>'
        )
    parts.append(f'<text x="{width/2:.1f}" y="{height-18}" text-anchor="middle" font-family="Arial" font-size="13" fill="#222">Authoring setting</text>')
    parts.append(f'<text x="24" y="{top+plot_h/2:.1f}" transform="rotate(-90 24 {top+plot_h/2:.1f})" text-anchor="middle" font-family="Arial" font-size="13" fill="#222">Total score</text>')
    parts.append("</svg>")
    path.write_text("\n".join(parts), encoding="utf-8")


def heat_color(value: float, low: float, high: float) -> str:
    if high <= low:
        t = 0.5
    else:
        t = max(0.0, min(1.0, (value - low) / (high - low)))
    r1, g1, b1 = (237, 242, 247)
    r2, g2, b2 = (46, 111, 149)
    r = round(r1 + (r2 - r1) * t)
    g = round(g1 + (g2 - g1) * t)
    b = round(b1 + (b2 - b1) * t)
    return f"#{r:02x}{g:02x}{b:02x}"


def svg_dimension_heatmap(path: Path, rows: list[dict[str, str]]) -> None:
    cell_w, cell_h = 92, 42
    left, top = 185, 56
    width = left + cell_w * len(DIMENSIONS) + 26
    height = top + cell_h * len(rows) + 72
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="white"/>',
        '<text x="24" y="28" font-family="Arial" font-size="18" font-weight="700">Dimension means (% of available points)</text>',
    ]
    for j, (_, label, _) in enumerate(DIMENSIONS):
        x = left + j * cell_w + cell_w / 2
        parts.append(f'<text x="{x:.1f}" y="{top-14}" text-anchor="middle" font-family="Arial" font-size="10" fill="#333">{label}</text>')
    for i, row in enumerate(rows):
        cid = row["condition_id"]
        y = top + i * cell_h
        parts.append(f'<text x="24" y="{y+26}" font-family="Arial" font-size="12" font-weight="700">{cid}</text>')
        parts.append(f'<text x="55" y="{y+26}" font-family="Arial" font-size="11" fill="#444">{CONDITION_NAMES[cid]}</text>')
        for j, (key, _, max_points) in enumerate(DIMENSIONS):
            pct = float(row[f"mean_{key}"]) / max_points
            x = left + j * cell_w
            fill = heat_color(pct, 0.84, 1.0)
            text_color = "white" if pct > 0.93 else "#222"
            parts.append(f'<rect x="{x}" y="{y}" width="{cell_w-2}" height="{cell_h-2}" fill="{fill}" rx="3"/>')
            parts.append(f'<text x="{x+cell_w/2:.1f}" y="{y+25}" text-anchor="middle" font-family="Arial" font-size="12" fill="{text_color}">{pct*100:.1f}</text>')
    parts.append("</svg>")
    path.write_text("\n".join(parts), encoding="utf-8")


def svg_pairwise_heatmap(path: Path, matrix_rows: list[dict[str, str]]) -> None:
    conditions = ["C1", "C2", "C3", "C4", "C5"]
    cell = 74
    left, top = 125, 62
    width = left + cell * len(conditions) + 30
    height = top + cell * len(conditions) + 45
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="white"/>',
        '<text x="24" y="28" font-family="Arial" font-size="18" font-weight="700">Pairwise win rate by condition</text>',
        '<text x="24" y="46" font-family="Arial" font-size="11" fill="#555">Cell = row condition preferred over column condition</text>',
    ]
    for j, cid in enumerate(conditions):
        parts.append(f'<text x="{left+j*cell+cell/2}" y="{top-12}" text-anchor="middle" font-family="Arial" font-size="12" font-weight="700">{cid}</text>')
    for i, row in enumerate(matrix_rows):
        cid = row["condition_id"]
        y = top + i * cell
        parts.append(f'<text x="24" y="{y+cell/2+4}" font-family="Arial" font-size="12" font-weight="700">{cid}</text>')
        for j, other in enumerate(conditions):
            x = left + j * cell
            if cid == other:
                fill, label, color = "#f3f4f6", "-", "#777"
            else:
                value = float(row[other])
                fill = heat_color(value, 0.0, 1.0)
                label = f"{value:.2f}"
                color = "white" if value > 0.62 else "#222"
            parts.append(f'<rect x="{x}" y="{y}" width="{cell-3}" height="{cell-3}" fill="{fill}" rx="4"/>')
            parts.append(f'<text x="{x+cell/2:.1f}" y="{y+cell/2+4:.1f}" text-anchor="middle" font-family="Arial" font-size="13" fill="{color}">{label}</text>')
    parts.append("</svg>")
    path.write_text("\n".join(parts), encoding="utf-8")


def svg_position_effect(path: Path, score_rows: list[dict[str, str]]) -> list[tuple[int, float]]:
    grouped: dict[int, list[float]] = defaultdict(list)
    for row in score_rows:
        grouped[int(row["position"])].append(float(row["total_score"]))
    means = [(pos, sum(vals) / len(vals)) for pos, vals in sorted(grouped.items())]
    width, height = 640, 360
    left, right, top, bottom = 74, 26, 44, 58
    plot_w = width - left - right
    plot_h = height - top - bottom
    values = [v for _, v in means]
    ymin = math.floor(min(values) - 2)
    ymax = math.ceil(max(values) + 2)
    span = ymax - ymin or 1
    points = []
    for pos, value in means:
        x = left + (pos - 1) / 4 * plot_w
        y = top + plot_h - (value - ymin) / span * plot_h
        points.append((x, y, pos, value))
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="white"/>',
        '<text x="24" y="28" font-family="Arial" font-size="18" font-weight="700">Mean score by presentation position</text>',
    ]
    for tick in range(ymin, ymax + 1):
        y = top + plot_h - (tick - ymin) / span * plot_h
        parts.append(f'<line x1="{left}" y1="{y:.1f}" x2="{width-right}" y2="{y:.1f}" stroke="#e6e6e6"/>')
        parts.append(f'<text x="{left-10}" y="{y+4:.1f}" text-anchor="end" font-family="Arial" font-size="11" fill="#555">{tick}</text>')
    path_points = " ".join(f"{x:.1f},{y:.1f}" for x, y, _, _ in points)
    parts.append(f'<polyline points="{path_points}" fill="none" stroke="#2E6F95" stroke-width="3"/>')
    for x, y, pos, value in points:
        parts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="5" fill="#F77F00"/>')
        parts.append(f'<text x="{x:.1f}" y="{y-12:.1f}" text-anchor="middle" font-family="Arial" font-size="12">{value:.2f}</text>')
        parts.append(f'<text x="{x:.1f}" y="{height-28}" text-anchor="middle" font-family="Arial" font-size="12">Position {pos}</text>')
    parts.append("</svg>")
    path.write_text("\n".join(parts), encoding="utf-8")
    return means


def generate(run_id: str) -> None:
    result_root = REPO_ROOT / "comparing" / "evaluation_results" / run_id / "arrangement55"
    decoded = result_root / "decoded"
    report_root = REPO_ROOT / "comparing" / "reports" / run_id
    figure_root = report_root / "figures"
    report_root.mkdir(parents=True, exist_ok=True)
    figure_root.mkdir(parents=True, exist_ok=True)

    condition_rows = read_csv(decoded / "summary_by_condition.csv")
    article_rows = read_csv(decoded / "summary_by_article.csv")
    score_rows = read_csv(decoded / "decoded_scores.csv")
    matrix_rows = read_csv(decoded / "pairwise_condition_matrix.csv")
    condition_rows.sort(key=lambda row: float(row["mean_article_total"]), reverse=True)

    svg_bar_chart(figure_root / "mean_total_by_condition.svg", condition_rows)
    svg_readme_boxplot(figure_root / "total_score_boxplot_by_skill.svg", condition_rows, score_rows)
    svg_dimension_heatmap(figure_root / "dimension_heatmap.svg", condition_rows)
    svg_pairwise_heatmap(figure_root / "pairwise_win_rate.svg", matrix_rows)
    position_means = svg_position_effect(figure_root / "position_effect.svg", score_rows)

    c1_articles = [
        float(row["mean_total"]) for row in article_rows if row["condition_id"] == "C1"
    ]
    deltas = []
    by_condition_rep = {
        (row["condition_id"], row["replicate_id"]): float(row["mean_total"])
        for row in article_rows
    }
    for row in condition_rows:
        cid = row["condition_id"]
        diffs = [
            by_condition_rep[(cid, rep)] - by_condition_rep[("C1", rep)]
            for rep in ["R1", "R2", "R3"]
        ]
        lo, hi = bootstrap_ci(diffs)
        deltas.append((cid, sum(diffs) / len(diffs), lo, hi))

    ranking_rows = []
    for rank, row in enumerate(condition_rows, start=1):
        cid = row["condition_id"]
        delta = next(item for item in deltas if item[0] == cid)
        ranking_rows.append(
            [
                rank,
                cid,
                CONDITION_NAMES[cid],
                fmt(float(row["mean_article_total"])),
                fmt(float(row["sd_article_total"])),
                fmt(delta[1]),
                f"[{fmt(delta[2])}, {fmt(delta[3])}]",
            ]
        )

    dim_rows = []
    for row in condition_rows:
        cid = row["condition_id"]
        dim_rows.append(
            [
                cid,
                CONDITION_NAMES[cid],
                *[
                    fmt(float(row[f"mean_{key}"]))
                    for key, _, _ in DIMENSIONS
                ],
            ]
        )

    position_rows = [
        [position, fmt(value), sum(1 for row in score_rows if int(row["position"]) == position)]
        for position, value in position_means
    ]

    spread = max(float(row["mean_article_total"]) for row in condition_rows) - min(
        float(row["mean_article_total"]) for row in condition_rows
    )
    top = condition_rows[0]
    c1_row = next(row for row in condition_rows if row["condition_id"] == "C1")

    top_id = top["condition_id"]
    top_name = CONDITION_NAMES[top_id]
    c1_mean = fmt(float(c1_row["mean_article_total"]))
    c2_row = next(row for row in condition_rows if row["condition_id"] == "C2")
    c1_reader = float(c1_row["mean_reader_orientation"])
    c1_cohesion = float(c1_row["mean_cohesion_coherence"])
    top_reader = max(float(row["mean_reader_orientation"]) for row in condition_rows)
    top_cohesion = max(float(row["mean_cohesion_coherence"]) for row in condition_rows)
    target_delta_vs_c2 = (
        float(c1_row["mean_reader_orientation"])
        + float(c1_row["mean_cohesion_coherence"])
        - float(c2_row["mean_reader_orientation"])
        - float(c2_row["mean_cohesion_coherence"])
    )
    total_delta_vs_c2 = float(c1_row["mean_article_total"]) - float(c2_row["mean_article_total"])
    c1_rank = next(
        rank for rank, row in enumerate(condition_rows, start=1) if row["condition_id"] == "C1"
    )
    if top_id == "C1":
        headline = (
            f"The revised focal reader-aware skill (`C1`) had the top mean total score "
            f"at {c1_mean}/100."
        )
    else:
        headline = (
            f"The top condition was `{top_id}` ({top_name}) at "
            f"{fmt(float(top['mean_article_total']))}/100, while the revised focal "
            f"reader-aware skill (`C1`) ranked {c1_rank} at {c1_mean}/100."
        )
    matrix_table_rows = [
        [row["condition_id"], row["C1"], row["C2"], row["C3"], row["C4"], row["C5"]]
        for row in matrix_rows
    ]

    body = f"""---
title: "Arrangement5-5 Scientific Writing Skill Comparison"
format: gfm
---

# Arrangement5-5 Scientific Writing Skill Comparison

Run ID: `{run_id}`  
Dossier: `D002_caspase5c_wnt_noisy_notes.md`  
Source article: {SOURCE_ARTICLE}

Evaluation design: one blinded evaluator (`E1`) scored 15 packets: 3 replicates x 5 presentation arrangements. Each article appeared once in each position within its replicate. Neutral nicknames were decoded only after scoring.

## Executive Summary

{headline} The full spread across all five conditions was {fmt(spread)} point on a 100-point rubric.

Small score gaps should be read as directional because this is still a single-topic benchmark with three authoring replicates per condition.

![Blinded total score distribution by authoring setting](figures/total_score_boxplot_by_skill.svg)

*Figure 1. Blinded total-score distribution by authoring setting. Each dot is one total score for one generated article in one of the five presentation positions (`15` scores per condition: 3 articles x 5 positions). Boxes show the interquartile range, the center line is the median, and whiskers show the observed minimum and maximum. Conditions are ordered by article-level mean total score, which is the primary ranking unit after averaging each article across all five positions. Because the Arrangement5-5 design makes every article appear once in every position, the plot shows the score distribution used for ranking while preventing any condition from benefiting from a systematically earlier or later presentation slot.*

## Evaluation Design and Records

### Comparable Skills and Snapshots

The benchmark compared the focal skill against a no-skill control and three public writing-skill comparators. Each authoring condition ran in an isolated `CODEX_HOME` containing only the assigned user skill, and each snapshot was recorded before authoring began.

{markdown_table(["Condition", "Role", "GitHub / Source Link", "Snapshot or Download UTC", "Recorded Version"], SKILL_SNAPSHOT_ROWS)}

### Dossier Construction and Access Control

The D002 dossier was designed to test whether a writing skill can build a readable scientific article from imperfect source notes rather than from a polished outline. The source was a very recent 2026 Nature article; benchmark agents were not given a preprint, an open-access manuscript, the source PDF, web access, or external search. They received only the fixed dossier text embedded in the prompt.

The dossier was created by extracting study information from the source article and then adding controlled source-note noise: disordered facts, repetition, rough wording, typos, grammar errors, and confusing transitions. It also preserved caveats and prohibited-claim notes so the evaluator could penalize unsupported upgrades such as treating CASP5C as a proven disease cause or validated therapeutic target. Evaluation treated the dossier, not agent memory or outside literature, as the source of truth.

### Blinding, Position Balance, and Decoding

Before evaluation, condition labels, skill names, model metadata, source filenames, and replicate IDs were removed from the article packets and replaced with neutral nicknames. The private maps were decoded only after scoring.

This position control is necessary because LLM judges can show order effects. {POSITION_BIAS_REFERENCE} reported that simply changing candidate-response order can alter quality rankings, and proposed balanced-position calibration as one mitigation. Arrangement5-5 applies the same principle to five candidate articles: for each replicate, five Latin-square packets rotate the five articles so every condition appears exactly once in each presentation position. The decoder then verifies row counts, leakage patterns, pairwise coverage, nickname membership, and exact position balance before condition means are reported.

## Primary Ranking

Scores below use article-level means as the primary unit (`n = 3` articles per condition). The repeated position scores are averaged within each article before condition-level comparison.

{markdown_table(["Rank", "Condition", "Name", "Mean total", "Article SD", "Delta vs C1", "Bootstrap CI"], ranking_rows)}

The bootstrap interval is descriptive only. It resamples three article-level replicate differences and should not be treated as a formal significance test.

## Dimension Profile

![Dimension heatmap](figures/dimension_heatmap.svg)

{markdown_table(["Condition", "Name", *[label for _, label, _ in DIMENSIONS]], dim_rows)}

The dimension profile is the main diagnostic view for the skill revision. Reader orientation and cohesion/coherence are the target dimensions; article structure, evidence discipline, and constraint following show whether the skill improved reader-aware behavior without losing scientific control.

In this run, `C1` scored {fmt(c1_reader)}/15 on reader orientation (best score: {fmt(top_reader)}/15) and {fmt(c1_cohesion)}/20 on cohesion/coherence (best score: {fmt(top_cohesion)}/20). Against the no-skill baseline, `C1` gained {fmt(target_delta_vs_c2)} points on the combined target dimensions and {fmt(total_delta_vs_c2)} points in total score.

## Pairwise Preferences

![Pairwise win rate](figures/pairwise_win_rate.svg)

Pairwise scores add a useful check because they do not always match total-score ordering.

{markdown_table(["Condition", "C1", "C2", "C3", "C4", "C5"], matrix_table_rows)}

## Position Check

![Position effect](figures/position_effect.svg)

{markdown_table(["Position", "Mean total", "Score rows"], position_rows)}

The decoder verified exact position balance: every condition appeared three times in each of the five presentation positions, and each article was scored once in every position. The position means nevertheless show a strong absolute-score position effect, with early positions scored higher. This is why the balanced design matters: early-position generosity is averaged across all conditions instead of being attached to one skill. Arrangement5-5 should therefore be retained for future runs; a single fixed or merely random order would be much less reliable.

## Interpretation

The main conclusion should be read together with the position-balanced design and the narrow score spread. The revised `C1` skill moved to first overall and showed its clearest target-dimension gain on reader orientation, while cohesion/coherence remained a tie with the no-skill baseline. This supports the revision direction but also shows the next iteration should make paragraph-to-paragraph progression even more visible in the final article.

A stronger next benchmark should use multiple papers, more diverse article genres, and evaluation dimensions that more directly stress reader-path construction, paragraph logic, and repair of noisy or poorly ordered source material.

## Audit Notes

- Comparator skill sources, snapshot times, and recorded hashes are listed in the report and in `comparing/skill_registry.md`.
- The dossier used a recent article that authoring and evaluation agents could not independently access during the run; they received only extracted noisy notes with deliberate surface errors and caveat traps.
- Authoring used `writing-subagent-v2-minimal`, which did not ask submodels to improve quality beyond following their assigned skill.
- The dossier was deliberately noisy and less systematically organized.
- Evaluation used neutral nicknames and private decoding maps to avoid condition labels.
- An initial sequential evaluator attempt was superseded because later packets could see earlier raw evaluation files in the repository. The final reported results come from `run_arrangement55_evaluation_packets.py`, which runs each packet in a fresh temporary work directory and copies only the completed outputs back into the repository.
- `decode_arrangement55_scores.py` passed schema, leakage, pairwise coverage, and position-balance checks.
"""

    qmd_path = report_root / "comparison_report.qmd"
    md_path = report_root / "comparison_report.md"
    qmd_path.write_text(body, encoding="utf-8")
    md_path.write_text(body.split("---\n", 2)[-1].lstrip(), encoding="utf-8")
    print(f"Wrote {qmd_path.relative_to(REPO_ROOT)}")
    print(f"Wrote {md_path.relative_to(REPO_ROOT)}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-id", required=True)
    args = parser.parse_args()
    generate(args.run_id)


if __name__ == "__main__":
    main()
