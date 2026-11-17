# Probe the child environment before the wave

A chief-of-staff gap found during the 2026-11-17 validation run, and the fix that closed it.

## 2026-11-17

Before dispatching three worktree-isolated implementer subagents, the orchestrator needed to know one fact that the dispatch depended on: are the children's prepared checkouts linked git worktrees of the shared repo (so a local integration branch made in the orchestrator's worktree is visible to every child) or independent clones (so the same branch would need a fetch, or the dispatch would silently fail)? Neither the chief-of-staff skill nor implement-spec said anything about verifying child environment assumptions; the skill's Subagents section covers context, reporting, and communication, not the environment the children land in.

A single research-probe child (a T3 delegate task with worktree isolation) answered the question: the child checkout is a linked worktree, `.git` is a file pointing at the shared repo's worktrees directory, and the probe branch made in the orchestrator's worktree resolved by name in the child. The probe cost one child run; the wave was then dispatched with the fact encoded into every task, and no child needed fetch instructions or network access.

The fix, committed to `t3/cos-validation` on 2026-11-17, is one paragraph in the Subagents section of `skills/engineering/chief-of-staff/SKILL.md` (commit 0c19057): when a dispatch leans on shared state the children must see or touch (branches across checkouts, hooks, paths outside the repo), verify the child environment once with a cheap probe child before the wave, and encode what it found into every task.

The probe pattern also surfaced a machine fact used later in the run: child worktrees are prepared from the live tip of the parent thread's branch at dispatch time, so a parent commit made between dispatches moves the preparation base. The reset-onto-the-integration-branch instruction in every implementer task absorbed the drift without friction.
