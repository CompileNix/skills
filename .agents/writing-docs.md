# Writing docs pages

Every skill in `engineering/` and `productivity/` has a human-facing **docs page** at `docs/<bucket>/<skill-name>.md`. The docs tree mirrors those two bucket folders under `skills/`. The page is not the skill and not a copy of `SKILL.md`. Only these two buckets are promoted; the rest (`misc/`, `in-progress/`, `deprecated/`) get no docs page.

Most of these skills are **user-invoked**: the agent will never fire them for you, so *you* are the index that has to remember they exist and when to reach for them. That memory is **cognitive load**. The job of a docs page is to relieve it: to orient one reader around one skill so they can hold it in their head, know when to reach for it, and see where it sits in the system. The pages are collectively a distributed router; each is a node.

Act whenever a promoted skill is added, renamed, or has its behaviour changed: create or re-sync its docs page. A rename moves the file too (`docs/<bucket>/<old>.md` → `docs/<bucket>/<new>.md`); a skill that moves between `engineering/` and `productivity/` moves its docs file to the matching folder. Skills in `misc/`, `in-progress/`, and `deprecated/` get no page, because none of those buckets is promoted. A skill moving *out* of one of them into `engineering/` or `productivity/` gains a page; one moving the other way loses it, and so does a promoted skill that is removed outright.

**Every link is repo-relative**, so it resolves in a clone and on any git host. A link to another skill points at its docs page (`<name>.md` in the same bucket, `../<bucket>/<name>.md` across buckets); a link into the repo points at the file's relative path.

The page opens with an H1 naming the skill: `# <skill-name>`.

## Page structure

Fill the template below, keeping its order. The **fixed frame** (`## What it does`, `## When to reach for it`, `## Where it fits`) appears on every page. `## Prerequisites` and the free-form substance sections carry only what this particular skill needs; delete the rest.

Four sections make a page worth reading: `What it does`, `When to reach for it`, `Common questions`, `It's working if`. The first two orient the reader; the last two are where the page stops summarising the skill and starts answering the reader's own situation. Each of the last two has a bar to clear, below. `Common questions` is dropped until real questions exist.

**A page carries no install commands.** A page explains what a skill does and when to reach for it; how it gets onto a machine is not part of that.

<page-template>

## What it does

One or two plain-language paragraphs. Lead with the skill's one-sentence job, then state the **defining constraint**: the single fact that makes this skill behave differently from the obvious default (for `to-spec`: it does not interview the user again, it synthesises what is already known). Write it as a plain declarative sentence, never a labelled aside like "The defining constraint:" or "The key thing:"; the formula reads as filler. This line is the most valuable on the page; never omit it.

## When to reach for it

How and when you reach for the skill, in two beats that are both effectively always present:

- **Invocation mode.** State whether you type it or the agent fires it. A user-invoked skill: "You invoke this by typing `/<name>`, and the agent won't reach for it on its own." A model-invoked skill: "Type `/<name>`, or the agent reaches for it automatically when a task fits."
- **Trigger boundary.** The index entry: "reach for this when …". Where the skill is confusable with a sibling, add the other half: "for <X> instead, use [<sibling>](<sibling>.md)."

## Prerequisites

Optional: include only when the skill needs something in place to be functional; omit the heading entirely otherwise. Covers: a **workspace it writes into** (a stateful skill like `grill-with-docs` writes `GLOSSARY.md` and ADRs; `teach` builds a whole directory, so say what it writes and where), **prior setup** (`triage`/`to-spec`/`to-issue` need `setup-skills` to have configured an issue tracker), or **repo-specific tooling**. A stateless skill that runs anywhere has no prerequisites, so drop the section.

## <free-form middle>

One to three short sections, in the skill's *own vocabulary*, that make it click. Choose whatever headings fit the skill: the loop it runs, the artifact it produces, the fork it makes, the one anti-pattern it kills. There is no prescribed heading; the skills are too heterogeneous for one.

The single non-negotiable: **surface the skill's leading word / defining idea** (`tight` feedback loop, `deep module`, throwaway-code-answers-a-question, red-green). It pays off twice: the reader learns what the skill *is*, and learns the word they'll later think with to *reach for* it.

## Common questions

The questions readers really ask about this skill, each in bold with the answer in the lines beneath it. No sub-headings.

An observed question always beats an invented one, so go and find them before you write any:

