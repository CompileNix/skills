# implement-spec

## What it does

`implement-spec` takes a [spec](../ai-coding-terms.md#spec) and its [issues](../ai-coding-terms.md#issue) and lands the whole thing in one run. The orchestrating [agent](../ai-coding-terms.md#agent) hands each issue to an implementer [subagent](../ai-coding-terms.md#subagent) working in its own git worktree, merges each finished branch into a single **integration branch**, runs [code-review](code-review.md) over the result, and resolves the issues.

It reads the issues as a **task graph**, not a list. Blocking edges decide what can start, so at any moment there is a **frontier** of issues whose blockers have all landed, and every issue on the frontier runs at once. That is the difference from working the issues one by one. The graph's shape sets the pace, not the issues' order on the tracker.

## When to reach for it

You invoke this by typing `/implement-spec`, and the agent won't reach for it on its own.

| Your situation | Reach for |
| --- | --- |
| A spec, split into issues with blocking edges, that you want landed in one run | `/implement-spec` |
| One issue at a time, in your own [context window](../ai-coding-terms.md#context-window), [clearing](../ai-coding-terms.md#clearing) between issues | [implement](implement.md) |
| A spec that isn't split into issues yet | [to-issue](to-issue.md) first |
| A small piece of work with no real graph to it | [implement](implement.md) directly |

## Prerequisites

- **An issue tracker.** The skill reads the issues from, and resolves them on, the tracker [setup-skills](setup-skills.md) configured. If none has been configured, it stops and tells you to run that first rather than guessing.
- **Issues with blocking edges**, as [to-issue](to-issue.md) writes them. Without edges the graph is flat and every issue starts at once.
- **A [harness](../ai-coding-terms.md#harness) that runs subagents in the background and gives each one a git worktree.** The skill exists to run issues at the same time, so on a harness that runs subagents one at a time, it is only a slower `implement`.

## The integration branch

Everything lands on one branch. Each implementer:

1. confirms its worktree is based on the integration branch before it starts,
2. builds its issue with [tdd](tdd.md), red-green one slice at a time,
3. merges the integration branch tip into its own branch before reporting done, so landing it is a fast-forward.

The tracker decides whether a pull request exists at all. If your tracker closes work through PRs, or you ask for one, the skill opens a draft PR after the first merge and marks it ready at the end. Otherwise the run stops on the integration branch with every issue resolved the way your tracker closes work, which works fully offline against a local markdown tracker.

Implementers talk to the orchestrator through [context pointers](../ai-coding-terms.md#context-pointer) (the spec, the issue, shared exploration notes, earlier commits) rather than pasted summaries. This keeps each subagent's prompt small and leaves room in the orchestrator's window for the graph.

## Common questions

**Blocked issues never start, even after their blocker has merged.**

This is a known problem on GitHub. The tracker's blocked-by count only drops when a blocker *closes*, and issues typically close when the PR merges, which is the end of the run. The tracker is the right source for the starting graph but a stale one mid-run. Tell the orchestrator to track which issues have merged into the integration branch itself and compute the frontier from that.

**An issue's key test was skipped inside its worktree, and it reported green.**

A worktree holds only what git tracks. Tests that read gitignored fixtures, local databases, or credentials can silently skip there. For an issue whose verification depends on untracked material, tell the orchestrator to run it in the main checkout instead.

## It's working if

- Several implementers are running at once whenever the graph allows, not one after another.
- An issue starts as soon as its last blocker lands on the integration branch, not when the whole run ends.
- Every issue's trace shows `tdd` running, with a failing test before the code.
- Merges into the integration branch are fast-forwards, not conflict resolutions.
- The run ends on one branch with every issue resolved, and a PR only if your tracker wanted one.

## Where it fits

`implement-spec` is the build step of the main chain, as the parallel alternative to running [implement](implement.md) once per issue:

```txt
grill-with-docs → to-spec → to-issue → implement-spec → retro
```

Its neighbours are [to-issue](to-issue.md), which declares the blocking edges it reads as a task graph, and [code-review](code-review.md), which it runs over the integration branch before closing out. [which-skill](which-skill.md) is the router over the whole set when you are not sure which flow you are in.
