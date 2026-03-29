# Temporary Staging

Use this shared root directory for files you want the model to inspect and organize.

Typical uses:

- drop in a skill pack before asking the model to organize it into the catalog
- drop in a raw document before asking the model to normalize it into a task file or another durable destination
- keep temporary source material that should be removed after successful processing

Rules:

- `.tmp/` is not a durable source of truth
- `.tmp/` is shared across all workstream execution directories
- explicitly tell the model which staged file or folder to process
- the model should suggest or confirm the best durable destination when it is not obvious
- `.tmp/` is not owned by any single skill
- after successful processing and confirmation, prefer cleaning the processed original out of `.tmp/`
- if the destination is still unclear, keep the source here until resolved
