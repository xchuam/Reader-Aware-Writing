# Evaluation Log

This file is the running audit trail for benchmark execution. Append to it
rather than replacing previous entries.

## Pre-Run Dossier Preparation

| UTC | Item | Decision / Impact |
|---|---|---|
| 2026-05-01T09:44:19Z | Created `D001_caspase5c_wnt_intestinal_homeostasis.md` from source PDF `comparing/blinded_articles/s41586-026-10343-8.pdf`. | Dossier will serve as the fixed source packet for authoring subagents. The source article is Jia et al., Nature 652, 1362-1374 (2026), DOI `10.1038/s41586-026-10343-8`. |
| 2026-05-01T10:42:51Z | Created `D002_caspase5c_wnt_noisy_notes.md` and `writing_subagent_prompt_minimal.md`. | Next benchmark run can use a deliberately less scaffolded, noisy source packet and a prompt that leaves writing strategy to the assigned skill. |
| 2026-05-01T10:42:51Z | Added Arrangement5-5 evaluation scripts. | `prepare_arrangement55_evaluation.py` creates neutral nickname maps and position-balanced evaluator prompts; `decode_arrangement55_scores.py` validates evaluator TSVs, checks leakage patterns and position balance, decodes nicknames back to condition IDs, and calculates means. |

## Completed Run: `run-2026-05-01-D001`

### Run Metadata

| Field | Value |
|---|---|
| Run ID | `run-2026-05-01-D001` |
| Dossier ID | `D001` |
| Dossier path | `comparing/dossiers/D001_caspase5c_wnt_intestinal_homeostasis.md` |
| Source PDF | `comparing/blinded_articles/s41586-026-10343-8.pdf` |
| Protocol version | `evaluation-protocol-v1` |
| Writing prompt version | `writing-subagent-v1`; generated prompts in `comparing/prompts/generated/run-2026-05-01-D001/authoring/` |
| Evaluation prompt version | `evaluation-subagent-v2-tsv`; generated prompts in `comparing/prompts/generated/run-2026-05-01-D001/evaluation/` |
| Started UTC | `2026-05-01T09:52:19Z` |
| Authoring completed UTC | `2026-05-01T10:15:40Z` |
| Evaluation completed UTC | `2026-05-01T10:18:12Z` |
| Aggregation/report completed UTC | `2026-05-01T10:18:57Z` |
| Authoring model | `gpt-5.5` |
| Evaluation model | `gpt-5.5` |
| Execution settings | `codex exec --ephemeral --ignore-user-config --sandbox danger-full-access -a never` |
| Web access allowed to authoring/evaluation submodels | false |

### Isolation Check

| Unit | Isolated `CODEX_HOME` | User skill installed |
|---|---|---|
| C1 authoring | `/home/vscode/.codex-benchmark/run-2026-05-01-D001/C1` | `reader-aware-writing` only |
| C2 authoring | `/home/vscode/.codex-benchmark/run-2026-05-01-D001/C2` | none |
| C3 authoring | `/home/vscode/.codex-benchmark/run-2026-05-01-D001/C3` | `scientific-writing` only |
| C4 authoring | `/home/vscode/.codex-benchmark/run-2026-05-01-D001/C4` | `scientific-writing` only |
| C5 authoring | `/home/vscode/.codex-benchmark/run-2026-05-01-D001/C5` | `academic-writing-standards` only |
| E1-E3 evaluation | `/home/vscode/.codex-benchmark/run-2026-05-01-D001/E1` through `E3` | none |

System `.system` skills may be auto-populated by the Codex CLI, but no extra
user writing skill was installed in any authoring or evaluation home.

### Skill Snapshots

