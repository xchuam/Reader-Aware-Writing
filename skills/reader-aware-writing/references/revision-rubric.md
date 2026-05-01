# Revision Rubric

Use this rubric before returning a substantial rewrite, critique, or reader-specific adaptation.

## Reader Fit

- The intended reader is clear or the assumption is stated.
- The opening answers the reader's first practical question.
- The level of detail matches the reader's expertise and time.
- The text foregrounds the reader's decision, action, or concern rather than the author's process.
- For scientific writing, the text anticipates the expected reader: specialist, interdisciplinary reader, reviewer, editor, student, practitioner, or public reader.

## Structure

- The main point appears before supporting detail unless suspense or pedagogy is intentional.
- Headings, bullets, and paragraph order reduce cognitive load.
- Related ideas are grouped together.
- Transitions explain why the next point matters.
- Optional depth is separated from essential reading.
- Paragraphs have one governing idea, usually visible near the beginning.
- Scientific sections answer their expected reader questions: why this problem, what was done, what was found, what it means, and how far it can be trusted.
- Section handoffs make the next section feel motivated rather than abrupt.

## Clarity

- Sentences are easy to parse on a first pass.
- Terms are defined when the reader needs definitions.
- Pronouns and references are unambiguous.
- Lists are parallel enough to scan.
- The text removes filler that does not help the reader decide, act, or understand.
- Sentence openings connect to familiar context; sentence endings carry new or important information when possible.
- New terms, mechanisms, methods, populations, or implications are introduced only after the reader has enough context.

## Trust

- Claims are specific and bounded.
- Evidence, examples, or reasoning support important claims.
- Uncertainty is named plainly.
- Caveats do not undercut the main message unless the caveat truly changes the conclusion.
- No unsupported facts, citations, metrics, or promises are introduced.
- Scientific claims distinguish observations, results, interpretations, implications, and speculation.
- Limitations are visible where they affect interpretation, generalization, or action.

## Tone

- The tone fits the reader relationship and stakes.
- The text avoids condescension toward less expert readers.
- The text avoids unnecessary hedging for expert or decision-making readers.
- Urgency, warmth, confidence, and caution are calibrated rather than generic.

## Actionability

- The reader knows what to do next, if action is expected.
- Requests include owner, deadline, scope, or decision criteria when relevant.
- Instructions are ordered in the way the reader will perform them.
- Risks, dependencies, and blockers are visible when they affect action.

## Final Pass

Before returning the result:

1. Preserve the user's facts, constraints, and intended voice.
2. Remove author-only scaffolding such as "this section will discuss" unless it helps navigation.
3. Check that the first paragraph earns continued reading.
4. Check that the last paragraph leaves the reader with the intended action or understanding.
5. If you changed strategy, mention the reader-specific reason in one concise note.
6. For scientific text, verify that no data, citations, methods, mechanisms, or conclusions were invented during revision.
7. For generated scientific articles, silently confirm coherence, no unexplained novelty, old-to-new flow, and one-reader-question-per-paragraph.
8. For generated scientific articles, silently run the reader contract, paragraph-question path, claim ladder, and paragraph gates. If the user requested an audit, provide a compact table with paragraph ID, reader question, orienting sentence, bridge need, evidence/interpretation status, and exit handoff.

## Optional Benchmark Audit

When the user explicitly asks to make reader-aware behavior testable, save or return a compact audit table separate from the final article. Do not include this table in a publication-ready article unless requested.

| Field | Test |
|---|---|
| `paragraph_id` | Stable paragraph number or section label. |
| `reader_question` | The one reader question this paragraph answers. |
| `orienting_sentence` | The sentence that tells the reader why the paragraph exists. |
| `new_concept_bridge` | Any bridge needed before a new term, method, mechanism, or implication. |
| `claim_strength` | Observation, result, mechanistic evidence, model-supported interpretation, implication, speculation, or forbidden upgrade removed. |
| `exit_handoff` | How the paragraph prepares the next reader question or closes the local point. |
