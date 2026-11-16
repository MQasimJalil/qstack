"""Validate the upstream inventory and render the portable suite and Graphify audit."""

import argparse
import json
import re
import subprocess
from collections import Counter
from pathlib import Path
from posixpath import normpath
from urllib.parse import quote, unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "catalog"
SOURCE_MAPS = ("core", "product", "operations", "engineering")
UPSTREAM = {
    "gstack": ("garrytan/gstack", ":(glob)**/SKILL.md"),
    "pstack": ("cursor/plugins", ":(glob)pstack/**/SKILL.md"),
}
DOCUMENTED_LINKS = (
    ("gstack/review/SKILL.md", "pstack/pstack/skills/interrogate/SKILL.md", 132),
    ("gstack/benchmark/SKILL.md", "pstack/pstack/skills/benchmark-checklist/SKILL.md", 139),
    ("gstack/plan-eng-review/SKILL.md", "pstack/pstack/skills/architect/SKILL.md", 140),
    ("gstack/ship/SKILL.md", "pstack/pstack/skills/blast-radius/SKILL.md", 142),
    ("gstack/context-restore/SKILL.md", "pstack/pstack/skills/recall/SKILL.md", 143),
)
MARKDOWN_LINK = re.compile(r"\[[^\]\n]+\]\(<?([^\s)>]+)>?")
SKILL_ID = re.compile(r"qstack(?:-[a-z0-9]+)*")


def require(condition, message):
    if not condition:
        raise ValueError(message)


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def git(repo, *args):
    return subprocess.check_output(["git", "-C", str(ROOT / repo), *args], text=True, encoding="utf-8")


def snapshot():
    revisions = {repo: git(repo, "rev-parse", "HEAD").strip() for repo in UPSTREAM}
    files = {}
    for repo, (_, pathspec) in UPSTREAM.items():
        require(not git(repo, "diff", "--name-only", "HEAD", "--", pathspec).strip(),
                f"Tracked {repo} skill documents differ from the pinned commit.")
        for name in git(repo, "ls-files", "-z", pathspec).rstrip("\0").split("\0"):
            path = f"{repo}/{name}"
            source = (ROOT / path).read_text(encoding="utf-8")
            match = re.search(r"(?m)^name:\s*([^\n]+)", source)
            require(match, f"No skill frontmatter name in {path}.")
            files[path] = {"lines": source.splitlines(), "name": match[1].strip("\"' ")}
    return revisions, files


def source_record(row, state, target, files, revisions):
    path, line, contribution = (row[key] for key in ("path", "line", "take"))
    require(path in files, f"Untracked source path in {state} decision: {path}")
    require(isinstance(line, int) and 1 <= line <= len(files[path]["lines"]), f"Invalid source line {path}:{line}")
    require(files[path]["lines"][line - 1].strip(), f"Source anchor is blank: {path}:{line}")
    require(isinstance(contribution, str) and contribution.strip(), f"Missing contribution for {path}:{line}")
    repo, relative = path.split("/", 1)
    mode = row.get("mode")
    require(mode is None or isinstance(mode, str) and mode.strip(), f"Invalid invocation mode: {path}")
    namespace = UPSTREAM[repo][0]
    url = f"https://github.com/{namespace}/blob/{revisions[repo]}/{quote(relative)}#L{line}"
    return {
        "path": path, "line": line, "take": contribution, "status": state, "target": target,
        "repo": repo, "name": files[path]["name"], "url": url, **({"mode": mode} if mode else {}),
    }


def inventory(revisions, files):
    items = sorted((item for name in SOURCE_MAPS for item in read_json(CATALOG / f"{name}.json")),
                   key=lambda item: item["id"])
    ids = [item["id"] for item in items]
    require(len(set(ids)) == len(ids), "Duplicate canonical qstack skill IDs.")
    records = {}

    def add(row, state, target=None):
        require(row["path"] not in records, f"Duplicate source decision for {row['path']}")
        require(target is None or target in ids, f"Unknown target skill {target} for {row['path']}")
        record = source_record(row, state, target, files, revisions)
        records[row["path"]] = record
        return record

    for item in items:
        skill = item["id"]
        require(SKILL_ID.fullmatch(skill), f"Invalid canonical name {skill}")
        require(item["category"] and item["description"], f"Missing category or description for {skill}")
        require(item["sources"], f"No upstream source for {skill}")
        if not item.get("manual"):
            require(isinstance(item.get("steps"), list) and len(item["steps"]) >= 3
                    and all(isinstance(step, str) and step.strip() for step in item["steps"]),
                    f"{skill} needs an actionable procedure.")
        status = "merged" if len(item["sources"]) > 1 else "retained"
        item["sources"] = [add(row, status, skill) for row in item["sources"]]

    editions = read_json(CATALOG / "editions.json")
    for row in editions["editions"]:
        add(row, "host edition", row["target"])
    for row in editions["fixtures"]:
        add(row, "test fixture")
    missing = set(files) - set(records)
    require(not missing, "Missing decisions for:\n" + "\n".join(sorted(missing)))
    return items, records


