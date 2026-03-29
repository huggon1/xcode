# Feature Worktrees

This directory is reserved for feature worktrees.

Each feature should map to exactly one:

- feature id
- branch
- worktree directory

Use real git worktrees here, not copied directories.

## Shape

```text
features/
├── <feature-id>/   # git worktree for one feature branch
└── ...
```

## Rules

- Treat each feature directory as an execution workspace for code changes.
- Start feature implementation sessions from inside the relevant feature directory.
- Keep long-lived shared records outside this directory, under the root shared layer.
- Each feature worktree should expose a local runtime shell for Codex:
  - `AGENTS.md`
  - `.agents/skills/`
  - `.codex/`
- Do not create a feature-local `.tmp/`; staged input stays at the shared root.
- Shared skills should be exposed here through local discoverable entries.
- Do not treat these directories as generic copies of the repository.

## Session Entry

Use the launcher from the shared root:

1. run `bin/xcode features/<feature-id>`
2. if `bin/` is on your `PATH`, run `xcode features/<feature-id>`
3. extra arguments are forwarded to `codex`

The launcher starts from the shared root and uses relative Codex paths:

- `-C "features/<feature-id>"`
- `--add-dir "."`
