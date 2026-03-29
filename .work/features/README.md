# Feature Records

This directory stores shared feature metadata and shared task records.

Each feature gets its own shared bucket under `.work/features/`.

## Structure

```text
.work/features/
└── <feature-id>/
    ├── feature.toml
    └── tasks/
```

## Feature Metadata

Each feature directory should include:

- `.work/features/<feature-id>/feature.toml`

Minimum fields:

- `feature_id`
- `title`
- `branch`
- `base_branch`
- `worktree_path`
- `status`
- `closed_at`
- `summary`
- `created_at`
- `updated_at`
- `spec_refs`
- `depends_on_features`
- `blocked_by_features`

Rules:

- `feature_id` must match the feature directory name.
- `branch` should be the branch checked out by `features/<feature-id>/`.
- `worktree_path` should point to the matching execution directory.
- Store `worktree_path` as a shared-root-relative path such as `features/<feature-id>`.
- Keep dependency fields explicit and lightweight.

Suggested `status` values:

- `active`
- `blocked`
- `merged`
- `abandoned`
- `archived`

## Task Location

Store feature tasks at:

- `.work/features/<feature-id>/tasks/YYYY-MM-DD-task-slug.md`

Every task belongs to exactly one feature.

There is no root-level global task pool in this model.

## Task Metadata

Each task file should use TOML frontmatter delimited by `+++`.

Use these metadata fields:

- `id`
- `feature_id`
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

- Treat the task file as the only durable dynamic record of active work for that feature.
- Do not create separate state files or plan files for task execution.
- Keep `feature_id` aligned with the containing feature directory.
- Keep `summary` and `next_action` useful enough for metadata-first resume.
- Keep `learning_status`, `learning_refs`, and `session_refs` current enough for transcript-backed root learning.
- Keep `Current State`, `Open Issues`, and `Next Step` useful for resume.
- Keep `Final Outcome` empty until the task is closed as `done` or `dropped`.
- Use `Important Events` only for meaningful turning points, not a full session diary.
- Update `updated` on every meaningful edit.
- Set `closed` only when `status` becomes `done` or `dropped`.
- Closed tasks remain in the same feature task directory; do not move them elsewhere.

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

- Use `$open-task` only from inside a feature worktree.
- Use `$close-task` only from inside a feature worktree.
- Use `$learn` from root or a feature worktree when you want to learn from feature work.
- These skills should write to the shared feature task directory, not to the local worktree.
- Use [.agents/skills/_shared/scripts/task_records.py](../../.agents/skills/_shared/scripts/task_records.py) behind those skills when structured reads or precise partial writes are needed.
- Use [.agents/skills/_shared/scripts/session_records.py](../../.agents/skills/_shared/scripts/session_records.py) when a completed task needs transcript-backed learning.
- Do not duplicate active tasks when a matching active task already exists in the same feature.
