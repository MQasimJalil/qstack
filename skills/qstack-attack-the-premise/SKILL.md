---
name: qstack-attack-the-premise
description: "Test a shared assumption when multiple fixes failed the same gate."
---

# Attack The Premise

## Procedure

1. Write the single assertion every failed fix relied on.
2. Build a rerunnable observation that would produce different evidence if that assertion were false. Compare how failures are distributed as well as whether the gate is red.
3. Use the result to select the next repair. If the evidence contradicts the assertion, trace the mechanism it misses. If it supports the assertion, test the next upstream cause.

## Upstream sources

- Falsify the common premise before another repair and use the evidence to select the next cause. [pstack/principle-attack-the-premise](https://github.com/cursor/plugins/blob/bf0c7cd80abdbf7fe47b634978a7d1b4071f71a7/pstack/skills/principle-attack-the-premise/SKILL.md#L13)
