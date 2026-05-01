#!/usr/bin/env python3
"""Decode Arrangement5-5 evaluator scores back to benchmark conditions."""

from __future__ import annotations

import argparse
import csv
import math
import re
import statistics
from collections import defaultdict
from itertools import combinations
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]

CONDITIONS = ["C1", "C2", "C3", "C4", "C5"]
POSITIONS = ["1", "2", "3", "4", "5"]

DIMENSIONS = [
    ("scientific_fidelity", 20),
    ("article_structure", 15),
    ("reader_orientation", 15),
    ("cohesion_coherence", 20),
    ("evidence_uncertainty", 15),
    ("style_readability", 10),
    ("constraint_following", 5),
]

SCORE_HEADER = [
    "evaluator_id",
    "packet_id",
    "nickname",
    *[name for name, _ in DIMENSIONS],
    "total_score",
    "rank",
    "one_sentence_justification",
]

PAIRWISE_HEADER = [
    "evaluator_id",
    "packet_id",
    "nickname_a",
    "nickname_b",
    "preferred_nickname",
    "reason",
]

LEAK_PATTERNS = [
    r"\bC[1-5]_R[1-3]\b",
    r"\bC[1-5]\b",
    r"\bArticle_[A-Z]\b",
    r"reader-aware-writing",
    r"reader-aware writing",
    r"no-skill baseline",
    r"scientific-writing",
    r"academic-writing-standards",
    r"sci-writing",
]


def rel(path: Path) -> str:
    return path.relative_to(REPO_ROOT).as_posix()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def read_tsv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        return list(reader.fieldnames or []), list(reader)


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def mean(values: list[float]) -> float:
    return sum(values) / len(values) if values else float("nan")


def sd(values: list[float]) -> float:
    return statistics.stdev(values) if len(values) > 1 else 0.0


def rounded(value: float, digits: int = 3) -> float | str:
    return "NA" if math.isnan(value) else round(value, digits)


def leakage_hits(text: str) -> list[str]:
    hits: list[str] = []
    for pattern in LEAK_PATTERNS:
        if re.search(pattern, text, flags=re.IGNORECASE):
            hits.append(pattern)
    return hits


def plan_by_packet(plan_rows: list[dict[str, str]]) -> dict[str, list[dict[str, str]]]:
    packets: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in plan_rows:
        packets[row["packet_id"]].append(row)
    for packet, rows in packets.items():
        rows.sort(key=lambda row: int(row["position"]))
        positions = [row["position"] for row in rows]
        if positions != POSITIONS:
            raise SystemExit(f"Packet {packet} does not have positions 1-5: {positions}")
    return dict(packets)


def validate_position_balance(plan_rows: list[dict[str, str]]) -> list[dict[str, object]]:
    counts: dict[tuple[str, str, str, str], int] = defaultdict(int)
    for row in plan_rows:
        key = (
            row["evaluator_id"],
            row["replicate_id"],
            row["condition_id"],
            row["position"],
        )
        counts[key] += 1

    balance_rows: list[dict[str, object]] = []
    evaluators = sorted({row["evaluator_id"] for row in plan_rows})
    replicates = sorted({row["replicate_id"] for row in plan_rows})
    ok = True
    for evaluator_id in evaluators:
        for replicate_id in replicates:
            for condition_id in CONDITIONS:
                for position in POSITIONS:
                    count = counts[(evaluator_id, replicate_id, condition_id, position)]
                    if count != 1:
                        ok = False
                    balance_rows.append(
                        {
                            "evaluator_id": evaluator_id,
                            "replicate_id": replicate_id,
                            "condition_id": condition_id,
                            "position": position,
                            "count": count,
                        }
                    )
    if not ok:
        raise SystemExit("Arrangement5-5 position balance check failed")
    return balance_rows


