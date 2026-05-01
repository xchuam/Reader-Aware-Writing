#!/usr/bin/env python3
"""Prepare position-balanced Arrangement5-5 evaluation packets.

This script does two things that should stay out of manual handling:

1. Replace condition-coded article identities such as C1/R1 with neutral
   random nicknames before evaluator prompts are created.
2. Generate a deterministic 5x5 Latin-square order for each replicate so every
   article appears once in each presentation position.

The private maps are required for decoding evaluator scores after scoring.
They must not be included in evaluator prompts.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import random
import re
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]

CONDITIONS = ["C1", "C2", "C3", "C4", "C5"]
REPLICATES = ["R1", "R2", "R3"]

NICKNAMES = [
    "Amber",
    "Beacon",
    "Cedar",
    "Dawn",
    "Ember",
    "Fjord",
    "Granite",
    "Harbor",
    "Ivory",
    "Juniper",
    "Keystone",
    "Lantern",
    "Meadow",
    "Nimbus",
    "Opal",
    "Prairie",
    "Quartz",
    "Ridge",
    "Summit",
    "Tundra",
    "Umber",
    "Vale",
    "Willow",
    "Yonder",
    "Zephyr",
]

DIMENSIONS = [
    ("scientific_fidelity", 20),
    ("article_structure", 15),
    ("reader_orientation", 15),
    ("cohesion_coherence", 20),
    ("evidence_uncertainty", 15),
    ("style_readability", 10),
    ("constraint_following", 5),
]

LEAK_PATTERNS = [
    r"\bC[1-5]_R[1-3]\b",
    r"\bC[1-5]\b",
    r"\bArticle_[A-Z]\b",
    r"\bcondition_id\b",
    r"\bassigned_skill\b",
    r"\bskill_source_snapshot\b",
    r"reader-aware-writing",
    r"reader-aware writing",
    r"no-skill baseline",
    r"scientific-writing",
    r"academic-writing-standards",
    r"sci-writing",
]


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


def source_path(run_id: str, condition_id: str, replicate_id: str) -> Path:
    return (
        REPO_ROOT
        / "comparing"
        / "authoring_results"
        / run_id
        / f"{condition_id}_{replicate_id}.md"
    )


def scrub_article_text(text: str, condition_id: str, replicate_id: str, nickname: str) -> str:
    """Remove exact benchmark identifiers without altering scientific terms."""
    source_stem = f"{condition_id}_{replicate_id}"
    text = re.sub(rf"\b{re.escape(source_stem)}\b", nickname, text)
    text = re.sub(rf"\b{re.escape(condition_id)}\b", nickname, text)
    text = re.sub(rf"\b{re.escape(replicate_id)}\b", nickname, text)
    return text.strip()


def leakage_hits(text: str) -> list[str]:
    hits: list[str] = []
    for pattern in LEAK_PATTERNS:
        if re.search(pattern, text, flags=re.IGNORECASE):
            hits.append(pattern)
    return hits


def packet_id(run_id: str, evaluator_id: str, replicate_id: str, arrangement_id: str) -> str:
    raw = f"{run_id}|{evaluator_id}|{replicate_id}|{arrangement_id}"
    digest = hashlib.sha1(raw.encode("utf-8")).hexdigest()[:10]
    return f"packet_{digest}"


def latin_square(items: list[dict[str, str]]) -> list[list[dict[str, str]]]:
    if len(items) != 5:
        raise ValueError("Arrangement5-5 requires exactly five items")
    return [items[offset:] + items[:offset] for offset in range(5)]


def has_alphabetic_order_cue(nicknames: list[str]) -> bool:
    lowered = [name.lower() for name in nicknames]
    return lowered == sorted(lowered) or lowered == sorted(lowered, reverse=True)


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def make_prompt(
    *,
    run_id: str,
    evaluator_id: str,
    packet: str,
    dossier_text: str,
    article_rows: list[dict[str, str]],
    article_texts: dict[str, str],
    md_path: Path,
    scores_path: Path,
    pairwise_path: Path,
) -> str:
    md_prompt_path = rel(md_path)
    scores_prompt_path = rel(scores_path)
    pairwise_prompt_path = rel(pairwise_path)
    article_packet = []
    for row in article_rows:
        nickname = row["nickname"]
        article_packet.append(f"### {nickname}\n\n{article_texts[nickname]}")

    dim_lines = "\n".join(
        f"- {name}: {points} points" for name, points in DIMENSIONS
    )
    return f"""You are an independent blinded evaluator in a benchmark of scientific writing quality.

