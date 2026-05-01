#!/usr/bin/env python3
"""Utilities for the scientific-writing skill comparison benchmark.

The script intentionally uses only the Python standard library so the
benchmark report can be regenerated in a minimal environment.
"""

from __future__ import annotations

import argparse
import csv
import html
import math
import random
import re
import statistics
from collections import defaultdict
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]

DIMENSIONS = [
    ("scientific_fidelity", "Scientific fidelity", 20),
    ("article_structure", "Article structure", 15),
    ("reader_orientation", "Reader orientation", 15),
    ("cohesion_coherence", "Cohesion/coherence", 20),
    ("evidence_uncertainty", "Evidence/uncertainty", 15),
    ("style_readability", "Style/readability", 10),
    ("constraint_following", "Constraint following", 5),
]

CONDITION_NAMES = {
    "C1": "Reader-aware writing",
    "C2": "No-skill baseline",
    "C3": "Scientific-writing representative",
    "C4": "Scientific-writing alternative",
    "C5": "Academic writing standards",
}

CONDITION_SHORT = {
    "C1": "Reader-aware",
    "C2": "No skill",
    "C3": "Sci-writing A",
    "C4": "Sci-writing B",
    "C5": "Academic std.",
}


def rel(path: Path) -> str:
    return path.relative_to(REPO_ROOT).as_posix()


def strip_frontmatter(text: str) -> str:
    if text.startswith("---\n"):
        end = text.find("\n---\n", 4)
        if end != -1:
            return text[end + 5 :].lstrip()
    return text.lstrip()


def word_count(text: str) -> int:
    return len(re.findall(r"[A-Za-z0-9]+(?:[-'][A-Za-z0-9]+)*", text))


def source_key(path: Path) -> tuple[int, int]:
    match = re.match(r"C([1-5])_R([1-3])\.md$", path.name)
    if not match:
        return (99, 99)
    return (int(match.group(1)), int(match.group(2)))


def parse_condition_replicate(path: Path) -> tuple[str, str]:
    match = re.match(r"(C[1-5])_(R[1-3])\.md$", path.name)
    if not match:
        raise ValueError(f"Unexpected article filename: {path}")
    return match.group(1), match.group(2)


def blind_articles(args: argparse.Namespace) -> None:
    run_id = args.run_id
    source_dir = REPO_ROOT / "comparing" / "authoring_results" / run_id
    blind_dir = REPO_ROOT / "comparing" / "blinded_articles" / run_id
    blind_dir.mkdir(parents=True, exist_ok=True)

    sources = sorted(source_dir.glob("C[1-5]_R[1-3].md"), key=source_key)
    if len(sources) != 15:
        raise SystemExit(f"Expected 15 source articles, found {len(sources)} in {source_dir}")

    rng = random.Random(args.seed)
    shuffled = sources[:]
    rng.shuffle(shuffled)

    mapping_path = blind_dir / "blinding_map_private.csv"
    with mapping_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "blinded_article_id",
                "source_output_path",
                "condition_id",
                "replicate_id",
                "word_count",
            ],
        )
        writer.writeheader()
        for idx, source in enumerate(shuffled):
            article_id = f"Article_{chr(ord('A') + idx)}"
            condition_id, replicate_id = parse_condition_replicate(source)
            article_text = strip_frontmatter(source.read_text(encoding="utf-8"))
            blinded_text = f"# {article_id}\n\n{article_text.rstrip()}\n"
            (blind_dir / f"{article_id}.md").write_text(blinded_text, encoding="utf-8")
            writer.writerow(
                {
                    "blinded_article_id": article_id,
                    "source_output_path": rel(source),
                    "condition_id": condition_id,
                    "replicate_id": replicate_id,
                    "word_count": word_count(article_text),
                }
            )

    print(f"Wrote blinded articles to {rel(blind_dir)}")
    print(f"Wrote private map to {rel(mapping_path)}")


