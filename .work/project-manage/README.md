# Project Runtime State

This directory stores the smallest durable state owned by `$project-manage` for the shared root control plane.

It is separate from `.work/catalog/active.yaml`.

## Purpose

Use this state to remember a few stable facts about the shared operating layer:

- which runtime model this project root follows
- which baseline revision it was last aligned to
- when the operating layer was initialized
- when the last runtime-layer change happened
- what the last runtime-layer change was

Feature lifecycle state itself belongs in `.work/features/<feature-id>/feature.toml`, not in `state.toml`.

This state is intentionally small.

## File

`state.toml` is the only required file in this directory.

## What Belongs Here

- control-plane metadata
- baseline revision markers
- the latest runtime-layer change summary

## What Does Not Belong Here

- task data
- catalog inventory
- full doctor reports
- recommendation reports
- verbose change history
- human-learning notes

## Relationship To Other Files

- `.work/catalog/active.yaml` tracks catalog-managed active capabilities only.
- `.work/project-manage/state.toml` tracks the minimal operating-layer state.
- `.work/project-manage/rule-candidates/` stores proposed project rules that are not active yet.
- `.work/features/` tracks feature metadata and feature-scoped task directories.
- Feature close/archive lifecycle is reflected in `.work/features/<feature-id>/feature.toml`, not in `state.toml`.
- `feature.toml` should keep `worktree_path` shared-root-relative, for example `features/<feature-id>`.
- Runtime files still live in:
  - `.agents/skills/`
  - `.codex/agents/`
  - `.codex/config.toml`
  - `.codex/rules/`

## Update Rules

- Create or repair `state.toml` during bootstrap or repair.
- Update it after confirmed runtime-layer changes such as install, remove, promote, bootstrap, repair, or managed import.
- Do not use this state file to track per-feature execution progress.
- Keep it concise and stable.
- Do not turn it into a log or audit trail.
