# Codex Project Root Kit

This repository is a private-first, single-project Codex root template.

The matching model-facing rules live in [AGENTS.md](/home/duu/code/mycodex/workspace/AGENTS.md).

## Quick Use

Use this kit when you want one project root to carry:

- a stable Codex runtime layer
- a small manual workflow surface
- durable task records
- a layered capability catalog
- a tiny project control-plane state
- private human-learning notes
- a neutral staging area for temporary inputs

The recommended daily loop is:

1. Use `$project-manage` when you need to inspect project health, understand the current setup, get capability recommendations, or change the runtime layer or the capability catalog.
2. Use `$open-task` when you start or resume real work.
3. Do the work.
4. Use `$close-task` when you stop so the task record stays resumable.
5. Use `$learn` only when you explicitly want to preserve a reusable lesson or a human-improvement item.

The core flow now uses internal helper scripts behind the skills for structured reads and precise updates. You still interact through the skills, not through new user-facing commands.

### Core Skills

| Skill | Use it for | Recommendation |
| --- | --- | --- |
| `$project-manage` | Project control plane: doctor, recommend, explain, bootstrap, repair, install, remove, promote | Use it when the question is about project capability or project health, not about task execution |
| `$open-task` | Creating, resuming, or normalizing a task record | Use it whenever you re-enter a task after a pause or want to turn rough intent into a task |
| `$close-task` | Updating task outcome and next step | Use it every time you stop working so the project stays resumable |
| `$learn` | Capturing reusable skills or human-improvement items | Use it explicitly and selectively; most tasks do not need a learned artifact |

### Interaction Pattern

All shipped workflow skills use the same interaction model:

- If you invoke a skill with no instruction, it explains what it can do, recommends the most useful next step, and shows a few examples.
- If you invoke a skill with an in-scope instruction, it starts that direction directly.
- If the instruction is still in-scope but too vague, it keeps going and only asks for the missing high-impact detail.
- If the instruction is out of scope, it tells you and points to the better skill instead of silently switching.

The main difference is style:

- `$project-manage` and `$open-task` are more open-ended.
- `$close-task` and `$learn` are more guided and stateful.

### Core Guidance

- All shipped workflow skills are manual-only. Invoke them explicitly.
- Treat task files under `.work/tasks/` as the main durable record of active work.
- Treat catalog items under `.work/catalog/` as reusable capabilities, not as task notes.
- Treat `.work/project-manage/state.toml` as the minimal memory of the operating layer, not as a report log.
- Treat human-learning items under `.work/human-learning/items/` as a small active improvement queue.
- Treat `.tmp/` as a neutral staging area, not as long-term memory.
- Task records and human-learning items use TOML frontmatter so the helpers can filter and update them cheaply.
- If staged material does not have an obvious destination, ask the model to suggest or confirm the best durable location before writing.
- After successful processing and confirmation, clean processed originals out of `.tmp/`.

### Git Recommendation

This repository tracks the baseline itself because it is the source template.

In a real project checkout that uses this structure, the same paths should usually stay local-only. Use [project-local-exclude.example](/home/duu/code/mycodex/workspace/project-local-exclude.example) as the source for `.git/info/exclude` in the real project checkout instead of modifying the team repo's tracked `.gitignore`.

## Design Notes

### Structure

```text
workspace/
├── .tmp/
├── .agents/skills/
│   └── _shared/
├── .codex/
│   ├── config.toml
│   ├── agents/
│   └── rules/
├── .work/
│   ├── catalog/
│   ├── project-manage/
│   ├── human-learning/
│   └── tasks/
├── AGENTS.md
├── README.md
└── project-local-exclude.example
```

### Core Model

The design separates the project root into three kinds of state:

- root runtime state
- private durable working state
- temporary staged input

The root runtime state is what Codex should actively use while operating in the project:

- `AGENTS.md`
- `.agents/skills/`
- `.agents/skills/_shared/`
- `.codex/config.toml`
- `.codex/agents/`
- `.codex/rules/`

The private durable working state lives under `.work/`:

- `.work/tasks/` for task records
- `.work/catalog/` for reusable capabilities and active inventory
- `.work/project-manage/` for minimal project control-plane state
- `.work/human-learning/` for private improvement material

