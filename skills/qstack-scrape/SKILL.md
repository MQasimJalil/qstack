---
name: qstack-scrape
description: "Extract requested fields from an authorized page through a bounded read-only flow."
---

# Scrape

## Requirements

- Authorized read access to the page and a browser tool when static retrieval is insufficient.

## Procedure

1. Identify the page, item boundaries, output schema and stop condition. Choose an authorized browser session and use rendered content as evidence.
2. Use DOM or accessibility structures and permitted navigation for pagination. Distinguish incomplete hydration from empty data and preserve source strings that carry meaning.
3. Deduplicate records and mark inaccessible fields and truncated coverage. Return structured output with source links and a reproducible read-only sequence when repeatability matters.

## Upstream sources

- Scope extraction to intended fields, avoid mutations and distinguish missing data. [gstack/scrape](https://github.com/garrytan/gstack/blob/5dcd76b4eae6bb06f73460d3ab29cef8e33e8537/scrape/SKILL.md#L270)
