# Skill Registry

Registry created: `2026-05-01T09:27:08Z`

Use this file to record the exact authoring conditions used in each benchmark
run. If an external skill is downloaded or installed later, add the exact
download time, commit SHA if available, and installation command before running
the authoring subagents.

## Version Policy

- Prefer immutable commit SHAs over floating `main` or `HEAD` references.
- If a commit SHA is unavailable, record the UTC download/access time and the
  source URL used.
- Keep only one representative of near-duplicate skill forks unless the
  benchmark explicitly tests fork drift.
- Do not update a skill during a benchmark run.

## Authoring Conditions

| Condition ID | Condition Name | Skill Name | Source / Link | Version or Snapshot | Rationale |
|---|---|---|---|---|---|
| C1 | Local reader-aware skill | `reader-aware-writing` | `skills/reader-aware-writing/` | Repo commit `97c06ad26991c68060a4094b6fbd63cb5ed4a671`; registry timestamp `2026-05-01T09:27:08Z` | Focal skill. Tests reader modeling, cohesion, coherence, paragraph logic, and scientific trust. |
| C2 | No-skill baseline | None | N/A | N/A | Control condition for same model without a writing skill. |
| C3 | Public scientific-writing representative | `scientific-writing` | https://skills.sh/smithery/ai/scientific-writing | Snapshot `comparing/skill_snapshots/C3_smithery_scientific_writing/`; accessed `2026-05-01T09:52:19Z`; SHA-256 `0bfe023703f47944ae8e66e54fcb067775142c256ded57cbbf196d68744d236d` | Popular IMRAD-style scientific manuscript skill emphasizing citations, reporting guidelines, figures/tables, and full-paragraph prose. Listed GitHub repo was not reachable, so the rendered skills.sh `SKILL.md` was used. |
| C4 | Public scientific-writing alternative | `scientific-writing` from `ovachiever/droid-tings` | https://agent-skills.md/skills/ovachiever/droid-tings/scientific-writing | Snapshot `comparing/skill_snapshots/C4_ovachiever_scientific_writing/`; commit `7acd12a7547ded8f801615e69c3b881a584ce323`; accessed `2026-05-01T09:52:19Z` | Direct manuscript-writing comparator with IMRAD, reporting-guideline, citation, figure/table, and field-terminology guidance. |
| C5 | Academic style standards | `academic-writing-standards` | https://skills.sh/seabbs/claude-code-config/academic-writing-standards | Snapshot `comparing/skill_snapshots/C5_academic_writing_standards/`; source repo `seabbs/skills` commit `006088dd99868765db0847d068b5089c192086b5`; accessed `2026-05-01T09:52:19Z` | Contrast condition focused on clarity, precision, active voice, citation hygiene, and academic style discipline. |

## Per-Run Snapshot Table

Fill one row per condition before each benchmark run.

