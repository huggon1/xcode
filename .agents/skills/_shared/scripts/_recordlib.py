#!/usr/bin/env python3

from __future__ import annotations

import json
from collections.abc import Iterable, Mapping
from datetime import datetime
from pathlib import Path
import tomllib


FRONTMATTER_BOUNDARY = "+++"


def now_iso() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def strip_blank_edges(text: str) -> str:
    lines = text.splitlines()
    while lines and not lines[0].strip():
        lines.pop(0)
    while lines and not lines[-1].strip():
        lines.pop()
    return "\n".join(lines)


def first_nonempty_line(text: str) -> str:
    for line in text.splitlines():
        if line.strip():
            return line.strip()
    return ""


def load_json_file(path: str | Path) -> dict:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("Payload must be a JSON object.")
    return data


def parse_frontmatter(text: str) -> tuple[dict, str]:
    if not text.startswith(f"{FRONTMATTER_BOUNDARY}\n"):
        if text.startswith("---\n"):
            raise ValueError("YAML frontmatter is not supported by these helpers. Migrate the file to TOML frontmatter first.")
        return {}, text

    lines = text.splitlines(keepends=True)
    for index in range(1, len(lines)):
        if lines[index].strip() == FRONTMATTER_BOUNDARY:
            frontmatter_text = "".join(lines[1:index])
            body = "".join(lines[index + 1 :])
            metadata = tomllib.loads(frontmatter_text) if frontmatter_text.strip() else {}
            if not isinstance(metadata, dict):
                raise ValueError("Frontmatter must decode to a TOML table.")
            return metadata, body.lstrip("\n")
    raise ValueError("Unterminated TOML frontmatter block.")


def dump_frontmatter(metadata: Mapping[str, object], key_order: Iterable[str]) -> str:
    lines: list[str] = [FRONTMATTER_BOUNDARY]
    emitted: set[str] = set()

    for key in key_order:
        if key in metadata:
            lines.append(f"{key} = {toml_value(metadata[key])}")
            emitted.add(key)

    for key in metadata:
        if key not in emitted:
            lines.append(f"{key} = {toml_value(metadata[key])}")

    lines.append(FRONTMATTER_BOUNDARY)
    return "\n".join(lines)


def toml_value(value: object) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, int):
        return str(value)
    if isinstance(value, str):
        escaped = value.replace("\\", "\\\\").replace('"', '\\"')
        return f'"{escaped}"'
    if isinstance(value, list):
        if not all(isinstance(item, str) for item in value):
            raise TypeError("Only lists of strings are supported in frontmatter.")
        inner = ", ".join(toml_value(item) for item in value)
        return f"[{inner}]"
    raise TypeError(f"Unsupported frontmatter value type: {type(value)!r}")


def parse_markdown_record(path: str | Path) -> dict:
    text = Path(path).read_text(encoding="utf-8")
    metadata, body = parse_frontmatter(text)
    title, sections, section_order = parse_sections(body)
    return {
        "path": str(path),
        "metadata": metadata,
        "title": title,
        "sections": sections,
        "section_order": section_order,
    }


def parse_sections(body: str) -> tuple[str, dict[str, str], list[str]]:
    title = ""
    sections: dict[str, str] = {}
    section_order: list[str] = []
    current_name: str | None = None
    current_lines: list[str] = []

    for line in body.splitlines():
        if not title and line.startswith("# "):
            title = line[2:].strip()
            continue

        if line.startswith("## "):
            if current_name is not None:
                sections[current_name] = strip_blank_edges("\n".join(current_lines))
            current_name = line[3:].strip()
            section_order.append(current_name)
            current_lines = []
            continue

        if current_name is not None:
            current_lines.append(line)

    if current_name is not None:
        sections[current_name] = strip_blank_edges("\n".join(current_lines))

    return title, sections, section_order


def build_markdown_record(
    title: str,
    sections: Mapping[str, str],
    canonical_order: list[str],
    existing_order: list[str] | None = None,
) -> str:
    extras: list[str] = []
    if existing_order:
        extras = [name for name in existing_order if name not in canonical_order]

    ordered_names = canonical_order + [name for name in extras if name in sections]
    lines: list[str] = [f"# {title.strip()}"]

    for name in ordered_names:
        lines.extend(["", f"## {name}", ""])
        content = strip_blank_edges(sections.get(name, ""))
        if content:
            lines.append(content)

    return "\n".join(lines).rstrip() + "\n"


def write_markdown_record(
    path: str | Path,
    metadata: Mapping[str, object],
    key_order: Iterable[str],
    title: str,
    sections: Mapping[str, str],
    canonical_order: list[str],
    existing_order: list[str] | None = None,
) -> None:
    frontmatter = dump_frontmatter(metadata, key_order)
    body = build_markdown_record(title=title, sections=sections, canonical_order=canonical_order, existing_order=existing_order)
    output = f"{frontmatter}\n\n{body}"
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(output, encoding="utf-8")


def print_output(payload: object, output_format: str) -> None:
    if output_format == "json":
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        return

    if isinstance(payload, str):
        print(payload)
        return

    print(json.dumps(payload, indent=2, ensure_ascii=False))
