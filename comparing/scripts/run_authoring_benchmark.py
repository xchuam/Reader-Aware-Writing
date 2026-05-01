#!/usr/bin/env python3
"""Generate and run isolated authoring jobs for the skill benchmark.

Each condition gets a fresh CODEX_HOME containing only the intended tested
user skill. Authoring happens in temporary work directories that receive only
the fixed prompt/dossier, so drafts cannot inspect prior repository outputs.
Completed article files and Codex logs are copied back into comparing/.
"""

from __future__ import annotations

import argparse
import concurrent.futures
import csv
import hashlib
import os
import shutil
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]


@dataclass(frozen=True)
class Condition:
    condition_id: str
    condition_name: str
    assigned_skill: str
    install_name: str | None
    source_path: Path | None
    source_label: str


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_tree(path: Path) -> str:
    digest = hashlib.sha256()
    for item in sorted(p for p in path.rglob("*") if p.is_file()):
        digest.update(item.relative_to(path).as_posix().encode("utf-8"))
        digest.update(b"\0")
        digest.update(sha256_file(item).encode("ascii"))
        digest.update(b"\0")
    return digest.hexdigest()


def git_head() -> str:
    proc = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=REPO_ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    return proc.stdout.strip() if proc.returncode == 0 else "unknown"


def build_conditions() -> list[Condition]:
    head = git_head()
    c1_source = REPO_ROOT / "skills" / "reader-aware-writing"
    c3_source = REPO_ROOT / "comparing" / "skill_snapshots" / "C3_smithery_scientific_writing"
    c4_source = REPO_ROOT / "comparing" / "skill_snapshots" / "C4_ovachiever_scientific_writing"
    c5_source = REPO_ROOT / "comparing" / "skill_snapshots" / "C5_academic_writing_standards"
    return [
        Condition(
            "C1",
            "Reader-aware writing",
            "reader-aware-writing",
            "reader-aware-writing",
            c1_source,
            f"skills/reader-aware-writing/ working tree; git_head {head}; tree_sha256 {sha256_tree(c1_source)}",
        ),
        Condition("C2", "No-skill baseline", "None", None, None, "no user writing skill installed"),
        Condition(
            "C3",
            "Scientific-writing representative",
            "scientific-writing",
            "scientific-writing",
            c3_source,
            f"comparing/skill_snapshots/C3_smithery_scientific_writing; tree_sha256 {sha256_tree(c3_source)}",
        ),
        Condition(
            "C4",
            "Scientific-writing alternative",
            "scientific-writing",
            "scientific-writing",
            c4_source,
            f"comparing/skill_snapshots/C4_ovachiever_scientific_writing; tree_sha256 {sha256_tree(c4_source)}",
        ),
        Condition(
            "C5",
            "Academic writing standards",
            "academic-writing-standards",
            "academic-writing-standards",
            c5_source,
            f"comparing/skill_snapshots/C5_academic_writing_standards; tree_sha256 {sha256_tree(c5_source)}",
        ),
    ]


def ensure_empty_dir(path: Path) -> None:
    if path.exists():
        shutil.rmtree(path)
    path.mkdir(parents=True, exist_ok=True)


def seed_codex_home(template: Path, target: Path) -> None:
    for name in ["auth.json", "config.toml", "models_cache.json", "installation_id"]:
        source = template / name
        if source.exists():
            shutil.copy2(source, target / name)


def install_condition_skill(condition: Condition, codex_home: Path) -> None:
    skills_root = codex_home / "skills"
    skills_root.mkdir(parents=True, exist_ok=True)
    (skills_root / ".system").mkdir(exist_ok=True)
    (skills_root / ".system" / ".codex-system-skills.marker").write_text("", encoding="utf-8")
    if condition.install_name is None:
        return
    assert condition.source_path is not None
    target = skills_root / condition.install_name
    if condition.source_path.is_dir():
        shutil.copytree(condition.source_path, target)
    else:
        target.mkdir(parents=True, exist_ok=True)
        shutil.copy2(condition.source_path, target / "SKILL.md")


def list_user_skills(codex_home: Path) -> list[str]:
    skills_root = codex_home / "skills"
    if not skills_root.exists():
        return []
    return sorted(
        path.name
        for path in skills_root.iterdir()
        if path.is_dir() and path.name != ".system"
    )


