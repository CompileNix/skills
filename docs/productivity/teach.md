# teach

## What it does

`teach` turns the directory you run it in into a standing teaching workspace and teaches you one topic across many [sessions](../ai-coding-terms.md#session), in short self-contained HTML lessons.

It does not teach from what the [model](../ai-coding-terms.md#model) already knows. It treats [parametric knowledge](../ai-coding-terms.md#parametric-knowledge) as untrusted. Before it teaches, it finds high-trust resources, records them in `RESOURCES.md`, and cites them inside every lesson. It is also [stateful](../ai-coding-terms.md#stateful). The mission, the resources, the lessons and the record of what you have learned all live as files in the directory, so the next session continues from those files, not from what is left of the last conversation.

## When to reach for it

You invoke this by typing `/teach`; the [agent](../ai-coding-terms.md#agent) won't reach for it on its own.

Reach for it when the learning is the project: a language, a framework, a codebase you have just joined, yoga, shaders, a certification. It is not the tool for one explanation in passing.

| What you want | What to reach for |
| --- | --- |
| To learn a topic over weeks, with sessions that accumulate | `teach` |
| One idea explained inside the session you are already in | Just ask, in that session |
| The agent's last message re-pitched because it didn't land | [wait-what](wait-what.md) |
| To sharpen thinking you already have, rather than acquire new material | [grill-me](grill-me.md) |
| A background agent to read [primary sources](../ai-coding-terms.md#primary-source) and leave you a cited document | [research](../engineering/research.md) |
| To learn something that came up mid-grilling, without derailing the [grilling](../ai-coding-terms.md#grilling) | [handoff](handoff.md) out to a teaching workspace, then `teach` there |

## Prerequisites

`teach` builds a directory rather than producing a file, and the skill assumes one mission per workspace, so run it somewhere you are happy to give over to a single topic. Keep it out of the project you are working in. A separate repo is the best home, better than a global `~/.learnings/` folder or the working project itself. A dedicated repo also lets you commit the lessons, which is how teams have shared them.

What accumulates in that directory:

| Path | What it holds |
| --- | --- |
| `MISSION.md` | Why you are learning this. Every other file depends on it. If it is missing, the first thing `teach` does is interview you until it isn't |
| `RESOURCES.md` | The vetted sources it teaches from, split into Knowledge and Wisdom (communities) |
| `lessons/*.html` | The numbered lessons: the primary unit of teaching |
| `reference/*.html` | Compressed cheat-sheets, algorithms, glossaries: the documents you return to |
| `learning-records/*.md` | ADR-style notes on what you have demonstrably learned, used to decide what to teach next |
| `assets/*` | Reusable components, starting with a shared stylesheet, so the lessons look like one course |
| `NOTES.md` | Your stated teaching preferences |

Two notes on that list. A glossary suits most topics, but the skill ships a `GLOSSARY-FORMAT.md` that `SKILL.md` no longer links to, so you only get one if you ask. All of it lands in the directory you ran `/teach` in.

## Storage strength, not fluency

The word to think with is **storage strength**: long-term retention, as opposed to **fluency**, the in-the-moment recall that feels like mastery while you are reading and is gone a week later. `teach` builds the former through desirable difficulty: retrieval practice, spacing, interleaving. Knowledge comes first. At that stage difficulty works against you, because it uses up the working memory you need to understand. Then `teach` drills the skill through a tight feedback loop, and at that stage difficulty is the tool.

Two things decide what you get taught. The **mission** (the concrete real-world reason you want this) is the basis of every lesson. Without it the lessons become abstract and nothing decides what comes next. From the mission and the learning records, `teach` picks the next lesson inside your **zone of proximal development**: hard enough to take effort, but not so far ahead that you cannot learn it.

Storage strength is also why the skill pushes back instead of agreeing. A question that needs **wisdom** (real-world judgement) gets an attempted answer and then a pointer to a community where you can test it. The skill does not let you skip a quiz.

## Lessons, references and components

A **lesson** is one self-contained HTML file, short enough to finish in a sitting, tied to the mission, giving one tangible win. It cites its sources, recommends one primary source to go and read yourself, and links to sibling lessons and reference documents.

You rarely go back to a lesson, but you do go back to reference documents. So the short form of a lesson (the syntax table, the algorithm, the pose sequence, the glossary) belongs in `reference/`, not buried in the lesson that introduced it.

Lessons are built from **components** in `assets/`: stylesheets, quiz widgets, simulators, diagram helpers. Reuse is the default. The agent reads `assets/` before authoring a lesson and builds from what is there. It writes anything new that a second lesson could use as a component, not inline. The shared stylesheet is the first component in every workspace, and it makes the lessons look like one course instead of many unrelated pages.

## It's working if

- The first thing it does in an empty directory is interview you about why you want this, rather than produce a lesson.
- `RESOURCES.md` fills up before the lessons do, and each lesson names one primary source worth reading yourself.
- Claims in a lesson carry links out. A lesson with no citations is the skill teaching from memory.
- A lesson takes one sitting and leaves you able to do one thing you couldn't before.
- Opening a fresh session in the folder and saying "next lesson" continues the course instead of restarting it.
- `learning-records/` grows, and lessons stop re-teaching what you have already demonstrated.
- The lessons look like one course: they link the stylesheet in `assets/` rather than each carrying its own.
- A question that needs judgement gets you pointed at a forum, subreddit or class, not just an answer.

## Where it fits

`teach` is a **reach-for-it-anytime standalone**. It is not a step in a build chain and shares no artifacts with the engineering flow; it works in its own directory for as long as you study the topic.

Its one real neighbour is [handoff](handoff.md). Together they answer "what do I do if I'm being grilled about something I don't understand?" Don't stop the grilling to learn. `/handoff` to a teaching workspace, learn the topic there with `/teach`, then go back and continue where you left off. The nearby alternative is [research](../engineering/research.md), for when what you want is a cited document rather than lessons and retention. When you are not sure which skill or flow fits, [which-skill](../engineering/which-skill.md) routes you over the whole set.
