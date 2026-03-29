# Codex Project Control Plane Kit

This repository is a private-first root kit for one project with multiple feature worktrees.

The matching model-facing rules live in [AGENTS.md](AGENTS.md).

## Quick Use

Use this kit when you want:

- one shared root for long-lived project knowledge
- one feature branch per worktree under `features/`
- shared task records, specs, dependencies, catalog, human-learning, and staging
- feature-local execution sessions with isolated code state

### Session Types

Use two session types on purpose.

#### Root session

Start Codex at the root when you want to:

- create or inspect feature branches and worktrees
- inspect shared project state
- manage shared capabilities
- review shared specs, dependencies, catalog, human-learning, or staged input

Primary skill:

- `$project-manage`

Use it for feature lifecycle as well:

- create a feature branch + worktree
- inspect feature status
- close a feature as `merged` or `abandoned`
- archive a finished feature

#### Feature session

Start a feature session from the root when you want to:

- open or resume a task for that feature
- implement code changes
- close out task progress
- capture explicit learning

Primary skills:

- `$open-task`
- `$close-task`
- `$learn`

`$learn` may also run from the root when you want to review completed tasks and learn from their shared records and linked transcripts.

Preferred entry:

1. from the root, run `bin/xcode features/<feature-id>`
2. if `bin/` is on your `PATH`, run `xcode features/<feature-id>`
3. any extra arguments are forwarded to `codex`

The launcher enters the shared root first and then runs Codex with relative paths:

- `-C "features/<feature-id>"`
- `--add-dir "."`

### Core Guidance

- Root is the shared control plane.
- `features/<feature-id>/` is the execution workspace for one feature branch.
- Every task belongs to exactly one feature.
- Root does not host task lifecycle.
- `open-task` and `close-task` should be used only from inside a feature worktree.
- `learn` may be used from either root or a feature worktree.
- Shared long-lived material stays outside feature worktrees.
- `.tmp/` is a shared flat staging area.
- `bin/xcode` is the standard launcher for feature sessions.

## Design Notes

### Structure

```text
workspace/
├── bin/
│   └── xcode                  # feature session launcher
├── features/
│   └── <feature-id>/          # git worktree
├── .tmp/
├── .agents/skills/            # shared skill source for root + feature shells
├── .codex/                    # root control-plane runtime
├── .work/
│   ├── features/
│   │   └── <feature-id>/
│   │       ├── feature.toml
│   │       └── tasks/
│   ├── specs/
│   ├── dependencies/
│   ├── catalog/
│   ├── human-learning/
│   └── project-manage/
│       └── rule-candidates/
├── AGENTS.md
├── README.md
└── project-local-exclude.example
```

### Shared Control Plane

The root shared layer owns all long-lived non-code state:

- feature metadata
- feature-scoped task records
- shared specs
- cross-feature dependency material
- shared capability catalog
- shared human-learning items
- shared staged input
- root project-manage state

This makes paths stable and allows multiple feature branches to reference the same durable material.

### Feature Worktrees

Each feature is exactly one:

- feature id
- branch
- git worktree

The worktree under `features/<feature-id>/` is the execution space for that feature.
In shared metadata, keep the worktree path relative to the shared root:

- `features/<feature-id>`

The standard way to enter that execution space is:

- `bin/xcode features/<feature-id>`
- or `xcode features/<feature-id>` when `bin/` is on `PATH`

That launcher keeps the Codex-facing paths relative by running from the shared root and using:

- `-C "features/<feature-id>"`
- `--add-dir "."`

It should contain a local runtime shell because Codex discovers runtime instructions and repo skills from the current working root:

- `AGENTS.md`
- `.agents/skills/`
- `.codex/`

Shared skills should be exposed into each feature worktree through local discoverable entries that point back to the shared skill source.

### Feature Metadata And Tasks

Shared feature metadata lives at:

- `.work/features/<feature-id>/feature.toml`

Shared feature tasks live at:

- `.work/features/<feature-id>/tasks/YYYY-MM-DD-task-slug.md`

This split is deliberate:

- task lifecycle happens inside the feature worktree
- durable task truth lives in the shared root layer

That gives you isolated execution with shared long-term records.

Feature metadata should keep lifecycle status explicit. Suggested statuses are:

- `active`
- `blocked`
- `merged`
- `abandoned`
- `archived`

Closing or archiving a feature should update `feature.toml`. It should not delete the shared feature record or shared task history.

### Runtime And Capability Management

`$project-manage` owns:

- feature creation
- branch/worktree creation
- root capability inspection
- root capability installation and repair
- feature/worktree explanation

It does not own task execution.
It is a root-only skill and should refuse to run from inside a feature worktree.

It does own feature lifecycle, including feature closure and archive state.

### Task Lifecycle

`$open-task` and `$close-task` are feature-worktree-only skills.

They should:

- determine the current feature from the current path
- resolve the matching shared task directory
- read and write only that feature’s tasks
- refuse to operate when started from root
- refuse to operate on a task that belongs to a different feature

Task metadata also keeps:

- learning state
- learning references
- session references

This allows root-side learning to work from completed tasks without guessing blindly.

### Shared Staging

`.tmp/` is shared and flat.

Use it for:

- incoming notes
- raw documents
- capability sources
- reference bundles

Do not treat it as durable knowledge, and do not proactively scan it.

### Human Learning And Catalog

Human-learning items and catalog items remain shared at root:

- `.work/human-learning/`
- `.work/catalog/`

This keeps reusable knowledge from fragmenting across feature branches.

### Root-Side Learning

`$learn` may run at root when you want to learn from completed feature work after the implementation session is over.

In that mode it should:

- select a completed task that is still pending learning
- read the task record first
- resolve related transcripts from the Codex session store using task-linked session refs when available
- fall back to inferred session candidates only when explicit links are missing
- write outputs to shared durable locations

Possible outputs are:

- a learned skill
- a human-learning item
- a project rule candidate

### Git Recommendation

This repository tracks the baseline because it is the maintained source template.

In a real project checkout:

- use [project-local-exclude.example](project-local-exclude.example) for the root control plane
- let `$project-manage` provision each feature worktree's local ignore rules for:
  - `/AGENTS.md`
  - `/.agents/`
  - `/.codex/`

That keeps the private runtime shell and shared control-plane files local by default.