def skill_markdown(item):
    skill = item["id"]
    title = " ".join({"qa": "QA", "ios": "iOS", "devex": "DevEx", "pdf": "PDF", "dx": "DX"}.get(word, word.title())
                     for word in skill.removeprefix("qstack-").split("-"))
    frontmatter = json.dumps(item["description"], ensure_ascii=False)
    lines = ["---", f"name: {skill}", f"description: {frontmatter}", "---", "", f"# {title}"]
    requirements = item.get("requirements", [])
    if requirements:
        lines.extend(["", "## Requirements", "", *[f"- {text}" for text in requirements]])
    lines.extend(["", "## Procedure", "", *[f"{index}. {step}" for index, step in enumerate(item["steps"], 1)]])
    lines.extend(["", "## Upstream sources", ""])
    for source in item["sources"]:
        lines.append(f"- {source['take']} [{source['repo']}/{source['name']}]({source['url']})")
    return "\n".join(lines) + "\n"


def catalogue_markdown(items, records, revisions):
    counts = Counter(row["repo"] for row in records.values())
    decisions = Counter(row["status"] for row in records.values())
    merges = sum(len(item["sources"]) > 1 for item in items)
    out = [
        "# Qstack skill catalog", "",
        f"Qstack ships **{len(items)} skills**. The inventory accounts for **{len(records)} tracked skill documents** "
        f"across gstack ({counts['gstack']}) and pstack ({counts['pstack']}).",
        "",
        f"The source review produced **{merges} merged workflows** from {decisions['merged']} primary source skills "
        f"and retained {decisions['retained']} distinct source skills. "
        f"It mapped {decisions['host edition']} host editions to portable workflows and excluded "
        f"{decisions['test fixture']} test fixtures.", "",
        "- gstack `" + revisions["gstack"] + "`",
        "- pstack `" + revisions["pstack"] + "`",
        "", "Use `qstack skills [search]` to discover a skill and `qstack skill <name>` to read it.",
        "", "## Installed skills", "",
        "| Skill | Category | Purpose |",
        "| --- | --- | --- |",
        *[f"| [`{item['id']}`](../skills/{item['id']}/SKILL.md) | {item['category']} | {item['description']} |"
          for item in items],
        "", "## Every source decision", "",
        "| Source | Decision | Qstack skill | Retained behavior or reason |",
        "| --- | --- | --- | --- |",
    ]
    for path, row in sorted(records.items()):
        target = f"[`{row['target']}`](../skills/{row['target']}/SKILL.md)" if row["target"] else "—"
        out.append(f"| [{path}]({row['url']}) | {row['status']} | {target} | {row['take']} |")
    return "\n".join(out) + "\n"


def output_files(items, records, revisions):
    for item in items:
        path = ROOT / "skills" / item["id"] / "SKILL.md"
        if item.get("manual"):
            text = path.read_text(encoding="utf-8")
            require(re.search(rf"(?m)^name: {re.escape(item['id'])}$", text), f"Invalid manual skill {path}")
        else:
            yield path, skill_markdown(item)

    index = {
        "revisions": revisions,
        "skills": [{key: item[key] for key in ("id", "category", "description")} for item in items],
        "sources": list(sorted(records.values(), key=lambda row: row["path"])),
    }
    yield CATALOG / "index.json", json.dumps(index, indent=2, ensure_ascii=False) + "\n"
    yield ROOT / "docs/catalog.md", catalogue_markdown(items, records, revisions)
    for repo, source in {"gstack": "gstack/LICENSE", "pstack": "pstack/pstack/LICENSE"}.items():
        yield ROOT / "docs/licenses" / f"{repo}.txt", (ROOT / source).read_text(encoding="utf-8")