The temporary staged input lives under `.tmp/`:

- it is only for files you explicitly want the model to inspect or organize
- it is not durable knowledge
- it is not owned by any single skill

### Why The Workflow Is Small

The workflow surface is intentionally narrow.

`$project-manage`, `$open-task`, and `$close-task` cover the main project loop. `$learn` exists for deliberate reflection, not for everyday mandatory use.

This keeps the operating model clear:

- `project-manage` manages project capability and project health
- `open-task` starts or resumes work
- `close-task` preserves work state
- `learn` preserves lessons

The intended boundary is:

- `project-manage` handles project-level setup and explanation
- `open-task` and `close-task` handle task lifecycle
- execution work happens between them
- `learn` stays explicit and separate from routine task flow

### Task Design

Task files are the only durable record of active work.

Each task lives at:

- `.work/tasks/YYYY-MM-DD-task-slug.md`

Each task uses TOML frontmatter and a stable section order so sessions can resume cleanly without inventing extra state files or generic planning documents.

The frontmatter holds fast-to-read routing fields such as:

- status
- summary
- next action
- tags
- related paths

The body still carries the human-readable task content. The internal helpers only own frontmatter and selected fixed sections. They do not replace model judgment.

Closed tasks remain in `.work/tasks/`; closure is represented in metadata and `Final Outcome`, not by moving files elsewhere.

### Catalog Design

The capability catalog under `.work/catalog/` is layered by trust:

- `external`
- `learned`
- `validated`

Its purpose is to separate reusable capability sources from the active runtime layer.

Active installed items live in standard root locations. Catalog items remain source material until intentionally materialized.

`active.yaml` tracks only catalog-managed active items. It does not track the baseline workflow skills that ship with this root.

The catalog intentionally keeps sidecar YAML metadata. It does not use frontmatter.

### Project Runtime State Design

`$project-manage` also owns a very small state file under:

- `.work/project-manage/state.toml`

This state is intentionally separate from the catalog inventory.

Its purpose is to remember a few control-plane facts:

- which runtime model this project root follows
- which baseline revision it was last aligned to
- when the runtime layer was initialized
- when the last runtime-layer change happened
- what the last runtime-layer change was

It is not a doctor log, recommendation log, or full audit trail.

This split is intentional:

- `.work/catalog/active.yaml` answers: what catalog-managed capabilities are active
- `.work/project-manage/state.toml` answers: what minimal runtime-layer state this project root is in

### Human-Learning Design

Human-learning items live under:

- `.work/human-learning/items/`

They are private working material, not active runtime capabilities.

Their job is to capture:

- alignment problems
- repeated blockers
- behaviors to improve
- successful collaboration patterns worth reinforcing

They are intentionally separate from learned skills because a personal improvement topic is not always the same thing as a reusable Codex skill.

Human-learning items also use TOML frontmatter so the helpers can update streaks and status without rewriting the full item.

### Temporary Staging Design

`.tmp/` exists so temporary source material has a clear place.

Typical staged inputs include:

- skill packs
- loose capability files
- raw notes
- reference folders
- documents that should be normalized into another durable location

The model should not proactively scan `.tmp/`. When you explicitly reference staged material, the model should first decide or confirm where it belongs:

- a catalog item
- a task update
- a human-learning item
- a project file update
- or no durable write at all

If the destination is unclear, the model should ask. If processing succeeds and you confirm the change, the staged original should be cleaned up.

### Shared Helper Design

The shared helper layer under `.agents/skills/_shared/` exists for two narrow reasons:

- metadata-first loading
- deterministic partial updates

It currently supports only the core flow:

- `$open-task`
- `$close-task`
- `$learn`

The helpers are implementation detail, not a second user workflow. When Python is unavailable or a helper fails, the model should fall back to the same documented file contracts and edit manually.

### Why Git Behavior Is Split

There are two different contexts:

1. This repository is the maintained source template, so baseline files are tracked here.
2. A real project checkout uses the same structure as local operating state, so those files should usually remain untracked there.

That is why this repository includes the baseline structure directly, while real project checkouts should normally rely on local excludes.
