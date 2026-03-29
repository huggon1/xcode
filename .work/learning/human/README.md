# Human Learning Items

Store one human improvement topic per file in this directory.

Use `.work/learning/README.md` for the higher-level intent and this file for the item contract.

## Item Metadata

Each item should use TOML frontmatter delimited by `+++`.

Use these metadata fields:

- `id`
- `status`
- `created`
- `updated`
- `success_streak`
- `retire_after`
- `scope`
- `tags`
- `applies_to`
- `summary`

Allowed `status` values:

- `active`
- `delete`

Keep the frontmatter flat:

- scalars
- integers
- arrays of strings

## Section Order

Use this section order:

- `# Title`
- `## Why This Matters`
- `## Applies When`
- `## Better Behavior`
- `## Success Signals`
- `## Failure Signals`
- `## Notes`

## Lifecycle

- New items start as `active`.
- Relevant work may increase `success_streak` when the behavior was handled well.
- If the same issue appears again, reset `success_streak` to `0`.
- When an item has been handled well enough times, the model may ask whether to set `status: delete`.
- Do not physically delete files automatically as part of the baseline workflow.

## Managed Update Surface

The internal helper layer may update these parts directly:

- all frontmatter fields
- canonical section skeletons when an item is first created

`$close-task` should only adjust metadata and streak state. It should not rewrite the main narrative sections.

## Workflow

- Use `$learn` to create or update human-learning items explicitly.
- `$close-task` may update existing active items when they are clearly relevant from within a workstream execution directory.
- Use `.agents/skills/_shared/scripts/human_learning.py` behind those skills when structured reads or metadata-only updates are enough.
- Human-learning items are shared private working material, not active runtime capabilities.
