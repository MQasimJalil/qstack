---
name: qstack-explain-code
description: "Explain how a subsystem works, how a request flows through it, or where a change belongs."
---

# Explain Code

## Procedure

1. State the scope you inferred from the question. Find the relevant entry point, data owner, layers, and callers in the repository.
2. Follow one representative request or state transition through the actual code. Show where inputs cross boundaries and where observable effects are produced.
3. Explain the responsibilities and navigation landmarks with source links. For a placement question, use the current ownership and data flow to justify the recommended layer.

## Upstream sources

- Read-only architectural exploration that provides a working mental model. [pstack/how](https://github.com/cursor/plugins/blob/bf0c7cd80abdbf7fe47b634978a7d1b4071f71a7/pstack/skills/how/SKILL.md#L13)
