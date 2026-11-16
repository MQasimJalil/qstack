---
name: qstack-browser-extractor-authoring
description: "Turn a successful read-only browser extraction into a tested reusable skill."
---

# Browser Extractor Authoring

## Requirements

- A previous successful extraction and an available browser or fixture test interface.

## Procedure

1. Identify the recent successful extraction, its site scope, input contract, returned fields and evidenced failure cases.
2. Stage the reusable procedure with stable selectors or semantic structures. Capture an authorized sanitized fixture and test success, missing data, allowed pagination and relevant markup drift.
3. Run the staged tests and replay the same read-only flow where necessary. Prove the skill works through its normal entry point, then install it in the requested scope.

## Upstream sources

- Require a proven scrape, representative fixture, tested script, and atomic installation. [gstack/skillify](https://github.com/garrytan/gstack/blob/5dcd76b4eae6bb06f73460d3ab29cef8e33e8537/skillify/SKILL.md#L122)
