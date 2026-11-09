# grilling

## What it does

`grilling` is the interview loop that stress-tests a plan, a decision, or an idea before anyone acts on it. It maps the subject as a **design tree**: every decision branches into the decisions that hang off it, and interviews you branch by branch until no assumption stays unstated.

It does not ask one question at a time, and it does not ask everything at once. Each **round** asks the whole **frontier**: every decision whose prerequisites are already settled, and nothing else. Two questions never share a round if one depends on the other; a question that hinges on an answer still open belongs to a later round. Your answers settle decisions, the frontier moves outward, and the next round asks what that unblocked. Thirteen questions typically land in about three rounds rather than thirteen.

## When to reach for it

Type `/grilling`, or the [agent](../ai-coding-terms.md#agent) reaches for it on its own when a task fits. It is the only [skill](../ai-coding-terms.md#skill) in the grilling family that is model-invoked, so you rarely type it. Usually a skill you *did* type runs it for you.

Typing `/grilling` directly gets you the plain interview and nothing else. Where you want something more than that:

| What you have | Reach for |
| --- | --- |
| You aren't working in a working directory | [grill-me](grill-me.md): the same [session](../ai-coding-terms.md#session), under a name the agent will never fire by itself |
| You are in a working directory | [grill-with-docs](../engineering/grill-with-docs.md): the same session, and it writes `GLOSSARY.md` and ADRs as it goes |
| An effort too big to hold in one session | [wayfinder](../engineering/wayfinder.md): it charts a map and runs grilling inside the decision issues |
| A question that talking cannot settle: how something should look or feel | [prototype](../engineering/prototype.md): build the throwaway version, then come back |
| A skill of your own that needs an interview | Invoke `/grilling` from it, rather than writing another interview |

## The round, the frontier, and who decides

The skill rests on three ideas.

The **design tree** is the model of the subject: decisions with decisions hanging off them. The **frontier** is the set of decisions whose prerequisites are all settled: the only questions the agent can ask yet. A **round** is one frontier, asked in full and answered in full.

Inside a round, every question has a fixed format: numbered and titled behind a `❓`, then the body, then the agent's recommended answer alone on a `➡️` line. This format lets you answer a round by number ("1 yes, 2 the second option, 3 no, here's why") instead of by quoting questions back. The format has one known problem. The recommendation sometimes argues *against* the question as it was worded, so agreeing with the recommendation means answering "no" to the question. When that happens, answer the recommendation and say so.

After the written round, if your [harness](../ai-coding-terms.md#harness) has a question tool, the agent also puts the round to you there, so you can pick answers instead of typing them. The written round keeps the reasoning, and each question in the dialog makes sense without it, with the recommendation as the first option. A round larger than the tool allows is split across calls. With no question tool, you answer the written round by number.

The other half of the design is the split between facts and decisions. Facts are the skill's own job. When a frontier question needs something the [environment](../ai-coding-terms.md#environment) can settle, the agent dispatches a [sub-agent](../ai-coding-terms.md#subagent) to find out rather than asking you. The round does not wait for that research; only the questions that depend on it wait. Decisions are yours, and the agent must wait for them. An agent running `grilling` that answers its own decisions has broken the skill. The session ends when the frontier is empty. The agent then waits for you to confirm a shared understanding before it acts on what you agreed.

The frontier has one limit. The agent chooses it by judgement; it does not compute it from a graph. So it can put two questions in one round and only later find that one answer should have changed the other. The only guard is to tell it. That reopens the affected branch in the next round.

## What lives here and what lives in the wrappers

This page covers the mechanism. The wrapper skills' pages cover how each one uses it.

| Question | Where it is answered |
| --- | --- |
| The tree, the frontier, rounds, the question format, facts vs decisions | Here |
| How long a session should run, what to do with a question you can't answer by talking, how to avoid nodding along | [grill-me](grill-me.md) |
| What gets written to `GLOSSARY.md`, what becomes an ADR | [grill-with-docs](../engineering/grill-with-docs.md) |

## Common questions

**Can I cap the number of questions?**
No, and a cap is out of scope on purpose. Some plans need three questions and some need fifty; a fixed ceiling either truncates the hard case or feels arbitrary on the easy one. The intended control is plain language. Tell it to wrap up, or stop and accept the plan where it stands. If a session is running very long, the cause is usually that the scope was too big; break the work up and grill the pieces.

**I installed `grill-me` on its own and nothing happens.**
`grill-me` is a one-line skill whose whole body is "run a `/grilling` session", so it needs this skill installed too. The same is true of `grill-with-docs`, which additionally needs [domain-modeling](../engineering/domain-modeling.md). Installing the whole set avoids the problem; installing selectively means installing the primitives as well.

## It's working if

- A round arrives as a numbered list, each question with its recommendation on a separate `➡️` line, and you can answer the whole round by number or, where your harness has a question tool, by picking options in the dialog that follows.
- Nothing in a round needs another question in the same round answered first.
- Later rounds ask things the first round could not have asked.
- It goes and looks facts up (reading files, dispatching a sub-agent) rather than asking you something it could have found out.
- Research running in the background does not stall the round; only the questions that depend on it wait.
- It stops at the end and asks you to confirm the understanding is shared, instead of starting work.
- Question count stays high while round count stays low.

## Where it fits

`grilling` is a **primitive**, not a step you schedule: the single source of truth for the interview technique, kept in one place so every skill that needs an interview reaches for it instead of inventing one. [grill-me](grill-me.md) and [grill-with-docs](../engineering/grill-with-docs.md) are its two user-invoked front doors, and `grill-with-docs` is where the main build chain begins, ahead of [to-spec](../engineering/to-spec.md). [wayfinder](../engineering/wayfinder.md) runs it to resolve decision issues, [triage](../engineering/triage.md) to grill a vague report into a workable one, and [improve-codebase-architecture](../engineering/improve-codebase-architecture.md) to walk the tree once you have picked a candidate to deepen. When you are unsure which entry point fits, [which-skill](../engineering/which-skill.md) routes you.
