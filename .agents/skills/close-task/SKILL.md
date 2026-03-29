---
name: close-task
description: Use when the user wants to stop work on a task for the current workstream execution directory, end a session, finish a task, or drop a task. Trigger on requests like close task, end session, stop work, finish task, or complete task.
---

# Close Task

Treat the current repository root as the current workstream execution directory.

## Purpose

Close out the current work state for a task in the current workstream, whether the task remains live or becomes closed.

This skill may also do a light review against existing shared human-learning items under the root `.work/learning/human/`.

## Interaction Model

- If invoked with no instruction:
  - enter guided close flow
  - identify the current workstream task candidate
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

- install or remove shared capabilities
- open a new task
- create new human-learning items
- run a full review workflow
- operate from the shared root control plane

## Workflow

1. Resolve workstream context from the current path.
   - if the request is clearly out of scope:
     - explain the boundary briefly
     - point to the better skill
     - stop without writing
   - if there is no instruction, start guided close flow instead of showing a help page
   - prefer `.agents/skills/_shared/scripts/task_records.py context` when `python3` is available
   - otherwise determine the current workstream from the execution path
2. Identify the task file.
   - if the user gives it directly, use it
   - otherwise prefer `.agents/skills/_shared/scripts/task_records.py list` for metadata-first search when `python3` is available
   - if the helper is unavailable, search the shared workstream task directory directly
   - if multiple candidates are plausible, ask
3. Read the task file.
   - prefer `.agents/skills/_shared/scripts/task_records.py read` with metadata and only the sections needed for closure when `python3` is available
   - otherwise read the task file directly
   - confirm that the task belongs to the current workstream
4. Collect the session outcome:
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
5. If shared `.work/learning/human/` exists:
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
6. Prepare a brief preview:
   - workstream id
   - fields to update
   - any human-learning item updates
   - whether `Final Outcome` and `closed` will be written
7. Ask for confirmation.
8. After confirmation:
   - update the shared task file
   - update any confirmed human-learning items
   - append one concise important event when meaningful
   - keep `session_refs` aligned with the current workstream session when helper-driven writes are available
   - if status is `done` or `dropped`, write `Final Outcome` and set `closed`
   - otherwise keep `Final Outcome` empty and `closed` unset
   - keep the file in the same workstream task directory

## Writing Rules

- Preview before writing.
- Refuse to operate when started from the shared root instead of a workstream execution directory.
- Do not close or update a task that belongs to a different workstream.
- Keep `Important Events` concise and append-only.
- Do not create an archive move; closed tasks remain in the same workstream task directory.
- Do not mark learning as captured from this skill; use `$learn` for that.
- Keep human-learning review brief and relevant.
- Only update existing human-learning items from this skill.
- Never delete human-learning files from this skill.
- When a human-learning item is no longer needed, set `status: delete` instead of removing it.
- Prefer helper-driven metadata and selected-section updates; fall back to manual edits only when needed.
- Return the final task path after the update.
