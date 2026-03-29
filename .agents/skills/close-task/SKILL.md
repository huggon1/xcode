---
name: close-task
description: Use when the user wants to stop work on a task, end a session, finish a task, or drop a task. Trigger on requests like close task, end session, stop work, finish task, or complete task.
---

# Close Task

Treat the current repository root as the path base for all files mentioned below.

## Purpose

Close out the current work state for a task, whether the task remains live or becomes closed.

This skill may also do a light review against existing human-learning items under `.work/human-learning/items/` when that directory exists.

## Interaction Model

- If invoked with no instruction:
  - enter guided close flow
  - identify the current task candidate
  - ask only for the minimum task-closing information
- If invoked with an in-scope instruction:
  - use that instruction to bias the close direction
  - examples include `done`, `blocked`, `pause`, or `drop`
- If the instruction is out of scope:
  - say so clearly
  - point to the better skill
  - do not silently switch

## In Scope

- pause a task while keeping it active
- mark a task as blocked
- mark a task as done
- mark a task as dropped

## Out Of Scope

Do not use this skill to:

- install or remove project capabilities
- open a new task
- create new human-learning items
- run a full review workflow

## Workflow

1. Identify the task file.
   - if the request is clearly out of scope:
     - explain the boundary briefly
     - point to the better skill
     - stop without writing
   - if there is no instruction, start guided close flow instead of showing a help page
   - if the user gives it directly, use it
   - otherwise prefer `.agents/skills/_shared/scripts/task_records.py list` for metadata-first search when `python3` is available
   - if the helper is unavailable, search `.work/tasks/` directly
   - if multiple candidates are plausible, ask
2. Read the task file.
   - prefer `.agents/skills/_shared/scripts/task_records.py read` with metadata and only the sections needed for closure when `python3` is available
   - otherwise read the task file directly
3. Collect the session outcome:
   - current state
   - active decisions
   - open issues
   - next step
   - meaningful event text
   - target status:
     - `planned`
     - `active`
     - `blocked`
     - `done`
     - `dropped`
   - prefer:
     - `active` when work should continue next time
     - `blocked` when progress depends on an unresolved blocker
     - `done` when the task is complete
     - `dropped` when the task is intentionally abandoned
     - `planned` only when the task is being parked before active work resumes
4. If `.work/human-learning/items/` exists:
   - prefer `.agents/skills/_shared/scripts/human_learning.py list --status active` when `python3` is available
   - inspect only `status: active` items
   - consider only items clearly relevant to the task that is being closed
   - classify each relevant item as:
     - `met`
     - `missed`
     - `not-applicable`
   - for metadata updates, prefer `.agents/skills/_shared/scripts/human_learning.py review`
   - for `met`:
     - increment `success_streak`
     - update `updated`
   - for `missed`:
     - reset `success_streak` to `0`
     - update `updated`
   - if `success_streak` reaches or exceeds `retire_after`, ask whether to set `status: delete`
   - do not create new human-learning items; use `$learn` for that
5. Prepare a brief preview:
   - fields to update
   - any human-learning item updates
   - whether `Final Outcome` and `closed` will be written
6. Ask for confirmation.
7. After confirmation:
   - update the task file
   - update any confirmed human-learning items
   - append one concise important event when meaningful
   - if status is `done` or `dropped`, write `Final Outcome` and set `closed`
   - otherwise keep `Final Outcome` empty and `closed` unset
   - keep the file in `.work/tasks/`

## Writing Rules

- Preview before writing.
- Keep `Important Events` concise and append-only.
- Do not create an archive move; closed tasks remain in `.work/tasks/`.
- Keep human-learning review brief and relevant.
- Only update existing human-learning items from this skill.
- Never delete human-learning files from this skill.
- When a human-learning item is no longer needed, set `status: delete` instead of removing it.
- Prefer helper-driven metadata and selected-section updates; fall back to manual edits only when needed.
- Return the final task path after the update.
