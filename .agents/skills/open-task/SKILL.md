---
name: open-task
description: Use when the user wants to start or resume a task for the current feature worktree. Trigger on requests like open task, start task, continue task, resume task, start session, or resume session.
---

# Open Task

Treat the current repository root as the current feature worktree.

## Purpose

Open the right task record for work, either by creating a new task file or by resuming an existing one for the current feature.

## Interaction Model

- If invoked with no instruction:
  - inspect the current feature task directory in the shared root
  - explain that this skill can create or resume a task for the current feature
  - recommend the most likely next step
  - show a few concrete examples
- If invoked with an in-scope instruction:
  - start that direction directly
  - only ask for the missing high-impact detail
- If the instruction is in-scope but vague:
  - continue with the most likely intent
  - ask only when multiple task candidates remain plausible
- If the instruction is out of scope:
  - say so clearly
  - point to the better skill
  - do not silently switch

## In Scope

- create a new task for the current feature
- resume an existing task for the current feature
- turn rough notes or explicit staged material into a task record for the current feature

## Out Of Scope

Do not use this skill to:

- create or manage feature branches
- install or remove project capabilities
- close a task
- run project-level health checks
- operate from the shared root control plane

## Preconditions

This skill must run from inside `features/<feature-id>/`.

The shared root layer must already exist, including:

- `.work/features/<feature-id>/tasks/`

If the current path is not inside a feature worktree:

- stop
- tell the user to use `$project-manage` at root or enter the correct feature worktree first

## Workflow

1. Resolve feature context from the current path:
   - prefer `.agents/skills/_shared/scripts/task_records.py context` when `python3` is available
   - otherwise determine:
     - `feature_id`
     - feature worktree root
     - shared root
     - shared task directory
2. If the request is clearly out of scope:
   - explain the boundary briefly
   - point to the better skill
   - stop without writing
3. If there is no instruction:
   - inspect recent task records for the current feature only
   - explain whether a resume or a new task looks more likely
   - show a few examples
   - then stop without writing
4. Decide whether this is a new task or an existing one:
   - prefer `.agents/skills/_shared/scripts/task_records.py list` for metadata-first search when `python3` is available
   - otherwise search the shared feature task directory directly
   - if there is a clear existing task, prefer resume
   - if there are multiple plausible candidates, ask
   - if there is no good candidate, create a new task
5. For a new task:
   - collect title, goal, out of scope when needed, inputs, constraints, relevant paths, current state, next step, and optional tags
   - propose a filename using `YYYY-MM-DD-task-slug.md`
   - create the file under `.work/features/<feature-id>/tasks/` in the shared root
   - create TOML frontmatter with:
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
   - default `feature_id` to the current feature
   - default `status` to `active` when the user is starting work now
   - default `learning_status` to `pending`
   - use `planned` only when the user explicitly wants to park the task before active work starts
   - leave `closed` empty on creation
   - build the task file with these sections in order:
     - `# Title`
     - `## Goal`
     - `## Out of Scope` when needed
     - `## Inputs / Constraints`
     - `## Relevant Paths`
     - `## Current State`
     - `## Active Decisions`
     - `## Open Issues`
     - `## Next Step`
     - `## Final Outcome`
     - `## Important Events`
   - prefer `.agents/skills/_shared/scripts/task_records.py init` for creation when `python3` is available
   - if the helper is unavailable, write the file manually using the same contract
6. For an existing task:
   - prefer `.agents/skills/_shared/scripts/task_records.py read` with metadata and selected sections when `python3` is available
   - otherwise read the task file directly
   - confirm that the task belongs to the current feature
   - summarize the current state, open issues, next step, and status
   - only prepare a file update if something needs to change
7. Prepare a brief preview:
   - feature id
   - task path
   - create vs resume
   - the most important fields to write or update
8. Ask for confirmation.
9. After confirmation, write only the needed changes.

## Writing Rules

- Preview before writing.
- Refuse to operate when started from the shared root instead of a feature worktree.
- Do not create a duplicate task if a matching active task already exists in the same feature.
- Do not open or update a task that belongs to a different feature.
- Prefer minimal updates when resuming an existing task.
- If no task-file change is needed, do not rewrite the file.
- Keep `session_refs` attached to the current feature session when helper-driven writes are available.
- Leave `Final Outcome` empty until the task is closed as `done` or `dropped`.
- Keep `Important Events` limited to meaningful turning points, not a full session log.
- Prefer the helper for frontmatter and selected-section updates; fall back to manual edits only when needed.
- After success, point the user to the reading order:
  - the feature worktree `AGENTS.md`
  - the shared task file
  - deeper project files only if needed