def read_blind_map(run_id: str) -> list[dict[str, str]]:
    path = REPO_ROOT / "comparing" / "blinded_articles" / run_id / "blinding_map_private.csv"
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def evaluator_order(article_ids: list[str], evaluator_id: str) -> list[str]:
    ids = article_ids[:]
    seed = f"{evaluator_id}-run-2026-05-01-D001-order"
    random.Random(seed).shuffle(ids)
    if evaluator_id == "E3":
        ids.reverse()
    return ids


def generate_eval_prompts(args: argparse.Namespace) -> None:
    run_id = args.run_id
    dossier_path = REPO_ROOT / "comparing" / "dossiers" / args.dossier
    blind_dir = REPO_ROOT / "comparing" / "blinded_articles" / run_id
    prompt_dir = REPO_ROOT / "comparing" / "prompts" / "generated" / run_id / "evaluation"
    result_dir = REPO_ROOT / "comparing" / "evaluation_results" / run_id
    prompt_dir.mkdir(parents=True, exist_ok=True)
    result_dir.mkdir(parents=True, exist_ok=True)

    article_ids = sorted(path.stem for path in blind_dir.glob("Article_*.md"))
    if len(article_ids) != 15:
        raise SystemExit(f"Expected 15 blinded articles, found {len(article_ids)} in {blind_dir}")

    dossier_text = dossier_path.read_text(encoding="utf-8").strip()

    for evaluator_id in args.evaluators:
        order = evaluator_order(article_ids, evaluator_id)
        articles = []
        for article_id in order:
            article_path = blind_dir / f"{article_id}.md"
            articles.append(f"## {article_id}\n\n{article_path.read_text(encoding='utf-8').strip()}")
        article_packet = "\n\n---\n\n".join(articles)

        md_path = result_dir / f"{evaluator_id}.md"
        scores_path = result_dir / f"{evaluator_id}_scores.tsv"
        pairwise_path = result_dir / f"{evaluator_id}_pairwise.tsv"
        prompt = f"""You are an independent blinded evaluator in a benchmark of scientific writing quality.

Evaluator Metadata
- Run ID: {run_id}
- Evaluator ID: {evaluator_id}
- Prompt version: evaluation-subagent-v2-tsv
- Markdown output path: {md_path}
- Scores TSV path: {scores_path}
- Pairwise TSV path: {pairwise_path}

Blinding and Isolation Rules
- You are using no authoring skill. Evaluate from the standard rubric only.
- Do not infer or guess which skill, model, condition, or replicate produced an article.
- Evaluate only the blinded article text and the fixed dossier.
- Do not use web search or external sources.
- Do not reward an article for adding facts absent from the dossier.
- Penalize invented or unsupported claims, even if they sound plausible.

Scoring Rubric: 100 Points
1. Scientific fidelity and source use: 20 points
   Uses only dossier-supported facts; preserves caveats; invents no data,
   methods, citations, mechanisms, or conclusions.
2. Article structure: 15 points
   Uses appropriate scientific article sections; shows the research problem,
   approach, findings, and defensible takeaway.
3. Reader orientation: 15 points
   Anticipates the target reader; introduces concepts before relying on them;
   matches technical density to the stated reader.
4. Cohesion and coherence: 20 points
   Paragraphs have governing ideas; sentences and paragraphs progress
   old-to-new; transitions make logic and section shifts clear.
5. Evidence discipline and uncertainty: 15 points
   Separates results, interpretation, implication, and speculation; bounds
   claims to the design, data, and limitations.
6. Scientific style and readability: 10 points
   Uses precise wording; sentences are parseable on a first pass; jargon,
   abbreviations, voice, and punctuation serve clarity.
7. Constraint following: 5 points
   Follows requested word count, section, citation, and dossier constraints.

Required Output Files
1. Save a Markdown evaluation log to `{md_path}`.
2. Save a tab-separated score table to `{scores_path}` with exactly this header:
   evaluator_id\tarticle_id\tscientific_fidelity\tarticle_structure\treader_orientation\tcohesion_coherence\tevidence_uncertainty\tstyle_readability\tconstraint_following\ttotal_score\trank\tone_sentence_justification
3. Save a tab-separated pairwise preference table to `{pairwise_path}` with exactly this header:
   evaluator_id\tarticle_a\tarticle_b\tpreferred_article\treason

Score Table Rules
- Include exactly one score row for each of the 15 articles.
- Scores should be integers.
- Total score must equal the seven dimension scores.
- Rank 1 is strongest. Use tied ranks only if scores and judgments are genuinely tied.
- Do not include tabs inside justifications.

Pairwise Table Rules
- Include every unordered pair among the 15 articles, exactly once: 105 rows.
- `preferred_article` must be one article ID or `Tie`.
- Do not include tabs inside reasons.

Markdown Log Sections
1. Metadata and article order
2. Per-article score table
3. Ranked list
4. Pairwise preference summary
5. Major strengths and weaknesses for each article
6. Evaluation caveats, including any possible order sensitivity

Before finalizing, validate that both TSV files have the required headers and row counts.

Fixed Dossier
---
{dossier_text}
---

Blinded Articles in Evaluation Order
---
{article_packet}
---
"""
        (prompt_dir / f"{evaluator_id}.txt").write_text(prompt, encoding="utf-8")
        print(f"Wrote {rel(prompt_dir / f'{evaluator_id}.txt')}")


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def mean(values: list[float]) -> float:
    return sum(values) / len(values) if values else float("nan")


