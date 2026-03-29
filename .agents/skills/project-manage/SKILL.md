---
name: project-manage
description: Use when the user wants to manage the shared root control plane for the current project. Trigger on requests like create feature, inspect features, inspect project setup, doctor the root layer, recommend capabilities, install or remove capabilities, repair the runtime layer, or explain current shared setup.
---

# Project Manage

Treat the current repository root as the shared control plane for one project.

## Purpose

Manage:

- the shared root runtime layer
- feature lifecycle
- shared capability sources
- shared control-plane health

This skill is responsible for project-level and feature-level management, not task execution.

This skill is root-only. Do not use it from inside `features/<feature-id>/`.

## Interaction Model

- If invoked with no instruction:
  - inspect the current root
  - explain what this skill can do
  - recommend the most useful next step
  - show a few concrete in-scope examples
- If invoked with an in-scope instruction:
  - start that direction directly
  - only ask for missing high-impact detail
- If the instruction is in-scope but ambiguous:
  - prefer the most likely intent
  - ask the smallest useful clarifying question only when needed
- If the instruction is out of scope:
  - say so clearly
  - point to the better skill
  - do not silently switch

## In-Scope Intent Families

- `doctor` / `status`
- `explain current setup`
- `recommend` / `suggest`
- `bootstrap` / `repair`
- `create feature`
- `close feature` / `archive feature`
- `inspect features`
- `install` / `remove` / `promote`
- `import local source into external`

## Out Of Scope

Do not use this skill to:

- create, resume, or close tasks
- execute implementation work
- perform review or test workflows
- own `.tmp/` as a general staging workflow
- write new human-learning items
- operate from inside a feature worktree

## Required Outcomes

After a bootstrap or repair run, these should exist at the shared root:

- `features/`
- `AGENTS.md`
- `.agents/skills/`
- `.codex/config.toml`
- `.codex/agents/`
- `.codex/rules/`
- `.work/features/`
- `.work/specs/`
- `.work/dependencies/`
- `.work/catalog/active.yaml`
- `.work/project-manage/state.toml`
- `.work/project-manage/rule-candidates/`
- `.work/catalog/external/`
- `.work/catalog/learned/`
- `.work/catalog/validated/`
- `.work/human-learning/`
- `.tmp/`
- `.agents/skills/_shared/`

## Workflow

1. Determine the user goal:
   - if the current path is inside `features/<feature-id>/`:
     - explain that this skill is root-only
     - tell the user to return to the shared root for `project-manage`
     - stop without writing
   - if there is no instruction, inspect the current root and respond with:
     - what this skill can do
     - the most useful next step for this project
     - a few example invocations
     - then stop without writing
2. Inspect the current shared root before asking obvious questions:
   - `features/`
   - `AGENTS.md`
   - `.agents/skills/`
   - `.codex/config.toml`
   - `.codex/agents/`
   - `.codex/rules/`
   - `.work/features/`
   - `.work/specs/`
   - `.work/dependencies/`
   - `.work/catalog/active.yaml`
   - `.work/project-manage/state.toml`
   - `.work/project-manage/rule-candidates/`
   - `.work/catalog/external/`
   - `.work/catalog/learned/`
   - `.work/catalog/validated/`
   - `.work/human-learning/`
   - `.tmp/`
   - `.agents/skills/_shared/`
3. For `doctor` or `status`:
   - inspect whether the expected root directories exist
   - inspect whether `.work/project-manage/state.toml` exists and still matches the minimal state contract
   - inspect whether `active.yaml` matches materialized catalog-managed items
   - inspect whether feature metadata and feature worktree directories obviously drift apart
   - inspect whether configured active files are obviously missing
   - summarize the result as:
     - `healthy`
     - `warning`
     - `broken`
   - explain findings and the smallest next actions
   - do not repair automatically unless the user asks
4. For `explain current setup`:
   - explain:
     - the shared root runtime layer
     - registered features and their worktree paths
     - active skills, subagents, MCP items, and config fragments at the shared root
     - the minimal project-manage state
     - which runtime items are baseline vs catalog-managed
   - focus on what the user can actually use next
5. For `recommend` or `suggest`:
   - inspect the repository for project signals before asking broad questions
   - prefer recommending from `validated`
   - if a useful item exists only in `learned` or `external`, say so explicitly
   - explain why each recommendation fits the shared project
   - do not install automatically unless the user asks
