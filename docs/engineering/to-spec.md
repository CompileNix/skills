# to-spec

## What it does

`to-spec` turns the conversation you have just had into a **[spec](../ai-coding-terms.md#spec)**, and publishes it to your issue tracker as a single issue.

It does not interview you. When you reach for it, the deciding is already done. So it synthesises what is known (from the thread, the codebase, your `GLOSSARY.md` and ADRs) and does not start a new round of questions. The spec records decisions you already made. It is not a place to make new ones.

## When to reach for it

You invoke this by typing `/to-spec`; the [agent](../ai-coding-terms.md#agent) won't reach for it on its own.

Reach for it when the build is too big for one agent [session](../ai-coding-terms.md#session) and must be split across several. That is the whole trigger:

| Where you are | What to run |
| --- | --- |
| You haven't decided anything yet | [grill-with-docs](grill-with-docs.md) first |
| Decided, and the work fits one [context window](../ai-coding-terms.md#context-window) | [implement](implement.md): skip the spec |
| Decided, and the work spans several sessions | `/to-spec`, then [to-issue](to-issue.md) |
| A [wayfinder](wayfinder.md) map has cleared | `/to-spec #<map_issue>` |

## Prerequisites

`to-spec` publishes the spec as an issue, so [setup-skills](setup-skills.md) must first configure a tracker and the triage-label vocabulary for this repo. Either kind of tracker works: a real tracker like GitHub, or local markdown files under `.scratch/`, which work with no extra setup.

## The spec is a decision record

The spec exists because context windows end. You settled many things while [grilling](../ai-coding-terms.md#grilling): the shape of the solution, the choices you argued through, and what you deliberately refused. All of that is in one conversation that you are about to clear. The spec keeps it.

So the spec does not validate or decide anything. It records what you decided, in your project's own vocabulary, so a fresh session can pick up the work without you explaining it again. If the spec states something you never said, that is a defect.

## Seams before prose

Before it writes anything, `to-spec` sketches the **seams** where the feature will be tested, and checks them with you. It prefers existing seams to new ones, and picks the highest seam it can. The ideal number of seams for a change is one.

Other skills use those agreed seams later. [tdd](tdd.md) works only at seams you agreed in advance. [code-review](code-review.md) reviews the diff against the spec, so a seam nobody agreed to shows up as a review finding. Both connections go through this document. That is why you should take the seam conversation seriously here, and not leave it for implementation.

## Common questions

**Why not go straight from grilling to `/to-issue` and skip the spec?**
Often you should. The spec is worth its step only on multi-session work. Its value is that the issues are disposable and the spec is not. Each issue is sized for one fresh context window and then gets deleted or closed, while the spec stays as the one place that records the reasoning behind them. On a single-session change, that gives you nothing, and you pay for an extra synthesis step where the [model](../ai-coding-terms.md#model) can drift. Go from grilling to `/implement`.

**I just finished a wayfinder map. What do I feed it?**
Give it the main map issue, `/to-spec #<map_issue>`, not the individual decision issues. [wayfinder](wayfinder.md) produces decisions spread across a map, not deliverables. `to-spec` collapses them into one document you can build from. If you loop the map straight into `/implement`, you lose that step.

**Do I keep the spec frozen once issues start, or let the agent rewrite it?**
Nothing keeps it in sync. In practice it is a snapshot of what you knew at that moment, and it goes out of date the first time implementation teaches you something. Treat it as disposable after the work ships. Your `GLOSSARY.md` and ADRs are the files meant to last. If you learn something during implementation that should last, put it there, not in an edited spec.

**My work is a refactor or a module boundary, not a feature. Does the template fit?**
Less well, and this is a known limitation. The template relies heavily on user stories, which do not fit architectural work. You end up writing stories nobody asked for around decisions that are really about interfaces and invariants. Use the implementation-decisions and testing-decisions sections instead. Record the lasting architectural decisions as ADRs through [grill-with-docs](grill-with-docs.md), not in the spec.

**Will it check the tracker for related work, or cite the ADRs it's respecting?**
No to both. It reads and follows the ADRs for the area it touches, but it does not link them. It also does not search the tracker for overlapping issues before it writes, so a spec can duplicate work that someone already filed, and nothing warns you. If the area is busy, search the tracker yourself first.

**`/to-issue` couldn't read my spec: it kept truncating.**
A tracker issue may not return a very large spec in full, and there is no local copy to use instead. To fix this, do not [clear](../ai-coding-terms.md#clearing) or [compact](../ai-coding-terms.md#compaction) between `/to-spec` and `/to-issue`. Run them in the same window, and `/to-issue` never has to fetch the spec again.

## It's working if

- It starts writing instead of asking you a new round of questions.
- It shows you the seams before it writes, and proposes as few as it can.
- It uses your project's nouns, not generic product-management boilerplate.
- You remember making every decision in it. It invented nothing to fill a section.
- The out-of-scope section lists real things. The things you refused are usually the most useful lines on the page.

## Where it fits

`to-spec` is a step in the main build chain, but only on the multi-session branch of it:

```txt
grill-with-docs → to-spec → to-issue → implement → code-review → retro
```

Upstream, [grill-with-docs](grill-with-docs.md) makes the decisions that this skill only records, and a finished [wayfinder](wayfinder.md) map joins the chain here. Downstream, [to-issue](to-issue.md) cuts the spec into tracer-bullet issues for [implement](implement.md) to build. When you're unsure which skill or flow fits, [which-skill](which-skill.md) routes you.
