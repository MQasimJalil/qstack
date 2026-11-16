---
name: qstack-test-behavior
description: "Design or evaluate a test against the observable contract it is meant to protect."
---

# Test Behavior

## Procedure

1. Name the observer and its entry point, then state the exact return value, error, readable state, or externally observable side effect the contract promises.
2. Choose a concrete input and derive the expectation from the requirement. Drive the interface the observer uses and assert the promised result at that boundary.
3. Check that the test would fail if the behavior broke and pass if internals changed while the same contract held. Replace assertions that trace a private implementation detail.
4. For interactions with an external collaborator, verify the observable request or effect. Include a positive case when it is needed to show the observer can detect an otherwise forbidden interaction.

## Upstream sources

- The behavior-break and implementation-refactor checks for durable tests [pstack/principle-test-behavior-not-implementation](https://github.com/cursor/plugins/blob/bf0c7cd80abdbf7fe47b634978a7d1b4071f71a7/pstack/skills/principle-test-behavior-not-implementation/SKILL.md#L7)
