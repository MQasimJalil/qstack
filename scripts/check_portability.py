"""Exercise installed non-pilot skills through qstack's real agent transports."""

import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

FIXTURE = """import argparse
import json
from pathlib import Path

parser = argparse.ArgumentParser()
commands = parser.add_subparsers(dest="command", required=True)
orders = commands.add_parser("orders")
orders.add_argument("--format", choices=["json"], required=True)
snapshot = commands.add_parser("snapshot", help="Write a JSON workspace snapshot")
snapshot.add_argument("--output", type=Path, required=True)
bench = commands.add_parser("benchmark")
bench.add_argument("variant", choices=["baseline", "candidate"])
candidate = commands.add_parser("candidate")
candidate.add_argument("variant", choices=["alpha", "beta"])
args = parser.parse_args()

if args.command == "orders":
    print(json.dumps({"orders": ["Q-101"]}))
elif args.command == "snapshot":
    args.output.write_text(json.dumps({"status": "ready", "records": 2}), encoding="utf-8")
elif args.command == "benchmark":
    readings = {
        "baseline": {"duration_ms": [101, 102, 100], "completed": 1000, "errors": 0},
        "candidate": {"duration_ms": [79, 80, 81], "completed": 850, "errors": 150},
    }
    print(json.dumps(readings[args.variant]))
elif args.command == "candidate":
    rows = ["beta", "Alpha", "alpha", "Beta", "aardvark"]
    print(json.dumps(sorted(rows, key=str.casefold) if args.variant == "beta" else sorted(rows)))
"""


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def command_output(command, cwd):
    return subprocess.check_output(command, cwd=cwd, text=True, encoding="utf-8", timeout=30)


def skill_text(runtime, name):
    return command_output(["node", str(runtime / "bin/qstack.cjs"), "skill", name], runtime)


def static_checks(runtime):
    index = json.loads((runtime / "catalog/index.json").read_text(encoding="utf-8"))
    ids = {item["id"] for item in index["skills"]}
    installed = {item.parent.name for item in (runtime / "skills").glob("*/SKILL.md")}
    assert ids == installed and len(ids) == len(index["skills"])
    host_only = re.compile(r"AskUserQuestion|TodoWrite|~[/\\]\.(?:claude|cursor)|\$(?:CLAUDE|CURSOR)_")
    for slug in ids:
        content = (runtime / "skills" / slug / "SKILL.md").read_text(encoding="utf-8")
        assert re.search(rf"(?m)^name: {re.escape(slug)}$", content), slug
        body = content.split("## Upstream sources", 1)[0]
        assert not host_only.search(body), slug
        assert not (set(re.findall(r"\bqstack-[a-z0-9-]+\b", body)) - ids), slug
    modes = [row for row in index["sources"] if row.get("mode")]
    for row in modes:
        exported = skill_text(runtime, row["path"])
        assert f"\n## Invocation mode\n\n{row['mode']}" in exported, row["path"]
        assert exported.startswith(skill_text(runtime, row["target"])), row["path"]
    return len(ids), len(modes)


def fixtures(root):
    fixture = root / "fixture_app.py"
    fixture.write_text(FIXTURE, encoding="utf-8")

    def run(*args):
        return command_output([sys.executable, str(fixture), *args], root)

    write_json(root / "orders.json", json.loads(run("orders", "--format", "json")))
    write_json(root / "benchmark.json", {
        name: json.loads(run("benchmark", name)) for name in ("baseline", "candidate")
    })
    (root / "snapshot-help.txt").write_text(run("snapshot", "--help"), encoding="utf-8")
    write_json(root / "candidates.json", {
        name: json.loads(run("candidate", name)) for name in ("alpha", "beta")
    })
    prior, head = (hashlib.sha256(data).hexdigest()[:12] for data in (b"old fixture", b"new fixture"))
    write_json(root / "release.json", {"head": head, "required": ["check"], "receipt": {"head": prior, "check": "pass"}})
    write_json(root / "checkpoint.json", {"ref": "feature/export", "saved_head": prior, "head": head,
                                          "verified": "snapshot fixture launched", "session_history": "unavailable"})
    for name in ("src", "src-old"):
        (root / name).mkdir()
    write_json(root / "paths.json", {"allowed": str(root / "src"), "proposed": str(root / "src-old" / "index.js"),
                                    "guard_hook": "unavailable"})
    return fixture, head


CASES = {
    "qa": ("gstack:qa-only", "orders.json",
           "Assess the CLI export against the contract that Q-101 and Q-102 must both appear. Apply the exported skill's mode. "
           'Return mode, edit_checkout (boolean), expected_count, actual_count, missing_order, and evidence (the filename).'),
    "benchmark": ("pstack:benchmark-checklist", "benchmark.json",
                  "A teammate claims the candidate is faster based on these recorded runs. Assess the claim. "
                  'Return comparable (boolean), claim_supported (boolean), baseline_completed, candidate_completed, and reason.'),
    "docs": ("qstack-document-generate", "snapshot-help.txt",
             "Write succinct instructions for a teammate who needs to create report.json from fixture_app.py. "
             'Return kind (tutorial, how-to, reference, or explanation), argv (the arguments after the script name), and markdown.'),
    "ship": ("qstack-ship", "release.json",
             "The request is a read-only ship readiness review. No forge or branch write is allowed. "
             'Return ready, rerun_check, mutate_branch, and publish (all booleans), and reason.'),
    "context": ("gstack:context-restore", "checkpoint.json",
                "Restore the recorded work state with a single available agent and no transcript access. "
                'Return mode, head (current head), drift (boolean), session_history, and next_action.'),
    "guardrails": ("gstack:freeze", "paths.json",
                   "Apply the named mode to the proposed edit. The only available permission tool is advisory. "
                   'Return mode (freeze, warn, release), enforcement (advisory or enforced), and outside_edit_allowed (boolean).'),
    "arena": ("pstack:arena", "candidates.json",
              "Choose a baseline for a stable case-insensitive sort. The two outputs came from separate implementations; "
              "your host has one context, no delegation and no independent judge. "
              'Return base (alpha or beta), independent_judgment (boolean), and reason.'),
}


