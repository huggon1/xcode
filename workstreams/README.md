# Workstream Execution Directories

This directory is reserved for workstream execution directories.

Each workstream should map to exactly one:

- workstream id
- execution directory
- optional repo branch/worktree when the type is `repo`

## Shape

```text
workstreams/
├── <workstream-id>/   # repo worktree or daily execution directory
└── ...
```

## Rules

- Treat each workstream directory as an execution workspace for actual work.
- Start workstream implementation sessions from inside the relevant workstream directory.
- Keep long-lived shared records outside this directory, under the shared root layer.
- Each workstream execution directory should expose a local runtime shell for Codex:
  - `AGENTS.md`
  - `.agents/skills/`
  - `.codex/`
- Do not create a workstream-local `.tmp/`; staged input stays at the shared root.
- Shared skills should be exposed here through local discoverable entries.
- Do not treat these directories as generic copies of the repository.

## Session Entry

Use the launcher from the shared root:

1. run `bin/xcode workstreams/<workstream-id>`
2. if `bin/` is on your `PATH`, run `xcode <workstream-id>`
3. extra arguments are forwarded to `codex`

The launcher starts from the shared root and uses relative Codex paths:

- `-C "workstreams/<workstream-id>"`
- `--add-dir "."`