| Condition ID | Skill Source Used | Commit / Version | Downloaded or Accessed UTC | Notes |
|---|---|---|---|---|
| C1 | `skills/reader-aware-writing/` | Repo commit `97c06ad26991c68060a4094b6fbd63cb5ed4a671` | `2026-05-01T09:27:08Z` | Focal local skill. |
| C2 | N/A | N/A | N/A | No-skill baseline. |
| C3 | `comparing/skill_snapshots/C3_smithery_scientific_writing/` | skills.sh rendered snapshot; SHA-256 `0bfe023703f47944ae8e66e54fcb067775142c256ded57cbbf196d68744d236d` | `2026-05-01T09:52:19Z` | Listed GitHub repo was not reachable by `git ls-remote`; rendered `SKILL.md` was used. |
| C4 | `comparing/skill_snapshots/C4_ovachiever_scientific_writing/` | `7acd12a7547ded8f801615e69c3b881a584ce323` | `2026-05-01T09:52:19Z` | Snapshot from `ovachiever/droid-tings`, path `skills/scientific-writing/`. |
| C5 | `comparing/skill_snapshots/C5_academic_writing_standards/` | `006088dd99868765db0847d068b5089c192086b5` | `2026-05-01T09:52:19Z` | Snapshot from `seabbs/skills`, path `plugins/research-academic/skills/academic-writing-standards/`. |

### Authoring Jobs

All authoring outputs are stored under
`comparing/authoring_results/run-2026-05-01-D001/`. Final Codex summaries are
stored under `comparing/authoring_results/run-2026-05-01-D001/codex_logs/`.

| Condition ID | Replicate ID | Output Path | Completed UTC | Word Count | Status |
|---|---|---|---|---:|---|
| C1 | R1 | `C1_R1.md` | `2026-05-01T10:01:31Z` | 1802 | completed |
| C1 | R2 | `C1_R2.md` | `2026-05-01T10:10:53Z` | 1804 | completed |
| C1 | R3 | `C1_R3.md` | `2026-05-01T10:14:11Z` | 1794 | completed |
| C2 | R1 | `C2_R1.md` | `2026-05-01T10:01:31Z` | 1810 | completed |
| C2 | R2 | `C2_R2.md` | `2026-05-01T10:07:54Z` | 1791 | completed |
| C2 | R3 | `C2_R3.md` | `2026-05-01T10:15:36Z` | 1813 | completed |
| C3 | R1 | `C3_R1.md` | `2026-05-01T10:01:31Z` | 1800 | completed |
| C3 | R2 | `C3_R2.md` | `2026-05-01T10:07:14Z` | 1811 | completed |
| C3 | R3 | `C3_R3.md` | `2026-05-01T10:14:10Z` | 1711 | completed |
| C4 | R1 | `C4_R1.md` | `2026-05-01T10:01:31Z` | 1782 | completed |
| C4 | R2 | `C4_R2.md` | `2026-05-01T10:10:02Z` | 1813 | completed |
| C4 | R3 | `C4_R3.md` | `2026-05-01T10:14:26Z` | 1706 | completed |
| C5 | R1 | `C5_R1.md` | `2026-05-01T10:01:31Z` | 1779 | completed |
| C5 | R2 | `C5_R2.md` | `2026-05-01T10:06:00Z` | 1734 | completed |
| C5 | R3 | `C5_R3.md` | `2026-05-01T10:15:40Z` | 1810 | completed |

### Private Blinding Map

Evaluator submodels received only blinded article IDs and never received this
map.

