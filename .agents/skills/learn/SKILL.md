---
name: learn
description: Use only when the user explicitly asks to capture a lesson, extract a reusable pattern, save a learning, reflect on how to improve, or turn recent work into a learned skill or a human improvement item.
---

# Learn

Treat the current repository root as the path base for project-local files.

## Purpose

Capture explicit learning from recent work without relying on automatic hooks.

This skill supports two learning outputs:

- a project-local learned skill under `.work/catalog/learned/skills/`
- a private human improvement item under `.work/human-learning/items/`

Use this skill only when the user explicitly asks to learn, capture a lesson, save a pattern, or reflect on personal improvement.

## Interaction Model

- If invoked with no instruction:
  - enter guided learning triage
  - explain the possible outputs
  - recommend the most likely learning direction from the current context
- If invoked with an in-scope instruction:
  - use that instruction to bias the verdict toward skill, human item, both, or evaluation
- If the instruction is out of scope:
  - say so clearly
  - point to the better skill
  - do not silently switch

## In Scope

- evaluate whether recent work is worth preserving
- save a learned skill
- save a human-improvement item
- save both when both are genuinely useful

## Out Of Scope

Do not use this skill to:

- close a task
- install or enable runtime capabilities
- write project config
- act as an automatic background observer

## Output Verdicts

Choose exactly one verdict before writing:

- `save-skill`
- `save-human-item`
- `both`
- `drop`

## Workflow

1. Identify the learning source:
   - if the request is clearly out of scope:
     - explain the boundary briefly
     - point to the better skill
     - stop without writing
   - if there is no instruction, enter guided learning triage
   - the current task file
   - the recent task outcome
   - the current conversation
   - explicit user notes
2. Determine what is worth preserving:
   - a reusable technical or workflow pattern for future project work
   - a human improvement topic about alignment, blockers, or better collaboration behavior
   - both
3. Inspect overlap before drafting:
   - `.work/catalog/learned/skills/`
   - `.work/catalog/validated/skills/`
   - `.agents/skills/`
   - `.work/human-learning/items/` when a human item is plausible
   - prefer `.agents/skills/_shared/scripts/task_records.py read` or `.agents/skills/_shared/scripts/human_learning.py list/read` when `python3` is available and a metadata-first read is enough
4. Decide the verdict:
   - `save-skill` for a reusable project pattern
   - `save-human-item` for a private human improvement topic
   - `both` when both outputs are genuinely useful
   - `drop` when the lesson is trivial, one-off, or already covered
5. For a learned skill:
   - create or update `.work/catalog/learned/skills/<id>/`
   - write `SKILL.md`
   - write `catalog.yaml`
   - keep it in the `learned` layer
   - do not auto-install it into `.agents/skills/` unless the user explicitly asks
6. For a human item:
   - create or update `.work/human-learning/items/<id>.md`
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
7. If there is clear overlap:
   - prefer updating the existing learned skill or human item
   - do not create duplicates
8. Prepare a brief preview:
   - verdict
   - target paths
   - whether this is a new item or an update
   - the core lesson being preserved
9. Ask for confirmation.
10. After confirmation, write only the needed changes.

## Writing Rules

- Do not rely on automatic hook-based observation.
- Keep learned skills focused on one reusable pattern.
- Keep human items focused on one improvement topic.
- Human items are private by default.
- Do not create or update project runtime config from this skill.
- Do not install a learned skill unless the user explicitly asks.
- Prefer helper-assisted reads and writes when available; fall back to manual edits only when needed.
- If the right answer is `drop`, explain why and do not write files.