def write_home_manifest(
    *,
    run_id: str,
    conditions: list[Condition],
    codex_root: Path,
    prompt_root: Path,
) -> None:
    rows = []
    text_lines = [
        f"# Authoring CODEX_HOME Manifest: {run_id}",
        "",
        "| Condition | CODEX_HOME | Installed user skills | Skill source/snapshot |",
        "|---|---|---|---|",
    ]
    for condition in conditions:
        home = codex_root / condition.condition_id
        installed = ", ".join(list_user_skills(home)) or "none"
        rows.append(
            {
                "condition_id": condition.condition_id,
                "condition_name": condition.condition_name,
                "codex_home": str(home),
                "installed_user_skills": installed,
                "skill_source_snapshot": condition.source_label,
            }
        )
        text_lines.append(
            f"| {condition.condition_id} | `{home}` | {installed} | {condition.source_label} |"
        )
    (prompt_root / "HOMES.txt").write_text("\n".join(text_lines) + "\n", encoding="utf-8")
    with (prompt_root / "home_manifest.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            [
                "condition_id",
                "condition_name",
                "codex_home",
                "installed_user_skills",
                "skill_source_snapshot",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)


def generate_prompt(
    *,
    run_id: str,
    dossier_id: str,
    dossier_text: str,
    condition: Condition,
    replicate: str,
    generated_at_utc: str,
    model: str,
) -> str:
    dossier_for_prompt = dossier_text
    if dossier_for_prompt.startswith("---\n"):
        dossier_for_prompt = dossier_for_prompt[4:]
    return f"""Benchmark authoring task.

Condition Metadata
- Run ID: {run_id}
- Condition ID: {condition.condition_id}
- Condition name: {condition.condition_name}
- Assigned skill: {condition.assigned_skill}
- Skill source/snapshot: {condition.source_label}
- Replicate ID: {replicate}
- Output path: comparing/authoring_results/{run_id}/{condition.condition_id}_{replicate}.md
- Prompt version: writing-subagent-v2-minimal

Skill Rule
- If an assigned skill is provided, load and follow only that writing skill.
- If the assigned skill is None, do not load or imitate a writing skill.

Source and Tool Rules
- Use only the Fixed Dossier below.
- Do not use web search or external sources.
- Do not read evaluator prompts, scoring rubrics, prior outputs, or other
  agents.
- Do not add references unless the Fixed Dossier supplies them.

Task
Draft one scientific article from the Fixed Dossier.

Output
- Save the article to the exact output path above.
- Begin the saved file with this metadata block:

---
run_id: {run_id}
condition_id: {condition.condition_id}
condition_name: {condition.condition_name}
assigned_skill: {condition.assigned_skill}
skill_source_snapshot: {condition.source_label}
replicate_id: {replicate}
prompt_version: writing-subagent-v2-minimal
dossier_id: {dossier_id}
generated_at_utc: {generated_at_utc}
model: {model}
---

- After the metadata block, provide the article only.

Fixed Dossier
---
{dossier_for_prompt}
"""


def run_job(
    *,
    run_id: str,
    condition: Condition,
    replicate: str,
    prompt_path: Path,
    codex_home: Path,
    work_root: Path,
    output_root: Path,
    log_root: Path,
    model: str,
    reasoning_effort: str,
    dry_run: bool,
) -> str:
    job_id = f"{condition.condition_id}_{replicate}"
    workdir = work_root / job_id
    ensure_empty_dir(workdir)
    transcript_path = log_root / f"{job_id}.transcript.txt"
    final_path = log_root / f"{job_id}.final.txt"
    rel_output = Path("comparing") / "authoring_results" / run_id / f"{job_id}.md"
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
        str(workdir),
        "--output-last-message",
        str(final_path),
        "-",
    ]
    if dry_run:
        return f"DRY {job_id}: {' '.join(cmd)}"
    env = os.environ.copy()
    env["CODEX_HOME"] = str(codex_home)
    prompt_text = prompt_path.read_text(encoding="utf-8")
    with transcript_path.open("w", encoding="utf-8") as transcript:
        proc = subprocess.run(
            cmd,
            input=prompt_text,
            text=True,
            cwd=workdir,
            env=env,
            stdout=transcript,
            stderr=subprocess.STDOUT,
            check=False,
        )
    if proc.returncode != 0:
        raise RuntimeError(
            f"{job_id} failed with exit code {proc.returncode}; see {transcript_path}"
        )
    source = workdir / rel_output
    if not source.exists():
        raise RuntimeError(f"{job_id} did not write {source}")
    target = output_root / f"{job_id}.md"
    shutil.copy2(source, target)
    return f"OK {job_id}"


