# Upstream issue verdicts

- 2026-11-18: Read all six upstream issues read-only with `gh issue view <n> -R mattpocock/skills --comments`. Verdicts, one per issue, against the fork state at `CompileNix/skills@5266a96`:

| Upstream issue | Failure reported | Verdict |
| --- | --- | --- |
| mattpocock/skills#1430 | A round does not show which decisions are high-impact or how sure the recommendation is | Declined, see [decline-1430.md](decline-1430.md) |
| mattpocock/skills#1424 | "Word each question so yes accepts" steers rounds toward yes-only questions | Already addressed on the fork mainline, no change in this run |
| mattpocock/skills#1411 | End each round with a blank answer sheet | Fixed, issue 04 |
| mattpocock/skills#1406 | A partly answered round is treated as finished, unanswered questions come back renumbered | Fixed, issue 01 |
| mattpocock/skills#1402 | A confirmation that brings new facts is treated as the end of the session | Fixed, issue 03 |
| mattpocock/skills#1401 | A recommendation built on a pending fact gets retracted | Fixed, issue 02 |

- 2026-11-18: mattpocock/skills#1424 is already addressed because the fork mainline merged the lettered diverging options format, `CompileNix/skills@be92972`, on 2026-11-18 (merge `CompileNix/skills@5266a96`). Every question now carries its options and the reason the recommended option beats them, the user answers by number and letter, and a bare "yes" accepts every recommendation. What is left of that issue, the discipline of not asking points the agent can settle itself, is a question-count concern in tension with the skill's "nothing left silently assumed" rule, and it is not pursued in this run.
- 2026-11-18: mattpocock/skills#1401 carries a comment from adamslowe confirming repeated retracts after researchers report back, which settles it as a standing failure mode rather than a one-off.
