---
name: reader-aware-writing
description: Draft, revise, critique, or transform writing for a clearly defined reader, especially scientific and academic articles. Use for reader-centered writing, audience orientation, cohesion, coherence, paragraph flow, abstracts, introductions, results, discussions, reviewer-facing revision, or adapting technical depth across reader expertise levels.
---

# Reader Aware Writing

## Overview

Use this skill to make writing land with the person who will read it. The core move is to build a lightweight reader model, revise around that reader's job, and preserve truth while improving clarity, cohesion, trust, and actionability.

For scientific writing, treat reader-centeredness as a form of rigor: the text should prepare the reader for each concept, make the argument's logic visible, distinguish evidence from interpretation, and avoid forcing the reader to infer missing links.

## Workflow

1. Identify the reader and their job.
   - Capture the reader role, expertise level, purpose for reading, decision or action needed, likely constraints, objections, and desired tone.
   - If the reader is unclear, infer a plausible reader from the artifact and state the assumption briefly. Ask only when the missing reader changes the work materially.
   - For scientific articles, build a compact reader contract before drafting:
     reader role, what the reader already knows, what they likely do not know, the reader's first question, the reader's likely confusion, and the article promise.
   - For complex or high-stakes writing, read [reader-model.md](references/reader-model.md).

2. Choose the work mode and artifact type.
   - Compose: create new writing from goals and context.
   - Revise: improve an existing draft while preserving meaning.
   - Critique: diagnose where the text mismatches the reader.
   - Transform: adapt one artifact for another audience or channel.
   - Compare: explain how multiple reader versions differ.
   - For abstracts, introductions, results, discussions, or full manuscripts, read [scientific-article.md](references/scientific-article.md).

3. Build the reader path before drafting.
   - Privately map each paragraph or section to the reader question it answers.
   - Sequence those questions so each answer prepares the next question.
   - Identify any concept, method, variable, result, or implication that needs a bridge before it appears.
   - For scientific articles, make the paragraph path explicit enough to test: each paragraph should have one reader question, one governing answer, and one handoff to the next reader question.
   - If two paragraphs answer the same reader question, merge or sharpen their roles. If one paragraph answers two unrelated questions, split it.
   - Omit this planning map from the final answer unless the user asks for reasoning or critique.

4. Make the reader path obvious.
   - Start with what the reader needs to know, decide, or do.
   - Put context before details, but do not bury the point.
   - Match density to expertise: define terms for newcomers, compress basics for experts, and expose assumptions for decision-makers.
   - Replace author-centered phrasing with reader-centered stakes, actions, and consequences.
   - Preserve required facts, caveats, citations, constraints, and the user's intended voice.
   - For academic introductions, paragraphs, cohesion, or coherence, read [academic-writing.md](references/academic-writing.md) and [cohesion-coherence.md](references/cohesion-coherence.md).

5. Revise for trust.
   - Separate facts from interpretation.
   - Name uncertainty without over-apologizing.
   - Prefer concrete claims, examples, and decision criteria over vague reassurance.
   - Remove jargon unless it is native to the reader's working vocabulary.
   - Avoid inventing evidence, metrics, policies, or citations.
   - For scientific articles, silently classify important statements on a claim ladder: observation, result, mechanistic evidence, model-supported interpretation, implication, speculation, and forbidden upgrade. Downgrade or remove any statement that exceeds the supplied evidence.
   - For sentence-level scientific clarity, active/passive choices, nominalization, modifiers, parallelism, and punctuation, read [scientific-style.md](references/scientific-style.md).

6. Finish with a reader check.
   - Use [revision-rubric.md](references/revision-rubric.md) for substantive revisions, high-stakes writing, or explicit review requests.
   - For scientific article drafting, run the paragraph gates before returning: orientation, unity, bridge, evidence/interpretation order, exit handoff, and claim strength.
   - If useful, provide a concise change note explaining the reader-specific choices.

## Scientific Article Operating Protocol

Use this protocol when composing a scientific article from notes, a dossier, a paper, or experimental results. Keep the protocol hidden unless the user requests an audit or reasoning.

1. Reader contract.
   - Reader role: who is reading and why.
   - Already knows: concepts the reader can be expected to know.
   - Likely gaps: concepts, methods, organisms, variables, or stakes that need preparation.
   - First question: what the reader needs answered before details matter.
   - Likely confusion: where the reader may lose the thread.
   - Article promise: what the article will make clear without exceeding the evidence.

2. Paragraph-question path.
   - Draft a one-line question for each planned paragraph or section.
   - Put the questions in the order the reader should ask them.
   - Ensure each answer prepares the next question.
   - Do not include a paragraph whose reader question is unclear.

3. Claim ladder.
   - Mark major claims internally as observation, result, mechanistic evidence, model-supported interpretation, implication, speculation, or forbidden upgrade.
   - Keep observations and results close to their evidence.
   - Signal model-supported interpretations with bounded language.
   - Remove forbidden upgrades: causal, clinical, mechanistic, translational, or novelty claims not supported by the source.

4. Paragraph gates.
   - Orientation: the first sentence tells the reader why this paragraph exists.
   - Unity: every sentence serves the same reader question.
   - Bridge: new concepts, methods, variables, subgroups, mechanisms, and limitations are introduced before they are used.
   - Evidence order: evidence appears before interpretation when the reader needs proof; interpretation appears before details when the reader first needs the point.
   - Handoff: the final sentence closes the local point or prepares the next paragraph.
   - Term discipline: repeat stable technical terms until the reader has a firm thread; avoid premature synonym swaps.

5. Final reader-path pass.
   - Read only the first sentence of each paragraph. They should form a coherent mini-outline.
   - Read only the final sentence of each paragraph. The handoffs should not feel abrupt.
   - Check that the central claim can be stated in one sentence and that every section serves it.
   - Return the article only unless the user asked for the hidden reader contract, paragraph path, or audit table.

## Reader-First Rules

Use these rules as defaults when drafting or revising:

- No unexplained novelty: introduce a new idea only after it has been named, implied, or explicitly motivated.
- One paragraph, one reader question: each paragraph should answer or develop one question the reader has at that point.
- Old before new: begin sentences with familiar information when possible; place new, complex, or emphasized information later.
- Signpost structural shifts: mark contrasts, turns, implications, changes of scale, and moves from evidence to interpretation.
- Handoff between sections: end or begin sections with enough shared language that the reader understands why the next section follows.
- Repeat key terms before varying them: premature synonym use can break the reader's thread.
- Do not simplify by default: expert readers may need more precision, stronger caveats, or clearer methods rather than easier vocabulary.

## Output Rules

- When the user asks for rewritten text, lead with the rewritten text.
- When the user asks for critique, lead with the highest-impact reader mismatches.
- When the user asks for multiple audiences, label each version by reader and keep the differences intentional.
- Keep meta commentary short unless the user asks for reasoning.
- Do not turn every edit into a generic simplification; reader-aware writing may become more technical, more direct, warmer, shorter, or more detailed depending on the reader.
- For scientific revisions, do not invent data, methods, results, citations, mechanisms, limitations, or implications. If evidence is missing, mark the gap or phrase the claim conditionally.

## Agent Portability

This skill follows the portable Agent Skills structure: one `SKILL.md` with `name` and `description`, plus optional resources. For placement in Codex, Claude, or another agent, read [agent-portability.md](references/agent-portability.md).
