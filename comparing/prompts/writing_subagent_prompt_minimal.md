# Minimal Writing Subagent Prompt

Prompt version: `writing-subagent-v2-minimal`

Use this prompt for the noisy-dossier benchmark. Only the `Condition Metadata`
block and loaded skill should differ across authoring conditions.

```text
Benchmark authoring task.

Condition Metadata
- Run ID: {RUN_ID}
- Condition ID: {CONDITION_ID}
- Condition name: {CONDITION_NAME}
- Assigned skill: {ASSIGNED_SKILL_NAME_OR_NONE}
- Skill source/snapshot: {SKILL_SOURCE_AND_VERSION}
- Replicate ID: {REPLICATE_ID}
- Output path: comparing/authoring_results/{RUN_ID}/{CONDITION_ID}_{REPLICATE_ID}.md
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
run_id: {RUN_ID}
condition_id: {CONDITION_ID}
condition_name: {CONDITION_NAME}
assigned_skill: {ASSIGNED_SKILL_NAME_OR_NONE}
skill_source_snapshot: {SKILL_SOURCE_AND_VERSION}
replicate_id: {REPLICATE_ID}
prompt_version: writing-subagent-v2-minimal
dossier_id: {DOSSIER_ID}
generated_at_utc: {GENERATED_AT_UTC}
model: {MODEL_NAME}
---

- After the metadata block, provide the article only.

Fixed Dossier
{PASTE_DOSSIER_HERE}
```

## Run Notes

- This prompt intentionally avoids article-structure suggestions, reader-path
  advice, revision advice, and explicit prose-quality criteria.
- Keep `writing_subagent_prompt.md` as the archived v1 scaffolded prompt used
  for `run-2026-05-01-D001`.

