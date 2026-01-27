#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import re
from pathlib import Path


IMG_TAG_RE = re.compile(r"<img\b[^>]*>", re.IGNORECASE)
# Important: don't treat `data-src` as `src` (word-boundary regex would match).
SRC_ATTR_RE = re.compile(r"\ssrc\s*=", re.IGNORECASE)
DATA_SRC_ATTR_RE = re.compile(r"\sdata-src\s*=\s*(\"[^\"]*\"|'[^']*')", re.IGNORECASE)

# RevealJS internal links: href="#/slide-id" should become href="#slide-id"
# RevealJS uses #/id format for navigation, but the actual HTML id is just "id"
REVEALJS_HASH_LINK_RE = re.compile(r'href="#/([^"]+)"', re.IGNORECASE)


def _inject_src_from_data_src(img_tag: str) -> str:
    if SRC_ATTR_RE.search(img_tag):
        return img_tag
    match = DATA_SRC_ATTR_RE.search(img_tag)
    if not match:
        return img_tag

    data_src_value = match.group(1)  # includes quotes
    # Insert immediately after the "<img" token so we don't have to reason about ordering.
    return img_tag.replace("<img", f"<img src={data_src_value}", 1)


def normalize_html(contents: str) -> tuple[str, int, int]:
    """
    Normalize HTML for HTML-Proofer validation.

    Returns: (updated_contents, img_replacements, link_replacements)
    """
    img_replacements = 0
    link_replacements = 0

    def repl_img(match: re.Match[str]) -> str:
        nonlocal img_replacements
        original = match.group(0)
        updated = _inject_src_from_data_src(original)
        if updated != original:
            img_replacements += 1
        return updated

    def repl_link(match: re.Match[str]) -> str:
        nonlocal link_replacements
        # Convert href="#/slide-id" to href="#slide-id"
        link_replacements += 1
        return f'href="#{match.group(1)}"'

    updated_contents = IMG_TAG_RE.sub(repl_img, contents)
    updated_contents = REVEALJS_HASH_LINK_RE.sub(repl_link, updated_contents)
    return updated_contents, img_replacements, link_replacements


def iter_html_files(root: Path) -> list[Path]:
    return [p for p in root.rglob("*.html") if p.is_file()]


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Normalize generated HTML so HTML-Proofer can statically validate RevealJS decks.\n\n"
            "Fixes two RevealJS-specific issues:\n"
            "1. Lazy-loaded images: <img data-src=...> (no src) get src injected.\n"
            "2. Internal hash links: href=\"#/slide-id\" becomes href=\"#slide-id\" "
            "(RevealJS uses #/id for navigation but HTML id attrs don't have the slash)."
        )
    )
    parser.add_argument("site_dir", help="Rendered site directory (e.g. _site)")
    args = parser.parse_args()

    site_dir = Path(args.site_dir)
    if not site_dir.exists() or not site_dir.is_dir():
        raise SystemExit(f"Not a directory: {site_dir}")

    total_files = 0
    total_img_fixes = 0
    total_link_fixes = 0

    for path in iter_html_files(site_dir):
        total_files += 1
        original = path.read_text(encoding="utf-8", errors="replace")
        updated, img_fixes, link_fixes = normalize_html(original)
        if img_fixes or link_fixes:
            path.write_text(updated, encoding="utf-8")
            total_img_fixes += img_fixes
            total_link_fixes += link_fixes

    print(
        f"normalize_html_for_proofer: scanned {total_files} HTML files; "
        f"injected src= into {total_img_fixes} <img> tags; "
        f"normalized {total_link_fixes} RevealJS internal links."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
