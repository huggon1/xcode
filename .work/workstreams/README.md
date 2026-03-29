# Workstream Records

This directory stores shared workstream metadata, shared task records, and shared session identity records.

Each workstream gets its own shared bucket under `.work/workstreams/`.

## Structure

```text
.work/workstreams/
└── <workstream-id>/
    ├── workstream.toml
    ├── tasks/
    └── sessions/
```

## Workstream Metadata

Each workstream directory should include:

- `.work/workstreams/<workstream-id>/workstream.toml`

Minimum fields:

- `workstream_id`
- `type`
- `title`
- `execution_path`
- `status`
- `closed_at`
- `summary`
- `created_at`
- `updated_at`
- `doc_refs`
- `depends_on_workstreams`
- `blocked_by_workstreams`

For `repo` workstreams, also keep:

- `branch`
- `base_branch`

Rules:

- `workstream_id` must match the workstream directory name.
- `execution_path` should point to the matching execution directory.
- Store `execution_path` as a shared-root-relative path such as `workstreams/<workstream-id>`.
- Keep dependency fields explicit and lightweight.

Supported `status` values:

- `active`
- `blocked`
- `completed`
- `abandoned`
- `archived`

## Task Location

Store workstream tasks at:

- `.work/workstreams/<workstream-id>/tasks/YYYY-MM-DD-task-slug.md`

Every task belongs to exactly one workstream.

There is no root-level global task pool in this model.

## Session Registry

Store shared session identity records at:

- `.work/workstreams/<workstream-id>/sessions/<session-id>.toml`

Each session record should keep:

- `session_id`
- `workstream_id`
- `task_id`
- `label`
- `started_at`
- `updated_at`
- `execution_path`

These records are the primary session identity layer for this baseline.

## Task Metadata

Each task file should use TOML frontmatter delimited by `+++`.

Use these metadata fields:

- `id`
- `workstream_id`
- `status`
- `learning_status`
- `created`
- `updated`
- `closed`
- `priority`
- `task_type`
- `tags`
- `related_paths`
- `source_refs`
- `learning_refs`
- `session_refs`
- `summary`
- `next_action`

Allowed `status` values:

- `planned`
- `active`
- `blocked`
- `done`
- `dropped`

Allowed `learning_status` values:

- `pending`
- `captured`
- `dropped`

Keep the frontmatter flat:

- scalars
- integers
- arrays of strings

Do not introduce nested tables.

## Section Order

Use this section order:

- `# Title`
- `## Goal`
- `## Out of Scope` when boundary control matters
- `## Inputs / Constraints`
- `## Relevant Paths`
- `## Current State`
- `## Active Decisions`
- `## Open Issues`
- `## Next Step`
- `## Final Outcome`
- `## Important Events`

## Writing Rules

- Treat the task file as the only durable dynamic record of active work for that workstream.
- Do not create separate state files or plan files for task execution.
- Keep `workstream_id` aligned with the containing workstream directory.
- Keep `summary` and `next_action` useful enough for metadata-first resume.
- Keep `learning_status`, `learning_refs`, and `session_refs` current enough for transcript-backed root learning.
- Keep `Current State`, `Open Issues`, and `Next Step` useful for resume.
- Keep `Final Outcome` empty until the task is closed as `done` or `dropped`.
- Use `Important Events` only for meaningful turning points, not a full session diary.
- Update `updated` on every meaningful edit.
- Set `closed` only when `status` becomes `done` or `dropped`.
- Closed tasks remain in the same workstream task directory; do not move them elsewhere.

## Managed Update Surface

The internal helper layer may update these parts directly:

- all frontmatter fields
- `## Current State`
- `## Open Issues`
- `## Next Step`
- `## Final Outcome`
- `## Important Events`

The rest of the body stays model-authored unless the user asks otherwise.

## Workflow

- Use `$open-task` only from inside a workstream execution directory.
- Use `$close-task` only from inside a workstream execution directory.
- Use `$learn` from root or a workstream execution directory when you want to learn from workstream work.
- These skills should write to the shared workstream task directory, not to the local execution directory.
- Use `.agents/skills/_shared/scripts/task_records.py` behind those skills when structured reads or precise partial writes are needed.
- Use `.agents/skills/_shared/scripts/session_records.py` when a completed task needs transcript-backed learning.
- Do not duplicate active tasks when a matching active task already exists in the same workstream.
