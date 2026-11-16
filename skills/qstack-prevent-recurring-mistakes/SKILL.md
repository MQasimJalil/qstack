---
name: qstack-prevent-recurring-mistakes
description: "Find repeated repository mistakes and prevent them at the highest level the codebase can enforce."
---

# Prevent Recurring Mistakes

## Procedure

1. Gather examples from corrections, review comments, reverts, tests, commits, or instructions. Group repeated symptoms by the same root mistake and distinguish actual recurrence from a one-off.
2. Choose the highest effective enforcement. Remove the wrong path through architecture first, then use types, a targeted lint or CI check with a fix message, or observable-behavior tests.
3. Prove the guard rejects a real past mistake and passes a correct case. Prefer one focused change per class and make the check usable locally as well as in CI where applicable.
4. Keep a short map of durable rules and their enforcers. Delete redundant guidance after structural prevention. For judgment that cannot be encoded, keep a concrete example.
5. For an explicitly requested single correction, apply the same ladder using that correction as the specimen. Preserve scope and report a broader historical audit only when you ran one.

## Upstream sources

- Identify mistake classes from history and prove the selected enforcement catches a prior mistake. [pstack/correct](https://github.com/cursor/plugins/blob/bf0c7cd80abdbf7fe47b634978a7d1b4071f71a7/pstack/skills/correct/SKILL.md#L13)
- Turn repeated guidance into an enforced invariant and reserve prose for decisions requiring judgment. [pstack/principle-encode-lessons-in-structure](https://github.com/cursor/plugins/blob/bf0c7cd80abdbf7fe47b634978a7d1b4071f71a7/pstack/skills/principle-encode-lessons-in-structure/SKILL.md#L7)
