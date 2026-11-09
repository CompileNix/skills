# triage

## What it does

`triage` works through the issues on your project's tracker. It moves each one through a small state machine of **triage roles** (a category role and a state role). Each issue ends as an agent-ready brief, a specific question for the reporter, or a closed issue with a recorded reason.

It is only for issues **you didn't create**. That means raw bug reports, incoming feature requests, or an external pull request that arrived unannounced: work that came into the tracker from outside, in whatever shape the reporter left it. [Issues](../ai-coding-terms.md#issue) from [to-issue](to-issue.md) are already agent-ready, so if you run `triage` over them, you waste the work. The rule is simple: `/triage` is only for incoming issues, not for issues you created yourself.

It also differs from labelling by hand because it recommends and then waits. It gives you its category and state call with reasoning, plus what it found in the codebase, and applies nothing until you tell it to.

## When to reach for it

You invoke this by typing `/triage` and then describing what you want in plain language. The [agent](../ai-coding-terms.md#agent) won't reach for it on its own. Examples: "Show me anything that needs my attention", "let's look at #42", "move #42 to ready-for-agent".

| What you have | Where to go |
| --- | --- |
| A tracker full of raw reports from other people | `/triage` |
| A rough idea of your own, nothing written down | [grill-with-docs](grill-with-docs.md) |
| A settled conversation to turn into a [spec](../ai-coding-terms.md#spec) | [to-spec](to-spec.md) |
| A spec to split into agent-ready issues | [to-issue](to-issue.md) |
| A confirmed bug that needs a root cause, not a label | [diagnosing-bugs](diagnosing-bugs.md) |

## Prerequisites

`triage` reads and writes your issue tracker, so [setup-skills](setup-skills.md) must first configure that tracker and its label vocabulary. The role names below are **canonical**. The label strings in your tracker may differ, and setup provides the mapping. If your tracker already uses the canonical names exactly, you have nothing to map and nothing to set up.

The tracker config also decides whether external pull requests count as a request surface, and who counts as external. That flag is off by default, and setup no longer asks about it. To bring PRs into scope, turn it on in `docs/agents/issue-tracker.md`.

## The state machine

Every triaged item ends with exactly one category role and one state role. There are two categories: `bug` (something is broken) and `enhancement` (new feature or improvement). There are five states:

| State | Means |
| --- | --- |
| `needs-triage` | You need to evaluate it. An unlabelled issue normally lands here first. |
| `needs-info` | Waiting on the reporter. Returns to `needs-triage` when they reply. |
| `ready-for-agent` | Fully specified, with an agent brief attached. An [AFK](../ai-coding-terms.md#afk) agent can take it. |
| `ready-for-human` | The same brief, plus why an agent can't do it: judgment, external access, manual testing. |
| `wontfix` | Closed, with the reason recorded. |

That is the whole vocabulary. The rule of exactly one state role per item keeps the queries simple.

`wontfix` has three cases. The difference matters because only one of them writes to the knowledge base:

| Why you're closing it | What happens |
| --- | --- |
| Already implemented | A comment that points to where the feature already lives. Nothing goes into `.out-of-scope/`, because it's a built feature, not a rejected one, and a file there would break the dedup checks. |
| Rejected bug | Polite explanation, then close. |
| Rejected enhancement | A file in `.out-of-scope/`, linked from the closing comment, then close. |

`.out-of-scope/` holds one markdown file per rejected **concept**, not per issue. Each file is a short design document, not a database row. It says what was rejected, why, and lists every issue that asked for it. `triage` reads the whole directory before it evaluates anything. It matches by concept, not keyword, so "night theme" matches `dark-mode.md`. When it finds a match, it shows you the old decision and asks if you still agree with it, instead of arguing the request again from the start.

## Verify before you brief

Before any [grilling](../ai-coding-terms.md#grilling), `triage` checks that the claim holds. For a bug, it reproduces it from the reporter's steps. For a PR, it checks out the branch and runs the relevant tests. Then it reports one of three results:

- Confirmed, with the code path.
- Failed to reproduce.
- Not enough detail to try. This is the strongest `needs-info` signal there is.

In the same pass, it runs two more checks against the codebase. The **redundancy** check asks if the feature is already implemented, and searches by domain concept, not by the reporter's wording. The **prior rejection** check asks if `.out-of-scope/` already says no. Both checks are cheap, and a hit on either produces a `wontfix`.

All of this work makes one artifact good: the **agent brief**. This is the structured comment that `triage` posts when an issue moves to `ready-for-agent`. After `triage` posts it, the brief is the contract and the original report is only context. Briefs are **durable** rather than precise, because an issue can sit in `ready-for-agent` for weeks while the code changes. So a brief names types, signatures and behavioural contracts, and never file paths or line numbers. A confirmed reproduction makes a much stronger brief than a guess.

## A PR is an issue with attached code

If the tracker treats external pull requests as a request surface, they go through the same machine, with the same categories, states and transitions. The states apply to the diff. `ready-for-agent` means a brief is attached and an agent should take the next step on the code. `ready-for-human` means a person can merge it. A brief on a PR describes what is left to do to the existing diff, not how to build the thing from nothing.

Discovery shows only *external* PRs, because a collaborator's in-progress branch is not triage work. That filter applies only to discovery. If you name a PR explicitly, `triage` handles it, whoever wrote it.

## Common questions

**Is `triage` still relevant now that there's a `to-spec` → `to-issue` → `implement` flow?**
Only if you have inbound work. `triage` is older than that flow and does a different job: it handles reports other people filed. If everything in your tracker came from your own planning, you will rarely use it. If you maintain anything public, or your team files bugs to you, it is where that work starts. The main use is open-source repos that take issues from external contributors.

## It's working if

- Every item it touches ends with exactly one category role and one state role, never zero, and never two conflicting states.
- It gives you a recommendation with reasoning and stops. It does not relabel the issue and move on.
- It reproduced the bug, or checked out and ran the PR, before anything reached `ready-for-agent`.
- The briefs it writes name types and behaviours, and contain no file paths and no line numbers.
- When a request you rejected six months ago comes back, it tells you and quotes the old reason instead of triaging it again.
- Every comment it posts starts with `> *This was generated by AI during triage.*`

## Where it fits

`triage` is an **on-ramp**, not a step in the main chain. The main flow starts from an idea you had (grill, spec, issues, implement, review). `triage` is the parallel lane for work that came from someone else. Both lanes end at the same place: an issue labelled `ready-for-agent` with a brief on it. [implement](implement.md) picks that up the same way it picks up an issue from [to-issue](to-issue.md). When a request needs more detail before `triage` can brief it, `triage` runs [grilling](../productivity/grilling.md) and [domain-modeling](domain-modeling.md) together, one round of questions at a time, so it records decisions in `GLOSSARY.md` and the ADRs as you make them. When you're not sure which lane you are in, [which-skill](which-skill.md) routes you.
