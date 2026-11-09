# code-review

## What it does

`code-review` reviews the diff between `HEAD` and a fixed point you name (a commit, a branch, a tag, `main`, `HEAD~5`) along two axes, or three when the repo supports it. **Standards** asks whether the code follows how this repo writes code. **Spec** asks whether the code does what the originating issue or [spec](../ai-coding-terms.md#spec) asked for. **Visual**, which joins them only when the repo advertises a visual-capture hook, asks whether the rendered UI still looks right. Each axis runs in its own [sub-agent](../ai-coding-terms.md#subagent) so none sees another's reasoning.

The skill never merges or re-ranks the axes. The report ends with a worst issue *per axis* and declines to name a single winner across them. A change can pass one axis and fail another. Code that follows every convention but implements the wrong thing passes Standards and fails Spec. Code that does exactly what the [issue](../ai-coding-terms.md#issue) asked but breaks the repo's conventions does the reverse. Code that is correct and conventional but renders with clipped text or a broken layout passes both and fails Visual. A blended verdict lets a passing axis hide a failing one.

## When to reach for it

Type `/code-review`, or the agent reaches for it automatically when you ask to review a branch, a PR, work in progress, or anything "since X".

| Your situation | Reach for |
| --- | --- |
| A diff exists and you want to know if it is built right *and* is the right thing | `code-review` |
| You want bugs hunted in the diff: null paths, races, off-by-one | Claude Code's own built-in review, not this one (see the name clash below) |
| Nothing is written yet and you want it written test-first | [tdd](tdd.md) |
| A whole spec needs building, review included | [implement](implement.md), which calls this skill itself |
| The whole codebase has drifted, not one diff | [improve-codebase-architecture](improve-codebase-architecture.md) |
| Something is broken and you do not know why | [diagnosing-bugs](diagnosing-bugs.md) |

You must supply the fixed point. If you do not, the skill asks for one rather than guessing. Before it spawns anything, it checks that the ref resolves and that the diff is not empty, so a mistyped branch name fails in front of you instead of inside the sub-agents.

## Prerequisites

The Standards axis needs nothing. It reads whatever the repo documents (`CODING_STANDARDS.md`, `CONTRIBUTING.md`, and the like) and falls back on a built-in baseline when the repo documents nothing.

The Spec axis needs a spec to exist and be findable. It looks in this order:

1. Issue references in the commit messages (`#123`, `Closes #45`, a GitLab `!67`), fetched through the tracker doc.
2. A path you pass in as an argument.
3. A spec file under `docs/`, `specs/`, or `.scratch/` matching the branch or feature name.
4. Asking you.

Step 1 depends on the tracker doc, which [setup-skills](setup-skills.md) writes. Without it the axis still works if you hand it a path. With no spec at all, the skill skips the Spec sub-agent and the report says "no spec available" rather than inventing requirements.

The Visual axis needs a visual-review doc that names a capture command: `docs/agents/visual-review.md`, or an equivalent doc your `AGENTS.md` points to. A capture script with no doc does not count, and without a doc the axis is skipped entirely. A surface map in the doc is optional. With none, the sub-agent works out the surfaces from the diff. The axis also needs a model with vision. With no vision, or if the capture fails, it reports "unavailable" rather than a failure.

## The axes

| | Standards | Spec | Visual (with a capture hook) |
| --- | --- | --- | --- |
| Question | Is it built right? | Is it the right thing? | Does it still look right? |
| Reads | The repo's documented standards, plus the smell baseline | The originating issue or spec | Images of the surfaces the diff touches, captured by the repo's hook |
| Reports | Documented breaches (can be hard), and smells (always judgement calls) | Missing or partial requirements, scope creep, requirements implemented wrongly | Advisory findings: alignment, spacing, overlap, clipping, palette, contrast, legibility, general brokenness |
| Every finding cites | The standards file and the rule, or the named smell plus the hunk | The line of the spec | The surface, a severity, and the image it reasoned from |

This design exists to avoid a generic review skill that does not know your standards. Such a skill flags what is deliberate in your codebase and misses the invariants your codebase depends on. So the repo's own documentation is the [primary source](../ai-coding-terms.md#primary-source) on the Standards axis, and **the repo always overrides**.

The **smell baseline** sits under the repo's standards. It is twelve code smells from chapter 3 of Fowler's _Refactoring_: Mysterious Name, Duplicated Code, Feature Envy, Data Clumps, Primitive Obsession, Repeated Switches, Shotgun Surgery, Divergent Change, Speculative Generality, Message Chains, Middle Man, Refused Bequest. Each is a labelled heuristic ("possible Feature Envy"), never a hard violation. Each states what the smell is and how to fix it, so a finding comes with a fix attached rather than only a complaint. The Standards axis skips anything your linter already enforces.

The Visual axis is **reference-free** and **advisory**. There is no golden image, no pixel comparison, and no approval step: the sub-agent looks at the captured images and judges them with its own vision. A judgement like that is a lead rather than a test, so its findings never gate the build.

## Common questions

**After every issue, or once at the end?**

Both work, and the skill does not decide for you. Per-issue keeps each diff small enough that the Spec axis has one clear spec to check against, which is the mode `implement` uses. Batching to the end of a branch catches interactions between issues that the per-issue passes each miss. If you are unsure, review per issue and run one final pass against the branch point.

**Does it review my uncommitted work?**

No. It diffs `<fixed-point>...HEAD`. The three-dot form measures from the merge-base and excludes staged and working-tree changes. If `implement` has not made an interim commit, the review cannot see the work that is about to go into the next commit. Commit first, then review, then amend or add a fixup.

## It's working if

- It refuses to start on a bad ref or an empty diff, before any sub-agent is spawned.
- The report arrives as separate blocks under `## Standards` and `## Spec`, plus `## Visual` when the repo has a capture hook, not one merged list.
- Every Standards finding names either a rule in one of your repo's files or one of the twelve smells, with the hunk quoted; every Spec finding quotes a line of the spec.
- The closing summary gives a worst issue per axis and declines to pick an overall winner.
- With no spec available, the Spec block says so instead of listing requirements it inferred from the code.
- A failed capture shows up as Visual "unavailable", a diff with nothing visual to check says "no visual risk, nothing captured", and Visual findings are labelled advisory instead of blocking anything.

## Where it fits

`code-review` is the review step near the tail of the build chain: `grill-with-docs → to-spec → to-issue → implement → code-review → retro`. It also stands alone on any branch or PR you point it at.

- [implement](implement.md) is the closest neighbour. It drives the build and calls this skill as its own closing review before committing. [implement-spec](implement-spec.md) does the same once, over the whole integration branch.
- [retro](retro.md) comes after it and tunes it. When a session shows the review missing a class of mistake, `retro` proposes the check or the `CODING_STANDARDS.md` rule the Standards axis then reads.
- [pr](pr.md) writes the pull request body once the reviewed work goes up.
- [to-spec](to-spec.md) and [to-issue](to-issue.md) produce the document the Spec axis checks against, so a vague spec makes that axis vague.
- [improve-codebase-architecture](improve-codebase-architecture.md) is the whole-codebase counterpart, because this skill only looks at one diff.

[which-skill](which-skill.md) routes across the whole set when you are unsure which skill the situation wants.
