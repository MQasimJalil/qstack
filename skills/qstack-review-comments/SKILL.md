---
name: qstack-review-comments
description: "Audit comments and suppressions in a scoped change, removing noise and fixing the code that needs explanatory workarounds."
---

# Review Comments

## Procedure

1. Read the caller’s scope or current diff. Use a fresh reviewer when available or conduct a separate review pass focused solely on comments and suppressions.
2. Keep proof-worthy external constraints and explain their evidence. Flag comments that explain avoidable surprises, obsolete behavior, or correctness and safety suppressions. Verify ambiguous constraints against code or change history.
3. Remove accepted noise. Fix the smallest in-scope cause that makes a workaround necessary. When a constraint is real, encode it in a type, test, lint rule, or runtime check if authorized.
4. Validate any code change on its normal path. Report deletions, retained constraints and their evidence, implemented enforcements, and open items.

## Upstream sources

- Independent comment review, acceptance rules, narrow root-cause fixes, and verifiable constraints. [pstack/no-comments](https://github.com/cursor/plugins/blob/bf0c7cd80abdbf7fe47b634978a7d1b4071f71a7/pstack/skills/no-comments/SKILL.md#L13)
