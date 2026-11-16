---
name: qstack-sequence-verifiable-units
description: "Arrange a sweep, migration, or delivery into independently verifiable units."
---

# Sequence Verifiable Units

## Procedure

1. Choose a known baseline and split work into units with one meaningful change and an exact verification command for each.
2. Run each gate before advancing. Repair or isolate a failing unit before building on it and retain the before-and-after result.
3. Order authorized commits or PRs so the evidence reads naturally, such as failure, then fix, or baseline, then treatment. Ensure the final sequence proves the intended outcome.

## Upstream sources

- Use known-good brackets and order delivery so a reviewer can replay the evidence. [pstack/principle-sequence-verifiable-units](https://github.com/cursor/plugins/blob/bf0c7cd80abdbf7fe47b634978a7d1b4071f71a7/pstack/skills/principle-sequence-verifiable-units/SKILL.md#L13)