def sample_sd(values: list[float]) -> float:
    return statistics.stdev(values) if len(values) > 1 else 0.0


def fmt(value: float, digits: int = 1) -> str:
    if math.isnan(value):
        return "NA"
    return f"{value:.{digits}f}"


def aggregate(args: argparse.Namespace) -> None:
    run_id = args.run_id
    result_dir = REPO_ROOT / "comparing" / "evaluation_results" / run_id
    report_dir = REPO_ROOT / "comparing" / "reports" / run_id
    figures_dir = report_dir / "figures"
    report_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    blind_rows = read_blind_map(run_id)
    article_meta = {row["blinded_article_id"]: row for row in blind_rows}

    score_rows: list[dict[str, object]] = []
    for scores_path in sorted(result_dir.glob("E*_scores.tsv")):
        for row in read_tsv(scores_path):
            article_id = row["article_id"]
            if article_id not in article_meta:
                raise SystemExit(f"Unknown article ID {article_id} in {scores_path}")
            meta = article_meta[article_id]
            output = {
                "run_id": run_id,
                "evaluator_id": row["evaluator_id"],
                "article_id": article_id,
                "condition_id": meta["condition_id"],
                "condition_name": CONDITION_NAMES[meta["condition_id"]],
                "replicate_id": meta["replicate_id"],
                "word_count": int(meta["word_count"]),
            }
            total = 0
            for key, _, _ in DIMENSIONS:
                value = int(row[key])
                output[key] = value
                total += value
            output["total_score"] = int(row.get("total_score") or total)
            output["rank"] = row.get("rank", "")
            output["one_sentence_justification"] = row.get("one_sentence_justification", "")
            score_rows.append(output)

    expected_scores = 15 * len({row["evaluator_id"] for row in score_rows})
    if score_rows and len(score_rows) != expected_scores:
        raise SystemExit(f"Score row count mismatch: {len(score_rows)} vs {expected_scores}")

    scorebook_path = result_dir / "scorebook.csv"
    score_fields = [
        "run_id",
        "evaluator_id",
        "article_id",
        "condition_id",
        "condition_name",
        "replicate_id",
        "word_count",
        *[key for key, _, _ in DIMENSIONS],
        "total_score",
        "rank",
        "one_sentence_justification",
    ]
    write_csv(scorebook_path, score_rows, score_fields)

    by_condition: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in score_rows:
        by_condition[str(row["condition_id"])].append(row)

    summary_rows: list[dict[str, object]] = []
    for condition_id in sorted(CONDITION_NAMES):
        rows = by_condition[condition_id]
        totals = [float(row["total_score"]) for row in rows]
        reader_scores = [
            float(row["reader_orientation"]) + float(row["cohesion_coherence"]) for row in rows
        ]
        reliability_scores = [
            float(row["scientific_fidelity"]) + float(row["evidence_uncertainty"])
            for row in rows
        ]
        summary = {
            "condition_id": condition_id,
            "condition_name": CONDITION_NAMES[condition_id],
            "n_scores": len(rows),
            "mean_total": round(mean(totals), 3),
            "sd_total": round(sample_sd(totals), 3),
            "mean_reader_centered": round(mean(reader_scores), 3),
            "mean_reliability": round(mean(reliability_scores), 3),
            "mean_word_count": round(mean([float(row["word_count"]) for row in rows]), 1),
        }
        for key, _, _ in DIMENSIONS:
            summary[f"mean_{key}"] = round(mean([float(row[key]) for row in rows]), 3)
        summary_rows.append(summary)

    summary_rows.sort(key=lambda row: float(row["mean_total"]), reverse=True)
    for index, row in enumerate(summary_rows, start=1):
        row["overall_rank"] = index

    summary_path = result_dir / "summary_by_condition.csv"
    summary_fields = [
        "overall_rank",
        "condition_id",
        "condition_name",
        "n_scores",
        "mean_total",
        "sd_total",
        "mean_reader_centered",
        "mean_reliability",
        "mean_word_count",
        *[f"mean_{key}" for key, _, _ in DIMENSIONS],
    ]
    write_csv(summary_path, summary_rows, summary_fields)

    article_groups: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in score_rows:
        article_groups[str(row["article_id"])].append(row)
    article_rows = []
    for article_id, rows in sorted(article_groups.items()):
        totals = [float(row["total_score"]) for row in rows]
        first = rows[0]
        article_rows.append(
            {
                "article_id": article_id,
                "condition_id": first["condition_id"],
                "replicate_id": first["replicate_id"],
                "word_count": first["word_count"],
                "mean_total": round(mean(totals), 3),
                "sd_total": round(sample_sd(totals), 3),
            }
        )
    write_csv(
        result_dir / "summary_by_article.csv",
        article_rows,
        ["article_id", "condition_id", "replicate_id", "word_count", "mean_total", "sd_total"],
    )

    matrix_rows = build_pairwise_matrix(run_id, result_dir, article_meta)
    write_csv(
        result_dir / "pairwise_condition_matrix.csv",
        matrix_rows,
        ["condition_id", *sorted(CONDITION_NAMES)],
    )

    make_figures(summary_rows, matrix_rows, figures_dir)
    make_report(run_id, score_rows, summary_rows, article_rows, matrix_rows, report_dir)

    print(f"Wrote {rel(scorebook_path)}")
    print(f"Wrote {rel(summary_path)}")
    print(f"Wrote report files in {rel(report_dir)}")


