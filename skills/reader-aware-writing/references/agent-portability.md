# Agent Portability

This skill is intentionally written in the common Agent Skills shape so Codex, Claude, and other compatible agents can use the same source folder.

## Core Skill Contract

Keep these files portable:

- `SKILL.md`: required entrypoint with YAML frontmatter and Markdown instructions.
- `references/`: optional focused documents agents load only when needed.
- `scripts/`: optional executable helpers if the skill later needs deterministic tooling.
- `assets/`: optional templates or static resources.

The `name` should match the folder name. Keep `description` specific because agents usually see it before deciding whether to load the full skill.

## Recommended Repo Layout

Use `skills/reader-aware-writing/` as the canonical source. Add platform-specific discovery paths that point to that source:

- Codex project skill: `.agents/skills/reader-aware-writing`
- Claude project skill: `.claude/skills/reader-aware-writing`
- Generic portable source: `skills/reader-aware-writing`

Prefer symlinks for project discovery paths so there is only one editable source. If a target environment does not follow symlinks, copy the skill folder and treat `skills/reader-aware-writing/` as canonical.

## Global Install Paths

Use these paths when a user wants the skill available across projects:

- Codex: `${CODEX_HOME:-$HOME/.codex}/skills/reader-aware-writing`
- Claude Code: `$HOME/.claude/skills/reader-aware-writing`

After adding or changing a global Codex skill, restart Codex so it can discover the new skill metadata. Claude Code usually watches existing skill directories, but restart if a top-level skills directory was created during setup.

## Compatibility Rules

- Keep frontmatter limited to `name` and `description` unless a platform-specific field is truly needed.
- Put platform-specific metadata in `agents/` or another adapter directory, not in the portable instructions.
- Do not rely on one agent's tool names in the core workflow.
- Keep file references relative to the skill root.
- Avoid deeply nested reference chains.