def validate_authoring_outputs(run_id: str, output_root: Path) -> None:
    expected = {f"C{c}_R{r}.md" for c in range(1, 6) for r in range(1, 4)}
    actual = {path.name for path in output_root.glob("C[1-5]_R[1-3].md")}
    missing = sorted(expected - actual)
    extra = sorted(actual - expected)
    if missing or extra:
        raise SystemExit(f"Authoring output mismatch; missing={missing}, extra={extra}")
    for path in output_root.glob("C[1-5]_R[1-3].md"):
        text = path.read_text(encoding="utf-8")
        if f"run_id: {run_id}" not in text[:1200]:
            raise SystemExit(f"Output frontmatter lacks run_id in {path}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--dossier", default="D002_caspase5c_wnt_noisy_notes.md")
    parser.add_argument("--dossier-id", default="D002")
    parser.add_argument("--model", default="gpt-5.5")
    parser.add_argument("--reasoning-effort", default="medium")
    parser.add_argument("--parallelism", type=int, default=3)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    run_id = args.run_id
    conditions = build_conditions()
    dossier_path = REPO_ROOT / "comparing" / "dossiers" / args.dossier
    dossier_text = dossier_path.read_text(encoding="utf-8").strip()
    prompt_root = REPO_ROOT / "comparing" / "prompts" / "generated" / run_id / "authoring"
    output_root = REPO_ROOT / "comparing" / "authoring_results" / run_id
    log_root = output_root / "codex_logs"
    work_root = Path(f"/tmp/authoring-benchmark-{run_id}").resolve()
    codex_root = Path(f"/home/vscode/.codex-benchmark/{run_id}")

    ensure_empty_dir(prompt_root)
    ensure_empty_dir(output_root)
    log_root.mkdir(parents=True, exist_ok=True)
    work_root.mkdir(parents=True, exist_ok=True)
    codex_root.mkdir(parents=True, exist_ok=True)

    previous_root = Path("/home/vscode/.codex-benchmark/run-2026-05-01-D002")
    for condition in conditions:
        home = codex_root / condition.condition_id
        ensure_empty_dir(home)
        seed_codex_home(previous_root / condition.condition_id, home)
        install_condition_skill(condition, home)
        installed = list_user_skills(home)
        expected = [] if condition.install_name is None else [condition.install_name]
        if installed != expected:
            raise SystemExit(
                f"{condition.condition_id} installed user skills {installed}; expected {expected}"
            )
    evaluator_home = codex_root / "E1"
    ensure_empty_dir(evaluator_home)
    seed_codex_home(previous_root / "E1", evaluator_home)
    (evaluator_home / "skills" / ".system").mkdir(parents=True, exist_ok=True)
    (evaluator_home / "skills" / ".system" / ".codex-system-skills.marker").write_text(
        "", encoding="utf-8"
    )
    if list_user_skills(evaluator_home):
        raise SystemExit("Evaluator template unexpectedly contains user skills")

    generated_at_utc = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    jobs: list[tuple[Condition, str, Path]] = []
    for condition in conditions:
        for replicate in ["R1", "R2", "R3"]:
            prompt = generate_prompt(
                run_id=run_id,
                dossier_id=args.dossier_id,
                dossier_text=dossier_text,
                condition=condition,
                replicate=replicate,
                generated_at_utc=generated_at_utc,
                model=args.model,
            )
            prompt_path = prompt_root / f"{condition.condition_id}_{replicate}.txt"
            prompt_path.write_text(prompt, encoding="utf-8")
            jobs.append((condition, replicate, prompt_path))

    write_home_manifest(run_id=run_id, conditions=conditions, codex_root=codex_root, prompt_root=prompt_root)
    print(f"Wrote authoring prompts to {prompt_root.relative_to(REPO_ROOT)}", flush=True)
    print(f"Wrote home manifest to {(prompt_root / 'home_manifest.csv').relative_to(REPO_ROOT)}", flush=True)
    print(f"Running {len(jobs)} authoring jobs with parallelism={args.parallelism}", flush=True)

    failures: list[str] = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.parallelism) as executor:
        future_map = {
            executor.submit(
                run_job,
                run_id=run_id,
                condition=condition,
                replicate=replicate,
                prompt_path=prompt_path,
                codex_home=codex_root / condition.condition_id,
                work_root=work_root,
                output_root=output_root,
                log_root=log_root,
                model=args.model,
                reasoning_effort=args.reasoning_effort,
                dry_run=args.dry_run,
            ): f"{condition.condition_id}_{replicate}"
            for condition, replicate, prompt_path in jobs
        }
        for future in concurrent.futures.as_completed(future_map):
            job_id = future_map[future]
            try:
                print(future.result(), flush=True)
            except Exception as exc:  # noqa: BLE001
                failures.append(f"{job_id}: {exc}")
                print(f"FAIL {job_id}: {exc}", flush=True)
    if failures:
        raise SystemExit("\n".join(failures))
    if not args.dry_run:
        validate_authoring_outputs(run_id, output_root)
    print(f"Completed authoring run {run_id}", flush=True)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit("Interrupted")