def build_pairwise_matrix(
    run_id: str, result_dir: Path, article_meta: dict[str, dict[str, str]]
) -> list[dict[str, object]]:
    wins = defaultdict(float)
    totals = defaultdict(float)
    for path in sorted(result_dir.glob("E*_pairwise.tsv")):
        rows = read_tsv(path)
        for row in rows:
            a = row["article_a"]
            b = row["article_b"]
            if a not in article_meta or b not in article_meta:
                raise SystemExit(f"Unknown pairwise article ID in {path}: {a}, {b}")
            ca = article_meta[a]["condition_id"]
            cb = article_meta[b]["condition_id"]
            if ca == cb:
                continue
            preferred = row["preferred_article"]
            totals[(ca, cb)] += 1
            totals[(cb, ca)] += 1
            if preferred == a:
                wins[(ca, cb)] += 1
            elif preferred == b:
                wins[(cb, ca)] += 1
            else:
                wins[(ca, cb)] += 0.5
                wins[(cb, ca)] += 0.5

    matrix_rows: list[dict[str, object]] = []
    for ca in sorted(CONDITION_NAMES):
        output: dict[str, object] = {"condition_id": ca}
        for cb in sorted(CONDITION_NAMES):
            if ca == cb:
                output[cb] = ""
            else:
                denominator = totals[(ca, cb)]
                output[cb] = round(wins[(ca, cb)] / denominator, 3) if denominator else ""
        matrix_rows.append(output)
    return matrix_rows


