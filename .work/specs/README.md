# Shared Specs

This directory stores long-lived shared specifications for the project.

Use it for:

- durable private specs
- design notes that should survive individual feature worktrees
- references that multiple features may point to

Rules:

- prefer stable relative paths from the root shared layer
- use `spec_refs` in feature metadata or task metadata when a spec should be linked explicitly
- do not treat this directory as task execution state

