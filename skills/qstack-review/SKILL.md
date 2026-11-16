---
name: qstack-review
description: Review a frozen implementation once against the agreed behavior and verification plan.
---

# Review

Read the paths that implement the acceptance behavior and the checks that observe it. Try the most plausible failure sequence, including stale results, wrong ordering, or missing observable side effects when relevant. Check that the test can reach the behavior and detect the wrong result.

Keep one finding per root cause. A blocker identifies the exact source location, a reachable sequence, and evidence that it breaks the agreed behavior. Use a failing observation or a precise trace through the supplied source. Label gaps and unconfirmed ideas as advisory. A clean review can have no findings.

For an explicitly independent or adversarial review, pass each reviewer the same frozen scope and intent when the host supports delegation. Combine their results into this review. Replay each claimed failure once and report the evidence and impact of each surviving finding.

Carry forward completed checks and the witness from the model run. Review their coverage and correspondence to the executable behavior. Leave live execution to verification and keep the planned assertions intact.
