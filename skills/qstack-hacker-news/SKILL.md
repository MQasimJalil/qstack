---
name: qstack-hacker-news
description: "Collect the current Hacker News front page as structured story records."
---

# Hacker News

## Procedure

1. Open the public Hacker News front page with an available browser or HTTP tool.
2. Pair each story row with its own metadata. Resolve relative story links against the origin and preserve the displayed rank and title.
3. Return up to 30 records with rank, title, URL, points, and comment count. Use an explicit missing value when the page omits metadata and check that ranks are unique.

## Upstream sources

- Match headline rows to metadata and return story rank, title, URL, points, and comment count. [gstack/hackernews-frontpage](https://github.com/garrytan/gstack/blob/5dcd76b4eae6bb06f73460d3ab29cef8e33e8537/browser-skills/hackernews-frontpage/SKILL.md#L16)
