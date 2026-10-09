#!/usr/bin/env python3
"""Create and list unpublished Facebook Page posts through Meta's Graph API."""
from __future__ import annotations

import argparse
import json
import os
import sys
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

GRAPH_VERSION = os.environ.get("META_GRAPH_VERSION", "v26.0")
GRAPH_BASE = f"https://graph.facebook.com/{GRAPH_VERSION}"


def required_environment() -> tuple[str, str]:
    page_id = os.environ.get("META_PAGE_ID")
    access_token = os.environ.get("META_PAGE_ACCESS_TOKEN")
    missing = [name for name, value in (("META_PAGE_ID", page_id), ("META_PAGE_ACCESS_TOKEN", access_token)) if not value]
    if missing:
        raise RuntimeError("Missing required environment variable(s): " + ", ".join(missing))
    return page_id, access_token


def request_graph(path: str, method: str, fields: dict[str, str]) -> dict[str, Any]:
    page_id, access_token = required_environment()
    payload = dict(fields)
    url = f"{GRAPH_BASE}/{page_id}/{path.lstrip('/')}"
    request = Request(url, data=urlencode(payload).encode("utf-8") if method == "POST" else None, method=method)
    if method == "GET":
        request = Request(f"{url}?{urlencode(payload)}", method="GET")
    request.add_header("Accept", "application/json")
    request.add_header("Authorization", f"Bearer {access_token}")
    try:
        with urlopen(request, timeout=30) as response:
            return json.loads(response.read().decode("utf-8"))
    except HTTPError as error:
        detail = error.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Meta Graph API returned HTTP {error.code}: {detail}") from error
    except URLError as error:
        raise RuntimeError(f"Meta Graph API connection failed: {error.reason}") from error


def create_draft(message: str, link: str | None = None) -> dict[str, Any]:
    if not message.strip():
        raise ValueError("message must not be empty")
    fields = {"message": message, "published": "false"}
    if link:
        fields["link"] = link
    return request_graph("feed", "POST", fields)


def list_drafts() -> dict[str, Any]:
    return request_graph("feed", "GET", {"is_published": "false", "fields": "id,message,created_time"})


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    create = subparsers.add_parser("create-draft")
    create.add_argument("--message", required=True)
    create.add_argument("--link")
    subparsers.add_parser("list-drafts")
    args = parser.parse_args()
    try:
        result = create_draft(args.message, args.link) if args.command == "create-draft" else list_drafts()
    except (RuntimeError, ValueError) as error:
        print(str(error), file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
