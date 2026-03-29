#!/usr/bin/env python3

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from _recordlib import (
    first_nonempty_line,
    load_json_file,
    now_iso,
    parse_markdown_record,
    print_output,
    write_markdown_record,
)


TASK_DIR = Path(".work/tasks")
TASK_SECTION_ORDER = [
    "Goal",
    "Out of Scope",
    "Inputs / Constraints",
    "Relevant Paths",
    "Current State",
    "Active Decisions",
    "Open Issues",
    "Next Step",
    "Final Outcome",
    "Important Events",
]
TASK_METADATA_ORDER = [
    "id",
    "status",
    "created",
    "updated",
    "closed",
    "priority",
    "task_type",
    "tags",
    "related_paths",
    "source_refs",
    "summary",
    "next_action",
]
VALID_STATUS = {"planned", "active", "blocked", "done", "dropped"}


def default_task_metadata(path: Path) -> dict[str, Any]:
    timestamp = now_iso()
    return {
        "id": path.stem,
        "status": "active",
        "created": timestamp,
        "updated": timestamp,
        "closed": "",
        "priority": "medium",
        "task_type": "general",
        "tags": [],
        "related_paths": [],
        "source_refs": [],
        "summary": "",
        "next_action": "",
    }


def list_task_files(root: Path) -> list[Path]:
    if not root.exists():
        return []
    return sorted(
        [
            path
            for path in root.glob("*.md")
            if path.name != "README.md"
        ]
    )


def normalize_task_metadata(
    path: Path,
    existing: dict[str, Any],
    updates: dict[str, Any],
    sections: dict[str, str],
    section_updates: dict[str, str],
    touch_updated: bool,
) -> dict[str, Any]:
    metadata = default_task_metadata(path)
    metadata.update(existing)
    metadata.update({key: value for key, value in updates.items() if value is not None})

    if metadata["status"] not in VALID_STATUS:
        raise ValueError(f"Invalid task status: {metadata['status']}")

    metadata["tags"] = list(metadata.get("tags") or [])
    metadata["related_paths"] = list(metadata.get("related_paths") or [])
    metadata["source_refs"] = list(metadata.get("source_refs") or [])

    if touch_updated or not metadata.get("updated"):
        metadata["updated"] = now_iso()

    if metadata["status"] in {"done", "dropped"}:
        metadata["closed"] = metadata.get("closed") or now_iso()
    else:
        metadata["closed"] = ""

    summary_was_explicit = "summary" in updates
    next_action_was_explicit = "next_action" in updates

    if not summary_was_explicit and {"Goal", "Current State"} & set(section_updates):
        metadata["summary"] = first_nonempty_line(sections.get("Goal", "")) or first_nonempty_line(sections.get("Current State", ""))
    elif not metadata.get("summary"):
        metadata["summary"] = first_nonempty_line(sections.get("Goal", "")) or first_nonempty_line(sections.get("Current State", ""))

    if not next_action_was_explicit and "Next Step" in section_updates:
        metadata["next_action"] = first_nonempty_line(sections.get("Next Step", ""))
    elif not metadata.get("next_action"):
        metadata["next_action"] = first_nonempty_line(sections.get("Next Step", ""))

    return metadata


def normalize_task_sections(existing: dict[str, str], updates: dict[str, str]) -> dict[str, str]:
    merged = dict(existing)
    for name in TASK_SECTION_ORDER:
        merged.setdefault(name, "")
    for name, value in updates.items():
        if value is None:
            continue
        merged[name] = value

    if merged.get("Final Outcome") and merged.get("Current State"):
        merged["Current State"] = merged["Current State"].rstrip()

    return merged


def record_summary(path: Path) -> dict[str, Any]:
    record = parse_markdown_record(path)
    metadata = record["metadata"]
    return {
        "path": str(path),
        "title": record["title"] or path.stem,
        "status": metadata.get("status", ""),
        "updated": metadata.get("updated", ""),
        "priority": metadata.get("priority", ""),
        "task_type": metadata.get("task_type", ""),
        "summary": metadata.get("summary", ""),
        "next_action": metadata.get("next_action", ""),
        "tags": metadata.get("tags", []),
        "related_paths": metadata.get("related_paths", []),
    }


