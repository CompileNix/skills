# research

## What it does

`research` answers a question by reading the sources that own the answer, then leaves a cited Markdown file in the repo. It works only from **[primary sources](../ai-coding-terms.md#primary-source)**: official docs, source code, specs, first-party APIs. It follows every claim back to the source that owns it, so it will not repeat a blog post's account of an API when the API's own docs are reachable.

It does not answer you in the conversation. The output is a file, written where the repo already keeps such notes, with a link on each claim. You get a document you can react to, hand to another agent, or throw away, rather than an answer that is gone when the [session](../ai-coding-terms.md#session) ends.

## When to reach for it

Type `/research`, or the [agent](../ai-coding-terms.md#agent) reaches for it automatically when a task turns into reading legwork.

Reach for it when the next step is *finding something out* from outside the working directory (how a third-party API behaves, what a spec says, whether a version claim holds), and you'd rather not stall your own thread doing the reading. What you need decides which skill:

| What you need | Reach for |
| --- | --- |
| An external fact a decision is waiting on | `research` |
| A decision made *with* you, by interview | [grilling](../productivity/grilling.md) |
| A durable architecture decision, written into `GLOSSARY.md` and ADRs | [grill-with-docs](grill-with-docs.md) |
| To find out whether an approach works in your codebase | [prototype](prototype.md) |
| A plan too big to hold in one session | [wayfinder](wayfinder.md) |

The line between `research` and `grill-with-docs` is the **shelf life of what comes back**. Research produces short-lived facts, such as what this library's auth mechanism does as of this week. An ADR records a decision you keep. If what you are producing is a decision rather than a fact, you are [grilling](../ai-coding-terms.md#grilling), not researching.

## Delegated legwork

The reading runs as a **background agent**. You keep working while it follows each claim to its primary source, writes one Markdown file, and reports back. Research is legwork you delegate, not thinking you outsource. You get a document to grill, plan, or design against, and you still make the decision.

Nothing stops the background agent from spawning another background agent of its own. This is the skill's best-documented problem.

The repo decides where the file goes, not the skill. It follows whatever convention already exists for notes. If there is none, it picks a sensible place and tells you where. It writes one file per run.

## Common questions

**Why not just ask the agent to go read the docs?**

You can, and a two-line prompt saying exactly that was the practice this skill replaced. The skill gives you two things the prompt does not. It runs in the background, so your session's [context](../ai-coding-terms.md#context) stays clean. And the primary-source constraint and the cited-file output are the same every time, rather than depending on how you phrased the prompt. Compared with a [harness](../ai-coding-terms.md#harness)'s own deep-research mode, the difference is the file and the primary-source rule, not the search. If a two-line prompt gets you what you need on a small question, use the two-line prompt.

## It's working if

- Your own session keeps going. If you are sitting watching it read, the delegation didn't happen.
- Exactly one new background task appears. A second one with a near-identical name is the nesting bug.
- One new Markdown file shows up, in the folder the repo already uses for notes, and the agent tells you the path.
- Every claim in it carries a link, and following two at random lands you on an official doc, a spec, or the source file itself, not on someone's write-up of it.
- You can make the decision you were stuck on from the file alone, without going back to the sources yourself.

## Where it fits

`research` is a reach-for-it-anytime standalone. It feeds the thinking skills and is not a step in the build chain. You take its file *into* the flow. [grilling](../productivity/grilling.md) and [grill-with-docs](grill-with-docs.md) ask sharper questions when they already have the facts, and [to-spec](to-spec.md) can synthesise against it. [wayfinder](wayfinder.md) is the one skill that invokes it directly. It resolves each research issue on its map with a `/research` subagent. For the whole map, see [which-skill](which-skill.md).
