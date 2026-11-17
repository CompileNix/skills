# Dialogue discipline: questions for decisions, status as plain text

A chief-of-staff failure found during the 2026-11-17 validation run, and the fix that closed it.

## 2026-11-17

During the grilling cluster run, the orchestrator sent a blocking status checkpoint to the principal, offering "proceed as written" as the first option and "adjust something" as the second. The principal's answer of 2026-11-17: "a blocking question with nothing to decide parks the whole session on me; reserve questions for real decisions and report status as plain text instead."

The chief-of-staff skill text did not push the question; it said nothing at all about the dialogue between the orchestrator and the user. The gap was the silence: with no rule on when to ask versus when to report, the default slid toward asking, and asking is the expensive option, because a blocking question stops every in-flight subagent's worth of progress on the user's reply.

The fix, committed to `t3/cos-validation` on 2026-11-17, is a new `## Dialogue` section in `skills/engineering/chief-of-staff/SKILL.md` (commit 7b55a24): status is plain text (what moved, what is in flight, what is next), and a blocking question is reserved for a real decision, a fork where the user must choose.

The same rule governs this page's own session behaviour: the rest of the validation run reported status in plain text and asked nothing further without a fork.
