---
name: open-task
description: Use when the user wants to start a new task or resume an existing task for the current project. Trigger on requests like open task, start task, continue task, resume task, start session, or resume session.
---

# Open Task

Treat the current repository root as the path base for all files mentioned below.

## Purpose

Open the right task record for work, either by creating a new task file or by resuming an existing one.

## Interaction Model

- If invoked with no instruction:
  - inspect `.work/tasks/`
  - explain that this skill can create, resume, or normalize a task record
  - recommend the most likely next step
  - show a few concrete examples
- If invoked with an in-scope instruction:
  - start that direction directly
  - only ask for the missing high-impact detail
- If the instruction is in-scope but vague:
  - continue with the most likely intent
  - ask only when multiple task candidates or task directions remain plausible
- If the instruction is out of scope:
  - say so clearly
  - point to the better skill
  - do not silently switch

## In Scope

- create a new task
- resume an existing task
- turn rough notes or explicit staged material into a task record

## Out Of Scope

Do not use this skill to:

- install or remove project capabilities
- close a task
- run project-level health checks

## Preconditions

The project operating layer must already exist, including `.work/tasks/`.

If it does not exist:

- stop
- tell the user to run `project-manage` first

## Workflow

1. Verify that `.work/tasks/` exists.
2. If the request is clearly out of scope:
   - explain the boundary briefly
   - point to the better skill
   - stop without writing
3. If there is no instruction:
   - inspect recent task records
   - explain whether a resume or a new task looks more likely
   - show a few examples
   - then stop without writing
4. Decide whether this is a new task or an existing one:
   - prefer `.agents/skills/_shared/scripts/task_records.py list` for metadata-first search when `python3` is available
   - otherwise search `.work/tasks/` directly
   - if there is a clear existing task, prefer resume
   - if there are multiple plausible candidates, ask
   - if there is no good candidate, create a new task
5. For a new task:
   - collect title, goal, out of scope when needed, inputs, constraints, relevant paths, current state, next step, and optional tags
   - propose a filename using `YYYY-MM-DD-task-slug.md`
   - create TOML frontmatter with:
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
   - default `status` to `active` when the user is starting work now
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
   - summarize the current state, open issues, next step, and status
   - only prepare a file update if something needs to change
7. Prepare a brief preview:
   - task path
   - create vs resume
   - the most important fields to write or update
8. Ask for confirmation.
9. After confirmation, write only the needed changes.

## Writing Rules

- Preview before writing.
- Do not create a duplicate task if a matching active task already exists.
- Prefer minimal updates when resuming an existing task.
- If no task-file change is needed, do not rewrite the file.
- Leave `Final Outcome` empty until the task is closed as `done` or `dropped`.
- Keep `Important Events` limited to meaningful turning points, not a full session log.
- Prefer the helper for frontmatter and selected-section updates; fall back to manual edits only when needed.
- After success, point the user to the reading order:
  - `AGENTS.md`
  - the task file
  - deeper project files only if needed
