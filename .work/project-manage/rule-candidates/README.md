# Project Rule Candidates

This directory stores candidate project rules that may later be promoted into a root or feature-local `AGENTS.md`.

Use it for lessons that are:

- too project-specific to become reusable skills
- not primarily human-improvement items
- stable enough to be considered for future project rules

## Location

Store candidates at:

- `.work/project-manage/rule-candidates/<id>.md`

## Purpose

These are not active rules yet.

They are reviewable proposals for:

- root shared control-plane rules
- feature-worktree-local execution rules

## Suggested Frontmatter

Use TOML frontmatter delimited by `+++`.

Suggested fields:

- `id`
- `status`
- `created`
- `updated`
- `target_scope`
- `target_feature`
- `source_tasks`
- `source_sessions`
- `summary`

Suggested `status` values:

- `active`
- `accepted`
- `dropped`

Suggested `target_scope` values:

- `root`
- `feature`

## Section Order

- `# Title`
- `## Why This Should Be A Rule`
- `## Proposed Rule`
- `## Evidence`
- `## Target Placement`
- `## Notes`

## Workflow

- Use `$learn` to draft or update candidates.
- Review them before promoting anything into `AGENTS.md`.
- Do not treat this directory as active runtime instruction by itself.
