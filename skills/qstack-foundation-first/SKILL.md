---
name: qstack-foundation-first
description: "Choose types, data structures, and prerequisite scaffolding before downstream implementation."
---

# Foundation First

## Procedure

1. Define the core data shape and trace dominant read and write patterns before introducing logic. Group shared decisions into a coherent abstraction.
2. Identify mutable objects that concurrent actors would otherwise share and isolate their ownership where practical.
3. Remove dead scaffolding, then land the test harness, checks, and shared types that every later phase needs. Keep each increment small and directly verifiable.

## Upstream sources

- Data-shape-first design, explicit access patterns, isolation, and prerequisite scaffolding. [pstack/principle-foundational-thinking](https://github.com/cursor/plugins/blob/bf0c7cd80abdbf7fe47b634978a7d1b4071f71a7/pstack/skills/principle-foundational-thinking/SKILL.md#L11)
