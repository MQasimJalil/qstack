---
name: qstack-build-a-lever
description: "Build a deterministic tool for nontrivial edits, analysis, generation, or verification."
---

# Build A Lever

## Procedure

1. Do one representative unit manually to learn the actual transformation or evidence contract.
2. Build the smallest rerunnable script, codemod, generator, or query that can perform or verify the work. Compare the first automated result to the manual baseline.
3. Run the tool across the remaining scope and retain its output or contract so another person can reproduce the result. Keep it with the work when it needs to outlive the session.

## Upstream sources

- Prove a small rerunnable tool against one manual unit and reuse it across the work. [pstack/principle-build-the-lever](https://github.com/cursor/plugins/blob/bf0c7cd80abdbf7fe47b634978a7d1b4071f71a7/pstack/skills/principle-build-the-lever/SKILL.md#L14)
