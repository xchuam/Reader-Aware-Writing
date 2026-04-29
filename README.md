# Reader-Aware Writing

Many agent writing skills improve grammar, tone, or generic clarity, but they often do not teach an agent how to guide a reader through a scientific argument. As a result, generated articles can be technically plausible sentence by sentence while still lacking audience orientation, paragraph purpose, cohesion, coherence, and clear old-to-new information flow.

Reader-Aware Writing fills that gap with a portable Agent Skill for reader-centered scientific and academic writing. It helps agents model the intended reader, build a visible path through the argument, introduce concepts only when the reader is prepared for them, and revise drafts so evidence, interpretation, limitations, and implications are easier to follow.

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

### Project-local use

For work inside this repository, no extra install step is needed. The project discovery paths already point to the canonical skill source:

- Codex: `.agents/skills/reader-aware-writing`
- Claude: `.claude/skills/reader-aware-writing`

## What This Skill Does

Reader-Aware Writing helps agents:

- model the target reader, including expertise, purpose, likely confusion, and evidence needs
- draft and revise scientific article sections, including abstracts, introductions, results, and discussions
- improve paragraph construction, topic sentences, old-to-new information flow, and section handoffs
- diagnose weak cohesion, weak coherence, unexplained novelty, and buried paragraph purpose
- calibrate scientific style choices, including active/passive voice, nominalization, concrete subjects, modifiers, parallelism, and punctuation
- preserve scientific trust by avoiding invented data, citations, mechanisms, methods, or implications

## Use The Skill

Ask your agent to use `reader-aware-writing` when drafting, revising, or critiquing scientific and academic prose.

Example prompts:

```text
Use reader-aware-writing to revise this introduction for interdisciplinary reviewers.
```

```text
Use reader-aware-writing to critique this Results section for cohesion, coherence, and old-to-new flow.
```

```text
Use reader-aware-writing to turn these study notes into a reader-friendly abstract without inventing results.
```
