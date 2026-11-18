# Fix the upstream grilling issue cluster

## Goal

Resolve, in this fork, the cluster of upstream issues about the `grilling` skill, mattpocock/skills #1430, #1424, #1411, #1406, #1402, #1401: decide per issue whether it is worth fixing here, then run one full cycle, spec to issues to implement-spec, with a retro on at least one subagent session. This run also validates the `chief-of-staff` skill itself, so failures of that skill are recorded as pages of their own.

## Status

- 2026-11-18: active
- 2026-11-18: done

## Pages

### Triage

- [upstream-issues.md](upstream-issues.md): Per-issue verdicts, one dated claim per upstream issue.
- [decline-1430.md](decline-1430.md): The dated decline note for the impact, scope, and confidence markers.

### Run

- [mainline-base.md](mainline-base.md): The fork mainline already carries the diverging options format, so the integration branch bases on `main`.
- [run-log.md](run-log.md): The spec, the issues, the branches, and the commits as they land.

### Chief-of-staff failures

- [cos-failure-worktree-lifecycle.md](cos-failure-worktree-lifecycle.md): A child's worktree outlives the child and keeps holding its branch checkout; fixed in the skill.

### Retro

- [retro-merger-04.md](retro-merger-04.md): Candidates and decisions from the one session that failed; one pursued.
