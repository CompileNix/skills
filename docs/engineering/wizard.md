# wizard

## What it does

`wizard` generates an interactive bash script that walks a human, step by step, through a manual procedure: wiring up third-party services, running a one-off migration, moving a project from state A to state B. It opens each URL, says what to click and copy, captures what comes back, and writes it into `.env` files and GitHub Actions secrets.

The [agent](../ai-coding-terms.md#agent) writes the script; it never runs it. You do, on your own machine. A wizard is a program, not a list of instructions. The script runs each step in order and keeps the values you enter. Your part is to click, paste, and press Enter.

## When to reach for it

You can type `/wizard`, and the agent can also reach for it on its own. When it hits a step you have to take (a key it can't mint, a dashboard it can't click), it builds you a wizard instead of writing the instructions into the chat, where they scroll away.

Reach for it when the next thing blocking you is a trip through a dashboard:

| Situation | What the wizard does |
| --- | --- |
| A new dev needs six services configured before the app boots | Opens each dashboard in order, captures the keys, writes them to `.env` and CI |
| A one-off migration needs switches flipped in a specific order | Sequences the irreversible steps behind confirmation gates |
| A project has to move from state A to state B once | Walks the transition and reports what it could not do |
| You are about to write those steps into a README | Writes an executable version instead, which fails visibly when a step goes stale |

Don't reach for it to *decide* what to build; for that, [grill-with-docs](grill-with-docs.md) and [to-spec](to-spec.md) are the tools.

## Prerequisites

None to generate one. The wizard it writes runs on bash, and uses `gh` when a stage sets a GitHub secret or variable. If `gh` is missing or not authenticated, the run does not fail. That stage shows a warning, and the closing summary tells you what to set by hand.

## Stages

A **stage** is one focused task on one screen. The script clears the terminal between stages, so a stage that overflows the screen loses the part that scrolled away. You author stages in dependency order and set `TOTAL_STAGES`, which drives the progress display.

The [skill](../ai-coding-terms.md#skill) scopes the procedure before it writes any script. It reads the repo instead of asking cold: `.env*`, `docker-compose*`, framework config, and every `secrets.*` / `vars.*` reference in `.github/workflows/`. Each of those references is a value the wizard has to produce. It then shows you the ordered stage list to confirm. Only after you confirm does it map each stage to the exact path a human follows ("Dashboard → Developers → API keys → Reveal test key → copy"). Where it doesn't know the current UI, it asks you or checks the docs rather than inventing clicks.

For each captured value, scoping decides where it goes:

| Destination | When |
| --- | --- |
| `.env` only | Local dev needs it, CI doesn't |
| GitHub secret | CI reads it, and it's sensitive |
| GitHub variable | CI reads it, and it's public |
| Both `.env` and a secret | Local dev and CI both need it |
| Nowhere | The stage is a pure action: a switch flipped, a plan upgraded |

## The template already solves the UX

The [template](../../skills/engineering/wizard/template.sh) ships the whole experience: progress with time remaining, confirmation gates, cross-platform URL opening including WSL, hidden entry for secrets, idempotent `.env` upserts, `gh secret` / `gh variable` writes, and a closing summary of everything it had to skip. Everything above the `STAGES` marker is a fixed library, identical in every wizard and never hand-edited. Because the library never changes, every wizard behaves the same way. The only work per wizard is to scope the procedure and author its stages.

The agent that writes a wizard never runs it end to end, because the script opens browsers and waits for human input. The agent checks it statically instead: `bash -n`, `shellcheck` where available, and a trace that every value lands where scoping said it would, with every `set_secret` name matching a real `secrets.*` reference in CI. So the first run is yours, and that run is the test.

## Ephemeral by default

| What you have | What to do with the script |
| --- | --- |
| A one-off migration, a personal setup, a transition you'll never repeat | Save it to a scratch or `scripts/` path, run it, delete it |
| A setup path the next person on the repo will also need | Commit it and link it from the README, so they run the script instead of re-asking an agent |

## Common questions

**Do my API keys end up in the model's context?**

No. The agent writes a script; it doesn't run it. You run the script yourself, and it captures the key with hidden terminal entry and writes it straight to `.env` or `gh secret`. The wizard is a CLI, and the model is not connected to it. This holds only for values the wizard captures at runtime. If you paste a key into the chat while scoping the procedure, it's in the [context](../ai-coding-terms.md#context) like any other pasted text.

## It's working if

- You're shown an ordered list of stages, and the values each one produces, and asked to confirm, before any script exists.
- Every URL is opened before the value from that page is asked for. You're never asked to paste something you haven't been sent to fetch.
- Secrets are typed blind. Nothing sensitive echoes into your scrollback.
- Each stage fits one screen. Nothing you still need has scrolled away.
- Ctrl-C and re-run picks up where you left off, offering the values already saved as defaults.
- The final screen lists what it wrote, and separately lists what it couldn't do and you have to finish by hand.

## Where it fits

`wizard` is a reach-for-it-anytime standalone, sitting at the line where automation stops and a human has to click. Its nearest neighbour is [setup-skills](setup-skills.md), because both exist to get a repo into a working state. That one configures this skill set, and `wizard` generates a setup path for everything else. It also pairs with [implement](implement.md): when a build lands a feature that needs credentials or a manual cutover, a wizard covers the steps only a human can do. When you're unsure which skill fits the moment, [which-skill](which-skill.md) routes you.
