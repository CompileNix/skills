# tdd

## What it does

`tdd` builds a feature or fixes a bug test-first: one failing test, then just enough code to pass it, then the next behaviour. It carries the standards that make that loop produce tests worth keeping: what a good test is, where tests go, what mocks are for, and the three anti-patterns that make a suite worthless.

It writes no test at a seam you have not agreed to first. Before any test exists, it names the public boundaries it intends to test at and stops for your confirmation. Testing effort is finite, and this step spends it on the critical paths instead of on every edge case. `tdd` is also a **reference**, not a driver. It contains the rules of the loop, and something else (you, or [implement](implement.md)) runs the [session](../ai-coding-terms.md#session) that applies them.

## When to reach for it

Type `/tdd`, or the [agent](../ai-coding-terms.md#agent) reaches for it automatically when a task fits: building a feature or fixing a bug test-first, or when you say "red-green-refactor".

Reach for it when there is a concrete behaviour to build, with an input and an observable output, and you want tests that survive a refactor.

| Your situation | Where to go |
| --- | --- |
| A behaviour with defined inputs and outputs (business logic, a request/response contract, a transformation, validation) | `tdd` |
| The behaviour isn't pinned down yet | [to-spec](to-spec.md), which also agrees the test seams before any code is written |
| The question is really the shape of the interface, not the tests | [codebase-design](codebase-design.md) |
| You have a [spec](../ai-coding-terms.md#spec) or [issues](../ai-coding-terms.md#issue) and want the whole build run for you | [implement](implement.md), which drives `tdd` per issue |
| Config, wiring, glue, type annotations, straight CRUD delegation | Nothing here fits well; see the open gap below |

That last row is a real gap. The skill decides *where* the seams go, but nothing in it decides *whether* a change is worth the loop at all. If you run it on a change with no independent source of truth to assert against, you get a test that restates the implementation. That is the tautological anti-pattern the skill warns about, reached from the other direction. You make that call yourself, or write the rule into your `CLAUDE.md`.

## Prerequisites

[codebase-design](codebase-design.md) needs to be installed. `tdd` uses its interface-design vocabulary. Nothing else; the skill is [stateless](../ai-coding-terms.md#stateless) and writes no files of its own.

## The loop, and the seam it runs at

The skill rests on three terms.

**Red-green.** Write the failing test, then only enough code to pass it. Do not write code for the test after next. There is no refactor phase. The skill dropped it in June 2026 because agents almost never performed it, and because review and implementation work better as separate sessions. Refactoring belongs to [code-review](code-review.md).

**Vertical slice.** Write one test at one seam, then the minimal implementation, then repeat. The first cycle is a **tracer bullet** that proves a single path end to end. The opposite is horizontal slicing: all the tests first, then all the code. Tests written in bulk verify *imagined* behaviour. They check the shape of things rather than what a user does, and they commit you to a test structure before you understand the implementation.

**Pre-agreed seam.** A seam is the public boundary you observe behaviour at without reaching inside. The rule has no exceptions. No test goes at an unconfirmed seam. In the full chain the seams are agreed earlier, during [to-spec](to-spec.md): "`/tdd` is told to only work at pre-agreed test seams, `/code-review` checks that only agreed-upon test seams were used." Invoked on its own, `tdd` asks you directly.

The three anti-patterns it is written to prevent:

| Anti-pattern | The tell |
| --- | --- |
| Implementation-coupled | The test breaks when you rename an internal function, though behaviour did not change. Mocked internal collaborators, asserted call counts, database queries used to verify instead of the interface. |
| Tautological | The expected value is computed the way the code computes it, so the test passes by construction. Expected values have to come from somewhere else: a known-good literal, a worked example, the spec. |
| Horizontal slicing | A batch of tests landed before any implementation. |

Mocks are for system boundaries only: external APIs, time, randomness, sometimes the filesystem or the database. Never mock your own modules.

## It's working if

- It stops and names the seams it intends to test at, and waits, before any test file exists.
- One test appears, goes red, gets just enough code to pass, and only then does the next test appear, not a batch of tests followed by a batch of code.
- Test names read as capabilities ("user can checkout with valid cart"), not as internals ("checkout calls paymentService.process").
- Expected values in assertions are literals you can trace to the spec, not values recomputed the way the code computes them.
- Renaming an internal function breaks nothing in the suite.
- Mocks appear only at external boundaries (the payment API, the clock) and never around your own modules.

## Where it fits

`tdd` runs inside the build step of the main chain; it is not a step of its own:

```txt
grill-with-docs → to-spec → to-issue → implement → code-review → retro
```

[to-spec](to-spec.md) agrees the test seams up front, [implement](implement.md) drives `tdd` per issue, and [code-review](code-review.md) checks afterwards that only the agreed seams were used, and owns the refactoring `tdd` no longer does. Its other neighbour is [codebase-design](codebase-design.md), the shared source of the seam and deep-module vocabulary that `tdd` uses. You can also reach for it on its own, whenever there is a concrete behaviour to build and no full spec in play. When you are unsure which skill fits your situation, [which-skill](which-skill.md) routes you.
