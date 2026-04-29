# Agent Instructions

This repository develops a portable Agent Skill that helps LLM agents write, revise, and critique scientific articles in a reader-centered way.

The main problem this skill should address is that LLM-generated scientific prose can be technically plausible while still being hard to read: weak cohesion, unclear paragraph logic, poor coherence across sections, unexplained conceptual jumps, and insufficient attention to what the reader needs at each point in the article.

## Repository Layout

- Canonical skill source: `skills/reader-aware-writing/`

Edit the canonical source under `skills/reader-aware-writing/`. Do not depend on project-local adapter folders; user installation should happen through `skill.sh`, Codex `$skill-installer`, or `skills.sh`.

## Skill Development Goal

When improving the skill, prioritize guidance that helps an agent produce scientific writing that is:

- Reader-centered: the text anticipates the reader's knowledge, expectations, questions, and likely points of confusion.
- Cohesive: sentences and paragraphs follow an old-to-new information flow, with clear links between ideas.
- Coherent: each paragraph, section, and article-level move has a visible purpose in the argument.
- Scientifically appropriate: claims are precise, bounded, evidence-aware, and careful about uncertainty.
- Usable by agents: instructions are explicit enough for Codex, Claude, and similar agents to apply during drafting, revision, critique, and transformation tasks.

## Writing Knowledge To Include

Keep the published skill self-contained. When expanding the skill, encode practical guidance directly inside `skills/reader-aware-writing/` and its bundled references rather than depending on repository-only development materials. The skill should include guidance on:

- Reader-first scientific writing and audience orientation.
- Research article structure, especially abstracts, introductions, results, and discussions.
- Paragraph construction, topic sentences, paragraph unity, and paragraph development.
- Cohesion and coherence, including old-to-new flow, signposting, repetition of key terms, and clear transitions.
- Clear scientific style, including active/passive voice choices, concrete subjects and verbs, parallelism, modifiers, clauses, punctuation, and sentence-level readability.
- Revision diagnostics that help an agent explain why a draft is difficult for readers and how to fix it.

Do not treat reader-centered writing as generic simplification. Expert readers may need more technical precision, clearer assumptions, stronger evidence logic, or more explicit limitations rather than shorter or less technical prose.

## When To Use The Skill

When the task involves drafting, revising, critiquing, or adapting writing for a specific audience, use the `reader-aware-writing` skill.

For scientific article tasks, apply the skill with special attention to:

- the target reader, such as domain experts, interdisciplinary readers, reviewers, editors, students, or policy/clinical readers;
- the reader's current question at each paragraph or section;
- whether new concepts are introduced before the reader is prepared for them;
- whether paragraph openings orient the reader and paragraph endings advance the argument;
- whether claims, evidence, caveats, and implications are ordered so the reader can follow the logic.

## Editing Principles

When updating this repository:

- Preserve portability across agent systems. Avoid instructions that only work for one vendor unless they are isolated in an adapter.
- Prefer concise, operational guidance over long theoretical explanation.
- Turn writing concepts into agent-actionable checks, workflows, rubrics, and examples.
- Keep examples scientific or academic when possible.
- Avoid inventing citations, evidence, or discipline-specific rules not supported by the provided materials or common scientific-writing practice.
