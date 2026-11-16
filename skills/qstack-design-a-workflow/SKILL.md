---
name: qstack-design-a-workflow
description: "Design and execute an auditable playbook for substantial work that has no narrower workflow."
---

# Design A Workflow

## Procedure

1. Ground a falsifiable done predicate in the real product. Estimate work and blockers, then size the evidence gates to reversibility, blast radius, and unknowns.
2. Sequence independently verifiable units. Resolve the riskiest unknown early, capture a pre-change baseline, and build the scaffold or verification harness that later phases need.
3. For every unit, record the hypothesis, smallest change, actual gate output, and keep-or-discard decision. Run the gate before advancing. Delegate only separable work with independent write targets.
4. Record decisions and links as each unit lands. Check the final product against the original predicate and state whether it is verified, failed, or inconclusive.
5. Expose decisions only the user can make. Show the chosen workflow, tradeoffs, decision trail, final evidence, and remaining work.

## Upstream sources

- Falsifiable done criteria, risk-adjusted gates, hypothesis loop, and an audit trail. [pstack/figure-it-out](https://github.com/cursor/plugins/blob/bf0c7cd80abdbf7fe47b634978a7d1b4071f71a7/pstack/skills/figure-it-out/SKILL.md#L15)
