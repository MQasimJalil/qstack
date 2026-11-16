---
name: qstack-plan-tune
description: "Review or change consented preferences about when an agent asks for planning decisions."
---

# Plan Tune

## Procedure

1. Interpret what the user wants to inspect or change and check the project's consent state before collecting or examining decision history.
2. Show declared preferences, inferred signals, and gaps between them. Include relevant question history and samples of automatic decisions so the user can inspect the rationale.
3. For edits, identify the exact question or decision type and update its preference. Preserve distinctions between always ask, decide when enough context exists, and a default recommendation.
4. When asked to distill history, propose specific changes with evidence from recent decisions. Keep them as proposals until adopted and distinguish explicit preferences from inferred patterns.

## Upstream sources

- Optional question tuning, declared and inferred profile review, and manual distillation [gstack/plan-tune](https://github.com/garrytan/gstack/blob/5dcd76b4eae6bb06f73460d3ab29cef8e33e8537/plan-tune/SKILL.md#L104)
