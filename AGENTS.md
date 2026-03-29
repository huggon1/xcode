# Project Control Plane Guide

## Scope

- This root is the shared control plane for one project with multiple feature worktrees.
- Treat `features/<feature-id>/` as execution workspaces, not as copied projects.

## Core Layout

- `features/` stores git worktrees, one per feature branch.
- `.work/features/` stores shared feature metadata and shared task records.
- `.work/specs/` stores long-lived shared specs.
- `.work/dependencies/` stores shared cross-feature dependency notes when metadata alone is not enough.
- `.work/catalog/` stores reusable capability sources and active inventory.
- `.work/human-learning/` stores shared private human improvement material.
- `.work/project-manage/` stores the minimal root control-plane state.
- `.work/project-manage/rule-candidates/` stores candidate project rules that are not active yet.
- `.tmp/` stores shared staged input.
- Root `.agents/skills/` is the shared skill source for this control plane.

## Primary Interface

- At root, use `$project-manage` as the main workflow surface.
- `$project-manage` is root-only and should refuse to run from inside feature worktrees.
- `$open-task` and `$close-task` are feature-worktree skills, not root skills.
- `$learn` may be used from root or feature worktrees and writes to shared durable locations.
- All shipped workflow skills are manual-only and must not be implicitly invoked.

## Read Order

- Start here for root behavior.
- For feature/worktree rules, read [features/README.md](features/README.md).
- For shared feature metadata and task rules, read [.work/features/README.md](.work/features/README.md).
- For shared specs, read [.work/specs/README.md](.work/specs/README.md).
- For shared dependency notes, read [.work/dependencies/README.md](.work/dependencies/README.md).
- For catalog rules, read [.work/catalog/README.md](.work/catalog/README.md).
- For human-learning rules, read [.work/human-learning/README.md](.work/human-learning/README.md).
- For project control-plane state, read [.work/project-manage/README.md](.work/project-manage/README.md).
- For project rule candidates, read [.work/project-manage/rule-candidates/README.md](.work/project-manage/rule-candidates/README.md).
- For shared helper behavior, read [.agents/skills/_shared/README.md](.agents/skills/_shared/README.md).
- For staged input rules, read [.tmp/README.md](.tmp/README.md).

## High-Priority Rules

- `README.md` files are human-facing; `AGENTS.md` files are model-facing.
- Root owns shared control-plane state. Feature worktrees own code execution only.
- `project-manage` is the only root-level feature and capability management entrypoint.
- `project-manage` also owns feature close/archive lifecycle at the shared root.
- Keep `feature.toml.worktree_path` shared-root-relative, for example `features/<feature-id>`.
- `open-task` and `close-task` should refuse to run from root.
- `learn` may run from root to learn from completed feature tasks and related transcripts.
- Every task belongs to exactly one feature.
- Store task records only under `.work/features/<feature-id>/tasks/`.
- Do not recreate a root-level global `.work/tasks/` pool.
- Keep long-lived non-code project material in the shared root layer, not inside feature worktrees.
- Feature worktrees still need a local runtime shell:
  - `AGENTS.md`
  - `.agents/skills/`
  - `.codex/`
- Do not create feature-local `.tmp/`; `.tmp/` belongs to the shared root only.
- Shared skills should be exposed into each feature worktree through local discoverable entries.
- Catalog and human-learning data are shared across features at the root layer.
- `.tmp/` is shared, flat staging. Do not proactively scan it.
- Keep this operating layer private by default unless the user explicitly asks to prepare shared versions.

## Done Means

- Root remains the shared control plane.
- Feature worktrees remain isolated execution spaces.
- Task records remain shared, feature-scoped, and resumable.
- Shared long-lived knowledge stays outside feature worktrees.
