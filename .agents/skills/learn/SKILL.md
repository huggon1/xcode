---
name: learn
description: Use only when the user explicitly asks to capture a lesson, extract a reusable pattern, save a learning, reflect on how to improve, or turn recent work into a learned skill, a human improvement item, or a project rule candidate.
---

# Learn

Treat the current repository root as either:

- the shared root control plane
- or a feature worktree that writes to shared durable locations

## Purpose

Capture explicit learning from recent work without relying on automatic hooks.

This skill supports three learning outputs:

- a shared learned skill under `.work/catalog/learned/skills/`
- a shared private human improvement item under `.work/human-learning/items/`
- a shared project rule candidate under `.work/project-manage/rule-candidates/`

Use this skill only when the user explicitly asks to learn, capture a lesson, save a pattern, or reflect on personal improvement.

## Interaction Model

- If invoked with no instruction:
  - enter guided learning triage
  - explain the possible outputs
  - recommend the most likely learning direction from the current context
  - at root, prefer selecting a completed task that is still pending learning
- If invoked with an in-scope instruction:
  - use that instruction to bias the output toward skill, human item, project rule, multi-output, or evaluation
- If the instruction is out of scope:
  - say so clearly
  - point to the better skill
  - do not silently switch

## In Scope

- evaluate whether recent work is worth preserving
- save a learned skill
- save a human-improvement item
- save a project-rule candidate
- save multiple outputs when multiple outputs are genuinely useful

## Out Of Scope

Do not use this skill to:

- close a task
- install or enable runtime capabilities
- write project config
- act as an automatic background observer

## Output Decisions

Choose exactly one decision before writing:

- `save-skill`
- `save-human-item`
- `save-project-rule`
- `multi`
- `drop`

If the decision is `multi`, explicitly list the selected targets from:

- `skill`
- `human-item`
- `project-rule`

## Workflow

1. Identify the learning source:
   - if the request is clearly out of scope:
     - explain the boundary briefly
     - point to the better skill
     - stop without writing
   - if there is no instruction, enter guided learning triage
   - possible source modes:
     - the current task file
     - the recent task outcome
     - the current conversation
     - explicit user notes
     - a completed task selected from the shared root
     - a transcript selected from the Codex session store
2. Resolve the durable shared destination:
   - if running inside a feature worktree, use the shared root derived from the current feature context
   - if running at root, use the root shared layer directly
3. If running at root and no explicit source is given:
   - prefer `.agents/skills/_shared/scripts/task_records.py learning-candidates` when `python3` is available
   - look for tasks with:
     - `status: done`
     - `learning_status: pending`
   - choose the most recent relevant task, or ask when several are plausible
4. Read the task context first when a task is involved:
   - prefer `.agents/skills/_shared/scripts/task_records.py read`
   - use metadata-first reads when possible
   - read the task outcome, important events, current summary, and next action before opening transcripts
5. Resolve transcript candidates when a task is involved or when the user explicitly asks for transcript-backed learning:
   - prefer `.agents/skills/_shared/scripts/session_records.py candidates --task-path <task>`
   - if `session_refs` exist on the task, treat them as the primary source
   - otherwise infer likely transcripts from feature path, task timestamps, and task keywords
   - if good transcript candidates exist, read only the selected candidates
   - prefer `.agents/skills/_shared/scripts/session_records.py read` to extract visible conversation messages instead of loading raw JSONL
   - if no good transcript candidates exist, continue with task-only learning
6. Determine what is worth preserving:
   - a reusable technical or workflow pattern for future project work
   - a human improvement topic about alignment, blockers, or better collaboration behavior
   - a project-specific rule candidate that may later belong in `AGENTS.md`
   - any combination of the above
7. Inspect overlap before drafting:
   - inspect:
     - `.work/catalog/learned/skills/`
     - `.work/catalog/validated/skills/`
     - the shared `.agents/skills/` source
     - `.work/human-learning/items/` when a human item is plausible
     - `.work/project-manage/rule-candidates/` when a project rule is plausible
8. Decide the output:
   - `save-skill` for a reusable project pattern
   - `save-human-item` for a private human improvement topic
   - `save-project-rule` for a stable project-specific rule candidate
   - `multi` when more than one output is genuinely useful
   - `drop` when the lesson is trivial, one-off, or already covered
9. For a learned skill:
   - create or update `.work/catalog/learned/skills/<id>/` in the shared root
   - write `SKILL.md`
   - write `catalog.yaml`
   - keep it in the `learned` layer
   - do not auto-install it into `.agents/skills/` unless the user explicitly asks
10. For a human item:
   - create or update `.work/human-learning/items/<id>.md` in the shared root
   - use TOML frontmatter with:
     - `id`
     - `status`
     - `created`
     - `updated`
     - `success_streak`
     - `retire_after`
     - `scope`
     - `tags`
     - `applies_to`
     - `summary`
   - default:
     - `status: active`
     - `success_streak: 0`
     - `retire_after: 3`
   - use section order:
     - `# Title`
     - `## Why This Matters`
     - `## Applies When`
     - `## Better Behavior`
     - `## Success Signals`
     - `## Failure Signals`
     - `## Notes`
   - prefer `.agents/skills/_shared/scripts/human_learning.py upsert` for writes when `python3` is available
   - if the helper is unavailable, write the file manually using the same contract
11. For a project rule candidate:
   - create or update `.work/project-manage/rule-candidates/<id>.md`
   - use TOML frontmatter with:
     - `id`
     - `status`
     - `created`
     - `updated`
     - `target_scope`
     - `target_feature`
     - `source_tasks`
     - `source_sessions`
     - `summary`
   - keep these as candidates, not active rules
   - do not modify `AGENTS.md` from this skill
12. If there is clear overlap:
   - prefer updating the existing learned skill, human item, or project rule candidate
   - do not create duplicates
13. If learning came from a task:
   - update the task metadata after confirmation
   - for preserved outputs:
     - set `learning_status: captured`
     - append the created relative paths to `learning_refs`
   - for `drop`:
     - set `learning_status: dropped`
14. Prepare a brief preview:
   - selected output decision
   - target paths
   - whether each target is new or an update
   - the core lesson being preserved
   - whether the source task will be marked as `captured` or `dropped`
15. Ask for confirmation.
16. After confirmation, write only the needed changes.

## Writing Rules

- Do not rely on automatic hook-based observation.
- Keep learned skills focused on one reusable pattern.
- Keep human items focused on one improvement topic.
- Keep project rule candidates focused on one stable rule proposal.
- Human items are private by default.
- Project rule candidates are not active runtime rules.
- Do not create or update project runtime config from this skill.
- Do not modify `AGENTS.md` directly from this skill.
- Do not install a learned skill unless the user explicitly asks.
- Prefer helper-assisted reads and writes when available; fall back to manual edits only when needed.
- If the right answer is `drop`, explain why and do not write learning files.
