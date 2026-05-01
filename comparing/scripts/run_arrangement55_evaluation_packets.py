#!/usr/bin/env python3
"""Run Arrangement5-5 evaluator packets in isolated work directories.

The evaluator prompt contains the fixed dossier and the five blinded articles,
so the evaluator does not need repository access. Running each packet from a
fresh temporary work directory prevents later packets from reading earlier
evaluation notes or TSVs, which would contaminate the position-balance check.
"""

from __future__ import annotations

import argparse
import concurrent.futures
import csv
import os
import shutil
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]


def read_manifest(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def ensure_empty_dir(path: Path) -> None:
    if path.exists():
        shutil.rmtree(path)
    path.mkdir(parents=True, exist_ok=True)


def seed_codex_home(template: Path, target: Path) -> None:
    """Copy auth/config into a fresh no-user-skill CODEX_HOME."""
    skills_dir = template / "skills"
    if skills_dir.exists():
        user_skill_dirs = [
            path.name
            for path in skills_dir.iterdir()
            if path.is_dir() and path.name != ".system"
        ]
        if user_skill_dirs:
            raise SystemExit(
                f"Refusing to seed evaluator home from {template}; "
                f"user skills present: {', '.join(sorted(user_skill_dirs))}"
            )
    for name in ["auth.json", "config.toml", "models_cache.json", "installation_id"]:
        source = template / name
        if source.exists():
            shutil.copy2(source, target / name)


def run_packet(
    *,
    row: dict[str, str],
    run_id: str,
    model: str,
    reasoning_effort: str,
    work_root: Path,
    codex_home_root: Path,
    codex_home_template: Path,
    log_root: Path,
    dry_run: bool,
) -> None:
    evaluator_id = row["evaluator_id"]
    packet_id = row["packet_id"]
    prompt_path = REPO_ROOT / row["prompt_path"]
    if not prompt_path.exists():
        raise SystemExit(f"Missing prompt: {prompt_path}")

    packet_workdir = work_root / packet_id
    ensure_empty_dir(packet_workdir)
    codex_home = codex_home_root / packet_id
    ensure_empty_dir(codex_home)
    seed_codex_home(codex_home_template, codex_home)
    log_root.mkdir(parents=True, exist_ok=True)

    transcript_path = log_root / f"{packet_id}.transcript.txt"
    final_path = log_root / f"{packet_id}.final.txt"
    cmd = [
        "codex",
        "exec",
        "--ephemeral",
        "--ignore-user-config",
        "--sandbox",
        "danger-full-access",
        "--skip-git-repo-check",
        "-m",
        model,
        "-c",
        f"model_reasoning_effort={reasoning_effort}",
        "--cd",
        str(packet_workdir),
        "--output-last-message",
        str(final_path),
        "-",
    ]
    print(f"Running {evaluator_id} {packet_id}", flush=True)
    if dry_run:
        print(" ".join(cmd), flush=True)
        return

    env = os.environ.copy()
    env["CODEX_HOME"] = str(codex_home)
    prompt_text = prompt_path.read_text(encoding="utf-8")
    with transcript_path.open("w", encoding="utf-8") as transcript:
        proc = subprocess.run(
            cmd,
            input=prompt_text,
            text=True,
            cwd=packet_workdir,
            env=env,
            stdout=transcript,
            stderr=subprocess.STDOUT,
            check=False,
        )
    if proc.returncode != 0:
        raise SystemExit(
            f"Packet {packet_id} failed with exit code {proc.returncode}; "
            f"see {transcript_path}"
        )

    for key in ["scores_path", "pairwise_path"]:
        rel_path = Path(row[key])
        source = packet_workdir / rel_path
        target = REPO_ROOT / rel_path
        if not source.exists():
            raise SystemExit(f"Packet {packet_id} did not write {source}")
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
    md_rel = Path(row["scores_path"]).with_name(f"{packet_id}.md")
    md_source = packet_workdir / md_rel
    md_target = REPO_ROOT / md_rel
    if not md_source.exists():
        raise SystemExit(f"Packet {packet_id} did not write {md_source}")
    shutil.copy2(md_source, md_target)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--model", default="gpt-5.5")
    parser.add_argument("--reasoning-effort", default="medium")
    parser.add_argument("--evaluators", nargs="*", default=None)
    parser.add_argument("--packets", nargs="*", default=None)
    parser.add_argument("--parallelism", type=int, default=1)
    parser.add_argument(
        "--work-root",
        default=None,
        help="Temporary parent directory for isolated packet workspaces.",
    )
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    run_id = args.run_id
    result_root = REPO_ROOT / "comparing" / "evaluation_results" / run_id / "arrangement55"
    manifest_path = result_root / "prompt_manifest.csv"
    rows = read_manifest(manifest_path)
    if args.evaluators:
        rows = [row for row in rows if row["evaluator_id"] in set(args.evaluators)]
    if args.packets:
        rows = [row for row in rows if row["packet_id"] in set(args.packets)]
    if not rows:
        raise SystemExit("No packets selected")

    work_root = Path(args.work_root or f"/tmp/arrangement55-eval-{run_id}").resolve()
    codex_home_root = Path(f"/home/vscode/.codex-benchmark/{run_id}/E1_isolated_packets")
    log_root = result_root / "codex_logs_isolated"
    work_root.mkdir(parents=True, exist_ok=True)
    codex_home_root.mkdir(parents=True, exist_ok=True)

    failures: list[str] = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.parallelism) as executor:
        future_map = {
            executor.submit(
                run_packet,
                row=row,
                run_id=run_id,
                model=args.model,
                reasoning_effort=args.reasoning_effort,
                work_root=work_root,
                codex_home_root=codex_home_root,
                codex_home_template=Path(
                    f"/home/vscode/.codex-benchmark/{run_id}/{row['evaluator_id']}"
                ),
                log_root=log_root,
                dry_run=args.dry_run,
            ): row["packet_id"]
            for row in rows
        }
        for future in concurrent.futures.as_completed(future_map):
            packet = future_map[future]
            try:
                future.result()
            except Exception as exc:  # noqa: BLE001
                failures.append(f"{packet}: {exc}")
                print(f"FAIL {packet}: {exc}", flush=True)
            else:
                print(f"OK {packet}", flush=True)
    if failures:
        raise SystemExit("\n".join(failures))
    print(f"Completed {len(rows)} isolated packet runs", flush=True)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit("Interrupted")
