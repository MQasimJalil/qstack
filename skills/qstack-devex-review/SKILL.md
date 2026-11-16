---
name: qstack-devex-review
description: "Exercise a live developer journey and compare observed friction with its plan."
---

# DevEx Review

## Requirements

- Use the project's supported developer environment and browser, CLI, or API tooling for the selected journey.

## Procedure

1. Identify the live target, the developer persona, and a comparable plan or previous baseline. Start from an appropriate clean environment and record prerequisites.
2. Follow the documented path through discovery, installation, first success, ordinary use, debugging, and upgrade. Test the CLI, SDK, or API that the persona actually uses and measure time to first useful result.
3. Trigger supported error cases. Record the message, exit or response code, recovery path, context, and whether a caller can act on the result without exposing secrets.
4. Audit docs, tooling, migration and deprecation guidance, and ecosystem touchpoints. Score each dimension against actual commands, logs, or screenshots and keep inaccessible paths marked untested.
5. Compare results with the plan's scores and assumptions. Report the biggest adoption blockers and link the smallest reproducible evidence for each.

## Upstream sources

- Evidence-based live DX scorecard and plan-to-reality comparison [gstack/devex-review](https://github.com/garrytan/gstack/blob/5dcd76b4eae6bb06f73460d3ab29cef8e33e8537/devex-review/SKILL.md#L639)