| Run ID | Condition ID | Model | Skill Source Used | Commit / Version | Downloaded or Accessed UTC | Installation Command | Notes |
|---|---|---|---|---|---|---|---|
| `run-2026-05-01-D001` | C1 | `gpt-5.5` | `skills/reader-aware-writing/` | `97c06ad26991c68060a4094b6fbd63cb5ed4a671` | `2026-05-01T09:27:08Z` | Copied into isolated `CODEX_HOME` at `/home/vscode/.codex-benchmark/run-2026-05-01-D001/C1/skills/reader-aware-writing/` | Only user writing skill installed for C1. |
| `run-2026-05-01-D001` | C2 | `gpt-5.5` | N/A | N/A | N/A | Isolated `CODEX_HOME` with no user skill | No-skill baseline. |
| `run-2026-05-01-D001` | C3 | `gpt-5.5` | `comparing/skill_snapshots/C3_smithery_scientific_writing/` | skills.sh rendered snapshot; SHA-256 `0bfe023703f47944ae8e66e54fcb067775142c256ded57cbbf196d68744d236d` | `2026-05-01T09:52:19Z` | Rendered `SKILL.md` extraction copied into isolated `CODEX_HOME` | Listed GitHub repo was not reachable by `git ls-remote`; adapter frontmatter added only inside the isolated run home. |
| `run-2026-05-01-D001` | C4 | `gpt-5.5` | `comparing/skill_snapshots/C4_ovachiever_scientific_writing/` | `7acd12a7547ded8f801615e69c3b881a584ce323` | `2026-05-01T09:52:19Z` | `git clone --depth 1 https://github.com/ovachiever/droid-tings`; snapshot copied into isolated `CODEX_HOME` | Only user writing skill installed for C4. |
| `run-2026-05-01-D001` | C5 | `gpt-5.5` | `comparing/skill_snapshots/C5_academic_writing_standards/` | `006088dd99868765db0847d068b5089c192086b5` | `2026-05-01T09:52:19Z` | `git clone --depth 1 https://github.com/seabbs/skills`; snapshot copied into isolated `CODEX_HOME` | Source page points to `seabbs/claude-code-config`; actual skill is in `seabbs/skills`. |
| `run-2026-05-01-D002` | C1 | `gpt-5.5` | `skills/reader-aware-writing/` | `97c06ad26991c68060a4094b6fbd63cb5ed4a671` | `2026-05-01T09:27:08Z` | Copied into isolated `CODEX_HOME` at `/home/vscode/.codex-benchmark/run-2026-05-01-D002/C1/skills/reader-aware-writing/` | Only user writing skill installed for C1. |
| `run-2026-05-01-D002` | C2 | `gpt-5.5` | N/A | N/A | N/A | Isolated `CODEX_HOME` with no user skill | No-skill baseline. |
| `run-2026-05-01-D002` | C3 | `gpt-5.5` | `comparing/skill_snapshots/C3_smithery_scientific_writing/` | skills.sh rendered snapshot; SHA-256 `0bfe023703f47944ae8e66e54fcb067775142c256ded57cbbf196d68744d236d` | `2026-05-01T09:52:19Z` | Rendered `SKILL.md` extraction copied into isolated `CODEX_HOME` | Adapter frontmatter added only inside the isolated run home. |
| `run-2026-05-01-D002` | C4 | `gpt-5.5` | `comparing/skill_snapshots/C4_ovachiever_scientific_writing/` | `7acd12a7547ded8f801615e69c3b881a584ce323` | `2026-05-01T09:52:19Z` | Snapshot copied into isolated `CODEX_HOME` | Only user writing skill installed for C4. |
| `run-2026-05-01-D002` | C5 | `gpt-5.5` | `comparing/skill_snapshots/C5_academic_writing_standards/` | `006088dd99868765db0847d068b5089c192086b5` | `2026-05-01T09:52:19Z` | Snapshot copied into isolated `CODEX_HOME` | Only user writing skill installed for C5. |
| `run-2026-05-01-D003` | C1 | `gpt-5.5` | `skills/reader-aware-writing/` | Working tree at git head `97c06ad26991c68060a4094b6fbd63cb5ed4a671`; skill tree SHA-256 `b3ade6b38356ddf5fe16b139a8ee13d371e1017e789e2aa39feac5031d352f65` | `2026-05-01T12:17:30Z` | Copied into isolated `CODEX_HOME` at `/home/vscode/.codex-benchmark/run-2026-05-01-D003/C1/skills/reader-aware-writing/` | Revised skill with reader contract, paragraph-question path, claim ladder, paragraph gates, and benchmark audit guidance. |
| `run-2026-05-01-D003` | C2 | `gpt-5.5` | N/A | N/A | N/A | Isolated `CODEX_HOME` with no user skill | No-skill baseline. |
| `run-2026-05-01-D003` | C3 | `gpt-5.5` | `comparing/skill_snapshots/C3_smithery_scientific_writing/` | tree SHA-256 `cf4c35607ffc8f5e1c57b447f201b941ce1597fb26ff69aa36821dbab1726332` | `2026-05-01T09:52:19Z` | Snapshot copied into isolated `CODEX_HOME` | Only user writing skill installed for C3. |
| `run-2026-05-01-D003` | C4 | `gpt-5.5` | `comparing/skill_snapshots/C4_ovachiever_scientific_writing/` | tree SHA-256 `faac0c616485479b7b0c9698541b17f6e82c0d6f10842849f7c1e5113d095b7a` | `2026-05-01T09:52:19Z` | Snapshot copied into isolated `CODEX_HOME` | Only user writing skill installed for C4. |
| `run-2026-05-01-D003` | C5 | `gpt-5.5` | `comparing/skill_snapshots/C5_academic_writing_standards/` | tree SHA-256 `0b92cea6eef9b58fa57ee01f5cc72605f43e55d1404c2b95eadcdd38b17728f7` | `2026-05-01T09:52:19Z` | Snapshot copied into isolated `CODEX_HOME` | Only user writing skill installed for C5. |