def svg_text(x: float, y: float, text: object, size: int = 12, anchor: str = "start") -> str:
    return (
        f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" '
        f'font-family="Arial, Helvetica, sans-serif" text-anchor="{anchor}">'
        f"{html.escape(str(text))}</text>"
    )


def make_figures(summary_rows: list[dict[str, object]], matrix_rows: list[dict[str, object]], out: Path) -> None:
    make_total_bar(summary_rows, out / "mean_total_by_condition.svg")
    make_dimension_heatmap(summary_rows, out / "dimension_heatmap.svg")
    make_pairwise_heatmap(matrix_rows, out / "pairwise_win_rate.svg")
    make_reader_reliability_plot(summary_rows, out / "reader_vs_reliability.svg")


def make_total_bar(rows: list[dict[str, object]], path: Path) -> None:
    width, height = 900, 470
    margin_l, margin_b, margin_t, margin_r = 90, 90, 55, 35
    plot_w = width - margin_l - margin_r
    plot_h = height - margin_t - margin_b
    max_y = 100
    ordered = sorted(rows, key=lambda row: row["condition_id"])
    bar_w = plot_w / len(ordered) * 0.58
    gap = plot_w / len(ordered)
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="#ffffff"/>',
        svg_text(width / 2, 30, "Mean total score by condition", 20, "middle"),
    ]
    for tick in range(0, 101, 20):
        y = margin_t + plot_h - plot_h * tick / max_y
        parts.append(f'<line x1="{margin_l}" y1="{y:.1f}" x2="{width-margin_r}" y2="{y:.1f}" stroke="#e6e6e6"/>')
        parts.append(svg_text(margin_l - 12, y + 4, tick, 11, "end"))
    parts.append(f'<line x1="{margin_l}" y1="{margin_t}" x2="{margin_l}" y2="{margin_t+plot_h}" stroke="#333"/>')
    parts.append(f'<line x1="{margin_l}" y1="{margin_t+plot_h}" x2="{width-margin_r}" y2="{margin_t+plot_h}" stroke="#333"/>')
    palette = ["#3465a4", "#7a7a7a", "#2f8f83", "#c07a2b", "#8e5aa9"]
    for index, row in enumerate(ordered):
        mean_total = float(row["mean_total"])
        sd_total = float(row["sd_total"])
        cx = margin_l + gap * index + gap / 2
        h = plot_h * mean_total / max_y
        x = cx - bar_w / 2
        y = margin_t + plot_h - h
        parts.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{bar_w:.1f}" height="{h:.1f}" fill="{palette[index]}"/>')
        err_top = margin_t + plot_h - plot_h * min(max_y, mean_total + sd_total) / max_y
        err_bot = margin_t + plot_h - plot_h * max(0, mean_total - sd_total) / max_y
        parts.append(f'<line x1="{cx:.1f}" y1="{err_top:.1f}" x2="{cx:.1f}" y2="{err_bot:.1f}" stroke="#222" stroke-width="2"/>')
        parts.append(f'<line x1="{cx-8:.1f}" y1="{err_top:.1f}" x2="{cx+8:.1f}" y2="{err_top:.1f}" stroke="#222" stroke-width="2"/>')
        parts.append(f'<line x1="{cx-8:.1f}" y1="{err_bot:.1f}" x2="{cx+8:.1f}" y2="{err_bot:.1f}" stroke="#222" stroke-width="2"/>')
        parts.append(svg_text(cx, y - 8, fmt(mean_total), 12, "middle"))
        parts.append(svg_text(cx, height - 55, row["condition_id"], 12, "middle"))
        parts.append(svg_text(cx, height - 35, CONDITION_SHORT[str(row["condition_id"])], 11, "middle"))
    parts.append(svg_text(25, margin_t + plot_h / 2, "Score out of 100", 13, "middle"))
    parts.append("</svg>")
    path.write_text("\n".join(parts), encoding="utf-8")


def color_scale(value: float, max_value: float) -> str:
    ratio = 0 if max_value == 0 else min(1, max(0, value / max_value))
    r = int(245 - 190 * ratio)
    g = int(247 - 90 * ratio)
    b = int(250 - 35 * ratio)
    return f"#{r:02x}{g:02x}{b:02x}"


