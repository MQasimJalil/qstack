---
name: qstack-minimize-reader-load
description: "Make maintenance easier by reducing the layers and mutable state a reader must trace."
---

# Minimize Reader Load

## Procedure

1. Pick a real maintenance question. Count the layers needed to trace the answer and list hidden or mutable values the reader must remember.
2. Collapse pass-through wrappers and prefer boundaries that hide meaningful decisions. Shrink state toward local values, derive instead of synchronizing, and name invariants at the boundary.
3. Check the revised path by tracing where the value originates and every way it can change. Keep an abstraction only when it lowers total reader load.

## Upstream sources

- Measure layers to trace and hidden state separately, then test how quickly a maintainer can trace ownership. [pstack/principle-minimize-reader-load](https://github.com/cursor/plugins/blob/bf0c7cd80abdbf7fe47b634978a7d1b4071f71a7/pstack/skills/principle-minimize-reader-load/SKILL.md#L9)
