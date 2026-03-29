# Single-Project Codex Guide

## Scope

- This directory is the maintained, reusable single-project Codex root.
- Treat the root as one project workspace, not as a multi-project control plane.

## Core Layout

- `AGENTS.md` is the root instruction file for this project.
- `.agents/skills/` stores active project skills.
- `.codex/` stores active project config, subagents, and rules.
- `.work/tasks/` stores durable task records.
- `.work/catalog/` stores reusable capability sources and active inventory.
- `.work/project-manage/` stores the minimal project control-plane state.
- `.work/human-learning/` stores private human improvement material.
- `.agents/skills/_shared/` stores helper infrastructure shared by multiple workflow skills.
- `.tmp/` stores temporary user-provided files waiting to be processed.

## Primary Interface

- Prefer these skills as the main workflow surface:
  - `$project-manage`
  - `$open-task`
  - `$close-task`
- `$learn` is an optional manual learning skill.
- These shipped workflow skills are manual-only and should not be implicitly invoked.
- Treat the files as the durable source of truth and the skills as guided entrypoints.
- Workflow skills follow one interaction protocol:
  - if invoked without an instruction, explain what the skill can do, recommend the most useful next step, and show a few concrete examples
  - if invoked with an in-scope instruction, start that direction immediately
  - if invoked with an ambiguous but in-scope instruction, continue with the most likely intent and ask only for the missing high-impact detail
  - if invoked with an out-of-scope instruction, say so clearly and point to the better skill instead of silently switching

## Read Order

- Start here for root-level behavior.
- For task-file structure and rules, read [.work/tasks/README.md](/home/duu/code/mycodex/workspace/.work/tasks/README.md).
- For catalog structure and runtime materialization rules, read [.work/catalog/README.md](/home/duu/code/mycodex/workspace/.work/catalog/README.md).
- For project runtime state rules, read [.work/project-manage/README.md](/home/duu/code/mycodex/workspace/.work/project-manage/README.md).
- For human-learning item rules, read [.work/human-learning/README.md](/home/duu/code/mycodex/workspace/.work/human-learning/README.md).
- For shared helper scripts and fallback behavior, read [.agents/skills/_shared/README.md](/home/duu/code/mycodex/workspace/.agents/skills/_shared/README.md).
- For staged input behavior, read [.tmp/README.md](/home/duu/code/mycodex/workspace/.tmp/README.md).
- Load deeper project files only when the current task actually needs them.

## High-Priority Rules

- `README.md` files are human-facing; `AGENTS.md` files are model-facing.
- Do not invent generic docs, templates, plans, registries, or archive folders for this baseline.
- Keep active runtime capabilities in standard root paths:
  - skills under `.agents/skills/`
  - subagents under `.codex/agents/`
  - config in `.codex/config.toml`
  - rules under `.codex/rules/`
- `project-manage` is the only project-level capability-management entrypoint.
- Treat `project-manage` as the project control plane:
  - health checking
  - capability recommendations
  - explaining the current setup
  - installing, removing, promoting, importing, repairing, or bootstrapping capabilities
- Keep project control-plane state small and separate:
  - `.work/catalog/active.yaml` tracks catalog-managed active items
  - `.work/project-manage/state.toml` tracks minimal operating-layer state
- Task files under `.work/tasks/` are the main durable record of active work.
- Catalog items under `.work/catalog/` are source material until intentionally materialized into the runtime layer.
- Human-learning items under `.work/human-learning/` are private working material, not active project capabilities.
- For structured task and human-learning operations, prefer the shared helpers under `.agents/skills/_shared/` when available.
- If a helper is unavailable or fails, follow the same contracts manually instead of changing the file shape.
- `.tmp/` is temporary staging, not durable project knowledge.
- Do not proactively scan `.tmp/` unless the user points to it or asks to organize staged material.
- When staged material is referenced and the destination is not obvious, determine or confirm the best durable destination first.
- Clean processed originals out of `.tmp/` only after successful processing, preview, and confirmation.
- Keep this operating layer private by default unless the user explicitly asks to prepare shared versions.

## Done Means

- The root remains a minimal single-project baseline.
- The workflow skills and the referenced contract files stay aligned.
- Task records remain compact and resumable.
- The catalog stays separate from the active runtime layer.