- **Your own sessions.** Moments where the skill surprised you or did the wrong thing, and what you had to look up to use it.
- **This repo's issues.** `gh issue list --search "<skill-name>" --state all`. A question filed twice is a question the page owes an answer to.

Where the hunt comes up thin, the section may also carry a question a reader would plainly ask, but **the count stays honest to the evidence**. A well-discussed skill earns six; an obscure one earns one or two, or none at all. Padding a thin skill out to match a rich one is how the section fills with questions nobody has, and an invented question teaches the reader nothing.

Put the sharpest first, and say the unflattering thing where it is true: a very long grilling session usually means the scope was too big; a model asked to write its own skill produces something verbose. Each answer stands as a plain claim about the skill as it is now: no issue citations, no claims about who asks or how often, and no history of how the skill changed. Omit the heading where there is nothing worth answering.

## It's working if

A few bullets naming what the reader sees when the skill is doing its job. The bar on each is that the reader can check it without opening `SKILL.md`: a signal in their own work, or in the trace in front of them. "The document gets shorter as it gets better" passes; "the library section is byte-identical to `template.sh`" is a compliance check on the skill's internals wearing this section's name. Include it wherever the tells are crisp; omit the heading where they stay vague.

## Where it fits

Always present. Situate the skill in the system in a sentence or two:

- **Role.** Name it: a **chain step** (`grill-with-docs → to-spec → to-issue → implement → code-review`), a **run-once setup** (`setup-skills`), **periodic maintenance** (`improve-codebase-architecture`, "every few days"), or a **reach-for-it-anytime standalone** (`diagnosing-bugs`, `prototype`, `handoff`). A standalone's map is one honest sentence, which is far better than omitting the section.
- **Neighbours.** The one or two siblings that matter, each with a because-clause, linked relatively.
- **The map.** Point to [which-skill](../engineering/which-skill.md), the router over the whole set, so this page stays a node and never has to redraw the graph.

</page-template>

## Conventions

- Explain the **why**, not the process. The page orients and situates the skill; it never reproduces the `SKILL.md` steps or template dumps: a human choosing a tool does not need the runbook.
- **Name no author or commenter.** The page is a technical document, not a record of who said what. State the substance as a plain claim about the skill ("the fix is a direct instruction: …", "the split comes down to session count") and drop the frame.
- Use the skill's **leading words** (_seam_, _deep module_, _tracer bullet_) so the page and the skill speak one language.
- **Use the [AI coding terms](../docs/ai-coding-terms.md) where one exists, and link its first use on the page.** Prefer the listed word over a synonym you invent. Link the first occurrence of each term to its heading in `docs/ai-coding-terms.md` (`../ai-coding-terms.md#context-window` from a docs page), and leave every later occurrence unlinked. Link only where the word carries the listed sense: a domain *model*, background *context* or an auth *token* is a different word that happens to match. Never link inside a heading, a code span, or an existing link, and never link a word that names a skill in this repo rather than the concept. When a page needs a term that is missing, add it there.
- **Branches go in a table or a list, never in a paragraph.** Where the page presents a choice (two artifacts the skill can produce, four situations that trigger it, five options at a boundary), the reader is scanning for the one row that matches their situation. A paragraph makes them read all of it to find out. A short markdown table (condition in the left column, what to do in the right) or a bulleted list gives it back in one glance. This applies wherever the branch appears, most often in `## When to reach for it` and the free-form middle.
- Keep the page itself low-load. It is documentation *about* low-cognitive-load skills; furniture (spare headings, restated links) is the thing it is arguing against.

## Done when

- The page exists at `docs/<bucket>/<name>.md`, and no stale page survives a rename or bucket move.
- The page carries no source link and writes no install command of its own.
- `## What it does` states the defining constraint, as plain prose rather than a labelled aside.
- The page names no author or commenter: every claim stands on its own.
- `## When to reach for it` states invocation mode and the trigger boundary.
- `## Where it fits` names the role and links to `which-skill`.
- A prerequisite (workspace, prior setup, tooling) is stated where one exists, and the section is absent where none does.
- The middle surfaces the leading word.
- Every term from `docs/ai-coding-terms.md` the page uses is spelt that way, and its first use (and only its first use) links to its entry.
- Every multi-way branch is a table or a list, not a paragraph the reader has to read in full.
- The hunt for real questions ran (your sessions, the issues), and `## Common questions` is sized to what it found, or absent if it found nothing.
- Every `## It's working if` bullet is checkable without opening `SKILL.md`.
- The sections appear in the template's order.
- Every link is repo-relative, and every one resolves.
