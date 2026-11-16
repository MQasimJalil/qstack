---
name: qstack-create-verification-skill
description: "Author a project-local skill that drives the real app and preserves verification evidence."
---

# Create Verification Skill

## Procedure

1. Inspect the real product surfaces and supported local entry points. Establish launch prerequisites, how to verify readiness, safe test data, and the isolation available.
2. Write a project-local skill with exact launch and read-only diagnosis steps, stable driving handles for the available tool, observable success signals, artifact locations, and cleanup instructions.
3. Add a feature map of high-value user journeys. For each, describe how the user reaches it, how to drive it, what outcome and side effects to observe, and where it can fail.
4. Run one mapped journey end to end from launch through cleanup. Confirm the captured actions and outcomes survive cleanup and record any setup differences from the real target.

## Upstream sources

- Portable launch, diagnosis, driving, evidence, feature map, and cleanup contract [pstack/create-verification-skill](https://github.com/cursor/plugins/blob/bf0c7cd80abdbf7fe47b634978a7d1b4071f71a7/pstack/skills/create-verification-skill/SKILL.md#L23)
