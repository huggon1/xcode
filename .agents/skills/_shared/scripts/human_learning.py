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


ITEM_DIR = Path(".work/human-learning/items")
ITEM_SECTION_ORDER = [
    "Why This Matters",
    "Applies When",
    "Better Behavior",
    "Success Signals",
    "Failure Signals",
    "Notes",
]
ITEM_METADATA_ORDER = [
    "id",
    "status",
    "created",
    "updated",
    "success_streak",
    "retire_after",
    "scope",
    "tags",
    "applies_to",
    "summary",
]
VALID_STATUS = {"active", "delete"}
VALID_REVIEW_RESULT = {"met", "missed", "not-applicable"}


def default_item_metadata(path: Path) -> dict[str, Any]:
    timestamp = now_iso()
    return {
        "id": path.stem,
        "status": "active",
        "created": timestamp,
        "updated": timestamp,
        "success_streak": 0,
        "retire_after": 3,
        "scope": "project",
        "tags": [],
        "applies_to": [],
        "summary": "",
    }


def list_item_files(root: Path) -> list[Path]:
    if not root.exists():
        return []
    return sorted(
        [
            path
            for path in root.glob("*.md")
            if path.name != "README.md"
        ]
    )


def normalize_item_metadata(
    path: Path,
    existing: dict[str, Any],
    updates: dict[str, Any],
    sections: dict[str, str],
    section_updates: dict[str, str],
    touch_updated: bool,
) -> dict[str, Any]:
    metadata = default_item_metadata(path)
    metadata.update(existing)
    metadata.update({key: value for key, value in updates.items() if value is not None})

    if metadata["status"] not in VALID_STATUS:
        raise ValueError(f"Invalid human-learning status: {metadata['status']}")

    metadata["tags"] = list(metadata.get("tags") or [])
    metadata["applies_to"] = list(metadata.get("applies_to") or [])
    metadata["success_streak"] = int(metadata.get("success_streak", 0))
    metadata["retire_after"] = int(metadata.get("retire_after", 3))

    if touch_updated or not metadata.get("updated"):
        metadata["updated"] = now_iso()

    summary_was_explicit = "summary" in updates

    if not summary_was_explicit and {"Why This Matters", "Better Behavior"} & set(section_updates):
        metadata["summary"] = first_nonempty_line(sections.get("Why This Matters", "")) or first_nonempty_line(sections.get("Better Behavior", ""))
    elif not metadata.get("summary"):
        metadata["summary"] = first_nonempty_line(sections.get("Why This Matters", "")) or first_nonempty_line(sections.get("Better Behavior", ""))

    return metadata


def normalize_item_sections(existing: dict[str, str], updates: dict[str, str]) -> dict[str, str]:
    merged = dict(existing)
    for name in ITEM_SECTION_ORDER:
        merged.setdefault(name, "")
    for name, value in updates.items():
        if value is None:
            continue
        merged[name] = value
    return merged


def record_summary(path: Path) -> dict[str, Any]:
    record = parse_markdown_record(path)
    metadata = record["metadata"]
    return {
        "path": str(path),
        "title": record["title"] or path.stem,
        "status": metadata.get("status", ""),
        "updated": metadata.get("updated", ""),
        "success_streak": metadata.get("success_streak", 0),
        "retire_after": metadata.get("retire_after", 3),
        "scope": metadata.get("scope", ""),
        "summary": metadata.get("summary", ""),
        "tags": metadata.get("tags", []),
        "applies_to": metadata.get("applies_to", []),
    }


def command_list(args: argparse.Namespace) -> None:
    root = Path(args.root)
    items: list[dict[str, Any]] = []
    for path in list_item_files(root):
        summary = record_summary(path)
        if args.status and summary["status"] not in args.status:
            continue
        if args.tag and not set(args.tag).issubset(set(summary["tags"])):
            continue
        if args.query:
            haystack = " ".join(
                [
                    path.stem,
                    summary["title"],
                    summary["summary"],
                    " ".join(summary["tags"]),
                    " ".join(summary["applies_to"]),
                ]
            ).lower()
            if args.query.lower() not in haystack:
                continue
        items.append(summary)

    items.sort(key=lambda item: item.get("updated", ""), reverse=True)
    if args.format == "json":
        print_output(items, "json")
        return

    for item in items:
        print(f"{item['path']} | {item['status']} | streak={item['success_streak']} | {item['title']}")


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