def decode_scores(args: argparse.Namespace) -> None:
    run_id = args.run_id
    result_root = REPO_ROOT / "comparing" / "evaluation_results" / run_id / "arrangement55"
    raw_root = result_root / "raw"
    decoded_root = result_root / "decoded"
    plan_path = result_root / "arrangement_plan_private.csv"
    if not plan_path.exists():
        raise SystemExit(f"Missing arrangement plan: {plan_path}")

    plan_rows = read_csv(plan_path)
    packets = plan_by_packet(plan_rows)
    plan_lookup = {
        (row["packet_id"], row["nickname"]): row
        for row in plan_rows
    }
    position_balance_rows = validate_position_balance(plan_rows)

    decoded_scores: list[dict[str, object]] = []
    decoded_pairwise: list[dict[str, object]] = []

    for packet, expected_rows in sorted(packets.items()):
        expected_nicknames = {row["nickname"] for row in expected_rows}
        scores_path = raw_root / f"{packet}_scores.tsv"
        pairwise_path = raw_root / f"{packet}_pairwise.tsv"
        md_path = raw_root / f"{packet}.md"
        for path in [scores_path, pairwise_path, md_path]:
            if not path.exists():
                raise SystemExit(f"Missing evaluator output for packet {packet}: {path}")
            hits = leakage_hits(path.read_text(encoding="utf-8"))
            if hits:
                raise SystemExit(
                    f"Leakage check failed for {path}: matched {', '.join(hits)}"
                )

        score_header, score_rows = read_tsv(scores_path)
        if score_header != SCORE_HEADER:
            raise SystemExit(f"Bad score header in {scores_path}: {score_header}")
        if len(score_rows) != 5:
            raise SystemExit(f"Expected 5 score rows in {scores_path}, found {len(score_rows)}")
        observed_nicknames = {row["nickname"] for row in score_rows}
        if observed_nicknames != expected_nicknames:
            raise SystemExit(
                f"Nickname mismatch in {scores_path}: {observed_nicknames} vs {expected_nicknames}"
            )

        for row in score_rows:
            if row["packet_id"] != packet:
                raise SystemExit(f"Wrong packet_id in {scores_path}: {row['packet_id']}")
            plan = plan_lookup[(packet, row["nickname"])]
            total = 0
            output: dict[str, object] = {
                "run_id": run_id,
                "evaluator_id": row["evaluator_id"],
                "packet_id": packet,
                "replicate_id": plan["replicate_id"],
                "arrangement_id": plan["arrangement_id"],
                "position": int(plan["position"]),
                "nickname": row["nickname"],
                "condition_id": plan["condition_id"],
                "source_output_path": plan["source_output_path"],
                "word_count": int(plan["word_count"]),
            }
            for key, max_points in DIMENSIONS:
                value = int(row[key])
                if not 0 <= value <= max_points:
                    raise SystemExit(f"{scores_path}: {row['nickname']} {key}={value} out of range")
                output[key] = value
                total += value
            total_score = int(row["total_score"])
            if total_score != total:
                raise SystemExit(
                    f"{scores_path}: total mismatch for {row['nickname']}: {total_score} vs {total}"
                )
            output["total_score"] = total_score
            output["rank"] = row["rank"]
            output["one_sentence_justification"] = row["one_sentence_justification"]
            decoded_scores.append(output)

        pair_header, pair_rows = read_tsv(pairwise_path)
        if pair_header != PAIRWISE_HEADER:
            raise SystemExit(f"Bad pairwise header in {pairwise_path}: {pair_header}")
        if len(pair_rows) != 10:
            raise SystemExit(f"Expected 10 pairwise rows in {pairwise_path}, found {len(pair_rows)}")
        expected_pairs = {tuple(sorted(pair)) for pair in combinations(expected_nicknames, 2)}
        observed_pairs = {
            tuple(sorted([row["nickname_a"], row["nickname_b"]])) for row in pair_rows
        }
        if observed_pairs != expected_pairs:
            raise SystemExit(f"Pairwise nickname mismatch in {pairwise_path}")
        for row in pair_rows:
            if row["packet_id"] != packet:
                raise SystemExit(f"Wrong packet_id in {pairwise_path}: {row['packet_id']}")
            a = row["nickname_a"]
            b = row["nickname_b"]
            preferred = row["preferred_nickname"]
            if preferred not in {a, b, "Tie"}:
                raise SystemExit(f"Invalid preferred_nickname in {pairwise_path}: {preferred}")
            plan_a = plan_lookup[(packet, a)]
            plan_b = plan_lookup[(packet, b)]
            decoded_pairwise.append(
                {
                    "run_id": run_id,
                    "evaluator_id": row["evaluator_id"],
                    "packet_id": packet,
                    "replicate_id": plan_a["replicate_id"],
                    "arrangement_id": plan_a["arrangement_id"],
                    "nickname_a": a,
                    "condition_a": plan_a["condition_id"],
                    "position_a": int(plan_a["position"]),
                    "nickname_b": b,
                    "condition_b": plan_b["condition_id"],
                    "position_b": int(plan_b["position"]),
                    "preferred_nickname": preferred,
                    "preferred_condition": "Tie"
                    if preferred == "Tie"
                    else plan_lookup[(packet, preferred)]["condition_id"],
                    "reason": row["reason"],
                }
            )

    score_fields = [
        "run_id",
        "evaluator_id",
        "packet_id",
        "replicate_id",
        "arrangement_id",
        "position",
        "nickname",
        "condition_id",
        "source_output_path",
        "word_count",
        *[key for key, _ in DIMENSIONS],
        "total_score",
        "rank",
        "one_sentence_justification",
    ]
    write_csv(decoded_root / "decoded_scores.csv", decoded_scores, score_fields)

    pairwise_fields = [
        "run_id",
        "evaluator_id",
        "packet_id",
        "replicate_id",
        "arrangement_id",
        "nickname_a",
        "condition_a",
        "position_a",
        "nickname_b",
        "condition_b",
        "position_b",
        "preferred_nickname",
        "preferred_condition",
        "reason",
    ]
    write_csv(decoded_root / "decoded_pairwise.csv", decoded_pairwise, pairwise_fields)
    write_csv(
        decoded_root / "position_balance.csv",
        position_balance_rows,
        ["evaluator_id", "replicate_id", "condition_id", "position", "count"],
    )

    article_rows = summarize_articles(decoded_scores)
    condition_rows = summarize_conditions(decoded_scores, article_rows)
    matrix_rows = summarize_pairwise(decoded_pairwise)
    write_csv(
        decoded_root / "summary_by_article.csv",
        article_rows,
        [
            "condition_id",
            "replicate_id",
            "nickname",
            "source_output_path",
            "n_scores",
            "mean_total",
            "sd_total",
            "mean_position",
            *[f"mean_{key}" for key, _ in DIMENSIONS],
        ],
    )
    write_csv(
        decoded_root / "summary_by_condition.csv",
        condition_rows,
        [
            "condition_id",
            "n_articles",
            "n_scores",
            "mean_total",
            "sd_total",
            "mean_article_total",
            "sd_article_total",
            *[f"mean_{key}" for key, _ in DIMENSIONS],
        ],
    )
    write_csv(decoded_root / "pairwise_condition_matrix.csv", matrix_rows, ["condition_id", *CONDITIONS])

    print(f"Decoded scores: {rel(decoded_root / 'decoded_scores.csv')}")
    print(f"Condition summary: {rel(decoded_root / 'summary_by_condition.csv')}")
    print(f"Position balance: {rel(decoded_root / 'position_balance.csv')}")


