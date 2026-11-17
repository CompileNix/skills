# Grilling upstream cluster

The effort to fix a cluster of six upstream issues in the `grilling` skill of this fork.

## 2026-11-17

A chief-of-staff validation session (working branch `t3/cos-validation`, history base 89fadac) read the six upstream issues on 2026-11-17: mattpocock/skills #1401 (a recommendation built on a pending fact got retracted), #1402 (a confirmation carrying new facts was treated as the end of the session), #1406 (a partly answered round was treated as finished and the unanswered questions came back renumbered), #1411 (multi-question rounds were hard to answer; a blank answer sheet was proposed), #1424 (the yes-wording line steered rounds toward yes-only questions), #1430 (every question carried the same weight, so a high-impact irreversible decision was rubber-stamped next to test-setup details).

The principal's disposition on 2026-11-17 was to fix all six, with no declines. The per-issue reasoning:

- #1401: the skill's pending-facts rule covered questions downstream of a fact, not recommended answers that rested on the fact; extending the definition was the minimal fix and composed with the existing sub-agent dispatch paragraph.
- #1402: the closing rule (do not act until the user confirms) was silent about confirmations that carry new material; one sentence closed the gap.
- #1406: the skill said nothing about partly answered rounds, and the reported renumbering was a repeat failure for the reporter; stable session-wide numbering was the fix.
- #1411: this fork carries a question-tool path that upstream lacks (a deliberate divergence), but the written round still stands alone on harnesses without a question tool, and the answer sheet is cheap and orthogonal to that path.
- #1424: the yes-wording line was the reported failure itself, so it was replaced rather than patched around.
- #1430: compact per-question markers composed with the question-tool path and closed the rubber-stamp risk that #1424 alone did not cover.

The work layout decided on 2026-11-17: a spec and four local issues under `.scratch/grilling-fixes/` (the local file tracker; this repo has no setup-skills configuration), three slices grouped by area (round content, round shape, facts and close) plus a coherence gate blocked by all three, and an integration branch `fix/grilling-upstream-cluster` based on `origin/main` at f4b7d93, not on `t3/cos-validation`, so the grilling fixes do not pick up the in-flight chief-of-staff work.

## 2026-11-17: environment facts found

Two facts about this machine's agent environment, durable for later sessions on this repo:

- The OpenCode harness loads skills from the main checkout (`~/code/git.compilenix.org/CompileNix_skills/skills/{engineering,productivity}` per `~/.config/opencode/opencode.json`) and from `~/.claude/skills`, not from the active worktree. As of 2026-11-17 the `tdd` and `grilling` copies in `~/.claude/skills` were byte-identical to the main checkout's versions. A subagent that must follow a procedure from the repo therefore gets the worktree copy only if the dispatch hands it the path, which is exactly what the orchestrator rules in `.agents/invocation.md` allow.
- Child checkouts prepared by T3 `delegate_task` with worktree isolation are linked git worktrees of the shared repo: local branches made in the orchestrator's worktree are visible in every child worktree, so no fetch or push is needed to share branches. Verified 2026-11-17 by a single research-probe child before the implementation wave was dispatched.

## Status

As of 2026-11-17: slices 01, 02, and 03 dispatched to background implementer subagents; the coherence gate (04) waits on all three merges.
