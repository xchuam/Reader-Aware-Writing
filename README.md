# Reader-Aware-Writing

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Skills](https://img.shields.io/badge/skills.sh-Compatible-green)](https://skills.sh)
[![GitHub stars](https://img.shields.io/github/stars/xchuam/Reader-Aware-Writing?style=social)](https://github.com/xchuam/Reader-Aware-Writing)

Many agent writing skills improve grammar, tone, or generic clarity, but they often do not teach an agent how to guide a reader through a scientific argument. As a result, generated articles can be technically plausible sentence by sentence while still lacking audience orientation, paragraph purpose, cohesion, coherence, and clear old-to-new information flow.

Reader-Aware-Writing fills that gap with a portable Agent Skill for **reader-centered scientific and academic writing**. It helps agents model the intended reader, build a visible path through the argument, introduce concepts only when the reader is prepared for them, and revise drafts so evidence, interpretation, limitations, and implications are easier to follow. A systematic test on a noisy life-science writing dossier showed that the current `reader-aware-writing` skill performed better than a no-skill baseline and three comparator writing-skill settings under permutation-balanced blinded scoring. More analysis detail is available in the [benchmark report](comparing/reports/run-2026-05-01-D003/comparison_report.md).

![Blinded total score distribution by authoring setting](comparing/reports/run-2026-05-01-D003/figures/total_score_boxplot_by_skill.svg)

## Install The Skill

Recommended: install with the method that matches your agent directly. This is more reliable than assuming every agent has already indexed the shared skills ecosystem.

### Codex

Run this in the Codex chat:

```text
$skill-installer install https://github.com/xchuam/Reader-Aware-Writing/tree/main/skills/reader-aware-writing
```

Or install from a local clone:

```bash
git clone https://github.com/xchuam/Reader-Aware-Writing.git
cd Reader-Aware-Writing
./skill.sh install codex
```

Restart Codex after adding a global skill so it can discover the new skill metadata.

### Claude

Run this in your shell:

```bash
git clone https://github.com/xchuam/Reader-Aware-Writing.git /tmp/reader-aware-writing
cd /tmp/reader-aware-writing
./skill.sh install claude
```

If you want to install for both Codex and Claude from a local clone, run:

```bash
./skill.sh install all
```

Restart Claude if the skill does not appear immediately.

### skills.sh ecosystem

This skill is also structured for the broader `skills.sh` ecosystem.

Run this in your shell:

```bash
npx skills add xchuam/Reader-Aware-Writing --skill reader-aware-writing
```

After ecosystem install, check inside your agent that `reader-aware-writing` is actually available before relying on it.

## What This Skill Does

Reader-Aware-Writing helps agents:

- model the target reader, including expertise, purpose, likely confusion, and evidence needs
- draft and revise scientific article sections, including abstracts, introductions, results, and discussions
- improve paragraph construction, topic sentences, old-to-new information flow, and section handoffs
- diagnose weak cohesion, weak coherence, unexplained novelty, and buried paragraph purpose
- calibrate scientific style choices, including active/passive voice, nominalization, concrete subjects, modifiers, parallelism, and punctuation
- preserve scientific trust by avoiding invented data, citations, mechanisms, methods, or implications

## Use The Skill

Ask your agent to use `reader-aware-writing` whenever the main challenge is helping a specific reader follow a scientific or academic argument. The skill is most useful when the text needs stronger audience orientation, paragraph logic, old-to-new flow, section handoffs, evidence discipline, or reader-aware revision.

For best results, name the reader and the task. For example, specify whether the draft is for domain experts, interdisciplinary reviewers, students, editors, clinicians, policy readers, or collaborators outside the immediate field.

Example prompts:

```text
Use reader-aware-writing to draft a 1,500-word scientific article from these notes for life-science researchers. Preserve only dossier-supported claims.
```

```text
Use reader-aware-writing to revise this introduction for interdisciplinary reviewers. Make the paragraph purpose and reader path clearer without oversimplifying the science.
```

```text
Use reader-aware-writing to critique this Results section for cohesion, coherence, old-to-new flow, and unsupported interpretive jumps.
```

```text
Use reader-aware-writing to turn these study notes into a reader-friendly abstract for busy journal editors without inventing results.
```