def build_prompt(runtime, root):
    sections = [
        "Apply the seven installed qstack skills below to independent local fixture cases. "
        "Use only the supplied skill and observed evidence. No tools, checkout edits, or external actions are needed. "
        "Return one JSON object keyed by the seven case names. Each case value is an object with the requested fields. "
        "Preserve the selected invocation mode and distinguish actual evidence from a proposed command.",
    ]
    for case, (skill, evidence, task) in CASES.items():
        observed = (root / evidence).read_text(encoding="utf-8")
        sections.append(f"## Case {case}\n\n{skill_text(runtime, skill)}\n\n"
                        f"Task: {task}\n\nEvidence {evidence}:\n{observed}")
    return "\n\n".join(sections)


def check_cases(reply, root, fixture, head):
    expected = {
        "qa": {"mode": "report", "edit_checkout": False, "expected_count": 2, "actual_count": 1,
               "missing_order": "Q-102", "evidence": "orders.json"},
        "benchmark": {"comparable": False, "claim_supported": False, "baseline_completed": 1000,
                      "candidate_completed": 850},
        "docs": {"kind": "how-to", "argv": ["snapshot", "--output", "report.json"]},
        "ship": {"ready": False, "rerun_check": True, "mutate_branch": False, "publish": False},
        "context": {"mode": "restore", "head": head, "drift": True, "session_history": "unavailable"},
        "guardrails": {"mode": "freeze", "enforcement": "advisory", "outside_edit_allowed": False},
        "arena": {"base": "beta", "independent_judgment": False},
    }
    notes = {"benchmark": "reason", "docs": "markdown", "ship": "reason", "context": "next_action", "arena": "reason"}
    outcomes = {}
    for case, shape in expected.items():
        actual = reply.get(case)
        if not isinstance(actual, dict):
            outcomes[case] = {"passed": False, "problems": ["missing result object"]}
            continue
        problems = [f"{key}: expected {expected!r}, got {actual.get(key)!r}"
                    for key, expected in shape.items()
                    if type(actual.get(key)) is not type(expected) or actual.get(key) != expected]
        note = notes.get(case)
        if note and (not isinstance(actual.get(note), str) or not actual[note].strip()):
            problems.append(f"Missing {note}.")
        if case == "docs" and not problems:
            markdown = actual["markdown"]
            if "fixture_app.py snapshot --output report.json" not in markdown:
                problems.append("The instructions omit the verified command.")
            else:
                artifact = root / "report.json"
                subprocess.run([sys.executable, str(fixture), *actual["argv"]], cwd=root, timeout=30, check=True)
                if json.loads(artifact.read_text(encoding="utf-8")) != {"status": "ready", "records": 2}:
                    problems.append("The generated instructions lead to the wrong output.")
                (root / "snapshot-how-to.md").write_text(markdown, encoding="utf-8")
        outcomes[case] = {"passed": not problems, "problems": problems}
    return outcomes


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--runtime", type=Path, default=ROOT)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--agent", choices=("codex", "claude", "bridge", "command"), required=True)
    parser.add_argument("--agent-command", type=json.loads)
    parser.add_argument("--model")
    parser.add_argument("--timeout", type=int)
    args = parser.parse_args()
    if (args.agent == "command") != bool(args.agent_command):
        parser.error("--agent command requires --agent-command JSON argv")
    runtime = args.runtime.resolve()
    sys.path.insert(0, str(runtime))
    from qstack_workflow import AgentTransport

    root = args.out.resolve()
    root.mkdir(parents=True)
    count, modes = static_checks(runtime)
    fixture, head = fixtures(root)
    transport = AgentTransport(args.agent, args.agent_command, args.model, args.timeout)
    result = {"agent": args.agent, "catalog_skills": count, "alias_modes": modes, "status": "running",
              "scenarios": list(CASES)}
    path = root / "result.json"
    write_json(path, result)
    try:
        reply = transport.request(root, "portability", build_prompt(runtime, root))
        outcomes = check_cases(reply, root, fixture, head)
        passed = sum(record["passed"] for record in outcomes.values())
        result.update(status="passed" if passed == len(CASES) else "failed", passed=passed, cases=outcomes)
        print(f"{args.agent}: {passed}/{len(CASES)} representative workflows passed.")
    except (RuntimeError, OSError, subprocess.SubprocessError, ValueError) as error:
        result.update(status="incomplete", error=str(error))
        print(f"{args.agent}: {error}", file=sys.stderr)
    write_json(path, result)
    return 0 if result["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
