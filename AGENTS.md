# Workstream Control Plane Guide

## Scope

- This root is the shared control plane for one private workspace with multiple workstreams.
- Treat `workstreams/<workstream-id>/` as execution directories, not as copied projects.

## Core Layout

- `workstreams/` stores execution directories, one per workstream.
- `.work/workstreams/` stores shared workstream metadata, shared task records, and shared session registry files.
- `.work/docs/` stores shared reference material for workstreams and tasks.
- `.work/catalog/` stores reusable capability sources and active inventory.
- `.work/learning/` stores shared learning material that still needs human review.
- `.work/state.toml` stores the minimal root control-plane state.
- `.tmp/` stores shared staged input.
- Root `.agents/skills/` is the shared skill source for this control plane.

## Primary Interface

- At root, use `$workstream-manage` as the main workflow surface.
- `$workstream-manage` is root-only and should refuse to run from inside workstream execution directories.
- `$open-task` and `$close-task` are workstream-execution skills, not root skills.
- `$learn` may be used from root or workstream execution directories and writes to shared durable locations.
- All shipped workflow skills are manual-only and must not be implicitly invoked.

## Read Order

- Start here for root behavior.
- For the shared working-data layout, read `.work/README.md`.
- For workstream execution rules, read `workstreams/README.md`.
- For shared workstream metadata and task rules, read `.work/workstreams/README.md`.
- For shared reference material, read `.work/docs/README.md`.
- For catalog rules, read `.work/catalog/README.md`.
- For shared learning rules, read `.work/learning/README.md`.
- For human-learning rules, read `.work/learning/human/README.md`.
- For shared rule candidates, read `.work/learning/rule-candidates/README.md`.
- For shared helper behavior, read `.agents/skills/_shared/README.md`.
- For staged input rules, read `.tmp/README.md`.

## High-Priority Rules

- `README.md` files are human-facing; `AGENTS.md` files are model-facing.
- Root owns shared control-plane state. Workstream directories own execution only.
- `workstream-manage` is the only root-level workstream and capability management entrypoint.
- `workstream-manage` also owns workstream close/archive lifecycle at the shared root.
- Keep `workstream.toml.execution_path` shared-root-relative, for example `workstreams/<workstream-id>`.
- `open-task` and `close-task` should refuse to run from root.
- `learn` may run from root to learn from completed workstream tasks and related transcripts.
- Every task belongs to exactly one workstream.
- Store task records only under `.work/workstreams/<workstream-id>/tasks/`.
- Do not recreate a root-level global task pool.
- Keep long-lived non-code material in the shared root layer, not inside workstream execution directories.
- Execution directories still need a local runtime shell:
  - `AGENTS.md`
  - `.agents/skills/`
  - `.codex/`
- Do not create workstream-local `.tmp/`; `.tmp/` belongs to the shared root only.
- Shared skills should be exposed into each workstream through local discoverable entries.
- Catalog, shared docs, and shared learning data are shared across workstreams at the root layer.
- `.tmp/` is shared, flat staging. Do not proactively scan it.
- Keep this operating layer private by default unless the user explicitly asks to prepare shared versions.

## Done Means

- Root remains the shared control plane.
- Workstream execution directories remain isolated execution spaces.
- Task records remain shared, workstream-scoped, and resumable.
- Shared long-lived knowledge stays outside workstream execution directories.
