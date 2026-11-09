## What it does

`implement-spec` takes a [spec](https://www.aihero.dev/ai-coding-dictionary/spec) and its [issues](https://www.aihero.dev/ai-coding-dictionary/issue) and lands the whole thing in one run. The orchestrating [agent](https://www.aihero.dev/ai-coding-dictionary/agent) hands each issue to an implementer [subagent](https://www.aihero.dev/ai-coding-dictionary/subagent) working in its own git worktree, merges each finished branch into a single **integration branch**, runs [code-review](https://aihero.dev/skills-code-review) over the result, and resolves the issues.

It reads the issues as a **task graph**, not a list. Blocking edges decide what can start, so at any moment there is a **frontier** of issues whose blockers have all landed, and every issue on the frontier runs at once. That is the difference from working the issues one by one. The graph's shape sets the pace, not the issues' order on the tracker.

## When to reach for it

You invoke this by typing `/implement-spec`, and the agent won't reach for it on its own.

| Your situation | Reach for |
| --- | --- |
| A spec, split into issues with blocking edges, that you want landed in one run | `/implement-spec` |
| One issue at a time, in your own [context window](https://www.aihero.dev/ai-coding-dictionary/context-window), [clearing](https://www.aihero.dev/ai-coding-dictionary/clearing) between issues | [implement](https://aihero.dev/skills-implement) |
| A spec that isn't split into issues yet | [to-issue](https://aihero.dev/skills-to-issue) first |
| A small piece of work with no real graph to it | [implement](https://aihero.dev/skills-implement) directly |

## Prerequisites

- **An issue tracker.** The skill reads the issues from, and resolves them on, the tracker [setup-skills](https://aihero.dev/skills-setup-skills) configured. If none has been configured, it stops and tells you to run that first rather than guessing.
- **Issues with blocking edges**, as [to-issue](https://aihero.dev/skills-to-issue) writes them. Without edges the graph is flat and every issue starts at once.
- **A [harness](https://www.aihero.dev/ai-coding-dictionary/harness) that runs subagents in the background and gives each one a git worktree.** The skill exists to run issues at the same time, so on a harness that runs subagents one at a time, it is only a slower `implement`.

## The integration branch

Everything lands on one branch. Each implementer:

1. confirms its worktree is based on the integration branch before it starts,
2. builds its issue with [tdd](https://aihero.dev/skills-tdd), red-green one slice at a time,
3. merges the integration branch tip into its own branch before reporting done, so landing it is a fast-forward.

The tracker decides whether a pull request exists at all. If your tracker closes work through PRs, or you ask for one, the skill opens a draft PR after the first merge and marks it ready at the end. Otherwise the run stops on the integration branch with every issue resolved the way your tracker closes work, which works fully offline against a local markdown tracker.

Implementers talk to the orchestrator through [context pointers](https://www.aihero.dev/ai-coding-dictionary/context-pointer) (the spec, the issue, shared exploration notes, earlier commits) rather than pasted summaries. This keeps each subagent's prompt small and leaves room in the orchestrator's window for the graph.

## Common questions

**How is this different from running `/implement` on each issue myself?**

This is the question the skill exists to answer. Before it shipped, people kept building their own versions, and one user described the need: they wanted "subagents implement the issues" instead of having "to individually create new session and tell them to implement an issue one by one, when a spec may contain over 5 issues." With `implement` you are the dispatcher: one [session](https://www.aihero.dev/ai-coding-dictionary/session) per issue, clearing in between, and keeping track yourself of which issues are unblocked. `implement-spec` hands that job to one orchestrating session. The price is that you no longer read each issue's work as it lands; you review the integration branch at the end. To start a run, clear the context and type `/implement-spec` with a pointer to the spec (an issue number or a file path). For a small change with no real graph, skip it and use `implement` directly.

**Does it need GitHub? I want it to stop at the branch.**

No, not any more. One user who liked the in-progress version had exactly this complaint: "it creates a PR at the end, which requires an online repository like GitHub. I wish it could do the same work offline and stop at the branch where all the work is merged." The run now ends on the integration branch. A PR opens only when the configured tracker closes work through PRs or you ask for one, so on a local markdown tracker the run ends with every issue resolved and the work merged on the branch.

**Its review and fix loop ran for hours, or kept "fixing" issues that hadn't been built yet.**

Both happen when `code-review` runs anywhere other than the one point the skill gives it. It compares the code against the whole spec, so it only makes sense once every issue has landed. If it runs mid-run, every unbuilt issue reads as a failure. The agent then builds that issue, and that triggers another review. At the end, the skill runs `code-review` once and sends every finding to one fix subagent. That pass includes any Visual findings. They are advisory in `code-review`, meaning they never block the build, but the fix pass still addresses them. The skill doesn't yet say when to stop after that fix. One user reported a five-issue feature where "the review and fix loop took roughly four hours". If you see a second broad review start, tell it to run focused checks for the fixed findings and stop. Expect that first review to find real problems. The run's output is a draft that the review completes, not something to ship on its own.

**Does it drive tdd like implement does?**

It does now, though it didn't at first. Users running the in-progress version noticed that "the implementer subagents don't inherit the /tdd directive", so red-green stopped as soon as they scaled up from one issue to a whole spec. Each implementer now builds its issue with `tdd`. There is still no step where you agree seams interactively, as there is in an `implement` session, so name the seams in the spec or the issues if you want them pinned.

**Two implementers running in parallel collided on the same file, or picked different names for the same thing.**

Worktrees don't remove collisions; they postpone them to merge time. A blocking edge written from issue text is a guess about which files each issue will touch, and two issues on "different parts of the codebase" still share a message catalogue, a config registry, or a type. Each implementer sees only its own issue and the shared notes, never the other's work in progress, so one user's web and mobile issues added the same string as `blockedSince` and `blockedOn`. When two frontier issues touch one shared file, either add a blocking edge between them so they run one after the other, or have the exploration notes fix the exact names each issue adds.

**Blocked issues never start, even after their blocker has merged.**

This is a known problem on GitHub. The tracker's blocked-by count only drops when a blocker *closes*, and issues typically close when the PR merges, which is the end of the run. The tracker is the right source for the starting graph but a stale one mid-run. Tell the orchestrator to track which issues have merged into the integration branch itself and compute the frontier from that.

**Does this replace Sandcastle or an AFK script?**

No. People ask because the skills now reach into implementation: "is Sandcastle still relevant? Your skills now seem to be able to handle implementation as well." `implement-spec` puts an agent in charge of orchestration inside one harness session, which needs no infrastructure and lets you watch and steer. For work that is truly [AFK](https://www.aihero.dev/ai-coding-dictionary/afk), a deterministic loop ([Sandcastle](https://github.com/mattpocock/sandcastle), a shell script, a CI job) is faster, cheaper, and more reliable, because no agent makes the orchestration decisions.

**An issue's key test was skipped inside its worktree, and it reported green.**

A worktree holds only what git tracks. Tests that read gitignored fixtures, local databases, or credentials can silently skip there. For an issue whose verification depends on untracked material, tell the orchestrator to run it in the main checkout instead.

## It's working if

- Several implementers are running at once whenever the graph allows, not one after another.
- An issue starts as soon as its last blocker lands on the integration branch, not when the whole run ends.
- Every issue's trace shows `tdd` running, with a failing test before the code.
- Merges into the integration branch are fast-forwards, not conflict resolutions.
- The run ends on one branch with every issue resolved, and a PR only if your tracker wanted one.

## Where it fits

`implement-spec` is the build step of the main chain, as the parallel alternative to running [implement](https://aihero.dev/skills-implement) once per issue:

```txt
grill-with-docs → to-spec → to-issue → implement-spec → retro
```

Its neighbours are [to-issue](https://aihero.dev/skills-to-issue), which declares the blocking edges it reads as a task graph, and [code-review](https://aihero.dev/skills-code-review), which it runs over the integration branch before closing out. [which-skill](https://aihero.dev/skills-which-skill) is the router over the whole set when you are not sure which flow you are in.