def summarize_articles(score_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    groups: dict[tuple[str, str, str], list[dict[str, object]]] = defaultdict(list)
    for row in score_rows:
        key = (str(row["condition_id"]), str(row["replicate_id"]), str(row["nickname"]))
        groups[key].append(row)

    out: list[dict[str, object]] = []
    for (condition_id, replicate_id, nickname), rows in sorted(groups.items()):
        totals = [float(row["total_score"]) for row in rows]
        first = rows[0]
        item: dict[str, object] = {
            "condition_id": condition_id,
            "replicate_id": replicate_id,
            "nickname": nickname,
            "source_output_path": first["source_output_path"],
            "n_scores": len(rows),
            "mean_total": rounded(mean(totals)),
            "sd_total": rounded(sd(totals)),
            "mean_position": rounded(mean([float(row["position"]) for row in rows])),
        }
        for key, _ in DIMENSIONS:
            item[f"mean_{key}"] = rounded(mean([float(row[key]) for row in rows]))
        out.append(item)
    return out


def summarize_conditions(
    score_rows: list[dict[str, object]], article_rows: list[dict[str, object]]
) -> list[dict[str, object]]:
    score_groups: dict[str, list[dict[str, object]]] = defaultdict(list)
    article_groups: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in score_rows:
        score_groups[str(row["condition_id"])].append(row)
    for row in article_rows:
        article_groups[str(row["condition_id"])].append(row)

    out: list[dict[str, object]] = []
    for condition_id in CONDITIONS:
        scores = score_groups[condition_id]
        articles = article_groups[condition_id]
        totals = [float(row["total_score"]) for row in scores]
        article_totals = [float(row["mean_total"]) for row in articles]
        item: dict[str, object] = {
            "condition_id": condition_id,
            "n_articles": len(articles),
            "n_scores": len(scores),
            "mean_total": rounded(mean(totals)),
            "sd_total": rounded(sd(totals)),
            "mean_article_total": rounded(mean(article_totals)),
            "sd_article_total": rounded(sd(article_totals)),
        }
        for key, _ in DIMENSIONS:
            item[f"mean_{key}"] = rounded(mean([float(row[key]) for row in scores]))
        out.append(item)
    out.sort(key=lambda row: float(row["mean_article_total"]), reverse=True)
    return out


def summarize_pairwise(pair_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    wins: dict[tuple[str, str], float] = defaultdict(float)
    totals: dict[tuple[str, str], float] = defaultdict(float)
    for row in pair_rows:
        ca = str(row["condition_a"])
        cb = str(row["condition_b"])
        if ca == cb:
            continue
        preferred = str(row["preferred_condition"])
        totals[(ca, cb)] += 1
        totals[(cb, ca)] += 1
        if preferred == ca:
            wins[(ca, cb)] += 1
        elif preferred == cb:
            wins[(cb, ca)] += 1
        else:
            wins[(ca, cb)] += 0.5
            wins[(cb, ca)] += 0.5

    out: list[dict[str, object]] = []
    for ca in CONDITIONS:
        row: dict[str, object] = {"condition_id": ca}
        for cb in CONDITIONS:
            if ca == cb:
                row[cb] = ""
            else:
                denom = totals[(ca, cb)]
                row[cb] = rounded(wins[(ca, cb)] / denom) if denom else ""
        out.append(row)
    return out


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-id", required=True)
    args = parser.parse_args()
    decode_scores(args)


if __name__ == "__main__":
    main()

