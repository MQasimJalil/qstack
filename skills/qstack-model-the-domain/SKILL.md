---
name: qstack-model-the-domain
description: "Represent stateful behavior in a domain structure that enforces shared invariants."
---

# Model The Domain

## Procedure

1. Identify legal states, transitions, and invariants before editing conditionals. Trace how callers read and change the data.
2. Choose a representation that naturally encodes those rules, such as a state machine, discriminated union, registry, or reducer. Group code by the facts it owns.
3. Remove now-redundant branches and checks. Prove the resulting state transitions at the boundary and keep simple code where the representation adds no value.

## Upstream sources

- Choose a state machine, union, registry, reducer, or matching collection to replace scattered branches. [pstack/principle-model-the-domain](https://github.com/cursor/plugins/blob/bf0c7cd80abdbf7fe47b634978a7d1b4071f71a7/pstack/skills/principle-model-the-domain/SKILL.md#L11)
