#!/usr/bin/env python3
"""Wire this sample into the default personal Codex marketplace.

The default personal marketplace file is ~/.agents/plugins/marketplace.json,
but its plugin source path ./plugins/<name> resolves to ~/plugins/<name>.
This script creates that canonical symlink and upserts the marketplace entry.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any


PLUGIN_NAME = "codex-agent-team"


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {
            "name": "personal",
            "interface": {"displayName": "Personal"},
            "plugins": [],
        }

    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)

    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a JSON object")
    if data.get("name") != "personal":
        raise ValueError(
            f"{path} has marketplace name {data.get('name')!r}; refusing to rewrite "
            "a non-personal marketplace"
        )
    data.setdefault("interface", {"displayName": "Personal"})
    data.setdefault("plugins", [])
    if not isinstance(data["plugins"], list):
        raise ValueError(f"{path} field plugins must be a list")
    return data


def upsert_plugin_entry(data: dict[str, Any]) -> None:
    entry = {
        "name": PLUGIN_NAME,
        "source": {
            "source": "local",
            "path": f"./plugins/{PLUGIN_NAME}",
        },
        "policy": {
            "installation": "AVAILABLE",
            "authentication": "ON_INSTALL",
        },
        "category": "Developer Tools",
    }

    plugins = data["plugins"]
    for index, existing in enumerate(plugins):
        if isinstance(existing, dict) and existing.get("name") == PLUGIN_NAME:
            plugins[index] = entry
            return
    plugins.append(entry)


def write_json(path: Path, data: dict[str, Any], dry_run: bool) -> None:
    rendered = json.dumps(data, indent=2) + "\n"
    if dry_run:
        print(f"Would write {path}")
        return

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(rendered, encoding="utf-8")


def ensure_symlink(link_path: Path, target_path: Path, dry_run: bool, force: bool) -> None:
    if link_path.exists() or link_path.is_symlink():
        current = link_path.resolve()
        if current == target_path.resolve():
            return
        if dry_run:
            action = "replace" if force else "refuse to replace"
            print(f"Would {action} existing {link_path} -> {current}")
            return
        if not force:
            raise FileExistsError(
                f"{link_path} already exists and points to {current}; use --force to replace it"
            )
        if link_path.is_dir() and not link_path.is_symlink():
            raise IsADirectoryError(
                f"{link_path} is a directory. Move it aside manually before using --force."
            )
        link_path.unlink()

    if dry_run:
        print(f"Would create symlink {link_path} -> {target_path}")
        return

    link_path.parent.mkdir(parents=True, exist_ok=True)
    link_path.symlink_to(target_path, target_is_directory=True)


def run_codex_add(dry_run: bool) -> None:
    command = ["codex", "plugin", "add", f"{PLUGIN_NAME}@personal"]
    if dry_run:
        print("Would run:", " ".join(command))
        return
    subprocess.run(command, check=True)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Install this repo's codex-agent-team plugin into the personal Codex marketplace."
    )
    parser.add_argument("--dry-run", action="store_true", help="show changes without writing")
    parser.add_argument(
        "--force",
        action="store_true",
        help="replace an existing wrong ~/plugins/codex-agent-team symlink",
    )
    parser.add_argument(
        "--refresh-cache",
        action="store_true",
        help="run `codex plugin add codex-agent-team@personal` after wiring the marketplace",
    )
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[1]
    plugin_source = repo_root / "plugins" / PLUGIN_NAME
    plugin_manifest = plugin_source / ".codex-plugin" / "plugin.json"
    if not plugin_manifest.exists():
        print(f"Missing plugin manifest: {plugin_manifest}", file=sys.stderr)
        return 1

    home = Path.home()
    marketplace_path = home / ".agents" / "plugins" / "marketplace.json"
    personal_plugin_path = home / "plugins" / PLUGIN_NAME

    data = load_json(marketplace_path)
    upsert_plugin_entry(data)
    ensure_symlink(personal_plugin_path, plugin_source, args.dry_run, args.force)
    write_json(marketplace_path, data, args.dry_run)

    print(f"Personal marketplace: {marketplace_path}")
    print(f"Plugin source link: {personal_plugin_path} -> {plugin_source}")
    if args.refresh_cache:
        run_codex_add(args.dry_run)
    else:
        print(f"Refresh Codex plugin cache with: codex plugin add {PLUGIN_NAME}@personal")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