Evaluator Metadata
- Run ID: {run_id}
- Evaluator ID: {evaluator_id}
- Packet ID: {packet}
- Prompt version: evaluation-arrangement55-v1
- Markdown output path: {md_prompt_path}
- Scores TSV path: {scores_prompt_path}
- Pairwise TSV path: {pairwise_prompt_path}

Blinding Rules
- Article labels are neutral nicknames. Do not infer source, skill, model, condition, or replicate from them.
- Evaluate only the fixed dossier and the five blinded articles in this packet.
- Ignore presentation position as much as possible; earlier or later placement is not meaningful.
- Do not use web search or external sources.
- Do not reward facts absent from the dossier.
- Penalize invented or unsupported claims.

Scoring Dimensions
{dim_lines}

Required Output Files
1. Save a Markdown evaluation note to `{md_prompt_path}`.
2. Save a tab-separated score table to `{scores_prompt_path}` with exactly this header:
   evaluator_id\tpacket_id\tnickname\tscientific_fidelity\tarticle_structure\treader_orientation\tcohesion_coherence\tevidence_uncertainty\tstyle_readability\tconstraint_following\ttotal_score\trank\tone_sentence_justification
3. Save a tab-separated pairwise table to `{pairwise_prompt_path}` with exactly this header:
   evaluator_id\tpacket_id\tnickname_a\tnickname_b\tpreferred_nickname\treason

Score Table Rules
- Include exactly one score row for each of the five article nicknames.
- Scores must be integers, and total_score must equal the seven dimension scores.
- Rank 1 is strongest within this packet.
- Do not include tabs inside justifications.

Pairwise Table Rules
- Include every unordered pair among the five article nicknames exactly once: 10 rows.
- preferred_nickname must be one article nickname or Tie.
- Do not include tabs inside reasons.

Fixed Dossier
---
{dossier_text}
---