| Blinded Article ID | Source Output Path | Condition ID | Replicate ID | Word Count |
|---|---|---|---|---:|
| Article_A | `comparing/authoring_results/run-2026-05-01-D001/C5_R2.md` | C5 | R2 | 1734 |
| Article_B | `comparing/authoring_results/run-2026-05-01-D001/C3_R1.md` | C3 | R1 | 1800 |
| Article_C | `comparing/authoring_results/run-2026-05-01-D001/C1_R3.md` | C1 | R3 | 1794 |
| Article_D | `comparing/authoring_results/run-2026-05-01-D001/C5_R3.md` | C5 | R3 | 1810 |
| Article_E | `comparing/authoring_results/run-2026-05-01-D001/C3_R3.md` | C3 | R3 | 1711 |
| Article_F | `comparing/authoring_results/run-2026-05-01-D001/C2_R2.md` | C2 | R2 | 1791 |
| Article_G | `comparing/authoring_results/run-2026-05-01-D001/C4_R2.md` | C4 | R2 | 1813 |
| Article_H | `comparing/authoring_results/run-2026-05-01-D001/C1_R2.md` | C1 | R2 | 1804 |
| Article_I | `comparing/authoring_results/run-2026-05-01-D001/C5_R1.md` | C5 | R1 | 1779 |
| Article_J | `comparing/authoring_results/run-2026-05-01-D001/C2_R3.md` | C2 | R3 | 1813 |
| Article_K | `comparing/authoring_results/run-2026-05-01-D001/C4_R3.md` | C4 | R3 | 1706 |
| Article_L | `comparing/authoring_results/run-2026-05-01-D001/C1_R1.md` | C1 | R1 | 1802 |
| Article_M | `comparing/authoring_results/run-2026-05-01-D001/C3_R2.md` | C3 | R2 | 1811 |
| Article_N | `comparing/authoring_results/run-2026-05-01-D001/C4_R1.md` | C4 | R1 | 1782 |
| Article_O | `comparing/authoring_results/run-2026-05-01-D001/C2_R1.md` | C2 | R1 | 1810 |

### Evaluation Jobs

All evaluator outputs are stored under
`comparing/evaluation_results/run-2026-05-01-D001/`. Final Codex summaries are
stored under `comparing/evaluation_results/run-2026-05-01-D001/codex_logs/`.

| Evaluator ID | Prompt Path | Score Output | Pairwise Output | Completed UTC | Validation Status |
|---|---|---|---|---|---|
| E1 | `comparing/prompts/generated/run-2026-05-01-D001/evaluation/E1.txt` | `E1_scores.tsv` | `E1_pairwise.tsv` | `2026-05-01T10:18:09Z` | passed: 15 scores, 105 pairwise rows |
| E2 | `comparing/prompts/generated/run-2026-05-01-D001/evaluation/E2.txt` | `E2_scores.tsv` | `E2_pairwise.tsv` | `2026-05-01T10:18:12Z` | passed: 15 scores, 105 pairwise rows |
| E3 | `comparing/prompts/generated/run-2026-05-01-D001/evaluation/E3.txt` | `E3_scores.tsv` | `E3_pairwise.tsv` | `2026-05-01T10:18:05Z` | passed: 15 scores, 105 pairwise rows |

### Aggregation Summary

| Rank | Condition ID | Condition Name | Mean Total | SD Total | Reader-Centered Mean | Reliability Mean | Mean Word Count |
|---:|---|---|---:|---:|---:|---:|---:|
| 1 | C1 | Reader-aware writing | 92.778 | 3.701 | 32.111 | 33.000 | 1800.0 |
| 2 | C2 | No-skill baseline | 92.222 | 4.295 | 32.000 | 33.000 | 1804.7 |
| 3 | C3 | Scientific-writing representative | 91.778 | 4.177 | 31.889 | 32.889 | 1774.0 |
| 4 | C4 | Scientific-writing alternative | 91.111 | 3.919 | 31.333 | 32.667 | 1767.0 |
| 5 | C5 | Academic writing standards | 86.556 | 4.613 | 29.889 | 30.778 | 1774.3 |

Pairwise condition win-rate matrix:

| Condition | C1 | C2 | C3 | C4 | C5 |
|---|---:|---:|---:|---:|---:|
| C1 |  | 0.556 | 0.519 | 0.630 | 0.889 |
| C2 | 0.444 |  | 0.556 | 0.519 | 0.889 |
| C3 | 0.481 | 0.444 |  | 0.556 | 0.778 |
| C4 | 0.370 | 0.481 | 0.444 |  | 0.741 |
| C5 | 0.111 | 0.111 | 0.222 | 0.259 |  |

### Report Outputs