def render_files(items, records, revisions, check):
    for path, content in output_files(items, records, revisions):
        if check:
            require(path.is_file() and path.read_text(encoding="utf-8") == content,
                    f"Missing or stale catalog output: {path.relative_to(ROOT)}")
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8", newline="\n")
    skill_paths = list((ROOT / "skills").glob("*/SKILL.md"))
    installed = {path.parent.name for path in skill_paths}
    require(installed == {item["id"] for item in items}, "Installed skill folders and catalog do not match.")
    for path in skill_paths:
        body = path.read_text(encoding="utf-8").split("## Upstream sources", 1)[0]
        unknown = set(re.findall(r"\bqstack-[a-z0-9-]+\b", body)) - installed
        require(not unknown, f"{path.parent.name} references unknown skills: {', '.join(sorted(unknown))}")


def extraction(items, records, files):
    nodes = []
    links = {}
    by_id = {}

    def node(key, label, path, line, category, **extra):
        identifier = re.sub(r"[^a-z0-9]+", "_", key.lower()).strip("_")
        require(identifier not in by_id.values(), f"Graph ID collision for {key}")
        nodes.append({"id": identifier, "label": label, "file_type": "document", "source_file": path,
                      "source_location": f"L{line}", "category": category, **extra})
        by_id[key] = identifier

    def edge(source, target, relation, path, line, evidence, confidence="EXTRACTED"):
        if source == target:
            return
        pair = (by_id[source], by_id[target])
        existing = links.get(pair)
        if existing:
            existing.setdefault("additional_evidence", []).append(
                {"relation": relation, "source_file": path, "source_location": f"L{line}", "evidence": evidence})
            return
        links[pair] = {
            "source": pair[0], "target": pair[1], "relation": relation, "confidence": confidence,
            "confidence_score": 1.0 if confidence == "EXTRACTED" else 0.85, "weight": 1.0,
            "source_file": path, "source_location": f"L{line}", "rationale": evidence,
        }

    categories = {item["id"]: item["category"] for item in items}
    for item in items:
        skill = item["id"]
        node(skill, skill, f"skills/{skill}/SKILL.md", 2, item["category"])
    for path, row in records.items():
        label = f"{row['repo']}:{row['name']}"
        if row["status"] == "host edition":
            label += " (" + Path(path).parent.parent.name + " edition)"
        node(path, label, path, row["line"], categories.get(row["target"], "test fixtures"),
             disposition=row["status"], source_url=row["url"], canonical=row["target"])
        if row["target"]:
            relation = "edition_of" if row["status"] == "host edition" else "consolidated_into"
            edge(path, row["target"], relation, path, row["line"], row["take"])

    for source, target, line in DOCUMENTED_LINKS:
        evidence = (ROOT / "gstack/NOTICE.md").read_text(encoding="utf-8").splitlines()[line - 1]
        edge(source, target, "influenced_by", "gstack/NOTICE.md", line, evidence)
    for path, source in files.items():
        destinations = set()
        for number, text in enumerate(source["lines"], 1):
            for link in MARKDOWN_LINK.findall(text):
                parsed = urlsplit(link)
                if parsed.scheme or parsed.netloc or not parsed.path:
                    continue
                target = normpath(Path(path).parent.as_posix() + "/" + unquote(parsed.path))
                if target in records and target not in destinations:
                    edge(path, target, "references", path, number, text.strip())
                    destinations.add(target)

    for item in items:
        target = item["id"]
        first, *others = item["sources"]
        for row in others:
            edge(first["path"], row["path"], "overlaps_in_workflow", row["path"], row["line"],
                 f"Shared workflow in {target}. Distinct contribution: {row['take']}", "INFERRED")
        if target != "qstack":
            edge("qstack", target, "routes_to", "skills/qstack/SKILL.md", 8, "Published in the qstack skill index.")
        skill_path = f"skills/{target}/SKILL.md"
        body = (ROOT / skill_path).read_text(encoding="utf-8").split("## Upstream sources", 1)[0]
        for number, text in enumerate(body.splitlines(), 1):
            for mentioned in sorted(set(re.findall(r"\bqstack-[a-z0-9-]+\b", text)) & categories.keys()):
                edge(target, mentioned, "references", skill_path, number, text.strip())

    for source, key, label, path, starts in [
        ("qstack-model", "tlc", "TLC model checker", "qstack.py", "TLC_URL ="),
        ("qstack-verify", "bombadil", "Bombadil browser check", "qstack.py", "BOMBADIL ="),
    ]:
        line = next(number for number, text in enumerate((ROOT / path).read_text(encoding="utf-8").splitlines(), 1)
                    if text.startswith(starts))
        node(key, label, path, line, "verification")
        edge(source, key, "invokes_tool", path, line, "Executable qstack pilot integration.")
    return {"nodes": nodes, "edges": list(links.values()), "hyperedges": []}


