#!/usr/bin/env python3
"""Fail-open subagent lifecycle logger for the local Codex team workflow."""

from __future__ import annotations

import fcntl
import json
import os
import sys
from datetime import datetime, timezone


def codex_home() -> str:
    configured = os.environ.get("CODEX_HOME")
    if configured:
        return os.path.abspath(os.path.expanduser(configured))

    home = os.environ.get("HOME")
    if home:
        return os.path.join(os.path.abspath(os.path.expanduser(home)), ".codex")

    return os.path.expanduser("~/.codex")


LOG_DIR = os.path.join(codex_home(), "team-logs")
LOG_PATH = os.path.join(LOG_DIR, "subagent-events.jsonl")
LOCK_PATH = f"{LOG_PATH}.lock"
MAX_LOG_BYTES = 1_048_576
BACKUP_COUNT = 3
ALLOWED_PAYLOAD_KEYS = {
    "agent_id",
    "agent_type",
    "cwd",
    "hook_event_name",
    "model",
    "permission_mode",
    "session_id",
    "state",
    "stop_hook_active",
    "turn_id",
}


def now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")


def rotate_log(path: str) -> None:
    try:
        if not os.path.exists(path) or os.path.getsize(path) < MAX_LOG_BYTES:
            return
        oldest_backup = f"{path}.{BACKUP_COUNT}"
        if os.path.exists(oldest_backup):
            os.remove(oldest_backup)
        for index in range(BACKUP_COUNT - 1, 0, -1):
            source = f"{path}.{index}"
            target = f"{path}.{index + 1}"
            if os.path.exists(source):
                os.replace(source, target)
        os.replace(path, f"{path}.1")
    except Exception:
        pass


def filtered_payload(payload: object) -> dict:
    if not isinstance(payload, dict):
        return {}
    return {
        key: value
        for key, value in payload.items()
        if key in ALLOWED_PAYLOAD_KEYS
    }


def main() -> int:
    event_name = "SubagentLifecycle"
    state = sys.argv[1] if len(sys.argv) > 1 else "unknown"
    try:
        raw = sys.stdin.read().strip()
        payload = json.loads(raw) if raw else {}
    except Exception:
        payload = {}

    record = {
        "captured_at": now(),
        "event": event_name,
        "state": state,
        "payload": filtered_payload(payload),
    }
    try:
        os.makedirs(LOG_DIR, exist_ok=True)
        with open(LOCK_PATH, "a", encoding="utf-8") as lock_handle:
            fcntl.flock(lock_handle.fileno(), fcntl.LOCK_EX)
            rotate_log(LOG_PATH)
            with open(LOG_PATH, "a", encoding="utf-8") as handle:
                handle.write(json.dumps(record) + "\n")
    except Exception:
        pass
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