def make_dimension_heatmap(rows: list[dict[str, object]], path: Path) -> None:
    cell_w, cell_h = 110, 52
    margin_l, margin_t = 160, 105
    width = margin_l + cell_w * len(DIMENSIONS) + 35
    height = margin_t + cell_h * len(rows) + 45
    ordered = sorted(rows, key=lambda row: row["condition_id"])
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="#ffffff"/>',
        svg_text(width / 2, 30, "Mean rubric score by condition", 20, "middle"),
    ]
    for j, (_, label, _) in enumerate(DIMENSIONS):
        x = margin_l + j * cell_w + cell_w / 2
        parts.append(svg_text(x, 75, label, 10, "middle"))
    for i, row in enumerate(ordered):
        y = margin_t + i * cell_h
        parts.append(svg_text(20, y + 32, f"{row['condition_id']} {CONDITION_SHORT[str(row['condition_id'])]}", 12))
        for j, (key, _, max_score) in enumerate(DIMENSIONS):
            value = float(row[f"mean_{key}"])
            x = margin_l + j * cell_w
            parts.append(
                f'<rect x="{x:.1f}" y="{y:.1f}" width="{cell_w-3}" height="{cell_h-3}" '
                f'fill="{color_scale(value, max_score)}" stroke="#ffffff"/>'
            )
            parts.append(svg_text(x + cell_w / 2, y + 31, fmt(value), 13, "middle"))
    parts.append("</svg>")
    path.write_text("\n".join(parts), encoding="utf-8")


def win_color(value: float) -> str:
    if math.isnan(value):
        return "#f4f4f4"
    if value >= 0.5:
        ratio = (value - 0.5) / 0.5
        return f"#{int(235 - 140 * ratio):02x}{int(244 - 60 * ratio):02x}{int(236 - 100 * ratio):02x}"
    ratio = (0.5 - value) / 0.5
    return f"#{int(248 - 70 * ratio):02x}{int(239 - 95 * ratio):02x}{int(229 - 105 * ratio):02x}"


def make_pairwise_heatmap(rows: list[dict[str, object]], path: Path) -> None:
    ids = sorted(CONDITION_NAMES)
    cell = 90
    margin_l, margin_t = 155, 95
    width = margin_l + cell * len(ids) + 40
    height = margin_t + cell * len(ids) + 50
    row_map = {row["condition_id"]: row for row in rows}
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="#ffffff"/>',
        svg_text(width / 2, 30, "Pairwise win rate by condition", 20, "middle"),
        svg_text(width / 2, height - 12, "Cells show row condition preferred over column condition", 12, "middle"),
    ]
    for j, cid in enumerate(ids):
        parts.append(svg_text(margin_l + j * cell + cell / 2, 70, cid, 12, "middle"))
    for i, ca in enumerate(ids):
        y = margin_t + i * cell
        parts.append(svg_text(20, y + 49, f"{ca} {CONDITION_SHORT[ca]}", 12))
        for j, cb in enumerate(ids):
            x = margin_l + j * cell
            raw = row_map[ca][cb]
            value = float(raw) if raw != "" else float("nan")
            parts.append(
                f'<rect x="{x:.1f}" y="{y:.1f}" width="{cell-3}" height="{cell-3}" '
                f'fill="{win_color(value)}" stroke="#ffffff"/>'
            )
            label = "-" if raw == "" else f"{100*value:.0f}%"
            parts.append(svg_text(x + cell / 2, y + 52, label, 13, "middle"))
    parts.append("</svg>")
    path.write_text("\n".join(parts), encoding="utf-8")


