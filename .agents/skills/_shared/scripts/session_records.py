#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import os
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

from _recordlib import current_codex_session_id, load_toml_file, parse_markdown_record, print_output


SESSION_STORE = Path.home() / ".codex" / "sessions"


@dataclass
class SessionMeta:
    session_id: str
    path: Path
    cwd: str
    started_at: str


def parse_iso(value: str) -> datetime | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def iter_session_files(root: Path) -> list[Path]:
    if not root.exists():
        return []
    return sorted(root.rglob("*.jsonl"))


def load_session_meta(path: Path) -> SessionMeta | None:
    try:
        with path.open(encoding="utf-8") as handle:
            first = handle.readline()
    except OSError:
        return None

    try:
        payload = json.loads(first)
    except json.JSONDecodeError:
        return None

    if payload.get("type") != "session_meta":
        return None

    meta = payload.get("payload") or {}
    session_id = str(meta.get("id") or "")
    if not session_id:
        return None

    return SessionMeta(
        session_id=session_id,
        path=path,
        cwd=str(meta.get("cwd") or ""),
        started_at=str(meta.get("timestamp") or payload.get("timestamp") or ""),
    )


def resolve_session_file(session_id: str, root: Path) -> Path | None:
    if not session_id:
        return None
    for path in iter_session_files(root):
        if session_id in path.name:
            return path
    return None


def extract_visible_messages(path: Path) -> list[dict[str, str]]:
    messages: list[dict[str, str]] = []
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            try:
                entry = json.loads(line)
            except json.JSONDecodeError:
                continue

            timestamp = str(entry.get("timestamp") or "")
            entry_type = entry.get("type")
            payload = entry.get("payload") or {}

            if entry_type == "event_msg" and payload.get("type") == "user_message":
                text = str(payload.get("message") or "").strip()
                if text:
                    messages.append({"role": "user", "timestamp": timestamp, "text": text})
                continue

            if entry_type == "response_item" and payload.get("type") == "message" and payload.get("role") == "assistant":
                chunks = []
                for item in payload.get("content") or []:
                    if item.get("type") == "output_text":
                        chunks.append(str(item.get("text") or ""))
                    elif item.get("type") == "input_text":
                        chunks.append(str(item.get("text") or ""))
                text = "\n".join(chunk for chunk in chunks if chunk).strip()
                if text:
                    messages.append({"role": "assistant", "timestamp": timestamp, "text": text})

    return messages


def task_keywords(record: dict[str, Any]) -> set[str]:
    keywords: set[str] = set()
    metadata = record.get("metadata") or {}
    text_bits = [
        record.get("title") or "",
        str(metadata.get("summary") or ""),
        str(metadata.get("next_action") or ""),
    ]
    for bit in text_bits:
        for token in bit.lower().replace("/", " ").replace("-", " ").split():
            token = token.strip(".,:;()[]{}<>\"'")
            if len(token) >= 4:
                keywords.add(token)
    return keywords


def session_registry_dir(task_path: Path) -> Path:
    return task_path.parent.parent / "sessions"


def registry_record_for_session(task_path: Path, session_id: str) -> dict[str, Any]:
    path = session_registry_dir(task_path) / f"{session_id}.toml"
    if not path.exists():
        return {}
    try:
        return load_toml_file(path)
    except Exception:
        return {}