def command_upsert(args: argparse.Namespace) -> None:
    path = Path(args.path)
    payload = load_json_file(args.payload)
    if path.exists():
        record = parse_markdown_record(path)
        existing_metadata = record["metadata"]
        existing_sections = record["sections"]
        existing_order = record["section_order"]
        title = str(payload.get("title") or record["title"]).strip()
    else:
        existing_metadata = {}
        existing_sections = {}
        existing_order = []
        title = str(payload.get("title", "")).strip()

    if not title:
        raise ValueError("Human-learning item title cannot be empty.")

    sections = normalize_item_sections(existing=existing_sections, updates=payload.get("sections", {}))
    metadata = normalize_item_metadata(
        path=path,
        existing=existing_metadata,
        updates=payload.get("metadata", {}),
        sections=sections,
        section_updates=payload.get("sections", {}),
        touch_updated=not args.no_touch_updated,
    )

    write_markdown_record(
        path=path,
        metadata=metadata,
        key_order=ITEM_METADATA_ORDER,
        title=title,
        sections=sections,
        canonical_order=ITEM_SECTION_ORDER,
        existing_order=existing_order,
    )
    print_output({"path": str(path), "upserted": True, "metadata": metadata}, args.format)


def command_review(args: argparse.Namespace) -> None:
    if args.result not in VALID_REVIEW_RESULT:
        raise ValueError(f"Invalid review result: {args.result}")

    path = Path(args.path)
    record = parse_markdown_record(path)
    metadata = normalize_item_metadata(
        path=path,
        existing=record["metadata"],
        updates={},
        sections=record["sections"],
        section_updates={},
        touch_updated=True,
    )

    if args.result == "met":
        metadata["success_streak"] = int(metadata.get("success_streak", 0)) + 1
    elif args.result == "missed":
        metadata["success_streak"] = 0

    if args.mark_delete:
        metadata["status"] = "delete"

    write_markdown_record(
        path=path,
        metadata=metadata,
        key_order=ITEM_METADATA_ORDER,
        title=record["title"],
        sections=record["sections"],
        canonical_order=ITEM_SECTION_ORDER,
        existing_order=record["section_order"],
    )

    suggest_delete = metadata["status"] != "delete" and metadata["success_streak"] >= metadata["retire_after"]
    print_output(
        {
            "path": str(path),
            "result": args.result,
            "metadata": metadata,
            "suggest_delete": suggest_delete,
        },
        args.format,
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Structured human-learning helper.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    list_parser = subparsers.add_parser("list", help="List human-learning items.")
    list_parser.add_argument("--root", default=str(ITEM_DIR))
    list_parser.add_argument("--status", action="append")
    list_parser.add_argument("--tag", action="append")
    list_parser.add_argument("--query")
    list_parser.add_argument("--format", choices=("text", "json"), default="text")
    list_parser.set_defaults(func=command_list)

    read_parser = subparsers.add_parser("read", help="Read one human-learning item.")
    read_parser.add_argument("--path", required=True)
    read_parser.add_argument("--metadata-only", action="store_true")
    read_parser.add_argument("--section", action="append")
    read_parser.add_argument("--format", choices=("text", "json"), default="json")
    read_parser.set_defaults(func=command_read)

    upsert_parser = subparsers.add_parser("upsert", help="Create or update a human-learning item from a JSON payload.")
    upsert_parser.add_argument("--path", required=True)
    upsert_parser.add_argument("--payload", required=True)
    upsert_parser.add_argument("--no-touch-updated", action="store_true")
    upsert_parser.add_argument("--format", choices=("text", "json"), default="json")
    upsert_parser.set_defaults(func=command_upsert)

    review_parser = subparsers.add_parser("review", help="Update streak metadata for an existing human-learning item.")
    review_parser.add_argument("--path", required=True)
    review_parser.add_argument("--result", required=True, choices=sorted(VALID_REVIEW_RESULT))
    review_parser.add_argument("--mark-delete", action="store_true")
    review_parser.add_argument("--format", choices=("text", "json"), default="json")
    review_parser.set_defaults(func=command_review)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