6. For `create feature`:
   - collect or confirm:
     - `feature_id`
     - title
     - base branch
     - summary
     - optional `spec_refs`
   - create a branch for that feature
   - create a git worktree at `features/<feature-id>/`
   - create `.work/features/<feature-id>/feature.toml`
   - create `.work/features/<feature-id>/tasks/`
   - create the minimal local runtime shell in the feature worktree:
     - `AGENTS.md`
     - `.agents/skills/`
     - `.codex/`
   - expose shared skills into the feature worktree through local discoverable entries
   - provision feature-worktree-local ignore rules so the private runtime shell stays local by default:
     - `/AGENTS.md`
     - `/.agents/`
     - `/.codex/`
   - keep the feature runtime shell private by default
   - after creation, tell the user the next preferred entry command:
     - `bin/xcode features/<feature-id>`
     - or `xcode features/<feature-id>` when `bin/` is on `PATH`
   - update `.work/project-manage/state.toml`
7. For `inspect features`:
   - explain feature ids, branches, worktree paths, status, summaries, and key dependencies from `feature.toml`
8. For `close feature` or `archive feature`:
   - identify the target feature from `.work/features/<feature-id>/feature.toml`
   - inspect its shared task directory before closing:
     - warn if active or blocked tasks still exist
     - do not silently discard unresolved task state
   - for feature closure:
     - set feature status to `merged` or `abandoned`
     - set `closed_at`
     - update `updated_at`
   - for archive:
     - require the feature to already be `merged` or `abandoned`
     - set status to `archived`
     - update `updated_at`
   - optionally remove the feature worktree after explicit confirmation
   - never delete the shared feature metadata or shared task directory
   - update `.work/project-manage/state.toml`
9. For installation:
   - allow install from any catalog layer
   - warn clearly when the source layer is `external` or `learned`
   - materialize shared active skills into the shared root `.agents/skills/`
   - materialize shared active subagents into the shared root `.codex/agents/`
   - materialize MCP items into the shared root `.codex/config.toml` as managed `[mcp_servers.<id>]` blocks
   - materialize config snippets into the shared root `.codex/config.toml` using managed blocks
   - materialize rule files into the shared root `.codex/rules/`
   - update `.work/catalog/active.yaml`
   - update `.work/project-manage/state.toml`
10. For pack installation:
   - read `pack.yaml`
   - inspect included item ids, dependencies, and warnings
   - preview the full install set before writing
11. For removal:
   - use `active.yaml` as the primary source of truth
   - remove only the installed paths or managed config blocks associated with that item
   - update `active.yaml`
   - update `.work/project-manage/state.toml`
12. For promotion:
   - move the item directory between `external`, `learned`, and `validated`
   - update the item's metadata to match the new layer and validation state
   - preserve provenance in `origin`, `source_ref`, and notes
   - update `.work/project-manage/state.toml`
13. For repair:
   - compare `active.yaml` with shared runtime files
   - compare `.work/project-manage/state.toml` with the expected minimal control-plane state contract
   - explain the drift
   - preview the smallest repair
   - after confirmed repair, update `.work/project-manage/state.toml`
14. If the user names a local capability source path, inspect it before asking for more detail.
15. If the request is clearly out of scope:
   - explain the boundary briefly
   - point to the better skill
   - stop without writing
16. Prepare a brief preview of the files or directories to create, update, install, remove, promote, or repair.
17. Ask for confirmation.
18. After confirmation, write only the needed changes.

## Writing Rules

- Preview before writing.
- `doctor`, `recommend`, and `explain current setup` are read-only by default.
- Keep all changes local to the shared root.
- Keep the catalog layer private under `.work/catalog/`.
- Use `.work/catalog/active.yaml` for catalog-managed active items only; do not track the baseline workflow skills there.
- Use `.work/project-manage/state.toml` for the minimal shared operating-layer state.
- Keep `state.toml` small:
  - runtime model
  - baseline revision
  - initialization time
  - last runtime-layer change time
  - last runtime-layer change kind
  - last runtime-layer change summary
- Do not store full doctor results or recommendation history in `state.toml`.
- Keep `.agents/skills/_shared/` as shared helper infrastructure for the core workflow; do not treat it as a catalog-managed capability.
- For feature creation, keep `feature.toml` minimal and explicit:
- For feature lifecycle, keep `feature.toml` minimal and explicit:
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
- Store `worktree_path` as a shared-root-relative path such as `features/<feature-id>`, not an absolute path.
- Feature statuses should stay within:
  - `active`
  - `blocked`
  - `merged`
  - `abandoned`
  - `archived`
- When closing a feature, prefer preserving history:
  - keep `.work/features/<feature-id>/`
  - keep shared tasks
  - remove the worktree only after explicit confirmation
- Use config block markers in `.codex/config.toml`:
  - `# project-manage: begin <item-id>`
  - `# project-manage: end <item-id>`
- For MCP items, the managed block should contain one `[mcp_servers.<id>]` definition sourced from `server.toml`.
- Do not create a root-level task lifecycle skill or a global `.work/tasks/` pool.
- Keep changes minimal and deterministic.
