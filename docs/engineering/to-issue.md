# to-issue

## What it does

`to-issue` takes a plan, a [spec](../ai-coding-terms.md#spec), or the conversation you are in, and breaks it into a set of **[issues](../ai-coding-terms.md#issue)** on your issue tracker. Each issue declares its **blocking edges**: the other issues that have to finish before it can start.

Every issue is a **tracer bullet**: a narrow but complete path through every layer of the change (schema, API, UI, tests) that you can demo on its own as soon as it lands. This is what makes the skill different from the obvious way to split work, which is to cut one layer at a time and integrate at the end. It also sizes each issue to fit in a single fresh [context window](../ai-coding-terms.md#context-window), because a [session](../ai-coding-terms.md#session) that has never seen your spec will pick the issue up.

## When to reach for it

You invoke this by typing `/to-issue`. The [agent](../ai-coding-terms.md#agent) won't reach for it on its own.

| Where you are | What to run |
| --- | --- |
| You have a spec issue and the build spans several sessions | `/to-issue`, or `/to-issue #<spec_issue>` |
| The plan is only in the conversation, never written up | `/to-issue` reads the thread directly, no spec needed |
| The whole change fits in one context window | [implement](implement.md), skip the issues |
| Nothing is decided yet | [grill-with-docs](grill-with-docs.md), then [to-spec](to-spec.md) |
| A [wayfinder](wayfinder.md) map has cleared | [to-spec](to-spec.md) first, to collapse the map, then `/to-issue` |

Issues that `to-issue` produced are agent-ready by construction. Don't run [triage](triage.md) over them. Triage is for work that arrived from someone else.

## Prerequisites

`to-issue` publishes into a tracker, so [setup-skills](setup-skills.md) must have configured one for this repo, along with the triage-label vocabulary. Either kind works: a real tracker like GitHub or Linear, or local markdown files under `.scratch/`, which work with no extra setup.

## Tracer bullets, not layers

A **horizontal** slice ships one layer of the change. Nothing works until every layer has landed, and each issue's acceptance criteria have to reach into work that another issue owns. A **vertical** slice (the tracer bullet) ships one thin path through all the layers at once, so it is verifiable alone and owns everything it grades.

This is the rule people break most often. One team ran a 26-issue stack sliced by layer (corpus, producer, aggregator, selector) and got roughly twenty agent runs per closed issue, about three quarters of them rework. Their own post-mortem traced every failure class back to the horizontal slicing rather than to the implementations.

Two things happen before anything is published. `to-issue` looks for prefactoring (the principle "make the change easy, then make the easy change") and orders that work first. Then it presents the breakdown as a numbered list and quizzes you on it: is the granularity right, are the blocking edges real, should anything merge or split. Nothing reaches the tracker until you approve, and that quiz is the place to push back.

## Blocking edges

The edges are the point of the artifact. They work in two ways, depending on the tracker:

| Tracker | Where the edges live | How you work them |
| --- | --- | --- |
| Local markdown | Text in one file per issue under `.scratch/<feature>/issues/<NN>-<slug>.md`, numbered blockers-first | Top to bottom, by hand |
| A real tracker (GitHub, Linear) | Native blocking links, or sub-issues where the tracker has them | Any issue whose blockers are done is on the **frontier** and can be grabbed |

The edges live in the issue either way. The tracker only decides whether anything can act on them in parallel. `to-issue` produces the artifact; running it (one session at a time, or a fleet) is your job, not the skill's.

## The wide-refactor exception

One shape breaks the tracer-bullet rule. A **wide refactor** is a single mechanical change (rename a column, retype a shared symbol) whose **blast radius** covers the whole codebase. One edit breaks thousands of call sites, so no vertical slice can land green.

`to-issue` sequences that as **expand–contract** instead:

- **Expand**: add the new form beside the old, so nothing breaks.
- **Migrate**: move call sites over in batches sized by blast radius (per package, per directory), one issue per batch, each blocked by the expand. CI stays green because the old form still exists.
- **Contract**: delete the old form once no caller remains, in an issue blocked by every migrate batch.

Where even the batches can't stay green alone, they share an integration branch and all block a final integrate-and-verify issue. CI only has to be green at that issue.

## Common questions

**It kept truncating when it tried to read my spec.**
A very large spec can outgrow what a tracker issue serves back cleanly. There is no local copy to fall back on, so the agent spends [tool calls](../ai-coding-terms.md#tool-call) fetching chunks again and never reaches the end. Don't [clear](../ai-coding-terms.md#clearing) or [compact](../ai-coding-terms.md#compaction) between `/to-spec` and `/to-issue`. Run them in the same context window and the agent never has to fetch the spec back.

**The acceptance criteria graded nothing: some passed before any work was done.**
The template asks for criteria and says nothing about whether they can fail, so this happens. Three shapes recur: a criterion already true at the base commit, a criterion that only work in another issue can satisfy, and one that restates the request rather than deriving from the artifact. Vertical slicing prevents most of it, because a slice that delivers new behaviour fails at the base commit by construction. The check is still worth doing by hand. For each criterion, name the observation that would show it false, and confirm it fails at the commit the implementer starts from.

**The issues are published. How do I actually run them?**
The skill stops at the artifact, and there is no auto-dispatch mode. Dispatch is manual: look at the board, count the issues with no open blockers, and open that many agent sessions. Give each issue a fresh context, and clear between them. [implement](implement.md) does not reliably close or check off the issue when it finishes, on GitHub or in local markdown, so you update the issue's state yourself.

## It's working if

- Every issue has an answer to "what can I demo when this is done?", and the answer is behaviour, not a layer.
- The list comes back to you numbered, with a "Blocked by" line on each, before anything is published.
- The issue at the top has no blockers and can be started immediately.
- Nothing in an issue body is a file path or a line number, except a snippet a prototype produced.
- Each issue reads like something a fresh session could finish without you in the room.
- Prefactoring, where it found any, is at the front of the order rather than mixed into feature issues.

## Where it fits

`to-issue` is a step in the main build chain:

```txt
grill-with-docs → to-spec → to-issue → implement → code-review → retro
```

Upstream is [to-spec](to-spec.md), which hands it a settled spec to slice against. Keep both in one context window, with no clear between them. Downstream is [implement](implement.md), which builds one issue per fresh session, driving [tdd](tdd.md) for the tests and closing with [code-review](code-review.md). [implement-spec](implement-spec.md) is the other way down. It reads the same blocking edges as a task graph and builds every ready issue in parallel on one integration branch. When you're unsure which skill or flow fits, [which-skill](which-skill.md) routes you.
