# which-skill

## What it does

`which-skill` is the router over the skills in this repo. You describe the situation you are in (an idea you cannot start, a pile of incoming bug reports, a [session](../ai-coding-terms.md#session) that has run long), and it names the skill or the sequence of skills that fits, plus where the human decisions in that sequence sit.

It recommends and stops. It does not grill, write a [spec](../ai-coding-terms.md#spec), open a file or fire the skill it just named; what you get back is the next thing to type, and you type it. It is also a hand-written map of the skills in this repo rather than a scan of what you have installed, so it will not route you over your own skills or another author's.

## When to reach for it

You invoke this by typing `/which-skill`; the agent won't reach for it on its own.

| Your situation | What the router gives back |
| --- | --- |
| An idea, and no idea where to start | The head of the main flow, and whether the build is small enough to skip the spec |
| Bugs and requests arriving from other people | The [triage](triage.md) on-ramp, and why [issues](../ai-coding-terms.md#issue) you generated yourself don't belong on it |
| Two skills that look interchangeable | The line between them, and it is usually one concrete test rather than a matter of taste. [grill-me](../productivity/grill-me.md) or [grill-with-docs](grill-with-docs.md) turns on whether you are in a working directory; [grill-with-docs](grill-with-docs.md) or [wayfinder](wayfinder.md) turns on whether the effort fits one session |
| A long session and a decision about the [context](../ai-coding-terms.md#context) | The ordered tree over the five options at a phase boundary |
| A skill you have already picked | Nothing useful. Invoke that skill directly. |

## Prerequisites

The router names skills; it does not install them. Everything it points at has to be installed for the recommendation to be actionable, and it only knows the promoted skills in this repo.

The tracker-dependent routes (triage, `to-spec`, `to-issue`, `implement`) assume [setup-skills](setup-skills.md) has already configured an issue tracker in the repo. The router recommends them even before that has happened.

## Flows, not skills

The skill's leading word is **flow**, a path *through* the skills rather than a single skill. When you name your situation, the router places you at a step on a flow. That is a different answer from "here is the skill that matches your keywords". There are five kinds of route, and the skill itself describes them in full:

- **The main flow**, idea to ship. Grill, spec, issues, implement (one issue at a time, or the whole task graph in parallel with [implement-spec](implement-spec.md)), review, then [retro](retro.md), which feeds what the build taught back into the agent's environment. It has two branches. One is a prototype detour, for when a question needs runnable code to settle it. The other is the spec-and-issues split, which is only worth its cost when the build spans more than one session.
- **On-ramps**, for a situation that generates work and then merges onto the main flow: incoming bug reports, something broken, or an effort too foggy and too large to hold in one session.
- **Codebase health**, upkeep rather than feature work. [improve-codebase-architecture](improve-codebase-architecture.md) surveys the code for deepening opportunities, and each one it finds re-enters the main flow as an idea.
- **Standalones**, which sit off every flow and which you use on their own: the prototype, the questionnaire, the research run.
- **A vocabulary layer underneath**, the two references the other skills pull in when the words rather than the process are the problem.

## The phase boundary

The skill's other key idea is the **phase boundary**. A phase is a chunk of work inside a session (the [grilling](../ai-coding-terms.md#grilling), the implementation, the QA), and the boundary between two of them is the only place the question "what do I do with this context?" belongs. Mid-phase there is nothing to decide: continue, or split what is left into [subagents](../ai-coding-terms.md#subagent).

| Option | Take it when |
| --- | --- |
| **Continue** | The next phase wants this one verbatim, or you have [smart zone](../ai-coding-terms.md#smart-zone) left. It is the only move that keeps the session as a [primary source](../ai-coding-terms.md#primary-source), so rule it out first |
| **`/clear`** | Everything behind you is disposable. The cheapest option, and you cannot undo it if you were wrong |
| **[handoff](../productivity/handoff.md)** | Something has to travel: a new [harness](../ai-coding-terms.md#harness), a new directory, a colleague, a side task forked mid-phase |
| **Subagent** | The task is scoped tightly enough to run with you [away from the keyboard](../ai-coding-terms.md#afk) |
| **`/compact`** | None of the above. It is the default, and the tree often ends here |

People often get two of these wrong, which is why the router gives the order and not only the list. `/handoff` looks like the general way to move between context windows, but it is not. All it gives you is portability. `/compact` is the last option in the tree, not the first, because each of the four options above it is cheaper or more precise.

## It's working if

- It ends by naming what to type and stops there, instead of starting the work itself.
- The route it gives back mentions where to clear or compact context and where you are expected to review, not just a list of skill names.
- Where two skills are close, it says which one and why the other is wrong for you.
- Any claim it makes about another skill's behaviour shows up in the trace as it reading that skill's `SKILL.md`.
- You recognise your own situation in what it hands back, rather than the nearest generic scenario.

## Where it fits

`which-skill` is a **standalone router** that sits over the whole set. It is never a step in a chain. It points into every chain, and the other docs pages link back to it so none of them has to redraw the graph. From here you most often land on [grill-with-docs](grill-with-docs.md), the head of the main flow, or [triage](triage.md), the on-ramp for work that arrived rather than work you started.

It is a [secondary source](../ai-coding-terms.md#secondary-source) over the skills it describes. Where the router and a `SKILL.md` disagree, the `SKILL.md` is right.
