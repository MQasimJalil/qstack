---
name: qstack-typescript-practice
description: "Apply TypeScript’s types and runtime schemas to make legal variants explicit and verify observable behavior."
---

# Typescript Practice

## Procedure

1. Model variants with discriminants and exhaust their cases. Brand semantic primitives only after boundary validation, and prefer the simplest type that keeps operations total.
2. Accept untrusted inputs as unknown. Parse with the project’s schema library and derive the static type where possible. Narrow from discriminants or checked guards and use satisfies for shape conformance.
3. Keep object arguments self-documenting where useful, and use existing types or schema-derived projections before parallel interfaces. Use the project logger with diagnostic context.
4. Run observable-behavior tests through the framework’s real primitives and check browser-visible changes in a running app where applicable.

## Upstream sources

- Discriminated unions, runtime schemas, safe narrowing, exhaustive cases, and real tests. [pstack/typescript-best-practices](https://github.com/cursor/plugins/blob/bf0c7cd80abdbf7fe47b634978a7d1b4071f71a7/pstack/skills/typescript-best-practices/SKILL.md#L12)
