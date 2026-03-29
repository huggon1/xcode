# Capability Catalog

The catalog stores reusable capability sources and the inventory of catalog-managed active items.

## Structure

```text
.work/catalog/
├── active.yaml
├── external/
├── learned/
└── validated/
```

Each layer contains:

- `skills/`
- `agents/`
- `mcp/`
- `config/`
- `packs/`

## Layer Meaning

- `external`: imported or collected candidate items
- `learned`: items created or learned from project work
- `validated`: items personally proven useful in practice

## Item Shapes

- skill items keep a full skill directory shape
- agent items keep `agent.toml` plus `catalog.yaml`
- MCP items keep `server.toml` plus `catalog.yaml`
- config items keep `catalog.yaml` plus material to install into `.codex/config.toml` or `.codex/rules/`
- pack items keep `pack.yaml` and reference other catalog items by id and kind

## Metadata

`catalog.yaml` should record:

- `id`
- `kind`
- `title`
- `summary`
- `layer`
- `origin`
- `source_ref`
- `dependencies`
- `validated`
- `notes`

`pack.yaml` should record:

- `id`
- `title`
- `summary`
- `layer`
- `origin`
- `source_ref`
- `validated`
- `includes`
- `warnings`
- `dependencies`
- `notes`

## Active Inventory

`active.yaml` tracks catalog-managed active capabilities only.

It should record:

- `id`
- `kind`
- `source_layer`
- `source_ref`
- `installed_paths`
- `installed_at`
- `managed`
- `notes`

It does not track the baseline workflow skills that ship with this root.
It also does not track the control-plane state owned by `$project-manage`.

## Runtime Relationship

Catalog items are source material.

Catalog metadata stays in sidecar YAML files. This directory does not use frontmatter.

They become active only when intentionally materialized into standard root locations:

- `.agents/skills/`
- `.codex/agents/`
- `.codex/config.toml`
- `.codex/rules/`

MCP items should be installed into `.codex/config.toml` as managed `[mcp_servers.<id>]` blocks.

Minimal project runtime state lives separately in:

- `.work/project-manage/state.toml`

## Workflow

- Use `$project-manage` to inspect, install, remove, promote, or repair catalog-managed items.
- Treat items outside `validated` as not yet fully trusted.
