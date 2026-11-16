---
name: qstack-create-formal-verification
description: "Author a reusable formal verification skill for a high-cost correctness property and prove that the check detects a fault."
---

# Create Formal Verification

## Procedure

1. Choose a correctness promise whose failure has a meaningful cost and is hard to reach with examples. Identify its code boundary and observable failure.
2. Select the lowest-cost technique that answers the question. Use TLC and qstack-model for event ordering, a proof assistant or solver-backed tool when relevant to the implementation, or generated runtime cases when a formal model would lose the behavior being checked.
3. Map each model assumption, atomic action, or bounded input to live code. Record scope, bounds, version, and revision in a reusable command and its project-local skill.
4. Run the check against the protected input and a small, deliberately broken control. Keep the failing witness and clean result. Verify that the protected input remains intact and link the evidence.
5. Explain the bounded property in project terms, document what must trigger the check again, and hand off to qstack-maintain-formal-verification when implementation or assumptions change.

## Upstream sources

- Choose the verification technique from the correctness question and keep a reproducible proof tied to the implementation. [pstack/create-formal-verification-skill](https://github.com/cursor/plugins/blob/bf0c7cd80abdbf7fe47b634978a7d1b4071f71a7/pstack/skills/create-formal-verification-skill/SKILL.md#L17)