Blinded Articles
---
{chr(10).join(article_packet)}
---
"""


def prepare(args: argparse.Namespace) -> None:
    run_id = args.run_id
    source_dir = REPO_ROOT / "comparing" / "authoring_results" / run_id
    if not source_dir.exists():
        raise SystemExit(f"Missing authoring result directory: {source_dir}")

    dossier_path = REPO_ROOT / "comparing" / "dossiers" / args.dossier
    dossier_text = dossier_path.read_text(encoding="utf-8").strip()

    blind_root = REPO_ROOT / "comparing" / "blinded_articles" / run_id / "arrangement55"
    article_dir = blind_root / "articles"
    prompt_root = REPO_ROOT / "comparing" / "prompts" / "generated" / run_id / "evaluation_arrangement55"
    result_root = REPO_ROOT / "comparing" / "evaluation_results" / run_id / "arrangement55"
    raw_root = result_root / "raw"
    article_dir.mkdir(parents=True, exist_ok=True)
    prompt_root.mkdir(parents=True, exist_ok=True)
    raw_root.mkdir(parents=True, exist_ok=True)

    rng = random.Random(args.seed)
    nicknames = NICKNAMES[:]
    rng.shuffle(nicknames)
    nicknames = nicknames[: len(CONDITIONS) * len(REPLICATES)]

    nickname_rows: list[dict[str, object]] = []
    article_texts: dict[str, str] = {}
    by_replicate: dict[str, list[dict[str, str]]] = {rep: [] for rep in REPLICATES}
    nick_iter = iter(nicknames)

    for replicate_id in REPLICATES:
        for condition_id in CONDITIONS:
            path = source_path(run_id, condition_id, replicate_id)
            if not path.exists():
                raise SystemExit(f"Missing expected article: {path}")
            nickname = next(nick_iter)
            raw_text = strip_frontmatter(path.read_text(encoding="utf-8"))
            article_text = scrub_article_text(raw_text, condition_id, replicate_id, nickname)
            hits = leakage_hits(article_text)
            if hits:
                raise SystemExit(
                    f"Leakage check failed for {path}: matched {', '.join(hits)}"
                )
            (article_dir / f"{nickname}.md").write_text(article_text + "\n", encoding="utf-8")
            article_texts[nickname] = article_text
            row = {
                "nickname": nickname,
                "source_output_path": rel(path),
                "condition_id": condition_id,
                "replicate_id": replicate_id,
                "word_count": word_count(article_text),
            }
            nickname_rows.append(row)
            by_replicate[replicate_id].append({k: str(v) for k, v in row.items()})

    write_csv(
        blind_root / "nickname_map_private.csv",
        nickname_rows,
        ["nickname", "source_output_path", "condition_id", "replicate_id", "word_count"],
    )

    plan_rows: list[dict[str, object]] = []
    prompt_rows: list[dict[str, object]] = []
    for evaluator_id in args.evaluators:
        for replicate_id in REPLICATES:
            replicate_articles = by_replicate[replicate_id]
            for arrangement_index, article_rows in enumerate(latin_square(replicate_articles), start=1):
                arrangement_id = f"A{arrangement_index}"
                packet = packet_id(run_id, evaluator_id, replicate_id, arrangement_id)
                nickname_order = [row["nickname"] for row in article_rows]
                if has_alphabetic_order_cue(nickname_order):
                    raise SystemExit(
                        "Nickname order cue detected in "
                        f"{evaluator_id} {replicate_id} {arrangement_id}; choose a different seed"
                    )
                md_path = raw_root / f"{packet}.md"
                scores_path = raw_root / f"{packet}_scores.tsv"
                pairwise_path = raw_root / f"{packet}_pairwise.tsv"
                prompt_path = prompt_root / evaluator_id / f"{packet}.txt"
                prompt_path.parent.mkdir(parents=True, exist_ok=True)
                prompt = make_prompt(
                    run_id=run_id,
                    evaluator_id=evaluator_id,
                    packet=packet,
                    dossier_text=dossier_text,
                    article_rows=article_rows,
                    article_texts=article_texts,
                    md_path=md_path,
                    scores_path=scores_path,
                    pairwise_path=pairwise_path,
                )
                hits = leakage_hits(prompt)
                if hits:
                    raise SystemExit(
                        f"Leakage check failed for prompt {prompt_path}: matched {', '.join(hits)}"
                    )
                prompt_path.write_text(prompt, encoding="utf-8")
                prompt_rows.append(
                    {
                        "evaluator_id": evaluator_id,
                        "packet_id": packet,
                        "prompt_path": rel(prompt_path),
                        "scores_path": rel(scores_path),
                        "pairwise_path": rel(pairwise_path),
                    }
                )
                for position, row in enumerate(article_rows, start=1):
                    plan_rows.append(
                        {
                            "evaluator_id": evaluator_id,
                            "packet_id": packet,
                            "replicate_id": replicate_id,
                            "arrangement_id": arrangement_id,
                            "position": position,
                            "nickname": row["nickname"],
                            "condition_id": row["condition_id"],
                            "source_output_path": row["source_output_path"],
                            "word_count": row["word_count"],
                        }
                    )

    write_csv(
        result_root / "arrangement_plan_private.csv",
        plan_rows,
        [
            "evaluator_id",
            "packet_id",
            "replicate_id",
            "arrangement_id",
            "position",
            "nickname",
            "condition_id",
            "source_output_path",
            "word_count",
        ],
    )
    write_csv(
        result_root / "prompt_manifest.csv",
        prompt_rows,
        ["evaluator_id", "packet_id", "prompt_path", "scores_path", "pairwise_path"],
    )

    print(f"Wrote nickname map: {rel(blind_root / 'nickname_map_private.csv')}")
    print(f"Wrote arrangement plan: {rel(result_root / 'arrangement_plan_private.csv')}")
    print(f"Wrote {len(prompt_rows)} evaluator prompts under {rel(prompt_root)}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--dossier", default="D002_caspase5c_wnt_noisy_notes.md")
    parser.add_argument("--evaluators", nargs="+", default=["E1", "E2", "E3"])
    parser.add_argument("--seed", default="arrangement55-neutral-nicknames-v1")
    args = parser.parse_args()
    prepare(args)


if __name__ == "__main__":
    main()
