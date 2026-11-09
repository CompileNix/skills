# diagnosing-bugs

## What it does

`diagnosing-bugs` runs a six-phase diagnosis on a hard bug or a performance regression: build a repro, minimise it, rank hypotheses, instrument, fix with a regression test, clean up.

It will not let the agent form a theory until a **tight** feedback loop exists: one named command, already run once, that goes red on *this* bug and green when it is fixed. Given a bug report, a coding agent by default reads code and guesses. This skill blocks that. If no red-capable command exists, there is no Phase 2. That single gate is what the skill is for. Once the loop exists, everything after it (bisection, hypothesis-testing, instrumentation) is mechanical.

## When to reach for it

Type `/diagnosing-bugs`, or the agent reaches for it on its own when a task fits. It is model-invoked, and fires on "diagnose" or "debug this", or on a report that something is broken, throwing, failing, or slow.

Reach for it on the hard ones: a bug you can't solve at first look, an intermittent flake, a regression introduced between two known-good states. It is slow and thorough on purpose, so it is the wrong tool for a question you want answered in one message.

| Your situation | Where to go |
| --- | --- |
| A specific defect you can describe as a symptom | This skill |
| A slow endpoint or a timing regression with a known before-and-after | This skill. It has a performance branch (measure a baseline, then bisect) |
| "Where are the bottlenecks in this codebase?", no specific symptom | Not this skill. It diagnoses one known failure, it does not audit |
| A raw bug report from someone else, not yet confirmed or written up | [triage](triage.md) first |
| Throwaway code to answer a design question, not chase a defect | [prototype](prototype.md) |
| Building a planned behaviour test-first | [tdd](tdd.md) |
| Asking what would have prevented the bug, once it is fixed | [retro](retro.md), run in the same session |
| No good seam exists to lock the bug down | [improve-codebase-architecture](improve-codebase-architecture.md), which you start yourself |

## The tight loop is the skill

Phase 1 gets the most effort because it is the only hard phase. The skill lists ways to build the loop, roughly in order of preference:

1. A failing test at whatever seam reaches the bug.
2. A curl or HTTP script against a running dev server.
3. A CLI invocation with a fixture input, diffed against a known-good snapshot.
4. A headless browser script asserting on DOM, console, or network.
5. A replayed capture: a saved request, payload, or event log, run through the code path in isolation.
6. A throwaway harness: a minimal subset of the system, one function call.
7. A property or fuzz loop, for "sometimes wrong output".
8. A bisection harness you can hand to `git bisect run`.
9. A differential loop: same input, old version against new.
10. A [human-in-the-loop](../ai-coding-terms.md#human-in-the-loop) bash script, last resort. The skill ships `scripts/hitl-loop.template.sh` for this: the agent runs the script, you follow prompts in your terminal, and your answers come back as parseable output.

*A* loop is not the goal. **Tight** is: fast (seconds), deterministic (same verdict every run), sharp (asserts your exact symptom, not "didn't crash"), and runnable by the agent without you. A 30-second flaky loop is barely better than none. For a bug that only shows up sometimes, the target is not a clean repro but a **higher reproduction rate**: loop the trigger, parallelise, add stress, inject sleeps, until the flake rate is high enough to debug against.

When the agent cannot build one, the skill tells it to stop and say so, list what it tried, and ask you for [environment](../ai-coding-terms.md#environment) access, a captured artifact, or permission to add temporary instrumentation. It must not go on to form hypotheses anyway.

## The gates between phases

The phases are gates, not a checklist. The agent cannot enter a phase until a specific condition is true.

| Gate | What has to be true |
| --- | --- |
| Into Phase 2 | A named command, already run and pasted with its output, that can go red on this bug |
| Into Phase 3 | The repro is reproduced *and* minimised: every remaining element is needed to reproduce the bug |
| Into Phase 4 | 3–5 ranked, falsifiable hypotheses exist, each stating its prediction, shown to you before any is tested |
| Into Phase 5 | Probes map to a specific prediction, one variable at a time, every debug log has a tag like `[DEBUG-a4f2]`, so one grep finds them all for cleanup |
| Done | The original repro no longer reproduces, the instrumentation is gone, and the commit message names the hypothesis that turned out correct |

Phase 5 has one exception. The agent writes the regression test before the fix, but only if a **correct seam** exists for it: one where the test exercises the real bug pattern as it occurs at the call site. Where the only available seam is too shallow, the skill tells the agent to say so instead of writing a test that gives false confidence. The missing seam is itself a finding, and the agent records it instead of hiding it.

## Common questions

**My security scanner flagged this skill as high risk.**
Snyk flags it, and the flag is a false positive. It is the only skill in the set that ships an executable shell script (`hitl-loop.template.sh`) alongside instructions to run it and to curl a dev server. A shipped `.sh` file, instructions to run it, and outbound HTTP together are enough to trigger a static scanner. The script itself is about 30 lines of `read -r -p` prompts that pause for human input. The scanner rates what the skill could do, not a proven exploit.

## It's working if

- It shows you a command and its red output before it offers a single theory. If theory arrives first, the skill is not running.
- The failure it reproduces is the one you reported, not a nearby one it found on the way.
- It shrinks the repro before it starts guessing, and can tell you why it needs each remaining piece.
- It shows you a ranked list of 3–5 hypotheses, each with a prediction you could falsify, before it tests any of them.
- Every debug log it adds carries a tag like `[DEBUG-a4f2]`, and a grep for that tag comes back empty when it declares done.
- The commit or PR message names which hypothesis was right.
- When it cannot lock the bug down with a test, it says so instead of writing a shallow one.

## Where it fits

`diagnosing-bugs` is a reach-for-it-anytime standalone. You start it when something is broken, and it ends when the fix and its regression test are in. It keeps no state and needs no prior setup. [which-skill](which-skill.md) routes "Something's broken" here.

Two neighbours matter. [retro](retro.md) comes after it: once the fix is in, run it in the same session to ask what would have prevented the bug, while the session has more information than it had at the start. `diagnosing-bugs` never invokes `retro` itself, because `retro` is user-invoked. [triage](triage.md) comes before it for bugs that arrive as raw reports from other people, and does a shallower version of the same first two phases.
