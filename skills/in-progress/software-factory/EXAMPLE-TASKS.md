# Example tasks

Tasks grouped by the problem they solve. Each names the trigger that starts its runs, what a run does, and what it triggers next. Most factories start as one of these and grow by chaining the next.

## Untriaged issues pile up

**Explore task**
- Trigger: an issue is created, or a human labels it.
- Does: checks the issue against the codebase and sorts it into a category (easy call, needs a human, not a bug).
- Triggers: an implementer run for easy calls. Anything else ends with the issue labelled as waiting for a human.

## Ready issues wait for someone to build them

**Implementer task**
- Trigger: an issue is labelled ready, by a human or an explore run.
- Does: builds the issue until the automated checks pass, and opens a draft PR.
- Triggers: an automated review run.

## PRs wait for review

**Automated review task**
- Trigger: a PR opens with no automated review yet, or a human labels it.
- Does: reviews the diff against the codebase's standards and the issue it came from.
- Triggers: a rework run on a fail. On a pass it ends, and the PR waits for human review before a human merges it.

## Failed automated reviews sit unfixed

**Rework task**
- Trigger: an automated review run fails a PR.
- Does: fixes only what the automated review named, and pushes.
- Triggers: an automated review run. After a set number of fails, it ends with the PR labelled as waiting for a human.

## Specs are too big for one run

**Decompose task**
- Trigger: a spec issue is labelled.
- Does: splits the spec into issues, each recording which issues it depends on.
- Triggers: an implementer run.

The implementer run here picks the next issue whose dependencies are all closed, and triggers itself again until no issue is left.

## Migrating to a stricter automated check

A new lint rule (or a stricter type setting) is switched on, but only some files pass it. The rule enforces on the passing files, and the failing ones sit on an exception list.

**Ratchet task**
- Trigger: a daily clock.
- Does: takes one file off the exception list, fixes it until the stricter check passes, and opens a PR.
- Triggers: an automated review run. Once the exception list is empty, the ratchet run has nothing to take and the migration is done.

One small PR a day keeps human review cheap, and the check only ever gets stricter.

## Users report bugs nobody reads

A feedback button in the app is an issue source: it files each report as an issue with the explore label already on it. The explore run does the rest.

## Production problems are found late

A monitor (slow queries, error rates) is an issue source. It files an issue per problem, and comments on the open issue instead when it sees the same problem again. After a fix merges, it reopens the issue if the problem persists.

## The factory's own runs fail

**Fix task**
- Trigger: the orchestrator reports a failed run.
- Does: files the failing log as an issue, and attempts a fix as a PR when the failure is fixable.
- Triggers: an automated review run. A failure in a fix run's own work triggers nothing, so fixes never chain. Because the fix changes the factory itself, it always gets human review.

## The codebase drifts

**Architecture task**
- Trigger: a nightly clock.
- Does: scans recent changes for refactoring candidates and files them as one issue.
- Triggers: nothing. A human picks a candidate and labels it, which starts the usual chain.

## The same mistakes keep coming back

**Retro task**
- Trigger: a PR merges, throttled to one merged PR in ten.
- Does: reads the PR, its issue, its automated reviews and its run logs, and proposes changes to the factory's own instructions as a PR.
- Triggers: an automated review run.
