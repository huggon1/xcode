# Shared Rule Candidates

This directory stores candidate shared rules that may later be promoted into a root or workstream-local `AGENTS.md`.

Use it for lessons that are:

- too workspace-specific to become reusable skills
- not primarily human-improvement items
- stable enough to be considered for future shared rules

## Location

Store candidates at:

- `.work/learning/rule-candidates/<id>.md`

## Purpose

These are not active rules yet.

They are reviewable proposals for:

- root shared control-plane rules
- workstream-local execution rules

## Suggested Frontmatter

Use TOML frontmatter delimited by `+++`.

Suggested fields:

- `id`
- `status`
- `created`
- `updated`
- `target_scope`
- `target_workstream`
- `source_tasks`
- `source_sessions`
- `summary`

Suggested `status` values:

- `active`
- `accepted`
- `dropped`

Suggested `target_scope` values:

- `root`
- `workstream`

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
