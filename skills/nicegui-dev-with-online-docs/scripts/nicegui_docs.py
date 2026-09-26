#!/usr/bin/env python3
"""Search NiceGUI's live, machine-readable documentation index.

NiceGUI publishes its whole documentation as JSON endpoints, so answers can be
grounded in the *current* docs instead of stale model knowledge. See:
https://nicegui.io/documentation/section_configuration_deployment#documentation_index

Endpoints (each is a JSON array of objects with title/content/format/url,
plus "demo" on the sitewide index only):

  sitewide_index.json  ~791 entries, includes Python demo code  (~158k tokens)
  search_index.json    ~850 entries, no demo code, includes GitHub examples
  examples_index.json   ~59 entries, GitHub examples only

Loading a whole index into context is expensive, so this script downloads once,
caches locally, and filters by regex before printing. Prefer this over pasting
the raw JSON into a prompt.

Examples:
  python3 nicegui_docs.py "ui.table"
  python3 nicegui_docs.py "gap" --demo --limit 5
  python3 nicegui_docs.py "upload" --index search
  python3 nicegui_docs.py "auth" --index examples
  python3 nicegui_docs.py --refresh
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
import urllib.request
from pathlib import Path

BASE_URL = "https://nicegui.io/static"
INDICES = ("sitewide", "search", "examples")
CACHE_TTL_SECONDS = 7 * 24 * 60 * 60  # re-download weekly by default


def cache_dir() -> Path:
    override = os.environ.get("NICEGUI_DOCS_CACHE")
    if override:
        return Path(override)
    return Path(os.environ.get("XDG_CACHE_HOME", Path.home() / ".cache")) / "nicegui-docs"


def fetch(index: str, refresh: bool = False) -> list[dict]:
    """Return the parsed index, downloading to the cache when missing or stale."""
    directory = cache_dir()
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / f"{index}_index.json"

    if not refresh and path.exists():
        age = time.time() - path.stat().st_mtime
        if age < CACHE_TTL_SECONDS:
            return json.loads(path.read_text(encoding="utf-8"))

    url = f"{BASE_URL}/{index}_index.json"
    print(f"# downloading {url}", file=sys.stderr)
    with urllib.request.urlopen(url, timeout=60) as response:
        payload = json.loads(response.read().decode("utf-8"))
    path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
    return payload


def matches(entry: dict, pattern: re.Pattern[str]) -> bool:
    return bool(pattern.search(entry.get("title", "")) or pattern.search(entry.get("content", "")))


def render(entry: dict, show_demo: bool) -> str:
    lines = [f"## {entry.get('title', '(untitled)')}", f"url: {entry.get('url', '')}"]
    content = (entry.get("content") or "").strip()
    if content:
        lines.append(content)
    if show_demo:
        demo = (entry.get("demo") or "").strip()
        if demo:
            lines.append("")
            lines.append("```python")
            lines.append(demo)
            lines.append("```")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("query", nargs="?", help="regex matched against title and content (case-insensitive)")
    parser.add_argument("--index", choices=INDICES, default="sitewide", help="which index to search (default: sitewide)")
    parser.add_argument("--demo", action="store_true", help="include demo code (sitewide index only)")
    parser.add_argument("--limit", type=int, default=10, help="maximum matches to print (default: 10)")
    parser.add_argument("--refresh", action="store_true", help="re-download the index even if cached")
    parser.add_argument("--json", action="store_true", help="print matching entries as raw JSON")
    args = parser.parse_args()

    entries = fetch(args.index, refresh=args.refresh)

    if not args.query:
        print(f"# {args.index}_index.json: {len(entries)} entries (cached in {cache_dir()})")
        return 0

    try:
        pattern = re.compile(args.query, re.IGNORECASE)
    except re.error as exc:
        parser.error(f"invalid regex {args.query!r}: {exc}")

    hits = [entry for entry in entries if matches(entry, pattern)]
    # Title matches are more relevant, so surface them first.
    hits.sort(key=lambda e: (not pattern.search(e.get("title", "")), e.get("title", "")))
    hits = hits[: args.limit]

    if args.json:
        print(json.dumps(hits, indent=2, ensure_ascii=False))
        return 0

    if not hits:
        print(f"No matches for {args.query!r} in {args.index}_index.json.", file=sys.stderr)
        return 1

    for i, entry in enumerate(hits):
        if i:
            print("\n---\n")
        print(render(entry, args.demo))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
