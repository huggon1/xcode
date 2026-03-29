# Codex Workstream Control Plane Kit

This repository is a private-first root kit for one shared workspace with multiple workstreams.

The matching model-facing rules live in `AGENTS.md`.

## Quick Use

Use this kit when you want:

- one shared root for docs, catalog, learning, staging, and workstream records
- multiple execution directories under `workstreams/`
- both code and non-code workstreams under one model
- shared task truth outside execution directories
- transcript-backed learning from completed tasks

### Session Types

Use two session types on purpose.

#### Root session

Start Codex at the root when you want to:

- create or inspect workstreams
- inspect shared workspace state
- manage shared capabilities
- review shared docs, catalog, learning, or staged input
- close or archive a workstream

Primary skill:

- `$workstream-manage`

#### Workstream session

Start a workstream session when you want to:

- open or resume a task for that workstream
- do implementation or structured work
- close out task progress
- capture explicit learning

Primary skills:

- `$open-task`
- `$close-task`
- `$learn`

`$learn` may also run from the root when you want to review completed tasks and learn from shared records and linked transcripts.

### Entry

Preferred entry:

1. from the root, run `bin/xcode workstreams/<workstream-id>`
2. if `bin/` is on your `PATH`, run `xcode <workstream-id>`
3. any extra arguments are forwarded to `codex`

The launcher enters the shared root first and then runs Codex with relative paths:

- `-C "workstreams/<workstream-id>"`
- `--add-dir "."`

### Core Guidance

- Root is the shared control plane.
- `workstreams/<workstream-id>/` is the execution directory for one workstream.
- Every task belongs to exactly one workstream.
- Root does not host task lifecycle.
- `open-task` and `close-task` should be used only from inside a workstream execution directory.
- `learn` may be used from either root or a workstream execution directory.
- Shared long-lived material stays outside execution directories.
- `.tmp/` is a shared flat staging area.
- `bin/xcode` is the standard launcher for workstream sessions.

## Design Notes

### Structure

```text
workspace/
├── bin/
│   └── xcode                      # workstream session launcher
├── workstreams/
│   └── <workstream-id>/           # repo worktree or daily execution directory
├── .tmp/
├── .agents/skills/                # shared skill source for root + workstream shells
├── .codex/                        # root control-plane runtime
├── .work/
│   ├── workstreams/
│   │   └── <workstream-id>/
│   │       ├── workstream.toml
│   │       ├── tasks/
│   │       └── sessions/
│   ├── docs/
│   ├── catalog/
│   ├── learning/
│   │   ├── human/
│   │   └── rule-candidates/
│   └── state.toml
├── AGENTS.md
├── README.md
└── project-local-exclude.example
```

### Shared Control Plane

The root shared layer owns all long-lived non-code state:

- workstream metadata
- workstream-scoped task records
- workstream session registry files
- shared docs
- shared capability catalog
- shared learning items
- shared staged input
- root runtime state

This makes paths stable and allows multiple workstreams to reference the same durable material.

### Workstreams

Each workstream is typed.

Supported types in this baseline:

- `repo`
- `daily`

Every workstream gets:

- one workstream id
- one execution directory under `workstreams/`
- one shared metadata bucket under `.work/workstreams/`

For `repo` workstreams:

- the execution directory is a git worktree
- metadata also records `branch` and `base_branch`

For `daily` workstreams:

- the execution directory is a plain local directory
- no git worktree is required

In shared metadata, keep the execution path relative to the shared root:

- `workstreams/<workstream-id>`

### Workstream Metadata And Tasks

Shared workstream metadata lives at:

- `.work/workstreams/<workstream-id>/workstream.toml`

Shared workstream tasks live at:

- `.work/workstreams/<workstream-id>/tasks/YYYY-MM-DD-task-slug.md`

Shared workstream session identity lives at:

- `.work/workstreams/<workstream-id>/sessions/<session-id>.toml`

This split is deliberate:

- task lifecycle happens inside the workstream execution directory
- durable task truth lives in the shared root layer
- session naming and retrieval use the shared workstream session registry

Workstream metadata should keep lifecycle status explicit. Supported statuses are:

- `active`
- `blocked`
- `completed`
- `abandoned`
- `archived`

Closing or archiving a workstream should update `workstream.toml`. It should not delete the shared workstream record, task history, or session registry.

### Runtime And Capability Management

`$workstream-manage` owns:

- workstream creation
- repo branch/worktree creation
- daily execution directory creation
- root capability inspection
- root capability installation and repair
- workstream explanation
- workstream close/archive lifecycle

It does not own task execution.

It is a root-only skill and should refuse to run from inside a workstream execution directory.

### Task Lifecycle

`$open-task` and `$close-task` are workstream-execution-only skills.

They should:

- determine the current workstream from the current path
- resolve the matching shared task directory
- read and write only that workstream’s tasks
- refuse to operate when started from root
- refuse to operate on a task that belongs to a different workstream

Task metadata also keeps:

- learning state
- learning references
- session references

This allows root-side learning to work from completed tasks without guessing blindly.

### Session Identity

This kit does not rely on Codex native thread naming as the primary mechanism.

Instead, it keeps a lightweight per-workstream session registry:

- `.work/workstreams/<workstream-id>/sessions/<session-id>.toml`

Each session record should keep:

- `session_id`
- `workstream_id`
- `task_id`
- `label`
- `started_at`
- `updated_at`
- `execution_path`

The label is derived from workstream and task identity rather than being manually named.

### Shared Staging

`.tmp/` is shared and flat.

Use it for:

- incoming notes
- raw documents
- capability sources
- reference bundles

Do not treat it as durable knowledge, and do not proactively scan it.

### Shared Docs, Learning, And Catalog

Shared reference material, learning material, and catalog items remain at root:

- `.work/docs/`
- `.work/learning/`
- `.work/catalog/`

This keeps reusable knowledge and reviewable learning from fragmenting across workstreams.

### Root-Side Learning

`$learn` may run at root when you want to learn from completed workstream work after the execution session is over.

In that mode it should:

- select a completed task that is still pending learning
- read the task record first
- resolve related transcripts from the Codex session store using task-linked session refs first
- consult the shared session registry for labels and context
- fall back to inferred session candidates only when explicit links are missing
- write outputs to shared durable locations

Possible outputs are:

- a learned skill
- a human-learning item
- a workstream rule candidate

### Git Recommendation

This repository tracks the baseline because it is the maintained source template.

In a real workspace checkout:

- use `project-local-exclude.example` for the shared root
- let `$workstream-manage` provision each workstream execution directory's local ignore rules for:
  - `/AGENTS.md`
  - `/.agents/`
  - `/.codex/`

That keeps the private runtime shell and shared control-plane files local by default.
