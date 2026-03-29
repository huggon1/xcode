# Shared Dependencies

This directory stores shared cross-feature dependency material when lightweight metadata in `feature.toml` is not enough.

Prefer explicit metadata first:

- `depends_on_features`
- `blocked_by_features`

Use this directory only when a relationship needs extra explanation or supporting notes.

Rules:

- keep dependency records shared at the root layer
- do not store code-execution state here
- do not duplicate the same dependency logic across multiple feature task files when a shared record is clearer
