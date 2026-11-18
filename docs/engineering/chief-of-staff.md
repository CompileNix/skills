# chief-of-staff

## What it does

`chief-of-staff` turns one long [session](../ai-coding-terms.md#session) into a coordinator for a long-running goal. The [agent](../ai-coding-terms.md#agent) becomes the goal's Directly Responsible Individual: it hands every piece of work to a [subagent](../ai-coding-terms.md#subagent), keeps what it learns in a dated, commit-cited wiki of its own for the goal, and runs the main flow's skills (spec, issues, build, retro) as procedures without you typing each one.

The coordinator does no work itself. Everything goes to subagents, and its memory lives in the wiki rather than in its [context window](../ai-coding-terms.md#context-window), so the session can run for hours and survive [compaction](../ai-coding-terms.md#compaction) with its judgement intact.

## When to reach for it

You invoke this by typing `/chief-of-staff`, and the agent won't reach for it on its own.

| Your situation | Reach for |
| --- | --- |
| A goal that spans many tasks and hours, where you want one session steering and improving the [environment](../ai-coding-terms.md#environment) as it goes | `/chief-of-staff` |
| One spec, already split into issues, to land in one run | [implement-spec](implement-spec.md) |
| An effort so foggy you can't yet name the tasks | [wayfinder](wayfinder.md) |
| A single feature you can hold in one session | the main flow, from [grill-with-docs](grill-with-docs.md) |

## Prerequisites

- **A wiki parent to write into.** It looks for an existing one first and follows its conventions; this repo keeps one at `.agents/wiki/`. With none, it agrees a location with you before the first write.
- **A [harness](../ai-coding-terms.md#harness) that runs subagents in the background.** Without them the coordinator blocks on every task and the session stops being a dialogue.
- **The procedures it follows.** It reads `retro`, `to-spec`, `to-issue` and `implement-spec` from beside its own folder, so install them alongside it. The [orchestrator rule](../../.agents/invocation.md#orchestrators) explains why a user-invoked skill may follow them.

## Two tracks

The leading idea is **two tracks**, held at once on every task:

- **Tactical**: finish the task in front of you.
- **Strategic**: change the environment so the *next* task goes better. That means constrained APIs, lint rules that force correctness, coding standards a reviewer can enforce, logs and test data the agents can reach, and a "no workarounds" rule.

The strategic track is what separates it from [implement-spec](implement-spec.md): every user message is a prompt to look for an environment fix, and retros on about one in five subagent sessions feed the hunt.

## The wiki

The wiki is the coordinator's long-term memory, and each goal gets **its own wiki**: a folder named by its start date, `<YYYY-MM-DD>-<goal-slug>/`, under one wiki parent whose `index.md` is a registry with one line per goal. A goal's own `index.md` opens with the goal and a dated status log (`active`, `paused`, `done`, `abandoned`), so a session months later sees at a glance which goals are live and asks you which to resume.

| Situation | What happens |
| --- | --- |
| Two goals at once | Two coordinators, two goal wikis; each writes only its own folder and its own registry line |
| The same goal from two sessions | One coordinator per goal; the second effort becomes a goal of its own that reads the first |
| A later goal needs an earlier one's lessons | It reads and cites the earlier goal wiki; it never writes there |
| A fact every goal needs | It is promoted out of the wiki into the environment (`AGENTS.md`, docs, a script) |

It is a **historical record**: every claim is dated, every claim about code cites `<repo>@<sha>`, and a changed fact gets a new dated claim beside the superseded one. A lint script at the wiki parent checks the mechanical part (orphans, broken links, undated pages, bare commit hashes, a registry status out of step with its goal) before every wiki commit. Subagents talk to the coordinator through [context pointers](../ai-coding-terms.md#context-pointer) (wiki pages, commits, research notes) instead of pasted summaries, so both sides keep their windows small.

## Common questions

**A subagent that dispatched its own children sits idle forever.**

The children's completion reports land in the coordinator's session, not in the subagent that spawned them. The skill tells the coordinator to forward each one to its parent subagent at once. If an orchestrator subagent is "waiting on its implementer" long after the implementer finished, that relay was missed.

**It keeps stopping to ask me whether to proceed.**

A blocking question with nothing to decide parks the whole session on you. The skill reserves questions for real forks and reports status as plain text. A checkpoint question that offers "proceed as written" first is the failure.

**Can I run two chief-of-staff sessions at once?**

Yes, on different goals: each gets its own goal wiki, and the only file they share is the registry, where each edits only its own line. Two sessions on the same goal is the case to avoid; split the second one into a goal of its own, which can read the first.

**Why does it write a lint script for the wiki?**

Orphan pages, broken links, pages missing from the index and undated claims are mechanical, so a script checks them and fails before a bad wiki commit. The coordinator keeps only the judgement checks: contradictions between pages, and claims a newer source has overtaken.

**My implementer subagents can't see the local issue tracker.**

A local tracker under `.scratch/` is untracked, so it stays in the coordinator's checkout and never reaches a subagent's worktree. Hand subagents absolute paths to the spec and issues. More generally, when a dispatch leans on shared state (branches across checkouts, hooks, paths outside the repo), the skill sends one cheap probe subagent to check the environment before the whole wave goes out.

**A later subagent fails to check out a branch: "already used by worktree".**

A finished subagent's worktree outlives it and still holds the branch it had checked out, so the next subagent that needs that branch, typically the next merger on the integration branch, can't check it out. The skill has the coordinator remove the finished worktree before that dispatch. For the same reason, anything a probe found about state that can move (which branch is checked out where, what a tip was) goes into each task as a check the subagent runs first, stopping to report if it differs, not as a fact.

## It's working if

- The coordinator's own trace is mostly dispatches and short reports, with little file reading or editing of its own.
- Each goal wiki grows with dated pages and commit-cited claims, its `index.md` lists every one, and the registry shows each goal's status.
- Changes to the environment (a lint rule, a hook, a coding standard) land alongside the feature work, not as a someday list.
- You get status as plain text and questions only when there is a real choice to make.

## Where it fits

`chief-of-staff` sits **above the main flow** and runs it for you across many tasks: `to-spec → to-issue → implement-spec → retro`, over and over, toward one goal. Its neighbours are [implement-spec](implement-spec.md), the single-spec build it dispatches, and [retro](retro.md), which feeds its strategic track. [which-skill](which-skill.md) is the router over the whole set.
