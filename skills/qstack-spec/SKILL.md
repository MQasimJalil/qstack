---
name: qstack-spec
description: "Create a backlog-ready issue or epic grounded in current code and observable acceptance criteria."
---

# Spec

## Procedure

1. Establish the stakeholder problem, desired outcome, target repository, scope, and exclusions before drafting. Search for duplicates where filing or splitting work is in scope.
2. Read the actual code paths and record current behavior, source locations, API or schema details, and what should stay as it is. Use an inventory and ranked changes for an audit issue.
3. Draft the proposed change, dependencies and sequence, testable acceptance criteria, testing plan, and rollback. For an epic, map child issues and their dependency order.
4. Review the draft against source evidence. Remove secrets and internal content outside the intended audience before any external review, archival sync, or filing. Record review results and follow-up choices.
5. Deliver the finished draft or file the authorized issue, then archive its exact approved text and reference locally. Start implementation only when the user requested it.

## Upstream sources

- Why, scope, code interrogation, draft review, evidence gate, filing, and optional implementation handoff [gstack/spec](https://github.com/garrytan/gstack/blob/5dcd76b4eae6bb06f73460d3ab29cef8e33e8537/spec/SKILL.md#L224)
