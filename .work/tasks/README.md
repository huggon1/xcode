# Task Records

Task files are the main durable record of active work in this project root.

## Location

Store task files at:

- `.work/tasks/YYYY-MM-DD-task-slug.md`

## Metadata

Each task file should use YAML frontmatter with:

- `status`
- `created`
- `updated`
- `closed`
- `tags`

Allowed `status` values:

- `planned`
- `active`
- `blocked`
- `done`
- `dropped`

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
- Keep `Current State`, `Open Issues`, and `Next Step` useful for resume.
- Keep `Final Outcome` empty until the task is closed as `done` or `dropped`.
- Use `Important Events` only for meaningful turning points, not a full session diary.
- Update `updated` on every meaningful edit.
- Set `closed` only when `status` becomes `done` or `dropped`.
- Closed tasks remain in `.work/tasks/`; do not move them elsewhere.

## Workflow

- Use `$open-task` to create or resume task files.
- Use `$close-task` to update task outcome and closure state.
- Do not duplicate active tasks when a matching active task already exists.
