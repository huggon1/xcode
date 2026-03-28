# Codex Project Root Kit

This repository is a private-first, single-project Codex root template.

The matching model-facing rules live in [AGENTS.md](/home/duu/code/mycodex/workspace/AGENTS.md).

## Quick Use

Use this kit when you want one project root to carry:

- a stable Codex runtime layer
- a small manual workflow surface
- durable task records
- a layered capability catalog
- private human-learning notes
- a neutral staging area for temporary inputs

The recommended daily loop is:

1. Use `$project-manage` when you need to set up, inspect, repair, or change the runtime layer or the capability catalog.
2. Use `$open-task` when you start or resume real work.
3. Do the work.
4. Use `$close-task` when you stop so the task record stays resumable.
5. Use `$learn` only when you explicitly want to preserve a reusable lesson or a human-improvement item.

### Core Skills

| Skill | Use it for | Recommendation |
| --- | --- | --- |
| `$project-manage` | Runtime-layer and catalog management | Keep it focused on active capabilities, not on task content or temporary staging |
| `$open-task` | Creating or resuming a task record | Use it whenever you re-enter a task after a pause or context switch |
| `$close-task` | Updating task outcome and next step | Use it every time you stop working so the project stays resumable |
| `$learn` | Capturing reusable skills or human-improvement items | Use it explicitly and selectively; most tasks do not need a learned artifact |

### Core Guidance

- All shipped workflow skills are manual-only. Invoke them explicitly.
- Treat task files under `.work/tasks/` as the main durable record of active work.
- Treat catalog items under `.work/catalog/` as reusable capabilities, not as task notes.
- Treat human-learning items under `.work/human-learning/items/` as a small active improvement queue.
- Treat `.tmp/` as a neutral staging area, not as long-term memory.
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
├── .codex/
│   ├── config.toml
│   ├── agents/
│   └── rules/
├── .work/
│   ├── catalog/
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
- `.codex/config.toml`
- `.codex/agents/`
- `.codex/rules/`

The private durable working state lives under `.work/`:

- `.work/tasks/` for task records
- `.work/catalog/` for reusable capabilities and active inventory
- `.work/human-learning/` for private improvement material

The temporary staged input lives under `.tmp/`:

- it is only for files you explicitly want the model to inspect or organize
- it is not durable knowledge
- it is not owned by any single skill

### Why The Workflow Is Small

The workflow surface is intentionally narrow.

`$project-manage`, `$open-task`, and `$close-task` cover the main project loop. `$learn` exists for deliberate reflection, not for everyday mandatory use.

This keeps the operating model clear:

- `project-manage` changes capabilities
- `open-task` starts or resumes work
- `close-task` preserves work state
- `learn` preserves lessons

### Task Design

Task files are the only durable record of active work.

Each task lives at:

- `.work/tasks/YYYY-MM-DD-task-slug.md`

Each task uses YAML frontmatter and a stable section order so sessions can resume cleanly without inventing extra state files or generic planning documents.

Closed tasks remain in `.work/tasks/`; closure is represented in metadata and `Final Outcome`, not by moving files elsewhere.

### Catalog Design

The capability catalog under `.work/catalog/` is layered by trust:

- `external`
- `learned`
- `validated`

Its purpose is to separate reusable capability sources from the active runtime layer.

Active installed items live in standard root locations. Catalog items remain source material until intentionally materialized.

`active.yaml` tracks only catalog-managed active items. It does not track the baseline workflow skills that ship with this root.

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

### Why Git Behavior Is Split

There are two different contexts:

1. This repository is the maintained source template, so baseline files are tracked here.
2. A real project checkout uses the same structure as local operating state, so those files should usually remain untracked there.

That is why this repository includes the baseline structure directly, while real project checkouts should normally rely on local excludes.