def command_list(args: argparse.Namespace) -> None:
    root = Path(args.root)
    items: list[dict[str, Any]] = []
    for path in list_task_files(root):
        summary = record_summary(path)
        if args.status and summary["status"] not in args.status:
            continue
        if args.tag and not set(args.tag).issubset(set(summary["tags"])):
            continue
        if args.task_type and summary["task_type"] != args.task_type:
            continue
        if args.query:
            haystack = " ".join(
                [
                    path.stem,
                    summary["title"],
                    summary["summary"],
                    summary["next_action"],
                    " ".join(summary["tags"]),
                ]
            ).lower()
            if args.query.lower() not in haystack:
                continue
        items.append(summary)

    items.sort(key=lambda item: item.get("updated", ""), reverse=True)
    if args.limit:
        items = items[: args.limit]

    if args.format == "json":
        print_output(items, "json")
        return

    for item in items:
        print(f"{item['path']} | {item['status']} | {item['updated']} | {item['title']} | {item['next_action']}")


def command_read(args: argparse.Namespace) -> None:
    record = parse_markdown_record(args.path)
    payload: dict[str, Any] = {
        "path": record["path"],
        "title": record["title"],
        "metadata": record["metadata"],
    }
    if not args.metadata_only:
        if args.section:
            payload["sections"] = {name: record["sections"].get(name, "") for name in args.section}
        else:
            payload["sections"] = record["sections"]
    print_output(payload, args.format)


def command_init(args: argparse.Namespace) -> None:
    path = Path(args.path)
    if path.exists():
        raise FileExistsError(f"Task file already exists: {path}")

    payload = load_json_file(args.payload)
    title = str(payload.get("title", "")).strip()
    if not title:
        raise ValueError("Task creation payload must include a non-empty title.")

    sections = normalize_task_sections(existing={}, updates=payload.get("sections", {}))
    metadata = normalize_task_metadata(
        path=path,
        existing={},
        updates=payload.get("metadata", {}),
        sections=sections,
        section_updates=payload.get("sections", {}),
        touch_updated=True,
    )

    write_markdown_record(
        path=path,
        metadata=metadata,
        key_order=TASK_METADATA_ORDER,
        title=title,
        sections=sections,
        canonical_order=TASK_SECTION_ORDER,
        existing_order=[],
    )
    print_output({"path": str(path), "created": True, "metadata": metadata}, args.format)


def command_update(args: argparse.Namespace) -> None:
    path = Path(args.path)
    record = parse_markdown_record(path)
    payload = load_json_file(args.payload)

    title = str(payload.get("title") or record["title"]).strip()
    if not title:
        raise ValueError("Task title cannot be empty.")

    sections = normalize_task_sections(existing=record["sections"], updates=payload.get("sections", {}))
    metadata = normalize_task_metadata(
        path=path,
        existing=record["metadata"],
        updates=payload.get("metadata", {}),
        sections=sections,
        section_updates=payload.get("sections", {}),
        touch_updated=not args.no_touch_updated,
    )

    write_markdown_record(
        path=path,
        metadata=metadata,
        key_order=TASK_METADATA_ORDER,
        title=title,
        sections=sections,
        canonical_order=TASK_SECTION_ORDER,
        existing_order=record["section_order"],
    )
    print_output({"path": str(path), "updated": True, "metadata": metadata}, args.format)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Structured task record helper.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    list_parser = subparsers.add_parser("list", help="List task records using metadata-first filters.")
    list_parser.add_argument("--root", default=str(TASK_DIR))
    list_parser.add_argument("--status", action="append")
    list_parser.add_argument("--tag", action="append")
    list_parser.add_argument("--task-type")
    list_parser.add_argument("--query")
    list_parser.add_argument("--limit", type=int)
    list_parser.add_argument("--format", choices=("text", "json"), default="text")
    list_parser.set_defaults(func=command_list)

    read_parser = subparsers.add_parser("read", help="Read one task record.")
    read_parser.add_argument("--path", required=True)
    read_parser.add_argument("--metadata-only", action="store_true")
    read_parser.add_argument("--section", action="append")
    read_parser.add_argument("--format", choices=("text", "json"), default="json")
    read_parser.set_defaults(func=command_read)

    init_parser = subparsers.add_parser("init", help="Create a task record from a JSON payload.")
    init_parser.add_argument("--path", required=True)
    init_parser.add_argument("--payload", required=True)
    init_parser.add_argument("--format", choices=("text", "json"), default="json")
    init_parser.set_defaults(func=command_init)

    update_parser = subparsers.add_parser("update", help="Update a task record from a JSON payload.")
    update_parser.add_argument("--path", required=True)
    update_parser.add_argument("--payload", required=True)
    update_parser.add_argument("--no-touch-updated", action="store_true")
    update_parser.add_argument("--format", choices=("text", "json"), default="json")
    update_parser.set_defaults(func=command_update)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