def write_graph(items, records, files, revisions):
    from graphify.analyze import god_nodes, suggest_questions, surprising_connections
    from graphify.build import build_from_json
    from graphify.cluster import cluster, score_all
    from graphify.diagnostics import diagnose_extraction
    from graphify.export import to_html, to_json
    from graphify.report import generate

    extracted = extraction(items, records, files)
    diagnostics = diagnose_extraction(extracted, directed=True, root=ROOT)
    for field in ("dangling_endpoint_edges", "missing_endpoint_edges", "self_loop_edges",
                  "directed_same_endpoint_collapsed_edges"):
        require(not diagnostics.get(field), f"Graphify extraction diagnostic {field}: {diagnostics[field]}")
    graph = build_from_json(extracted, directed=True, root=ROOT)
    require(graph.number_of_nodes() == len(extracted["nodes"]), "Graphify dropped an inventory node.")
    require(graph.number_of_edges() == len(extracted["edges"]), "Graphify dropped an inventory edge.")
    mapped = [(graph.nodes[a]["source_file"], graph.nodes[b]["label"])
              for a, b, data in graph.edges(data=True) if data["relation"] in ("consolidated_into", "edition_of")]
    require(Counter(mapped) == Counter((path, row["target"]) for path, row in records.items() if row["target"]),
            "Graphify routes do not match the source decisions.")
    groups = cluster(graph)
    labels = {}
    for key, members in groups.items():
        category = Counter(graph.nodes[n]["category"] for n in members).most_common(1)[0][0]
        labels[key] = category.title() + " Skills" if len(members) > 1 else graph.nodes[members[0]]["label"]
    output = ROOT / "graphify-out" / "consolidation"
    output.mkdir(parents=True, exist_ok=True)
    to_json(graph, groups, str(output / "graph.json"), community_labels=labels, force=True)
    to_html(graph, groups, str(output / "graph.html"), labels)
    detection = {"total_files": len(files) + len(items), "total_words": sum(len(" ".join(doc["lines"]).split())
                                                                              for doc in files.values()),
                 "files": {"document": list(files), "code": [], "paper": [], "image": [], "video": []},
                 "needs_graph": True}
    report = generate(graph, groups, score_all(graph, groups), labels, god_nodes(graph),
                      surprising_connections(graph, groups), detection, {"input": 0, "output": 0}, str(ROOT),
                      suggested_questions=suggest_questions(graph, groups, labels))
    summary = (
        f"# Consolidation validation\n\n{len(files)} tracked input documents were accounted for. "
        f"All {len(mapped)} installable or edition routes match the pinned inventory. "
        f"Graphify retained {graph.number_of_nodes()} nodes and {graph.number_of_edges()} directed edges.\n\n"
        "EXTRACTED edges represent manifest decisions, source links, or executable integrations. "
        "INFERRED edges represent editorial workflow overlap. "
        "The graph validates coverage and links. Behavioral verification uses the packaged pilot. "
        "Graph export uses no measured LLM tokens. Human and agent reading for the audit is outside this counter.\n\n"
        "[Complete source decisions](../../docs/catalog.md)\n\n"
    )
    (output / "GRAPH_REPORT.md").write_text(summary + report, encoding="utf-8")
    (output / "validation.json").write_text(json.dumps({
        "revisions": revisions, "sources": len(files), "mapped": len(mapped), "skills": len(items),
        "nodes": graph.number_of_nodes(), "edges": graph.number_of_edges(),
        "diagnostics": {key: value for key, value in diagnostics.items() if isinstance(value, (int, str, float, bool))},
    }, indent=2) + "\n", encoding="utf-8")
    print(f"Graphify validated {len(mapped)} routes, {graph.number_of_nodes()} nodes, {graph.number_of_edges()} edges.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="check the generated output without updating it")
    parser.add_argument("--graph", action="store_true", help="render and validate the dedicated Graphify graph")
    args = parser.parse_args()
    revisions, files = snapshot()
    items, records = inventory(revisions, files)
    render_files(items, records, revisions, args.check)
    print(f"{len(files)} upstream documents -> {len(items)} installable skills.")
    if args.graph:
        write_graph(items, records, files, revisions)


if __name__ == "__main__":
    main()
