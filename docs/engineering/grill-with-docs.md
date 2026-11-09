# grill-with-docs

## What it does

`grill-with-docs` interviews you about a plan or design until you and the [agent](../ai-coding-terms.md#agent) share one understanding of it, and writes the vocabulary and the hard decisions into your repo while it does. It is the same interview [grill-me](../productivity/grill-me.md) runs (a round of questions, then wait, then the next round), pointed at a codebase.

It is **[stateful](../ai-coding-terms.md#stateful)**. Every other grilling skill leaves the [session](../ai-coding-terms.md#session) in your head; this one leaves files on disk. When a term resolves, the skill writes it to `GLOSSARY.md` at once, not in a batch at the end. When a decision passes three gates, the skill writes it as an ADR. That is the whole difference, and it also causes most of the trouble people have with the skill. The artifacts are real files in a real repo, so they can be missing when you expected them, and they can drift when more than one person writes them.

## When to reach for it

You invoke this by typing `/grill-with-docs`, and the agent won't reach for it on its own.

Reach for it at the start of a change, in a repo, when the plan is still fuzzy and the words for the thing are not settled yet. It is the single-session tool. Which grilling skill you want depends on what is in front of you:

| What you have | Reach for |
| --- | --- |
| You aren't working in a working directory at all | [grill-me](../productivity/grill-me.md) |
| A repo, and a change you can settle in one session | `grill-with-docs` |
| An effort too big to hold in one session (a greenfield build, a large feature) | [wayfinder](wayfinder.md) |
| A repo with no domain docs at all, and no particular feature in mind | `grill-with-docs`, aimed at the repo rather than a change |
| A decision blocked on knowledge in someone else's head | [to-questionnaire](../productivity/to-questionnaire.md) |

The wayfinder split comes down to session count: `/grill-with-docs` for single-session planning, `/wayfinder` for multi-session planning.

## Prerequisites

The skill writes into your repo, so you need to be somewhere it is safe to write. Resolved terms go to a `GLOSSARY.md` glossary at the root, or to the relevant context's `GLOSSARY.md`, if a `GLOSSARY-MAP.md` at the root marks the repo as multi-context. Decisions go to `docs/adr/`. The skill creates both only when it needs them. Nothing exists until the first term or decision is settled, so you set up nothing in advance.

It also needs two other skills present, because its own `SKILL.md` is one line that delegates to them. [grilling](../productivity/grilling.md) supplies the interview, and [domain-modeling](domain-modeling.md) supplies the writing. Installing `grill-with-docs` alone gets you a skill that does not work.

## The paper trail

Three things come out of a session, and they are not equal.

| What resolved | Where it lands |
| --- | --- |
| A term: the project's own word for a thing | `GLOSSARY.md`, inline, the moment it resolves |
| A decision that is hard to reverse, surprising without context, and a real trade-off | An ADR under `docs/adr/` |
| Everything else you decided | The conversation, and nowhere else |

That third row is the one that catches people out. `GLOSSARY.md` is only a glossary. It holds no implementation details, no [spec](../ai-coding-terms.md#spec), and no scratch notes. An ADR needs all three conditions at once, so most decisions do not qualify and most sessions produce none. A session that yields a sharper glossary and zero ADRs is working as designed, but it means most of what you agreed exists only in the [context window](../ai-coding-terms.md#context-window) you agreed it in. Hand that same conversation to [to-spec](to-spec.md) rather than [clearing](../ai-coding-terms.md#clearing) it.

The glossary is the main output. This skill builds domain language: the project's own words, agreed once, so you, the agent and your colleagues do not have to work them out again. Not everyone agrees that this improves agent performance. The strongest objection is that a term and its plain-English expansion get the same result from the [model](../ai-coding-terms.md#model), and that the vocabulary mainly shortens communication between the humans who share it. On that view the glossary is still valuable, but the value goes to the humans.

## Common questions

**Should I use this or `/wayfinder`?**
Scope decides it. Use this for anything you can settle in one session; use [wayfinder](wayfinder.md) when the effort is too big to hold in one, and it charts the work as a map of decision [issues](../ai-coding-terms.md#issue) first. Wayfinder is slower and denser, and reaching for it on a well-scoped feature is the common mistake. It does not replace this skill, and it can start a grilling session for the parts of the map that suit one.

**What should I do when the session ends?**
The skill's closing message is often open-ended, which is a known problem. In the main flow the answer is [to-spec](to-spec.md), in the same conversation. If the change is small enough to build immediately, go straight to [implement](implement.md) instead.

## It's working if

- `GLOSSARY.md` changes *during* the session, term by term, rather than appearing in one lump at the end.
- The glossary reads as pure vocabulary (your project's words with tight definitions) and contains no implementation detail or spec-like prose.
- Questions the codebase can answer get answered by reading the codebase, not asked of you.
- You get few or no ADRs, and the ones you get are decisions you would be annoyed to have to argue again.
- It challenges a word you used because your existing glossary defines it differently.

## Where it fits

`grill-with-docs` is the head of the main build chain:

```txt
grill-with-docs → to-spec → to-issue → implement → code-review → retro
```

It comes before anything is written down as a spec. It produces the shared understanding and settled vocabulary that [to-spec](to-spec.md) then synthesises without interviewing you again. Its close neighbours are [grill-me](../productivity/grill-me.md), the same interview with no repo and no files, and [domain-modeling](domain-modeling.md), the glossary-and-ADR discipline it drives; both use the [grilling](../productivity/grilling.md) primitive for the interview. Upstream of it, [wayfinder](wayfinder.md) charts efforts too large for one session and can hand parts of the map back down to it. When you're unsure which skill or flow fits, [which-skill](which-skill.md) routes you.
