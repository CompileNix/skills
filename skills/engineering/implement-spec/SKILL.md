---
name: implement-spec
description: "Implement the result of /to-spec and /to-issue in code."
disable-model-invocation: true
---

You have been provided a spec. This spec should have issues associated with it, describing how to implement the spec.

The issue tracker should have been provided to you. If not, tell the user to run `/setup-skills`.

The goal is the entire spec implemented on a single **integration branch**, with every issue resolved the way the issue tracker closes work.

The issues are not a list of steps. They are a **task graph** with blocking relationships between them. This means there is always a **frontier** of issues which are ready to be grabbed.

Start every subagent with a fresh context window.

Communication to and from subagents should be sparse. Communicate primarily through **context pointers**: to the spec, issues, research notes, and previous commits. Don't duplicate information already available via pointers.

**Implementer subagents** should be run in the background where possible for maximum concurrency.

## Steps

1. Read the spec and issues to understand the task graph.

2. (optional) Use an **exploration subagent** to conduct any exploration required by the issues - relevant codebase files or external documentation. Ensure the exploration subagent can save files - it should save its markdown notes in a directory outside the repo, accessible by all future subagents. This lets **implementer subagents** focus on implementation rather than exploration.

3. Create the integration branch. If the issue tracker closes work through PRs, or the user asks for one, open a draft PR after the first merge in step 5 (a branch with no commits ahead of main can't open one), marked as closing the spec and issues.

4. Use a fresh **implementer subagent** for each issue, each in its own worktree on its own branch. Each implementer subagent:
   - confirms its worktree is based on the integration branch before starting, and resets onto it if not;
   - calls the Skill tool with `tdd` to build the issue;
   - merges the integration branch tip into its own branch before reporting done

5. Once an **implementer subagent** completes, merge its work to the integration branch with a **merger subagent**.

6. If this changes the **frontier** of available issues, kick off more **implementer subagents** to work on the new issues. This allows for maximum concurrency.

7. Once all issues are complete, call the Skill tool with `code-review` on the integration branch. Fix all issues raised by the code review, advisory Visual findings included, in a single fresh **implementer subagent**.

8. If a draft PR exists, mark it ready for review. Otherwise, resolve each issue the way the issue tracker closes work, and report the integration branch.

9. Clean up all **implementer subagent** worktrees.
