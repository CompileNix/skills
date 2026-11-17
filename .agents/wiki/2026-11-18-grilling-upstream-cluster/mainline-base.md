# The integration branch bases on main

- 2026-11-18: At session start, the fork mainline `main` at `CompileNix/skills@5266a96` (merged 2026-11-18 00:10 +0100) already carries `t3/grilling-divergent-options`: the lettered diverging options format in `skills/productivity/grilling/SKILL.md` and its re-synced docs page. This worktree's branch `t3/cos-validation-2` diverged from main at `CompileNix/skills@89fadac` and does not carry that work.
- 2026-11-18: The integration branch for this run therefore bases on `main`, not on this worktree's branch, so the fixes compose on the current fork format. The verdicts in [upstream-issues.md](upstream-issues.md) follow from that state, in particular the no-change verdict for mattpocock/skills#1424.
- 2026-11-18: The earlier run's branches `fix/grilling-upstream-cluster-run1` and `t3/cos-validation-run1` hold an earlier attempt's output. Per the principal, this run leaves them untouched and starts fresh.