| Artifact | Path |
|---|---|
| Quarto source report | `comparing/reports/run-2026-05-01-D001/comparison_report.qmd` |
| GitHub-readable Markdown report | `comparing/reports/run-2026-05-01-D001/comparison_report.md` |
| Scorebook | `comparing/evaluation_results/run-2026-05-01-D001/scorebook.csv` |
| Condition summary | `comparing/evaluation_results/run-2026-05-01-D001/summary_by_condition.csv` |
| Article summary | `comparing/evaluation_results/run-2026-05-01-D001/summary_by_article.csv` |
| Pairwise matrix | `comparing/evaluation_results/run-2026-05-01-D001/pairwise_condition_matrix.csv` |
| Figures | `comparing/reports/run-2026-05-01-D001/figures/` |

### Deviations and Decisions

| UTC | Item | Decision / Impact |
|---|---|---|
| `2026-05-01T09:52:19Z` | C3 source repository was not reachable by `git ls-remote`. | Used the rendered skills.sh `SKILL.md` snapshot and recorded SHA-256. |
| `2026-05-01T09:52:19Z` | C3 rendered skill lacked YAML frontmatter. | Added adapter frontmatter only inside the isolated C3 `CODEX_HOME`; the recorded snapshot remains unchanged. |
| `2026-05-01T10:01:31Z` | First-replicate output paths were relative to the temporary execution directory. | Copied generated R1 articles back into the repo unchanged; later prompts used absolute output paths. |
| `2026-05-01T10:18:57Z` | Quarto and Pandoc were not installed. | Kept the `.qmd` source and generated the GitHub-readable `.md` deterministically with `comparing/scripts/benchmark_pipeline.py`. |
| `2026-05-01T10:18:57Z` | Some Codex runs emitted remote plugin sync or analytics HTTP 403 warnings. | Warnings did not affect local skill isolation, article outputs, evaluator outputs, or aggregation. |
| `2026-05-01T10:18:57Z` | Body word-count checks varied slightly by tokenizer. | No generated article was manually revised; constraint-following scores account for small overages where evaluators judged them relevant. |

### Notes for Final Report

- C1 ranked first by mean total score, but the margin over C2 was small
  (0.556 points), so the result should be framed as directional evidence rather
  than a decisive superiority claim.
- The strongest separation was between C1-C4 and C5; C5 trailed on both
  reader-centered dimensions and reliability.
- This run used one dossier, three replicates per condition, and three
  evaluator passes. Broader topical sampling would be needed before making a
  robust general claim.

## Completed Run: `run-2026-05-01-D002`

### Run Metadata

| Field | Value |
|---|---|
| Run ID | `run-2026-05-01-D002` |
| Dossier ID | `D002` |
| Dossier path | `comparing/dossiers/D002_caspase5c_wnt_noisy_notes.md` |
| Source PDF | `comparing/blinded_articles/s41586-026-10343-8.pdf` |
| Writing prompt version | `writing-subagent-v2-minimal`; generated prompts in `comparing/prompts/generated/run-2026-05-01-D002/authoring/` |
| Evaluation prompt version | `evaluation-arrangement55-v1`; generated prompts in `comparing/prompts/generated/run-2026-05-01-D002/evaluation_arrangement55/E1/` |
| Authoring model | `gpt-5.5` |
| Evaluation model | `gpt-5.5` |
| Evaluation design | Arrangement5-5, one blinded evaluator (`E1`), 3 replicates x 5 positions = 15 packets |
| Evaluation completed UTC | `2026-05-01T11:51:01Z` |

### Isolation Check

| Unit | Isolated `CODEX_HOME` | User skill installed |
|---|---|---|
| C1 authoring | `/home/vscode/.codex-benchmark/run-2026-05-01-D002/C1` | `reader-aware-writing` only |
| C2 authoring | `/home/vscode/.codex-benchmark/run-2026-05-01-D002/C2` | none |
| C3 authoring | `/home/vscode/.codex-benchmark/run-2026-05-01-D002/C3` | `scientific-writing` only |
| C4 authoring | `/home/vscode/.codex-benchmark/run-2026-05-01-D002/C4` | `scientific-writing` only |
| C5 authoring | `/home/vscode/.codex-benchmark/run-2026-05-01-D002/C5` | `academic-writing-standards` only |
| E1 evaluation | `/home/vscode/.codex-benchmark/run-2026-05-01-D002/E1` seeded into packet homes for auth/config only | none |

