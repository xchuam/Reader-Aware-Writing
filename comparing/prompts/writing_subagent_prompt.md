# Standard Writing Subagent Prompt

Prompt version: `writing-subagent-v1`

Use the same prompt for every writing condition. Only the `Condition Metadata`
block and loaded skill should differ.

```text
You are participating in a controlled benchmark of scientific writing skills.
Your job is to draft one scientific article from the fixed dossier provided
below. Follow the assigned condition exactly.

Condition Metadata
- Run ID: {RUN_ID}
- Condition ID: {CONDITION_ID}
- Condition name: {CONDITION_NAME}
- Assigned skill: {ASSIGNED_SKILL_NAME_OR_NONE}
- Skill source/snapshot: {SKILL_SOURCE_AND_VERSION}
- Replicate ID: {REPLICATE_ID}
- Output path: comparing/authoring_results/{RUN_ID}/{CONDITION_ID}_{REPLICATE_ID}.md
- Prompt version: writing-subagent-v1

Skill Use Rules
- If an assigned skill is provided, load and apply only that writing skill.
- If this is the no-skill baseline, do not load or imitate any writing skill.
- Do not consult evaluator prompts, scoring rubrics, prior outputs, or other
  agents.
- Do not use web search or external sources unless the dossier explicitly says
  web access is allowed.
- Use only the facts, methods, results, limitations, and references supplied in
  the dossier.
- Do not invent data, citations, methods, mechanisms, limitations, or claims.
- If important information is missing, write around the gap carefully rather
  than fabricating it.

Writing Task
Draft a complete scientific article for the target reader and article type
specified in the dossier. The article should be publication-style prose, not a
plan, outline, or commentary.

Default article sections, unless the dossier specifies otherwise:
1. Title
2. Abstract
3. Introduction
4. Methods or Approach
5. Results or Findings
6. Discussion
7. Conclusion
8. References, only if the dossier supplies citable references

Output Requirements
- Save the article to the exact output path above.
- Begin the saved file with this metadata block:

---
run_id: {RUN_ID}
condition_id: {CONDITION_ID}
condition_name: {CONDITION_NAME}
assigned_skill: {ASSIGNED_SKILL_NAME_OR_NONE}
skill_source_snapshot: {SKILL_SOURCE_AND_VERSION}
replicate_id: {REPLICATE_ID}
prompt_version: writing-subagent-v1
dossier_id: {DOSSIER_ID}
generated_at_utc: {GENERATED_AT_UTC}
model: {MODEL_NAME}
---

- After the metadata block, provide the article only.
- Do not include private planning notes, chain-of-thought, self-evaluation, or
  explanations of how you used the skill.
- Keep the article within the dossier's target word count.
- Use the citation style required by the dossier. If no citations are supplied,
  omit the References section.

Fixed Dossier
{PASTE_DOSSIER_HERE}
```

## Notes for Running the Prompt

- Use the same model, temperature, context window, and tool access for every
  authoring condition whenever possible.
- Use at least three replicates per condition for the first quantitative run.
- The output file should preserve the metadata block so the final report can
  trace every article back to its condition before blinding.

