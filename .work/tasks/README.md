# Task Records

Task files are the main durable record of active work in this project root.

## Location

Store task files at:

- `.work/tasks/YYYY-MM-DD-task-slug.md`

## Metadata

Each task file should use TOML frontmatter delimited by `+++`.

Use these metadata fields:

- `id`
- `status`
- `created`
- `updated`
- `closed`
- `priority`
- `task_type`
- `tags`
- `related_paths`
- `source_refs`
- `summary`
- `next_action`

Allowed `status` values:

- `planned`
- `active`
- `blocked`
- `done`
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

- Treat the task file as the only durable dynamic record of active work.
- Do not create separate state files or plan files for this baseline.
- Keep `summary` and `next_action` useful enough for metadata-first resume.
- Keep `Current State`, `Open Issues`, and `Next Step` useful for resume.
- Keep `Final Outcome` empty until the task is closed as `done` or `dropped`.
- Use `Important Events` only for meaningful turning points, not a full session diary.
- Update `updated` on every meaningful edit.
- Set `closed` only when `status` becomes `done` or `dropped`.
- Closed tasks remain in `.work/tasks/`; do not move them elsewhere.

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

- Use `$open-task` to create or resume task files.
- Use `$close-task` to update task outcome and closure state.
- Use [.agents/skills/_shared/scripts/task_records.py](/home/duu/code/mycodex/workspace/.agents/skills/_shared/scripts/task_records.py) behind those skills when structured reads or precise partial writes are needed.
- Do not duplicate active tasks when a matching active task already exists.
