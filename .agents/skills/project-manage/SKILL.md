---
name: project-manage
description: Use when the user wants to initialize, inspect, repair, or change the active Codex operating layer and layered catalog for the current project. Trigger on requests like project setup, project bootstrap, inspect project config, inspect catalog, add skill, add subagent, install pack, promote item, change config, or repair project layer.
---

# Project Manage

Treat the current repository root as the path base for all files mentioned below.

## Purpose

Act as the project control plane for the current repository.

This skill is responsible for project-level capability and health questions, not task execution.

## Interaction Model

- If invoked with no instruction:
  - inspect the current project root
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
- `recommend` / `suggest`
- `explain current setup`
- `bootstrap` / `repair`
- `inspect catalog` / `inspect active inventory`
- `install` / `remove` / `promote`
- `import local source into external`

## Out Of Scope

Do not use this skill to:

- create, resume, or close tasks
- execute implementation work
- perform review or test workflows
- own `.tmp/` as a general staging workflow
- write new human-learning items

## Required Outcomes

After a bootstrap or repair run, these should exist:

- `AGENTS.md`
- `.agents/skills/`
- `.codex/config.toml`
- `.codex/agents/`
- `.codex/rules/`
- `.work/catalog/active.yaml`
- `.work/project-manage/state.toml`
- `.work/catalog/external/`
- `.work/catalog/learned/`
- `.work/catalog/validated/`
- `.work/human-learning/`
- `.work/tasks/`
- `.agents/skills/_shared/`

## Workflow

1. Determine the user goal:
   - if there is no instruction, inspect the current root and respond with:
     - what this skill can do
     - the most useful next step for this project
     - a few example invocations
     - then stop without writing
   - bootstrap or repair the project layer
   - doctor or status-check the project layer
   - recommend capability additions for this project
   - explain the current active setup
   - inspect the layered catalog or active inventory
   - inspect current active capabilities
   - add, remove, or update active skills
   - add, remove, or update active subagents
   - add, remove, enable, disable, or inspect MCP servers
   - add, remove, or update active config or rules
   - install a pack
   - promote an item between layers
   - import a local source into `external`
2. Inspect the current root before asking obvious questions:
   - `AGENTS.md`
   - `.agents/skills/`
   - `.codex/config.toml`
   - `.codex/agents/`
   - `.codex/rules/`
   - `.work/catalog/active.yaml`
   - `.work/project-manage/state.toml`
   - `.work/catalog/external/`
   - `.work/catalog/learned/`
   - `.work/catalog/validated/`
   - `.work/human-learning/`
   - `.work/tasks/`
   - `.agents/skills/_shared/`
3. For catalog inspection, prefer explaining:
   - current active managed items from `active.yaml`
   - available items by layer
   - dependencies, warnings, and validation state from item metadata
   - inventory structure:
     - `id`
     - `kind`
     - `source_layer`
     - `source_ref`
     - `installed_paths`
     - `installed_at`
     - `managed`
     - `notes`
4. For `doctor` or `status`:
   - inspect whether the expected runtime and working-layer directories exist
   - inspect whether `.work/project-manage/state.toml` exists and still matches the minimal state contract
   - inspect whether `active.yaml` matches materialized catalog-managed items
   - inspect whether configured active files are obviously missing
   - summarize the result as:
     - `healthy`
     - `warning`
     - `broken`
   - explain findings and the smallest next actions
   - do not repair automatically unless the user asks
5. For `recommend` or `suggest`:
   - inspect the repository for project signals before asking broad questions:
     - top-level manifests
     - test framework traces
     - browser or e2e tooling traces
     - repo layout signals
   - prefer recommending from `validated`
   - if a useful item exists only in `learned` or `external`, say so explicitly
   - explain why each recommendation fits the current repository
   - do not install automatically unless the user asks
6. For `explain current setup`:
   - explain:
     - active skills
     - active subagents
     - active MCP items
     - active config fragments
     - the minimal project-manage state
     - where they came from
     - which ones are baseline vs catalog-managed
   - focus on what the user can actually use next
7. For installation:
   - allow install from any layer
   - warn clearly when the source layer is `external` or `learned`
   - materialize active skills into `.agents/skills/`
   - materialize active subagents into `.codex/agents/`
   - materialize MCP items into `.codex/config.toml` as managed `[mcp_servers.<id>]` blocks
   - materialize config snippets into `.codex/config.toml` using managed blocks
   - materialize rule files into `.codex/rules/`
   - update `.work/catalog/active.yaml`
   - update `.work/project-manage/state.toml`
8. For pack installation:
   - read `pack.yaml`
   - inspect included item ids, dependencies, and warnings
   - preview the full install set before writing
9. For agent installation:
   - ensure the agent is usable after install
   - prefer a matching catalog config item when one exists
   - otherwise add the smallest managed config block needed to register the subagent and record that in `active.yaml`
10. For removal:
   - use `active.yaml` as the primary source of truth
   - remove only the installed paths or managed config blocks associated with that item
   - update `active.yaml`
   - update `.work/project-manage/state.toml`
11. For MCP inspection:
   - explain the installed server id
   - explain the command or URL source
   - explain required env or other prerequisites if metadata records them
   - explain whether the item is enabled through the current managed block
12. For promotion:
   - move the item directory between `external`, `learned`, and `validated`
   - update the item's metadata to match the new layer and validation state
   - preserve provenance in `origin`, `source_ref`, and notes
   - update `.work/project-manage/state.toml`
13. For repair:
   - compare `active.yaml` with active runtime files
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
- Keep all changes local to the current project root.
- Keep the catalog layer private under `.work/catalog/`.
- Prefer materializing active capabilities into `.agents/skills/`, `.codex/agents/`, `.codex/config.toml`, and `.codex/rules/`.
- Use `.work/catalog/active.yaml` for catalog-managed active items only; do not track the baseline workflow skills there.
- Use `.work/project-manage/state.toml` for the minimal operating-layer state.
- Keep `state.toml` small:
  - runtime model
  - baseline revision
  - initialization time
  - last runtime-layer change time
  - last runtime-layer change kind
  - last runtime-layer change summary
- Do not store full doctor results or recommendation history in `state.toml`.
- Keep `.agents/skills/_shared/` as shared helper infrastructure for the core workflow; do not treat it as a catalog-managed capability.
- When writing `active.yaml`, use the fields:
  - `id`
  - `kind`
  - `source_layer`
  - `source_ref`
  - `installed_paths`
  - `installed_at`
  - `managed`
  - `notes`
- Use config block markers in `.codex/config.toml`:
  - `# project-manage: begin <item-id>`
  - `# project-manage: end <item-id>`
- For MCP items, the managed block should contain one `[mcp_servers.<id>]` definition sourced from `server.toml`.
- Do not assume a global catalog exists.
- Do not create generic docs, templates, plan files, registries, or archive folders.
- Keep changes minimal and deterministic.
