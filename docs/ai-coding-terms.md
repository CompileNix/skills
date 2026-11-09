# AI coding terms

Shared vocabulary for the skills and their docs pages. Repo-specific terms live in [GLOSSARY.md](../GLOSSARY.md).

### Agent

A model running in a loop with tools, taking actions toward a goal until it finishes or needs input.

### Agent mode

The harness setting that lets the agent act on its own judgement. Plan mode is the opposite: the agent produces a plan and holds off on changes.

### AFK

Away from keyboard. Work that runs without a human watching, because nothing in it waits on a person.

### AGENTS.md

A file at a repo's root that agents load at the start of every session. `CLAUDE.md` plays the same part in Claude Code.

### Automated check

A verification that runs without judgement and fails loudly: a lint rule, a type, a test, a pre-commit hook, a CI job.

### Clearing

Emptying the context window so the next prompt starts from nothing. Unlike compaction, nothing carries over.

### Compaction

Replacing the conversation in the context window with a summary of it, so a session can continue with more room.

### Context

Everything the model can see on a given turn: instructions, conversation, file contents and tool results.

### Context pointer

A reference to where information lives (a path, an issue, a commit) given in place of the information itself, so the reader loads it only when needed.

### Context window

The limited amount of context a model can hold at once, measured in tokens.

### Effort

The setting that controls how much reasoning a model spends before it answers.

### Environment

Everything around the agent that shapes its work: the repo, its tooling and checks, and the steering files it reads.

### Grilling

An interview in which the agent questions you about a plan, branch by branch, until you share one understanding of it.

### Harness

The program that runs the agent loop and supplies its tools, permissions and context. Claude Code and Codex are harnesses.

### Human review

A person reading a change before it is relied on, as opposed to an automated check or an agent's own review.

### Human-in-the-loop

Work where the agent stops for a person's input or approval at defined points.

### Issue

A single tracked unit of work in an issue tracker, sized to be picked up on its own. See [GLOSSARY.md](../GLOSSARY.md).

### MCP

Model Context Protocol, an open standard for connecting tools and data sources to a harness.

### Memory system

A store that carries facts between sessions and loads them back into context later.

### Model

The LLM itself, as distinct from the harness that runs it and the agent the two form together.

### Parametric knowledge

What a model absorbed in training and recalls without looking it up. It can be stale or wrong, and it carries no citation.

### Primary source

The original record of something: the code, the official docs, the conversation as it happened.

### Progressive disclosure

Showing a reader only what it needs now, with pointers to the detail, so the rest costs nothing until it is wanted.

### Prototyping

Building throwaway code to answer one design question that talking can't settle.

### Secondary source

A summary or interpretation of a primary source. Each step away from the original can lose detail or introduce error.

### Session

One continuous conversation with an agent, from its first prompt until it is cleared or closed.

### Skill

A packaged set of instructions an agent can load for a particular kind of task, either on demand or when the task fits.

### Smart zone

The part of the context window, up to roughly 150k tokens on current models, where a model still reasons sharply. Past it lies the dumb zone, where quality falls off.

### Spec

A document recording what a piece of work should achieve and the decisions that fix it. It is the destination; issues are the steps there.

### Stateful

Keeping information across sessions, usually in files. A stateful skill reads what earlier runs left behind.

### Stateless

Keeping nothing between runs. Each invocation starts from only what it is given.

### Subagent

An agent started by another agent to do a scoped job in its own context window, reporting back when done.

### Token

The unit a model reads and writes text in, roughly three quarters of an English word. Context windows and costs are measured in tokens.

### Tool

An action a harness exposes to the model, such as reading a file or running a command.

### Tool call

One request from the model to run a tool, with the result returned into context.

### Turn

One exchange in a session: a prompt, plus everything the agent does before it hands control back.

### Vibe coding

Accepting AI-generated code without reading or understanding it, steering only by whether the result seems to work.
