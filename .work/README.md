# Shared Working Data

`.work/` stores the shared durable data layer for this workspace.

It does not store execution directories or local runtime shells.

## Structure

```text
.work/
├── workstreams/
├── docs/
├── catalog/
├── learning/
└── state.toml
```

## What Each Part Does

- `workstreams/`
  - shared workstream metadata
  - shared task records
  - shared session registry files
- `docs/`
  - shared reference material that workstreams or tasks may cite
- `catalog/`
  - reusable capability sources and active inventory
- `learning/`
  - shared learning material that still needs human review
- `state.toml`
  - the smallest shared runtime-state record for the root control plane

## Rules

- keep code execution state out of `.work/`
- keep task truth under `.work/workstreams/`
- keep reference material under `.work/docs/`
- keep reviewable learning under `.work/learning/`
- keep runtime-state metadata minimal in `.work/state.toml`
