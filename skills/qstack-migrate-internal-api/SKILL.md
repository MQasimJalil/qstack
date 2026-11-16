---
name: qstack-migrate-internal-api
description: "Move all internal consumers to a replacement API and remove the old interface in the same coordinated change."
---

# Migrate Internal Api

## Procedure

1. Confirm the old interface is internal and the affected consumers can migrate together. Inventory callers and tests that pin the old behavior.
2. Move every consumer to the new contract and adjust its behavior checks. Remove obsolete implementation-only tests and delete the old entry point once its callers are gone.
3. Search for stale callers and run checks through the new public entry points. Preserve the compatibility contract if external users still depend on the prior API.

## Upstream sources

- Coordinated internal migration with new-contract tests and explicit compatibility preconditions. [pstack/principle-migrate-callers-then-delete-legacy-apis](https://github.com/cursor/plugins/blob/bf0c7cd80abdbf7fe47b634978a7d1b4071f71a7/pstack/skills/principle-migrate-callers-then-delete-legacy-apis/SKILL.md#L11)