System `.system` skills may be auto-populated by the Codex CLI, but no extra
user writing skill was installed in any authoring or evaluation home.

### Authoring Outputs

All 15 authoring outputs are stored under
`comparing/authoring_results/run-2026-05-01-D002/`. Final Codex summaries are
stored under `comparing/authoring_results/run-2026-05-01-D002/codex_logs/`.

### Blinding and Arrangement

| Artifact | Path |
|---|---|
| Neutral nickname map, private | `comparing/blinded_articles/run-2026-05-01-D002/arrangement55/nickname_map_private.csv` |
| Blinded article packets | `comparing/blinded_articles/run-2026-05-01-D002/arrangement55/articles/` |
| Arrangement plan, private | `comparing/evaluation_results/run-2026-05-01-D002/arrangement55/arrangement_plan_private.csv` |
| Prompt manifest | `comparing/evaluation_results/run-2026-05-01-D002/arrangement55/prompt_manifest.csv` |

The decoder verified exact position balance: each condition appeared three
times in each position, and each article appeared once in every position.

### Evaluation Outputs

The first sequential evaluator attempt was superseded because later packets
could see earlier raw evaluation outputs in the repository. Those files are
archived under
`comparing/evaluation_results/run-2026-05-01-D002/arrangement55/superseded_sequential_repo_visible/`
and are not used in the final analysis.

The final analysis used `comparing/scripts/run_arrangement55_evaluation_packets.py`,
which ran every packet from a fresh temporary working directory and copied only
the completed packet outputs back to the repository. Clean raw outputs are in
`comparing/evaluation_results/run-2026-05-01-D002/arrangement55/raw/`; isolated
transcripts are in
`comparing/evaluation_results/run-2026-05-01-D002/arrangement55/codex_logs_isolated/`.

### Decoded Summary

| Rank | Condition ID | Condition Name | Mean Total | Article SD | Pairwise Notes |
|---:|---|---|---:|---:|---|
| 1 | C3 | Scientific-writing representative | 94.600 | 1.442 | Beat C1 at 0.667; lost to C2 at 0.400 |
| 2 | C4 | Scientific-writing alternative | 94.600 | 1.400 | Beat C1 at 0.667 and C5 at 0.667 |
| 3 | C2 | No-skill baseline | 94.333 | 0.306 | Lost to C1 at 0.400 despite slightly higher total mean |
| 4 | C1 | Reader-aware writing | 94.067 | 2.101 | Beat C2 at 0.600 and C5 at 0.533; lost to C3/C4 |
| 5 | C5 | Academic writing standards | 93.600 | 1.562 | Lowest total mean; pairwise rates near tie against C1-C3 |

Position means showed a strong absolute position effect despite the prompt to
ignore ordering: positions 1-2 were scored higher than positions 3-5. Because
the Arrangement5-5 design balanced every article across all positions, condition
means remain position-balanced, but future evaluations should keep this design
or add multiple independent judges.

### Report Outputs

| Artifact | Path |
|---|---|
| Quarto source report | `comparing/reports/run-2026-05-01-D002/comparison_report.qmd` |
| GitHub-readable Markdown report | `comparing/reports/run-2026-05-01-D002/comparison_report.md` |
| Decoded scores | `comparing/evaluation_results/run-2026-05-01-D002/arrangement55/decoded/decoded_scores.csv` |
| Condition summary | `comparing/evaluation_results/run-2026-05-01-D002/arrangement55/decoded/summary_by_condition.csv` |
| Article summary | `comparing/evaluation_results/run-2026-05-01-D002/arrangement55/decoded/summary_by_article.csv` |
| Pairwise matrix | `comparing/evaluation_results/run-2026-05-01-D002/arrangement55/decoded/pairwise_condition_matrix.csv` |
| Figures | `comparing/reports/run-2026-05-01-D002/figures/` |

