# pr

## What it does

`pr` defines the shape of a pull request body: a **Summary** that shows the change, **Evidence** that it works, and a **Merge Danger** call on how risky it is to land. It is a format reference, not a workflow. It does not push a branch, open the PR, or decide what goes into it. It tells the [agent](../ai-coding-terms.md#agent) what the body should look like when it writes one.

The summary is a visual, not a paragraph. A default PR body describes the diff in prose. This one picks the **smallest view** that makes the key point clear (pseudocode, a call tree, a component tree, a file tree, a Mermaid diagram, or a shaped diff) and keeps the words around it brief. The reviewer already has the diff open, so the body shows them its shape before they read it.

## When to reach for it

Type `/pr`, or the agent reaches for it automatically whenever it is writing a PR body.

| Your situation | Reach for |
| --- | --- |
| A branch is ready and needs a body a reviewer can scan | `pr` |
| The code is written but nobody has reviewed it yet | [code-review](code-review.md) first, then `pr` |
| The PR is open and review comments are coming back | Nothing in this set yet; `pr` only writes the body |

## The template

Three sections, in this order:

- **Summary**: one or more small visuals, each placed next to the short text it supports. Use one, sometimes several, rarely all of them. Keep only the calls, files, props, and boundaries the reviewer needs.
- **Evidence**: a before and after. A screenshot is the strongest evidence when the change is visual and the [environment](../ai-coding-terms.md#environment) can take one. Otherwise, use the exact test that failed and now passes, written as pseudocode, or the console output that changed.
- **Merge Danger**: whether the change is a **one-way door** or a **two-way door**, and its **blast radius**. A two-way door is cheap to reverse; a one-way door (a destructive migration, a public API removal, a hard-to-reverse decision) is not. Blast radius names what could break if the change is wrong: layout shift, consumers of an API, mobile responsiveness.

The door call is the leading idea. It changes "is this safe to merge?" from a gut feeling into a stated claim the reviewer can disagree with. It also tells them where to spend their [human review](../ai-coding-terms.md#human-review). Skim a two-way door with a small blast radius, and read a one-way door slowly.

## Common questions

**Does it keep the body up to date as the PR changes?**

No. It writes the body at one point in time, and a PR that changes under review leaves that body stale. Ask the agent to rewrite the body after a large change. The agent is writing a PR body again, so it uses the same shape.

**My change has no UI. What goes in Evidence?**

Everything except the screenshot. The screenshot is the strongest evidence only when the change is visual. For a migration, a background job or a refactor, the evidence is the exact test that failed before and passes now, or the console output that changed. "Tests are green" on its own is a claim, not a before and after.

## It's working if

- You can tell what the PR changes from the Summary visual alone, before opening the diff.
- The body has no preamble: it starts at the Summary heading.
- The Evidence section shows a before and an after, not a claim that tests pass.
- Every PR states a door and a blast radius, and the one-way doors are the ones you slow down on.

## Where it fits

`pr` comes between review and retro when the build ships as a pull request: `to-spec → to-issue → implement → code-review → pr → retro`. It is model-invoked, so it also fires on its own any time the agent writes a PR body outside that chain.

- [code-review](code-review.md) runs before it, because a PR body should describe a diff that has already been reviewed.
- [implement](implement.md) produces the commits the body describes.

[which-skill](which-skill.md) routes across the whole set when you are unsure which skill the situation wants.
