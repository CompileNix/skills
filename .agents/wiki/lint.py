#!/usr/bin/env python3
"""Lint the goal wikis under .agents/wiki/.

Layout (see the Wiki section of skills/engineering/chief-of-staff/SKILL.md):

  .agents/wiki/index.md                 registry, one line per goal
  .agents/wiki/<YYYY-MM-DD>-<slug>/     one goal wiki
      index.md                          goal statement, ## Status log, pages

Mechanical checks only, the lint half chief-of-staff hands to a script:
  1. every goal folder has a registry line, the registry is sorted by goal id,
     and no stray page sits beside the registry
  2. each registry status matches the last line of its goal's status log
  3. every page of a goal wiki is linked from that goal's index
  4. every relative link resolves to a file in the repo
  5. every page except an index carries a YYYY-MM-DD date
  6. no bare commit hash: cite code as <repo>@<sha> (7 to 64 hex characters)
  7. no em-dash anywhere (this repo's prose rule)

Judgment checks (contradictions, claims a newer source has overtaken) are not
lintable; the coordinator does those by hand.

Usage: python3 .agents/wiki/lint.py   Exits non-zero on any failure.
"""

import re
import sys
from pathlib import Path

GOAL_ID = re.compile(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}-[a-z0-9]+(?:-[a-z0-9]+)*$")
DATE = re.compile(r"\b[0-9]{4}-[0-9]{2}-[0-9]{2}\b")
LINK = re.compile(r"\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
URL = re.compile(r"https?://\S+")
# A hex run of commit-hash length (7 to 64), not already prefixed by
# "<repo>@". It must hold a digit, so hex-only words ("defaced") never match;
# issue ids stay well under 7 digits.
BARE_HASH = re.compile(r"(?<![@\w/.-])(?=[0-9a-f]*[0-9])[0-9a-f]{7,64}(?![\w])")
STATUSES = ("active", "paused", "done", "abandoned")
STATUS_LINE = re.compile(r"^- ([0-9]{4}-[0-9]{2}-[0-9]{2}): (" + "|".join(STATUSES) + r")\b")
REGISTRY_LINE = re.compile(
    r"^- \[([^\]]+)\]\(([^)]+)\): .*Status: (" + "|".join(STATUSES) + r")\.\s*$"
)
EM_DASH = "\u2014"


def link_targets(text: str) -> list[str]:
    return [t.split("#", 1)[0].removeprefix("./") for t in LINK.findall(text)]


def last_status(goal_index: str) -> str | None:
    in_status = False
    status = None
    for line in goal_index.splitlines():
        if line.startswith("## "):
            in_status = line.strip() == "## Status"
            continue
        if in_status:
            match = STATUS_LINE.match(line)
            if match:
                status = match.group(2)
    return status


def main() -> int:
    wiki = Path(__file__).resolve().parent
    root = wiki.parent.parent
    failures: list[str] = []

    def rel(path: Path) -> str:
        return str(path.relative_to(wiki))

    registry = wiki / "index.md"
    if not registry.is_file():
        print(f"FAIL: registry missing: {registry}", file=sys.stderr)
        return 1
    registry_text = registry.read_text(encoding="utf-8")

    for stray in sorted(p for p in wiki.glob("*.md") if p.name != "index.md"):
        failures.append(f"page outside a goal wiki: {rel(stray)}")

    goals = sorted(p for p in wiki.iterdir() if p.is_dir() and not p.name.startswith((".", "_")))

    # 1, 2: registry
    registered: dict[str, str] = {}
    order: list[str] = []
    for line in registry_text.splitlines():
        if not line.startswith("- "):
            continue
        match = REGISTRY_LINE.match(line)
        if not match:
            failures.append(f"index.md: malformed registry line: {line}")
            continue
        goal_id, target, status = match.groups()
        if target.removeprefix("./") != f"{goal_id}/index.md":
            failures.append(f"index.md: {goal_id} links to {target}, not {goal_id}/index.md")
        registered[goal_id] = status
        order.append(goal_id)
    if order != sorted(order):
        failures.append("index.md: registry lines are not sorted by goal id")

    for goal in goals:
        if not GOAL_ID.match(goal.name):
            failures.append(f"goal folder not named <YYYY-MM-DD>-<slug>: {goal.name}")
        goal_index = goal / "index.md"
        if not goal_index.is_file():
            failures.append(f"{goal.name}: no index.md")
            continue
        index_text = goal_index.read_text(encoding="utf-8")
        status = last_status(index_text)
        if status is None:
            failures.append(f"{goal.name}/index.md: no '## Status' log with a dated status line")
        if goal.name not in registered:
            failures.append(f"index.md: no registry line for {goal.name}")
        elif status and registered[goal.name] != status:
            failures.append(
                f"index.md: {goal.name} registered as {registered[goal.name]}, status log says {status}"
            )
        # 3: every page listed in its goal index
        listed = set(link_targets(index_text))
        for page in sorted(goal.rglob("*.md")):
            if page == goal_index:
                continue
            if str(page.relative_to(goal)) not in listed:
                failures.append(f"missing from {goal.name}/index.md: {rel(page)}")
    for goal_id in registered:
        if not (wiki / goal_id).is_dir():
            failures.append(f"index.md: registry line for missing goal folder {goal_id}")

    # 4 to 7: every page
    pages = [registry] + sorted(p for g in goals for p in g.rglob("*.md"))
    for page in pages:
        text = page.read_text(encoding="utf-8")
        for target in LINK.findall(text):
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            path = target.split("#", 1)[0]
            if not path:
                continue
            candidate = (page.parent / path).resolve()
            try:
                candidate.relative_to(root)
            except ValueError:
                failures.append(f"{rel(page)}: link escapes the repo: {target}")
                continue
            if not candidate.exists():
                failures.append(f"{rel(page)}: broken link: {target}")
        if page.name != "index.md" and not DATE.search(text):
            failures.append(f"{rel(page)}: undated page (no YYYY-MM-DD claim)")
        for number, line in enumerate(text.splitlines(), 1):
            for match in BARE_HASH.finditer(URL.sub("", line)):
                failures.append(
                    f"{rel(page)}:{number}: bare commit hash {match.group(0)}, cite as <repo>@<sha>"
                )
        if EM_DASH in text:
            failures.append(f"{rel(page)}: em-dash")

    if failures:
        for failure in failures:
            print(f"FAIL: {failure}", file=sys.stderr)
        print(f"wiki lint: {len(failures)} failure(s)", file=sys.stderr)
        return 1
    print(f"wiki lint: ok ({len(goals)} goal wiki(s), {len(pages)} pages)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