def infer_candidates(task_path: Path, sessions_root: Path, limit: int | None = None) -> list[dict[str, Any]]:
    task = parse_markdown_record(task_path)
    metadata = task["metadata"]
    workstream_id = str(metadata.get("workstream_id") or "")
    created = parse_iso(str(metadata.get("created") or ""))
    updated = parse_iso(str(metadata.get("updated") or ""))
    closed = parse_iso(str(metadata.get("closed") or ""))
    keywords = task_keywords(task)

    explicit_ids = list(metadata.get("session_refs") or [])
    explicit_paths: list[dict[str, Any]] = []
    seen_ids: set[str] = set()

    for session_id in explicit_ids:
        resolved = resolve_session_file(str(session_id), sessions_root)
        if not resolved:
            continue
        meta = load_session_meta(resolved)
        if not meta:
            continue
        registry = registry_record_for_session(task_path, meta.session_id)
        explicit_paths.append(
            {
                "session_id": meta.session_id,
                "path": str(meta.path),
                "cwd": meta.cwd,
                "started_at": meta.started_at,
                "label": str(registry.get("label") or ""),
                "source": "task.session_refs",
                "score": 100,
                "reasons": ["explicit task session ref"],
            }
        )
        seen_ids.add(meta.session_id)

    if explicit_paths:
        return explicit_paths[:limit] if limit else explicit_paths

    candidates: list[dict[str, Any]] = []
    lower_workstream_marker = f"{os.sep}workstreams{os.sep}{workstream_id}" if workstream_id else ""

    for path in iter_session_files(sessions_root):
        meta = load_session_meta(path)
        if not meta or meta.session_id in seen_ids:
            continue

        score = 0
        reasons: list[str] = []
        cwd_lower = meta.cwd.lower()
        if lower_workstream_marker and lower_workstream_marker in cwd_lower:
            score += 50
            reasons.append("workstream execution cwd match")

        started_dt = parse_iso(meta.started_at)
        window_start = created or updated or closed
        window_end = closed or updated or created
        if started_dt and window_start and window_end:
            window_start = window_start - timedelta(days=1)
            window_end = window_end + timedelta(days=1)
            if window_start <= started_dt <= window_end:
                score += 20
                reasons.append("timestamp near task activity window")

        if keywords:
            try:
                content = path.read_text(encoding="utf-8", errors="ignore").lower()
            except OSError:
                content = ""
            keyword_hits = [keyword for keyword in keywords if keyword in content]
            if keyword_hits:
                score += min(20, len(keyword_hits) * 5)
                reasons.append(f"keyword hits: {', '.join(sorted(keyword_hits)[:4])}")

        if score <= 0:
            continue

        registry = registry_record_for_session(task_path, meta.session_id)
        candidates.append(
            {
                "session_id": meta.session_id,
                "path": str(meta.path),
                "cwd": meta.cwd,
                "started_at": meta.started_at,
                "label": str(registry.get("label") or ""),
                "source": "inferred",
                "score": score,
                "reasons": reasons,
            }
        )

    candidates.sort(key=lambda item: (-int(item["score"]), item["started_at"]), reverse=False)
    return candidates[:limit] if limit else candidates


def command_current(args: argparse.Namespace) -> None:
    session_id = current_codex_session_id()
    session_file = resolve_session_file(session_id, Path(args.sessions_root))
    payload = {
        "session_id": session_id,
        "path": str(session_file) if session_file else "",
    }
    print_output(payload, args.format)


def command_resolve(args: argparse.Namespace) -> None:
    resolved = resolve_session_file(args.session_id, Path(args.sessions_root))
    payload = {
        "session_id": args.session_id,
        "path": str(resolved) if resolved else "",
    }
    print_output(payload, args.format)


def command_candidates(args: argparse.Namespace) -> None:
    items = infer_candidates(Path(args.task_path), Path(args.sessions_root), args.limit)
    print_output(items, args.format)


def command_read(args: argparse.Namespace) -> None:
    path = Path(args.path)
    meta = load_session_meta(path)
    if not meta:
        raise ValueError(f"Could not parse session metadata from: {path}")

    messages = extract_visible_messages(path)
    if args.max_messages:
        messages = messages[-args.max_messages :]

    payload = {
        "session_id": meta.session_id,
        "path": str(path),
        "cwd": meta.cwd,
        "started_at": meta.started_at,
        "message_count": len(messages),
        "messages": messages,
    }

    if args.format == "text":
        print(f"Session: {meta.session_id}")
        print(f"Path: {path}")
        print(f"CWD: {meta.cwd}")
        print(f"Started: {meta.started_at}")
        print("")
        for item in messages:
            role = item["role"].capitalize()
            print(f"[{role}] {item['timestamp']}")
            print(item["text"])
            print("")
        return

    print_output(payload, "json")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Codex session transcript helper.")
    parser.add_argument(
        "--sessions-root",
        default=str(SESSION_STORE),
        help="Path to the Codex session store.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    current_parser = subparsers.add_parser("current", help="Resolve the current Codex session file.")
    current_parser.add_argument("--format", choices=("text", "json"), default="json")
    current_parser.set_defaults(func=command_current)

    resolve_parser = subparsers.add_parser("resolve", help="Resolve one session id to a transcript path.")
    resolve_parser.add_argument("--session-id", required=True)
    resolve_parser.add_argument("--format", choices=("text", "json"), default="json")
    resolve_parser.set_defaults(func=command_resolve)

    candidates_parser = subparsers.add_parser("candidates", help="Find likely session transcripts for a task.")
    candidates_parser.add_argument("--task-path", required=True)
    candidates_parser.add_argument("--limit", type=int, default=5)
    candidates_parser.add_argument("--format", choices=("text", "json"), default="json")
    candidates_parser.set_defaults(func=command_candidates)

    read_parser = subparsers.add_parser("read", help="Read visible messages from one session transcript.")
    read_parser.add_argument("--path", required=True)
    read_parser.add_argument("--max-messages", type=int)
    read_parser.add_argument("--format", choices=("text", "json"), default="json")
    read_parser.set_defaults(func=command_read)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
