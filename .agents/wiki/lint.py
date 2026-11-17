#!/usr/bin/env python3
"""Lint the shared wiki at .agents/wiki/.

Mechanical checks only, per the chief-of-staff skill's lint half:
  1. every page (except index.md) is linked from index.md
  2. every relative markdown link in every page resolves to a file in the repo
  3. every page (except index.md) carries at least one YYYY-MM-DD date: the
     wiki is a dated historical record, so a page with no dated claim is
     undated and fails
  4. no em-dash anywhere in a wiki page: this repo's prose rule, which the
     wiki pages are bound by

Judgment checks (contradictions between pages, claims a newer source has
overtaken) are not lintable; chief-of-staff does those by hand.

Usage: python3 lint.py   (run from the repo root, or anywhere: it finds the
wiki folder as .agents/wiki relative to the git repo root)
Exits non-zero on any failure.
"""

import re
import sys
from pathlib import Path

DATE_RE = re.compile(r"\b[0-9]{4}-[0-9]{2}-[0-9]{2}\b")
EM_DASH = "\u2014"
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")


def repo_root() -> Path:
    root = Path(__file__).resolve().parent.parent.parent
    return root if (root / "CLAUDE.md").is_file() else Path.cwd()


def index_targets(index_text: str) -> set[str]:
    targets = set()
    for target in LINK_RE.findall(index_text):
        bare = target.split("#", 1)[0]
        if bare.startswith("./"):
            bare = bare[2:]
        targets.add(bare)
    return targets


def main() -> int:
    root = repo_root()
    wiki = root / ".agents" / "wiki"
    if not wiki.is_dir():
        print(f"wiki not found: {wiki}", file=sys.stderr)
        return 1

    failures: list[str] = []
    pages = sorted(p for p in wiki.glob("*.md") if p.name != "index.md")
    index = wiki / "index.md"
    index_text = index.read_text(encoding="utf-8") if index.is_file() else ""

    # 1. every page is linked from the index
    listed = index_targets(index_text)
    for page in pages:
        if page.name not in listed and page.stem not in listed:
            failures.append(f"missing from index.md: {page.name}")

    # 2. every relative link in every page resolves in the repo
    all_pages = [index] + pages
    for page in all_pages:
        text = page.read_text(encoding="utf-8")
        for target in LINK_RE.findall(text):
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            target_path = target.split("#", 1)[0]
            if not target_path:
                continue
            candidate = (page.parent / target_path).resolve()
            try:
                candidate.relative_to(root)
            except ValueError:
                failures.append(f"{page.name}: link escapes the repo: {target}")
                continue
            if not candidate.is_file():
                failures.append(f"{page.name}: broken link: {target}")

    # 3. every page carries a date
    for page in pages:
        text = page.read_text(encoding="utf-8")
        if not DATE_RE.search(text):
            failures.append(f"undated page (no YYYY-MM-DD claim): {page.name}")

    # 4. no em-dash
    for page in all_pages:
        text = page.read_text(encoding="utf-8")
        if EM_DASH in text:
            failures.append(f"em-dash in {page.name}")

    if failures:
        for failure in failures:
            print(f"FAIL: {failure}", file=sys.stderr)
        print(f"wiki lint: {len(failures)} failure(s) in {len(all_pages)} pages", file=sys.stderr)
        return 1

    print(f"wiki lint: ok ({len(all_pages)} pages)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