### Deviations and Decisions

| UTC | Item | Decision / Impact |
|---|---|---|
| `2026-05-01T11:19:51Z` | Initial evaluation prompts used repo-relative paths after a leakage check caught absolute path text containing the repo name. | `prepare_arrangement55_evaluation.py` was patched to keep evaluator prompts free of focal skill-name leakage in output paths. |
| `2026-05-01T11:25:04Z` | Sequential evaluator pass inspected earlier raw evaluation outputs. | The sequential pass was archived and excluded; final evaluation used isolated per-packet workdirs. |
| `2026-05-01T11:27:47Z` | Fully fresh evaluator `CODEX_HOME` lacked Codex auth. | `run_arrangement55_evaluation_packets.py` now seeds only auth/config from the no-skill E1 home and refuses homes containing user skills. |
| `2026-05-01T11:51:01Z` | Position means showed strong absolute position bias. | Arrangement5-5 averaging was retained; report warns against single-order scoring. |

## Completed Run: `run-2026-05-01-D003`

### Run Metadata

| Field | Value |
|---|---|
| Run ID | `run-2026-05-01-D003` |
| Dossier ID | `D002` |
| Dossier path | `comparing/dossiers/D002_caspase5c_wnt_noisy_notes.md` |
| Source PDF | `comparing/blinded_articles/s41586-026-10343-8.pdf` |
| Writing prompt version | `writing-subagent-v2-minimal`; generated prompts in `comparing/prompts/generated/run-2026-05-01-D003/authoring/` |
| Evaluation prompt version | `evaluation-arrangement55-v1`; generated prompts in `comparing/prompts/generated/run-2026-05-01-D003/evaluation_arrangement55/E1/` |
| Authoring model | `gpt-5.5` |
| Evaluation model | `gpt-5.5` |
| Evaluation design | Arrangement5-5, one blinded evaluator (`E1`), 3 replicates x 5 positions = 15 packets |
| Evaluation completed UTC | `2026-05-01T12:42:48Z` |

### Skill Revision Tested

The focal C1 skill was revised before this run. The canonical source under
`skills/reader-aware-writing/` now makes reader-aware behavior more explicit
and testable through a reader contract, paragraph-question path, claim ladder,
paragraph gates, and optional benchmark audit guidance. The isolated C1
authoring home used skill tree SHA-256
`b3ade6b38356ddf5fe16b139a8ee13d371e1017e789e2aa39feac5031d352f65`.

### Isolation Check

| Unit | Isolated `CODEX_HOME` | User skill installed |
|---|---|---|
| C1 authoring | `/home/vscode/.codex-benchmark/run-2026-05-01-D003/C1` | `reader-aware-writing` only |
| C2 authoring | `/home/vscode/.codex-benchmark/run-2026-05-01-D003/C2` | none |
| C3 authoring | `/home/vscode/.codex-benchmark/run-2026-05-01-D003/C3` | `scientific-writing` only |
| C4 authoring | `/home/vscode/.codex-benchmark/run-2026-05-01-D003/C4` | `scientific-writing` only |
| C5 authoring | `/home/vscode/.codex-benchmark/run-2026-05-01-D003/C5` | `academic-writing-standards` only |
| E1 evaluation | `/home/vscode/.codex-benchmark/run-2026-05-01-D003/E1` seeded into packet homes for auth/config only | none |

System `.system` skills may be auto-populated by the Codex CLI, but no extra
user writing skill was installed in any authoring or evaluation home. The
generated home manifest is
`comparing/prompts/generated/run-2026-05-01-D003/authoring/home_manifest.csv`.

### Authoring Outputs

All 15 authoring outputs are stored under
`comparing/authoring_results/run-2026-05-01-D003/`. Codex transcripts and final
messages are stored under
`comparing/authoring_results/run-2026-05-01-D003/codex_logs/`.

