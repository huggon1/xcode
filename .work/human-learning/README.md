# Human Learning

This directory stores private human improvement material for the current project root.

Use it for lessons about how you work with the model, where alignment tends to fail, and what behaviors you want to improve over time.

## Location

Human-learning items live under:

- `.work/human-learning/items/`

Keep one improvement topic per file.

## Item Metadata

Each item should use YAML frontmatter with:

- `id`
- `status`
- `created`
- `updated`
- `success_streak`
- `retire_after`
- `tags`

Allowed `status` values:

- `active`
- `delete`

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

## Workflow

- Use `$learn` to create or update human-learning items explicitly.
- `$close-task` may update existing active items when they are clearly relevant.
- Human-learning items are private working material, not active runtime capabilities.
