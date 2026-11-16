---
name: qstack-configure-agents
description: "Map installed agent models and reasoning effort to workflow roles without assuming provider-specific defaults."
---

# Configure Agents

## Procedure

1. Find the model choices and effort levels the selected host exposes. Read existing project or user preferences when the user authorized that scope.
2. Map roles for implementation, harder reasoning, independent candidates and judging, swarm workers, and reflection. Scale effort to the chosen budget, preserving explicit family, list, and inherit choices.
3. Validate every explicit model against the detected capabilities. If selection is unavailable, use the current agent or the host’s supported default and explain the fallback.
4. Write the configuration only to the host and scope the user requested. Show the effective mapping, when it takes effect, and any unsupported role that will run serially.

## Upstream sources

- Detect available models, preserve user overrides, scale role budgets, and validate before writing host settings. [pstack/setup-pstack](https://github.com/cursor/plugins/blob/bf0c7cd80abdbf7fe47b634978a7d1b4071f71a7/pstack/skills/setup-pstack/SKILL.md#L28)
