# Evaluation Protocol

Protocol version: `evaluation-protocol-v1`

## Purpose

Compare the local `reader-aware-writing` skill with selected public scientific
or academic writing skills under controlled drafting conditions.

Primary question:

Does `reader-aware-writing` improve reader orientation, cohesion, coherence, and
scientific trust compared with a no-skill baseline and public writing skills?

## Authoring Design

- Conditions: C1-C5 as defined in `skill_registry.md`.
- Topic source: one fixed dossier per run.
- Replicates: at least three generated articles per condition for the first
  quantitative run.
- Model control: use the same model and model settings across all authoring
  conditions whenever possible.
- Tool control: no web search or external sources unless the run explicitly
  enables the same access for every condition.
- Output control: all authoring subagents use
  `prompts/writing_subagent_prompt.md`.

### Noisy-Dossier Variant

After `run-2026-05-01-D001`, the benchmark added a leaner variant to reduce
the scaffold given to the no-skill baseline:

- Dossier: `dossiers/D002_caspase5c_wnt_noisy_notes.md`.
- Authoring prompt: `prompts/writing_subagent_prompt_minimal.md`.
- Intended effect: the source packet contains scientific facts in rough,
  partly disordered note form, while the prompt avoids reader-path,
  article-structure, and prose-quality guidance.

## Blinding

Before evaluation:

1. Copy article text from `authoring_results/<run_id>/` into
   `blinded_articles/<run_id>/`.
2. Remove metadata and any trace of condition, skill, model, or timestamp.
3. Randomly assign article IDs such as `Article_A`, `Article_B`, and so on.
4. Record the private blinding map only in `evaluation_log.md`.

## Evaluation Design

- Evaluators: at least three independent evaluator subagents.
- Evaluator input: fixed dossier plus blinded articles only.
- Evaluator prompt: `prompts/evaluation_subagent_prompt.md`.
- Scoring: 100-point rubric with seven dimensions.
- Ranking: each evaluator provides both pointwise scores and pairwise
  preferences.
- Order control: provide articles in different randomized orders across
  evaluators. If feasible, repeat one evaluator order in reverse to check
  position sensitivity.

### Position-Balanced Arrangement5-5 Evaluation

For the noisy-dossier benchmark variant, replace random ordering with the
saved Arrangement5-5 scripts:

1. Run `comparing/scripts/prepare_arrangement55_evaluation.py`.
2. For each replicate, group the five condition outputs into one five-article
   set.
3. Generate five Latin-square arrangements for that replicate, so each article
   appears exactly once in each presentation position.
4. Replace condition-coded article identities with random neutral nicknames.
   Evaluator prompts must not contain `C1`-`C5`, replicate IDs, source
   filenames, condition names, skill names, or `Article_A`-style labels.
5. Score each five-article packet independently.
6. Run `comparing/scripts/decode_arrangement55_scores.py` after scoring. This
   validates headers, row counts, nickname membership, pairwise coverage,
   leakage patterns, and position balance, then decodes nicknames back to
   condition and replicate IDs.

The primary score for this mode is the mean decoded score after each article
has been scored once in every position. Condition summaries should use the
decoded outputs in
`evaluation_results/<run_id>/arrangement55/decoded/`.

## Scoring Dimensions

| Dimension | Points |
|---|---:|
| Scientific fidelity and source use | 20 |
| Article structure | 15 |
| Reader orientation | 15 |
| Cohesion and coherence | 20 |
| Evidence discipline and uncertainty | 15 |
| Scientific style and readability | 10 |
| Constraint following | 5 |
| Total | 100 |

## Aggregation Plan

For each condition:

- Mean total score across articles and evaluators.
- Standard deviation of total score.
- Mean score for each rubric dimension.
- Pairwise win rate against every other condition.
- Overall rank by mean total score.
- Reader-centered rank using only reader orientation plus cohesion/coherence.
- Scientific reliability rank using scientific fidelity plus evidence
  discipline.

Report all ties and close calls. A condition should not be described as clearly
better unless the score gap is stable across evaluators and replicates.

## Deviation Policy

Record every deviation in `evaluation_log.md`, including:

- Missing skill snapshot or uncertain version.
- Failed authoring run.
- Any manual edit to generated text.
- Dossier correction after generation begins.
- Evaluator seeing unblinded metadata.
- Tool access difference between conditions.
- Article excluded from aggregation.
