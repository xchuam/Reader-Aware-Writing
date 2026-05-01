# Scientific Writing Skill Comparison

This folder stores the benchmark materials for comparing `reader-aware-writing`
against selected public scientific or academic writing skills.

The goal is to keep the comparison reproducible enough for a later quantitative
report: every skill source, prompt version, dossier, generated article,
blinding step, evaluator result, and deviation from protocol should be recorded
here.

## Folder Map

- `skill_registry.md`: selected authoring conditions and provenance.
- `prompts/writing_subagent_prompt.md`: standard prompt for every writing
  subagent in the first scaffolded run.
- `prompts/writing_subagent_prompt_minimal.md`: stripped-down authoring prompt
  for noisy-dossier runs where the skill should provide the writing strategy.
- `prompts/evaluation_subagent_prompt.md`: standard prompt for blinded
  evaluator subagents.
- `skill_snapshots/`: exact comparator skill text used during a run.
- `dossiers/`: fixed topic dossiers used as source material for drafting.
- `authoring_results/`: unblinded article outputs from writing subagents.
- `blinded_articles/`: anonymized article copies used for evaluation.
- `evaluation_results/`: evaluator score sheets and ranking outputs.
- `scripts/`: local utilities for blinding, evaluator prompt generation,
  aggregation, figures, and report rendering.
- `reports/`: run-specific `.qmd` reports, GitHub-readable `.md` exports, and
  generated figures.
- `evaluation_protocol.md`: quantitative evaluation design and scoring rules.
- `evaluation_log.md`: running audit log for each benchmark run.
- `scorebook_template.csv`: tabular template for score aggregation.

## Recommended Workflow

1. Create or select a fixed topic dossier in `dossiers/`.
2. Confirm skill provenance in `skill_registry.md` before authoring starts.
3. Start one writing subagent per condition and give each the same standard
   authoring prompt plus the same dossier. For the next noisy run, use
   `prompts/writing_subagent_prompt_minimal.md` with
   `dossiers/D002_caspase5c_wnt_noisy_notes.md`.
4. Save every generated article under `authoring_results/<run_id>/`.
5. Create blinded copies under `blinded_articles/<run_id>/` and record the
   private mapping in `evaluation_log.md`.
6. Run evaluator subagents with `prompts/evaluation_subagent_prompt.md`.
7. Save evaluator outputs under `evaluation_results/<run_id>/`.
8. Aggregate scores, rank stability, and pairwise wins in `evaluation_log.md`.
9. Write the final run report under `reports/<run_id>/`.

## Position-Balanced Evaluation

For noisy-dossier runs, use the Arrangement5-5 scripts instead of random
article order:

```bash
python3 comparing/scripts/prepare_arrangement55_evaluation.py \
  --run-id <run_id> \
  --dossier D002_caspase5c_wnt_noisy_notes.md \
  --evaluators E1 E2 E3
```

This creates neutral nickname maps, 5x5 Latin-square evaluator prompts for
each replicate, and private arrangement maps. Evaluators should receive only
the generated prompts under
`comparing/prompts/generated/<run_id>/evaluation_arrangement55/`.

Run evaluator packets from isolated temporary work directories so one packet
cannot read a previous packet's judgments:

```bash
python3 comparing/scripts/run_arrangement55_evaluation_packets.py \
  --run-id <run_id> \
  --evaluators E1
```

After the evaluator TSV files are saved, decode and aggregate with:

```bash
python3 comparing/scripts/decode_arrangement55_scores.py --run-id <run_id>
```

Decoded condition summaries are written under
`comparing/evaluation_results/<run_id>/arrangement55/decoded/`.

Generate the `.qmd`, GitHub-readable `.md`, and SVG figures with:

```bash
python3 comparing/scripts/report_arrangement55.py --run-id <run_id>
```

Do not overwrite old runs. Use a new `run_id` for every benchmark execution.
