---
name: grilling
description: Grill the user relentlessly about a plan, decision, or idea. Use when the user wants to stress-test their thinking, or uses any 'grill' trigger phrases.
---

Interview the user relentlessly until you reach a shared understanding. Map this as a **design tree**: every decision branches into the decisions that hang off it.

Work the tree in **rounds**. The **frontier** is every decision whose prerequisites are already settled: the questions you can ask _now_ without guessing at answers you haven't heard yet. Ask the whole frontier in one round: number each question, offer its options, and recommend one. Then wait for the user's answers before the next round.

Format a round like so:

```
❓ **Q1** - **<question title>**: <question body, might be multiple paragraphs>
- **A.** <your recommended option>
- **B.** <a diverging option>
- **C.** <another diverging option, as many as the decision has>

➡️ A. <why A beats the others>

---

❓ **Q2** - **<question title>**: <question body, might be multiple paragraphs>
- **A.** <your recommended option>
- **B.** <a diverging option>

➡️ A. <why A beats the others>
```

Every question offers two or more **diverging** options, as many as the decision genuinely has: each a distinct path a reasonable person could defend, each named by where it leads. Option A is always your recommendation. Count the options by the decision's real branches: a reworded A ("Yes, but…") or a strawman is the same path twice, so cut it, and leave "something else" to the user's free-form answer. A decision with only two outcomes gets two options named by outcome ("Keep X: …" / "Drop X: …"). The user answers by number and letter ("1A, 2C"); a bare "yes" accepts every A in the round.

After the written round, put it to the user through your harness's question tool, if it has one, so they have an easy, interactive way to answer: one question per decision, each understandable without the written round, offering the same options in the same order, with A first and labelled "(Recommended)". Header: Q{Number} - {question title}; Body: {the question, understandable without the fully written one}. Where the tool caps the options per question, offer A and the strongest alternatives up to the cap; the written round still lists them all, and the user picks any other by typing its letter as a free-form answer. Where the tool limits the questions per call, split the round across calls. With no question tool, the written round stands alone.

Each round the user answers reshapes the tree: settled decisions push the frontier outward and unblock questions that depended on them. Recompute the frontier and ask the next round. A question whose answer depends on another question still open in this round belongs to a _later_ round, not this one.

Finding _facts_ is your job, never the user's. When a frontier question needs a fact from the environment (filesystem, tools, etc.), dispatch a sub-agent with a fresh context window to find it; don't ask the user for anything you could look up yourself. Don't block on it: a running exploration is an unsettled prerequisite, so only the questions downstream of it wait for the sub-agent to report; ask the rest of the frontier now. The _decisions_ are the user's: put each to them and wait.

The session is done when the frontier is empty: every branch of the design tree visited, nothing left silently assumed. Do not act on it until the user confirms you have reached a shared understanding.
