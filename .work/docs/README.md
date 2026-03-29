# Shared Docs

This directory stores shared reference material for the root control plane.

Use it for anything that should be cited, reused, or linked from workstreams and tasks, including:

- specs
- dependency notes
- reports
- investigations
- design notes
- decision records
- meeting notes
- reference bundles

Rules:

- treat this directory as shared reference material, not execution state
- prefer stable relative paths from the root shared layer
- use `doc_refs` in `workstream.toml` when a document matters at the workstream level
- use `source_refs` in task metadata when a document matters at the task level
- keep lightweight dependency structure in workstream metadata when possible:
  - `depends_on_workstreams`
  - `blocked_by_workstreams`
- use docs for explanation and supporting detail when metadata alone is not enough
