#!/usr/bin/env python3
"""Create a safe, importable inventory of a Termux workspace.

Only paths, file sizes, timestamps, and detected extensions are exported.
File contents, dotfiles, credentials, tokens, cookies, and archives are never read.
"""
from __future__ import annotations

import argparse
import json
import os
from datetime import datetime, timezone
from pathlib import Path

SKIP_NAMES = {
    ".git", ".env", ".env.local", ".ssh", ".gnupg", "credentials.json",
    "token.json", "cookies.json", "mcp_config.json", "config.json",
}
SKIP_SUFFIXES = {".zip", ".tar", ".gz", ".key", ".pem", ".p12", ".sqlite", ".db"}


def safe_path(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def scan(root: Path) -> dict:
    root = root.expanduser().resolve()
    if not root.is_dir():
        raise SystemExit(f"Not a directory: {root}")
    files = []
    skipped = []
    for current, dirs, names in os.walk(root):
        dirs[:] = [d for d in dirs if d not in SKIP_NAMES and not d.startswith(".")]
        for name in sorted(names):
            path = Path(current) / name
            rel = safe_path(path, root)
            if name in SKIP_NAMES or name.startswith(".") or path.suffix.lower() in SKIP_SUFFIXES:
                skipped.append(rel)
                continue
            try:
                stat = path.stat()
            except OSError:
                continue
            files.append({
                "path": rel,
                "name": name,
                "extension": path.suffix.lower().lstrip("."),
                "bytes": stat.st_size,
                "modified": datetime.fromtimestamp(stat.st_mtime, timezone.utc).isoformat(),
            })
    return {
        "format": "profitnoter.termux-manifest.v1",
        "source": "Termux workspace inventory",
        "root_name": root.name or "/",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "files": files,
        "skipped_for_safety": skipped,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path, help="Termux directory to inventory")
    parser.add_argument("-o", "--output", type=Path, help="JSON output path; defaults to stdout")
    args = parser.parse_args()
    payload = json.dumps(scan(args.root), indent=2) + "\n"
    if args.output:
        args.output.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()
