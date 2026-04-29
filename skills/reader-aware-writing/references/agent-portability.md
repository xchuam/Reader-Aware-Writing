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

Use `skills/reader-aware-writing/` as the canonical source. Keep the published repository focused on the portable skill folder plus installation helpers. Do not require project-local adapter folders for users to install or use the skill.

## Global Install Paths

Use these paths when a user wants the skill available across projects:

- Codex: `${CODEX_HOME:-$HOME/.codex}/skills/reader-aware-writing`
- Claude Code: `$HOME/.claude/skills/reader-aware-writing`

After adding or changing a global Codex skill, restart Codex so it can discover the new skill metadata. Claude Code usually watches existing skill directories, but restart if a top-level skills directory was created during setup.

## Compatibility Rules

- Keep frontmatter limited to `name` and `description` unless a platform-specific field is truly needed.
- Put platform-specific metadata in `agents/` inside the skill folder or another bundled adapter directory, not in the portable instructions.
- Do not rely on one agent's tool names in the core workflow.
- Keep file references relative to the skill root.
- Avoid deeply nested reference chains.
