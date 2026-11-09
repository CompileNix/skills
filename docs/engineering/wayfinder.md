# wayfinder

## What it does

`wayfinder` takes an effort too big for one agent [session](../ai-coding-terms.md#session). This is an idea whose **destination** you can name but whose route you cannot yet see. Wayfinder charts it as a shared **map** of **decision issues** on your issue tracker, then resolves the issues one at a time until the route is clear.

It plans and does not build. Every issue asks a question, and the answer is a decision, not a slice of a build. The map is finished when nothing is left to decide before someone builds the thing. This rule separates a wayfinder issue from an ordinary implementation [issue](../ai-coding-terms.md#issue), and it is the rule agents break most often. When the map clears, wayfinder hands off and does not continue into code.

## When to reach for it

You invoke this by typing `/wayfinder`; the [agent](../ai-coding-terms.md#agent) won't reach for it on its own.

It is the heaviest flow in the set, so the trigger is narrow. The effort must be larger than one agent session can hold, and the route to the destination must be unclear. The split is session count: `/grill-with-docs` for single-session planning, `/wayfinder` for multi-session planning.

| What you have in front of you | What to run |
| --- | --- |
| A well-scoped feature you can settle in one sitting | [grill-me](../productivity/grill-me.md), or [grill-with-docs](grill-with-docs.md) when there is a codebase |
| A greenfield project, or a build spanning many sessions, with the route still unclear | `/wayfinder` |
| A thread where the deciding is already done | [to-spec](to-spec.md): skip straight past the map |
| A cleared wayfinder map | [to-spec](to-spec.md), then [to-issue](to-issue.md) and [implement](implement.md) |
| An existing session that has already grown too big | say "hand off to `/wayfinder`" ([handoff](../productivity/handoff.md) bridges into a map as well as out of one) |

Greenfield is not a requirement. People use wayfinder routinely on legacy and half-built codebases, and it can be more useful there, because much of the fog is "what is already true here" rather than "what should we do".

## Prerequisites

The map and its issues live on the repo's issue tracker, so wayfinder needs the tracker setup from [setup-skills](setup-skills.md). That step writes a "Wayfinding operations" section. The section describes how to express the map, its child issues, blocking edges, and frontier queries on GitHub, GitLab, or local markdown. Wayfinder finds that doc through the pointer in your `CLAUDE.md` / `AGENTS.md`, not at a fixed path. With no tracker configured, it falls back to local markdown files.

The tracker does real work. Its native blocking links show the frontier in the tracker's own UI. On a tracker without native dependency links (a self-hosted Gitea, say), wayfinder infers blockers from the map text. That works, but you must supervise it more closely.

## The map, the fog, and the frontier

The **map** is a single issue labelled `wayfinder:map`, and its child issues are the units of work. It is an **index, not a store**. A decision lives in exactly one place, its issue, and the map only gives a one-line summary and a link. A session loads the map at low resolution and opens individual issues when it needs them. This lets a map keep growing without every session loading its whole history.

The map has four sections:

- **Destination.** What the end of this map looks like. You name it first, before any issue exists, because the destination fixes the scope you measure every issue against.
- **Decisions so far.** One line per closed issue, each with a link to where the detail lives.
- **Not yet specified.** This is the **fog of war**: decisions you can tell are coming but cannot yet phrase sharply. The test for fog versus issue is whether you can state the question precisely *now*, not whether you can answer it. When you resolve an issue, the fog ahead of it clears, and anything you can now specify graduates into a new issue.
- **Out of scope.** Work beyond the destination. Fog only gathers *toward* the destination, so out-of-scope work stays closed and never graduates.

The **frontier** is the set of open, unblocked, unclaimed issues (the edge of the known). A session claims an issue by assigning it to itself before it does any work. The assignee *is* the claim, so concurrent sessions skip that issue. Sessions refer to issues by name, never by a bare `#42`, because a wall of issue numbers is hard to read in narration.

## The four decision-issue types

Every issue carries a `wayfinder:<type>` label. Each issue is either **[HITL](../ai-coding-terms.md#human-in-the-loop)** (worked with a human who speaks for themselves) or **[AFK](../ai-coding-terms.md#afk)** (driven by the agent alone). A HITL issue resolves only through the live exchange. An agent that answers its own [grilling](../ai-coding-terms.md#grilling) questions has broken it.

| Type | Mode | Reach for it when | Resolved by |
| --- | --- | --- | --- |
| `grilling` | HITL | The default. The question can be settled by talking it through. | [grilling](../productivity/grilling.md) plus [domain-modeling](domain-modeling.md), in a fresh session |
| `prototype` | HITL | "How should this look" or "how should this behave": a question talking cannot settle. | [prototype](prototype.md), with a link from the issue to the built artifact |
| `research` | AFK | A fact outside the working directory is blocking a decision. | A [research](research.md) [subagent](../ai-coding-terms.md#subagent), started when you chart the map and run in parallel on a `research/<name>` branch |
| `chore` | Either | Nothing to decide, but manual work blocks a decision, such as provisioning access, signing up for a service, or moving data so you can see its shape. | The agent alone where it can, otherwise a precise checklist for the human |

`chore` is the only type that *does* rather than decides. It belongs on the map only because it unblocks a decision, never because it delivers part of the destination. This type goes wrong most often in practice. Agents read it as an implementation step and start to write product code inside the map.

Research is the only exception to *one issue per session*.

## Common questions

**When it asks for the "destination", does it mean the end of this session or the end of everything?**
The end of the whole map, not just the first session. The question reads ambiguously, but wayfinder is a multi-session tool by definition, so a session-scoped answer never makes sense. Typical destinations are a [spec](../ai-coding-terms.md#spec) to hand off, a decision to lock before planning starts, a proof of concept, or an in-place change such as a data migration.

**A decision I already closed turned out to be wrong. Do I edit the old issue or make a new one?**
There is no official guidance, and the agent's default is unhelpful. It tends to design around the bad decision instead of challenging it, so you must steer it yourself. What works is to tell wayfinder plainly what changed. It then updates the map, revises the affected issues, and comments on the closed ones. You can recover from scope changes mid-map. But if you *designed* a map to change, that is a sign the scope is wrong.

## It's working if

- The destination is written down and agreed before a single issue exists.
- Every open issue reads as a question. Any issue that reads "build the X" is either mis-typed or belongs downstream of the map.
- You can look at your tracker and see which issues are takeable without opening the map, because native blocking shows the frontier.
- A session resolves one issue, posts the answer as a resolution comment, closes it, and adds one line to the map's *Decisions so far*. Then it stops.
- **Not yet specified** shrinks over time. When fog graduates into an issue, it leaves that section and does not appear in both places.
- When the opening breadth-first grill finds no fog at all, the skill stops and tells you the effort is small enough to skip the map.
- The session that finishes the map points you toward a spec, not a pull request.

## Where it fits

`wayfinder` is a **situational on-ramp**, not the default starting point. Most work still starts on the grill-led idea → ship chain. You use wayfinder when the idea is too big to hold in one session. It rejoins that chain at [to-spec](to-spec.md), because a cleared map hands off and does not build.

Most of the work happens in other skills that wayfinder schedules. [grilling](../productivity/grilling.md) and [domain-modeling](domain-modeling.md) resolve the default issue type, [prototype](prototype.md) resolves the issues that talk cannot settle, and [research](research.md) runs as a subagent so its reading stays out of your session. [handoff](../productivity/handoff.md) moves work in and out: into a map from a conversation that grew too big, and out of a map when a side quest appears mid-session. For anything else, [which-skill](which-skill.md) routes over the whole set.