def make_reader_reliability_plot(rows: list[dict[str, object]], path: Path) -> None:
    width, height = 760, 470
    margin_l, margin_r, margin_t, margin_b = 85, 35, 55, 70
    plot_w = width - margin_l - margin_r
    plot_h = height - margin_t - margin_b
    x_max, y_max = 35, 35
    ordered = sorted(rows, key=lambda row: row["condition_id"])
    palette = ["#3465a4", "#7a7a7a", "#2f8f83", "#c07a2b", "#8e5aa9"]
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="#ffffff"/>',
        svg_text(width / 2, 30, "Reader-centered score versus scientific reliability", 20, "middle"),
    ]
    for tick in range(0, 36, 5):
        x = margin_l + plot_w * tick / x_max
        y = margin_t + plot_h - plot_h * tick / y_max
        parts.append(f'<line x1="{x:.1f}" y1="{margin_t}" x2="{x:.1f}" y2="{margin_t+plot_h}" stroke="#eeeeee"/>')
        parts.append(f'<line x1="{margin_l}" y1="{y:.1f}" x2="{width-margin_r}" y2="{y:.1f}" stroke="#eeeeee"/>')
        parts.append(svg_text(x, height - 45, tick, 10, "middle"))
        parts.append(svg_text(margin_l - 12, y + 4, tick, 10, "end"))
    parts.append(f'<line x1="{margin_l}" y1="{margin_t}" x2="{margin_l}" y2="{margin_t+plot_h}" stroke="#333"/>')
    parts.append(f'<line x1="{margin_l}" y1="{margin_t+plot_h}" x2="{width-margin_r}" y2="{margin_t+plot_h}" stroke="#333"/>')
    for index, row in enumerate(ordered):
        x_value = float(row["mean_reliability"])
        y_value = float(row["mean_reader_centered"])
        x = margin_l + plot_w * x_value / x_max
        y = margin_t + plot_h - plot_h * y_value / y_max
        parts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="10" fill="{palette[index]}" stroke="#222"/>')
        parts.append(svg_text(x + 14, y + 4, row["condition_id"], 13))
    parts.append(svg_text(width / 2, height - 15, "Scientific fidelity + evidence discipline (max 35)", 12, "middle"))
    parts.append(svg_text(25, margin_t + plot_h / 2, "Reader orientation + cohesion (max 35)", 12, "middle"))
    parts.append("</svg>")
    path.write_text("\n".join(parts), encoding="utf-8")


