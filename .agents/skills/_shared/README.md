# Shared Skill Helpers

This directory holds implementation support shared by multiple workflow skills.

It is part of the skill layer, not the working-data layer.

## Purpose

Use these helpers behind the core workflow skills to:

- read task and human-learning metadata without loading full files
- update frontmatter and selected fixed sections deterministically
- keep canonical section order stable
- resolve Codex session transcripts and extract visible conversation messages

## Runtime

- Preferred runtime: `python3`
- Dependency policy: standard library only
- Fallback: if `python3` is unavailable or a helper fails, follow the same file contracts manually

## Scripts

The shared scripts live under:

- `.agents/skills/_shared/scripts/`

Current helpers:

- `task_records.py`
- `human_learning.py`
- `session_records.py`
- `_recordlib.py`

## Scope

These helpers support TOML frontmatter for:

- `.work/features/<feature-id>/tasks/*.md`
- `.work/human-learning/items/*.md`

They do not manage catalog item metadata. The catalog keeps sidecar YAML files.

When invoked from inside `features/<feature-id>/`, the helpers should auto-detect:

- the current feature id
- the shared root
- the shared feature task directory

## Payload Model

Write helpers accept a JSON payload file with this general shape:

```json
{
  "title": "Record title",
  "metadata": {
    "summary": "Short summary"
  },
  "sections": {
    "Current State": "Updated text"
  }
}
```

Rules:

- `title` is optional on update and required on creation
- `metadata` only changes the keys you provide
- `sections` only changes the named sections you provide
- managed timestamps are filled automatically when omitted

## Recommended Use

- `$open-task`
  - prefer metadata-first reads
  - use `task_records.py init` and `task_records.py update` for writes
- `$close-task`
  - use `task_records.py update` for task updates
  - use `human_learning.py review` for relevant item streak updates
- `$learn`
  - use `human_learning.py upsert` for human-learning items
  - use helper-assisted reads to avoid reloading full task files unless needed
  - use `task_records.py learning-candidates` to find completed tasks that are still pending learning
  - use `session_records.py candidates` and `session_records.py read` when transcript-backed learning is needed
