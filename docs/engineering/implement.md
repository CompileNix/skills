# implement

## What it does

`implement` builds work that has already been decided. You point it at a [issue](../ai-coding-terms.md#issue), a [spec](../ai-coding-terms.md#spec), or the plan you just agreed in the conversation, and it writes the code, drives [tdd](tdd.md) at the seams, typechecks as it goes, runs [code-review](code-review.md) at the end, and commits to the current branch.

It never reopens the plan. There is no interview, no clarifying round, no proposal of a different approach. Whatever was settled upstream is the input, and the skill's whole job is to turn that into a commit. That is what separates it from typing "build this" at a fresh [agent](../ai-coding-terms.md#agent), which often redesigns the work while it builds it.

## When to reach for it

You invoke this by typing `/implement` yourself, and the agent won't reach for it on its own. It ships with `disable-model-invocation: true`, so no other skill can call it either. Wherever [which-skill](which-skill.md) or [to-issue](to-issue.md) says "then `/implement` per issue", that is an instruction to you, not something the agent will do unprompted.

Where the work currently lives decides whether this is the right skill:

| The work is… | Reach for |
| --- | --- |
| An issue on the tracker | `/implement #42`, one issue per [session](../ai-coding-terms.md#session), [clearing](../ai-coding-terms.md#clearing) context between issues |
| A spec, not yet split up, and the build spans sessions | [to-issue](to-issue.md) first, then `/implement` per issue |
| A spec, and the build is small | `/implement` directly against the spec |
| Only in the conversation you just had, and it's still small | `/implement` right there, in the same window |
| Not written down anywhere yet | [grill-with-docs](grill-with-docs.md), or [grill-me](../productivity/grill-me.md) if there's no codebase |
| One concrete behaviour you want test-first, with no spec | [tdd](tdd.md) directly |
| Already built, and you want it checked | [code-review](code-review.md) directly |

The same-session case is worth naming because the skill's own first line doesn't cover it. `SKILL.md` says "the spec or issues", which pushes the [model](../ai-coding-terms.md#model) to look for a file that doesn't exist. If the plan lives only in the thread, say so when you invoke it.

## Prerequisites

`implement` commits to the branch you are on. It does not create one, and it does not ask. Check you are on the branch you want the work on before you start.

If the issues came from [to-issue](to-issue.md), [setup-skills](setup-skills.md) configured the tracker they live on. `code-review` reads the same configuration to find the originating spec at close-out.

## What one run does

A run has five steps, in order:

1. Read the issue or spec and work out the seams.
2. Drive [tdd](tdd.md) at the pre-agreed seams, one red-green slice at a time.
3. Typecheck often, run single test files as it goes.
4. Run the full test suite once, at the end.
5. Run [code-review](code-review.md), then commit to the current branch.

One run covers one issue. The issues [to-issue](to-issue.md) produces are tracer-bullet vertical slices sized to fit a single fresh [context window](../ai-coding-terms.md#context-window), so the intended rhythm is: clear context, implement one issue, commit, clear again. Each issue is self-contained, so you can discard the previous issue's context.

## Pre-agreed seams

The skill's central idea is the **seam**, the public boundary you observe behaviour at without reaching inside. Tests live at seams. When the seam is agreed before any code exists, the tests last, and you can rewrite the implementation underneath without changing them.

The "pre-agreed" part matters, and it is also the skill's weakest point. Nothing inside `implement` agrees the seams. `tdd` is the skill that asks, and it refuses to write a test at an unconfirmed seam. So in practice the agreement happens either upstream in the spec, or in the first exchange of the run. If it happens nowhere, the run becomes "just write the code" and nothing warns you. Naming the seams in the spec is what stops that.

## Common questions

**It finished, but my issue is still open and the acceptance criteria are still unchecked.**

Correct, and expected. `implement` has no completion step. It ends at the commit and never touches the work item. This is the same on GitHub Issues and on the local markdown tracker, so it is not a tracker integration problem. It also does not act on the findings `code-review` produced, and does not tick the `- [ ]` boxes on the originating issue. Close the issue and reconcile the criteria yourself. This matters most on a dependency chain, because `to-issue` defines the frontier as issues whose blockers are all closed. If nothing gets closed, nothing ever becomes visibly unblocked.

**One issue burned 150k tokens. Am I using it wrong?**

Probably not. The issue is more likely too big. A run does codebase exploration, a red-green loop per seam, a full suite, and a review, so a non-trivial issue exceeding 100k [tokens](../ai-coding-terms.md#token) is normal rather than a sign something broke. The fix is upstream. Right-size the issues in [to-issue](to-issue.md) so each fits one fresh window. If a single issue keeps going over, split it rather than raising the [effort](../ai-coding-terms.md#effort) level.

**`/implement #2` in a fresh session worked on something completely unrelated.**

The agent resolved `#2` against another numbered list in context, such as a todo file or checklist, rather than the configured tracker. `implement` now fetches a passed reference from the issue tracker and states its title before starting, and asks when the reference is ambiguous. Check that title matches the issue you meant; passing the issue URL or `owner/repo#2` removes the ambiguity entirely.

## It's working if

- The session opens by reading the issue or spec and restating what it will build, rather than asking you what to build.
- You can see an actual `tdd` Skill tool call in the trace, not just tests appearing in the diff.
- Typechecks and single test files run repeatedly during the run, and the full suite runs once near the end.
- The run reaches a commit on your current branch without you prompting it to carry on.
- The diff is one issue's worth of change: a vertical slice through every layer, not several issues swept together.

## Where it fits

`implement` is the build step of the main chain:

```txt
grill-with-docs → to-spec → to-issue → implement → code-review → retro
```

Its neighbours are [to-issue](to-issue.md), which produces the issues it consumes and declares the blocking edges that decide their order; [tdd](tdd.md), which it drives internally at each seam; and [code-review](code-review.md), which it runs before committing. It sits downstream of the planning skills and trusts them. It does not re-validate the shape of what it was handed, so a badly-structured map or a horizontally-layered issue gets built as written.

That trust is why [wayfinder](wayfinder.md) merges onto the chain at [to-spec](to-spec.md) rather than looping its map straight into `implement`. Go straight to `implement` from a map only when the effort turned out small.

[which-skill](which-skill.md) is the router over the whole set when you are not sure which flow you are in.