def markdown_table(rows: list[dict[str, object]], columns: list[tuple[str, str]]) -> str:
    header = "| " + " | ".join(label for _, label in columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    lines = [header, sep]
    for row in rows:
        values = []
        for key, _ in columns:
            value = row.get(key, "")
            if isinstance(value, float):
                values.append(fmt(value, 1))
            else:
                values.append(str(value))
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def make_report(
    run_id: str,
    score_rows: list[dict[str, object]],
    summary_rows: list[dict[str, object]],
    article_rows: list[dict[str, object]],
    matrix_rows: list[dict[str, object]],
    report_dir: Path,
) -> None:
    qmd_path = report_dir / "comparison_report.qmd"
    md_path = report_dir / "comparison_report.md"
    eval_ids = sorted({str(row["evaluator_id"]) for row in score_rows})
    n_articles = len({row["article_id"] for row in score_rows})
    top = summary_rows[0]
    runner_up = summary_rows[1] if len(summary_rows) > 1 else None
    gap = float(top["mean_total"]) - float(runner_up["mean_total"]) if runner_up else 0.0

    summary_table = markdown_table(
        summary_rows,
        [
            ("overall_rank", "Rank"),
            ("condition_id", "Condition"),
            ("condition_name", "Skill condition"),
            ("n_scores", "N scores"),
            ("mean_total", "Mean total"),
            ("sd_total", "SD"),
            ("mean_reader_centered", "Reader-centered"),
            ("mean_reliability", "Reliability"),
            ("mean_word_count", "Mean words"),
        ],
    )
    article_table = markdown_table(
        sorted(article_rows, key=lambda row: float(row["mean_total"]), reverse=True),
        [
            ("article_id", "Article"),
            ("condition_id", "Condition"),
            ("replicate_id", "Replicate"),
            ("word_count", "Words"),
            ("mean_total", "Mean total"),
            ("sd_total", "SD"),
        ],
    )
    matrix_table = markdown_table(
        matrix_rows,
        [("condition_id", "Row beats column"), *[(cid, cid) for cid in sorted(CONDITION_NAMES)]],
    )

    body = f"""---
title: "Reader-Aware Writing Skill Benchmark"
format: gfm
run_id: "{run_id}"
---

# Reader-Aware Writing Skill Benchmark

## Executive Summary

This report compares five authoring conditions on the same controlled life-science dossier.
Each condition generated three independent articles.
The articles were blinded before evaluation, and {len(eval_ids)} independent evaluator runs scored {n_articles} articles with a 100-point rubric.

The top mean total score was **{fmt(float(top['mean_total']))}** for **{top['condition_id']} {top['condition_name']}**.
The gap to the next condition was **{fmt(gap)}** points, so the result should be interpreted with the replicate and evaluator variation shown below.

## Conditions

| Condition | Skill condition |
|---|---|
| C1 | Reader-aware writing, local repository skill |
| C2 | No-skill baseline |
| C3 | Public scientific-writing representative |
| C4 | Public scientific-writing alternative |
| C5 | Academic writing standards |

## Main Score Summary

![Mean total score by condition](figures/mean_total_by_condition.svg)

{summary_table}

## Rubric Profile

![Rubric dimension heatmap](figures/dimension_heatmap.svg)

Reader-centered score is `reader orientation + cohesion/coherence` out of 35.
Reliability score is `scientific fidelity + evidence discipline` out of 35.

![Reader-centered score versus reliability](figures/reader_vs_reliability.svg)

## Pairwise Preference Analysis

Pairwise win rates use evaluator pairwise preferences between articles from different conditions.
A value above 0.50 means the row condition was preferred more often than the column condition.

![Pairwise win-rate matrix](figures/pairwise_win_rate.svg)

{matrix_table}

## Article-Level Scores

{article_table}

## Methods

The source dossier was `D001_caspase5c_wnt_intestinal_homeostasis.md`, extracted from the user-supplied blinded PDF.
All authoring runs used the same model family and the same fixed writing prompt, except for the assigned skill and its isolated `CODEX_HOME`.
Each authoring condition had only its assigned user skill installed, with C2 intentionally containing no user writing skill.
System skills bundled with Codex were present but not the tested writing skills.

Articles were blinded by removing authoring metadata and assigning random `Article_*` identifiers with a fixed seed.
Evaluators received only the dossier, blinded articles, and the standard scoring rubric.
They did not receive condition names, skill names, replicate IDs, or the private blinding map.

## Limitations

This is a single-topic, single-model benchmark with three authoring replicates per condition.
The results estimate performance for this controlled scientific-writing task, not universal writing quality.
Small score gaps should be treated as directional until repeated on additional dossiers and evaluators.

## Audit Trail

- Protocol: `comparing/evaluation_protocol.md`
- Skill registry: `comparing/skill_registry.md`
- Evaluation log: `comparing/evaluation_log.md`
- Scorebook: `comparing/evaluation_results/{run_id}/scorebook.csv`
- Condition summary: `comparing/evaluation_results/{run_id}/summary_by_condition.csv`
- Private blinding map: `comparing/blinded_articles/{run_id}/blinding_map_private.csv`
"""
    qmd_path.write_text(body, encoding="utf-8")

    md_body = re.sub(r"^---\n.*?\n---\n\n", "", body, flags=re.S)
    md_body += "\n\n_Rendered from `comparison_report.qmd` by `comparing/scripts/benchmark_pipeline.py`._\n"
    md_path.write_text(md_body, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)

    blind = sub.add_parser("blind")
    blind.add_argument("--run-id", required=True)
    blind.add_argument("--seed", default="run-2026-05-01-D001-blinding")
    blind.set_defaults(func=blind_articles)

    prompts = sub.add_parser("eval-prompts")
    prompts.add_argument("--run-id", required=True)
    prompts.add_argument("--dossier", default="D001_caspase5c_wnt_intestinal_homeostasis.md")
    prompts.add_argument("--evaluators", nargs="+", default=["E1", "E2", "E3"])
    prompts.set_defaults(func=generate_eval_prompts)

    agg = sub.add_parser("aggregate")
    agg.add_argument("--run-id", required=True)
    agg.set_defaults(func=aggregate)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
