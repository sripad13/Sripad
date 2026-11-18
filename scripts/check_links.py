#!/usr/bin/env python3
"""Check the static site for broken local links, images and in-page anchors.

Run from the repo root:  python3 scripts/check_links.py
Exits with 1 if anything is broken or a page is missing the GA4 tag.
Standard library only.
"""
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://work.falsewinger.com"
GA_ID = "G-KQTR53TG03"
SKIP_SCHEMES = ("http:", "https:", "mailto:", "tel:", "sms:", "data:", "javascript:")


class Collector(HTMLParser):
    def __init__(self):
        super().__init__()
        self.refs = []  # (value, is_meta)
        self.ids = set()

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if a.get("id"):
            self.ids.add(a["id"])
        if a.get("name") and tag == "a":
            self.ids.add(a["name"])
        if tag in ("a", "link", "area") and a.get("href"):
            self.refs.append(a["href"])
        if tag in ("img", "script", "source", "iframe", "video", "audio") and a.get("src"):
            self.refs.append(a["src"])
        if tag == "meta" and a.get("property") in ("og:image", "og:url") or (
            tag == "meta" and a.get("name") == "twitter:image"
        ):
            if a.get("content"):
                self.refs.append(a["content"])


def html_files():
    skip = {".git", "node_modules"}
    for p in ROOT.rglob("*.html"):
        if not skip.intersection(p.parts):
            yield p


def resolve(page: Path, ref: str):
    """Return the local file a reference points at, or None for external refs."""
    if ref.startswith(SITE):
        ref = ref[len(SITE):] or "/"
    if ref.startswith(SKIP_SCHEMES):
        return None
    path = unquote(urlsplit(ref).path)
    if path == "":
        return page  # same-page anchor
    base = ROOT if path.startswith("/") else page.parent
    target = (base / path.lstrip("/")).resolve()
    if target.is_dir():
        target = target / "index.html"
    elif not target.exists() and target.with_name(target.name + ".html").exists():
        target = target.with_name(target.name + ".html")  # GitHub Pages clean URLs
    return target


def main():
    parsed = {}
    problems = []
    for page in sorted(html_files()):
        text = page.read_text(encoding="utf-8", errors="replace")
        c = Collector()
        c.feed(text)
        parsed[page.resolve()] = c
        if GA_ID not in text:
            problems.append(f"{page.relative_to(ROOT)}: GA4 tag {GA_ID} missing")

    for page, c in parsed.items():
        rel = page.relative_to(ROOT)
        for ref in c.refs:
            target = resolve(page, ref)
            if target is None:
                continue
            fragment = urlsplit(ref).fragment
            if not target.exists():
                problems.append(f"{rel}: '{ref}' points to a missing file")
                continue
            if fragment and target.suffix == ".html":
                tc = parsed.get(target)
                if tc is None:
                    tc = Collector()
                    tc.feed(target.read_text(encoding="utf-8", errors="replace"))
                if fragment not in tc.ids:
                    problems.append(f"{rel}: anchor '#{fragment}' not found in {target.relative_to(ROOT)}")

    for p in problems:
        print(p)
    print(f"Checked {len(parsed)} pages. Problems: {len(problems)}")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