### Blinding and Arrangement

| Artifact | Path |
|---|---|
| Neutral nickname map, private | `comparing/blinded_articles/run-2026-05-01-D003/arrangement55/nickname_map_private.csv` |
| Blinded article packets | `comparing/blinded_articles/run-2026-05-01-D003/arrangement55/articles/` |
| Arrangement plan, private | `comparing/evaluation_results/run-2026-05-01-D003/arrangement55/arrangement_plan_private.csv` |
| Prompt manifest | `comparing/evaluation_results/run-2026-05-01-D003/arrangement55/prompt_manifest.csv` |

The decoder verified exact position balance: each condition appeared three
times in each position, and each article appeared once in every position.

### Decoded Summary

| Rank | Condition ID | Condition Name | Mean Total | Article SD | Pairwise Notes |
|---:|---|---|---:|---:|---|
| 1 | C1 | Reader-aware writing | 95.667 | 1.286 | Beat C2 at 0.867, C3 at 0.800, C4 at 0.667, and C5 at 0.533 |
| 2 | C3 | Scientific-writing representative | 94.667 | 0.902 | Beat C2 at 0.667, C4 at 0.800, and C5 at 0.600 |
| 3 | C5 | Academic writing standards | 94.333 | 2.139 | Beat C2 at 0.600 and C4 at 0.533; lost to C1/C3 |
| 4 | C4 | Scientific-writing alternative | 93.000 | 1.709 | Beat C2 at 0.467 only by near-tie; lost to C1/C3/C5 |
| 5 | C2 | No-skill baseline | 92.000 | 1.114 | Lowest total mean; only beat C4 at 0.533 |

Target-dimension means: C1 led reader orientation at 14.600/15 and tied C2 on
cohesion/coherence at 18.867/20. C1 also had the strongest total score and the
best pairwise profile in this run.

### Report Outputs

| Artifact | Path |
|---|---|
| Quarto source report | `comparing/reports/run-2026-05-01-D003/comparison_report.qmd` |
| GitHub-readable Markdown report | `comparing/reports/run-2026-05-01-D003/comparison_report.md` |
| Decoded scores | `comparing/evaluation_results/run-2026-05-01-D003/arrangement55/decoded/decoded_scores.csv` |
| Condition summary | `comparing/evaluation_results/run-2026-05-01-D003/arrangement55/decoded/summary_by_condition.csv` |
| Article summary | `comparing/evaluation_results/run-2026-05-01-D003/arrangement55/decoded/summary_by_article.csv` |
| Pairwise matrix | `comparing/evaluation_results/run-2026-05-01-D003/arrangement55/decoded/pairwise_condition_matrix.csv` |
| Figures | `comparing/reports/run-2026-05-01-D003/figures/` |

### Deviations and Decisions

| UTC | Item | Decision / Impact |
|---|---|---|
| `2026-05-01T12:17:30Z` | Added `comparing/scripts/run_authoring_benchmark.py`. | Authoring prompt generation, skill-home setup, isolated temporary workdirs, transcripts, and article copying are now reproducible. |
| `2026-05-01T12:19:10Z` | First D003 authoring attempt produced a double YAML fence around the dossier. | Stopped the attempt before completion, patched the prompt generator to match D002 dossier formatting, and restarted D003 from scratch. |
| `2026-05-01T12:37:30Z` | Added `--parallelism` to `run_arrangement55_evaluation_packets.py`. | Evaluation packets remain isolated but can run concurrently; D003 used parallelism 3. |
| `2026-05-01T12:42:48Z` | Position means again showed an absolute position effect. | Position-balanced Arrangement5-5 averaging was retained for condition means. |
| `2026-05-02T13:13:24Z` | Expanded the D003 comparison report audit trail. | The report now lists comparator skill links, snapshot/download times, dossier access controls, the position-bias rationale with Wang et al. (ACL 2024), and the README-style boxplot with a detailed caption. |
