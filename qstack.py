"""One entry point to plan, run, and inspect qstack's verification workflow."""

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
import urllib.request
import uuid
from contextlib import contextmanager
from html import escape
from pathlib import Path

from pilot.preview import ACTIONS, PILOT_STEPS, Scenario, page, serve
from qstack_workflow import Workflow, write_json


ROOT = Path(__file__).resolve().parent
PILOT = ROOT / "pilot"
SKILLS = ROOT / "skills"
TLC_FILENAME = "tla2tools-1.7.4.jar"
TLC_URL = "https://github.com/tlaplus/tlaplus/releases/download/v1.7.4/tla2tools.jar"
TLC_SHA256 = "936a262061c914694dfd669a543be24573c45d5aa0ff20a8b96b23d01e050e88"
BOMBADIL = "antithesishq/bombadil:0.7.10@sha256:66c6793da1b54ec3ff8e64935bf9bc9d4e6c30a3db2c768ef0a777d69b982a80"
PREVIEW_IMAGE = "python:3.12-slim-bookworm"
MODEL_PROPERTY = "StaleCompletionCannotChangeStatus"
BROWSER_PROPERTY = "staleCompletionCannotReplaceRetry"
ORIGIN = "http://127.0.0.1:8080"


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def find_java(override):
    candidates = [
        override,
        Path(os.environ["JAVA_HOME"]) / "bin" / ("java.exe" if os.name == "nt" else "java")
        if os.environ.get("JAVA_HOME") else None,
        shutil.which("java"),
        Path(os.environ.get("ProgramFiles", "C:/Program Files")) / "Android/Android Studio/jbr/bin/java.exe"
        if os.name == "nt" else None,
    ]
    for candidate in candidates:
        if candidate and Path(candidate).is_file():
            return str(candidate)
    raise RuntimeError("Java was unavailable. Put it on PATH, set JAVA_HOME, or pass --java.")


def ensure_tlc(jar):
    def check_hash(path):
        require(hashlib.sha256(path.read_bytes()).hexdigest() == TLC_SHA256,
                f"TLC 1.7.4 checksum did not match for {path}")

    if jar.exists():
        check_hash(jar)
        return
    jar.parent.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(dir=jar.parent) as staging:
        download = Path(staging) / jar.name
        print("Fetching pstack's pinned TLC release.", flush=True)
        with urllib.request.urlopen(TLC_URL, timeout=45) as response, download.open("wb") as target:
            shutil.copyfileobj(response, target)
        check_hash(download)
        download.replace(jar)


def logged(command, path, *, cwd=ROOT, timeout=90):
    with path.open("wb") as out:
        return subprocess.run(command, cwd=cwd, stdout=out, stderr=subprocess.STDOUT, timeout=timeout).returncode


def run_model(java, jar, folder, *, faulty):
    label = "faulty" if faulty else "fixed"
    log = folder / f"tlc-{label}.log"
    code = logged([java, "-XX:+UseParallelGC", "-cp", str(jar), "tlc2.TLC",
                   "-workers", "1", "-metadir", str(folder / f"states-{label}"),
                   "-config", f"{label.title()}.cfg", "CancelRetry.tla"], log, cwd=folder / "model")
    output = log.read_text(encoding="utf-8", errors="replace")
    if faulty:
        require(code == 12 and f"Invariant {MODEL_PROPERTY} is violated." in output,
                f"TLC did not report the expected invariant violation (exit {code}). See {log}")
    else:
        require(code == 0 and "No error has been found." in output,
                f"TLC did not complete the fixed model (exit {code}). See {log}")
    states = re.search(r"([0-9,]+) distinct states found", output)
    return {"exit": code, "distinctStates": int(states[1].replace(",", "")) if states else None}, output


def extract_witness(tlc_output):
    states = []
    for block in re.split(r"^State \d+:.*\n", tlc_output, flags=re.M)[1:]:
        event = re.search(r'^/\\ event = "([a-z-]+)"$', block, re.M)
        status = re.search(r'^/\\ status = "([a-z-]+)"$', block, re.M)
        attempt = re.search(r"^/\\ attempt = (\d+)$", block, re.M)
        require(event and status and attempt, "A TLC counterexample state is missing event, status, or attempt.")
        states.append({"action": event[1], "status": status[1], "attempt": int(attempt[1])})
    steps = [state["action"] for state in states[1:]] + ["refresh"]
    require(bool(states) and states[0]["action"] == "start" and tuple(steps) == PILOT_STEPS,
            f"TLC returned a different counterexample. Review the TLC log. Browser steps: {steps}")
    return {"property": MODEL_PROPERTY, "source": "tlc-faulty.log", "modelStates": states, "steps": steps}


def mount(source, target, *, readonly=False):
    return ["--mount", f"type=bind,source={source},target={target}" + (",readonly" if readonly else "")]


@contextmanager
def docker_preview(case, source, *, faulty):
    command = [
        "docker", "run", "--detach", "--rm", "--network", "none",
        *mount(source, "/pilot", readonly=True), *mount(case, "/artifacts"),
        PREVIEW_IMAGE, "python", "-B", "/pilot/preview.py", "--port", "8080",
        "--handoff", "/artifacts/handoff.json", "--journal", "/artifacts/events.json",
    ]
    if faulty:
        command.append("--faulty")
    result = subprocess.run(command, capture_output=True, text=True, timeout=60)
    require(result.returncode == 0, f"Could not start the Docker preview. {result.stderr.strip()}")
    container = result.stdout.strip()
    probe = ["docker", "exec", container, "python", "-c",
             f"import urllib.request; urllib.request.urlopen('{ORIGIN}/health', timeout=1).read()"]
    try:
        for _ in range(20):
            if subprocess.run(probe, capture_output=True, timeout=5).returncode == 0:
                break
            time.sleep(0.25)
        else:
            record = subprocess.run(["docker", "logs", container], capture_output=True, text=True, timeout=10)
            raise RuntimeError(f"Preview did not become ready. {record.stderr.strip()}")
        yield container
    finally:
        subprocess.run(["docker", "stop", "-t", "1", container], capture_output=True, timeout=15)


def read_browser_trace(case, *, faulty):
    trace = case / "trace" / "trace.jsonl"
    states = [json.loads(line) for line in trace.read_text(encoding="utf-8").splitlines() if line.strip()]
    violations = [item for state in states for item in state["violations"]]
    if faulty:
        require(BROWSER_PROPERTY in json.dumps(violations),
                f"Bombadil did not capture the stale completion violation. See {trace}")
    else:
        require(not violations, f"Bombadil reported a violation in the protected preview. See {trace}")

    def observed(state, expected):
        return any(snapshot["name"] == "preview" and snapshot["value"] == expected
                   for snapshot in state["snapshots"])

    before = {"staleDelivered": False, "refreshed": False, "attempt": "2", "status": "Succeeded"}
    after = dict(before, staleDelivered=True, status="Failed" if faulty else "Succeeded")
    before_index = next((i for i, state in enumerate(states) if observed(state, before)), -1)
    after_index = next((i for i, state in enumerate(states) if observed(state, after)), -1)
    require(0 <= before_index < after_index,
            f"Bombadil did not observe retry success before and the expected result after the late callback. See {trace}")
    expected = dict(after, refreshed=True)
    # The last matching frame gives Chromium's screencast time to show the DOM
    # that the property extractor already observed.
    for state in reversed(states):
        if observed(state, expected):
            screenshot = case / "trace" / "screenshots" / Path(state["state"]["screenshot"]).name
            require(screenshot.is_file(), f"Missing browser screenshot {screenshot}")
            return len(states), expected, screenshot.relative_to(case).as_posix()
    raise RuntimeError(f"Bombadil never observed the expected browser state. See {trace}")


def run_browser(root, handoff, *, faulty):
    case = root / ("faulty-browser" if faulty else "fixed-browser")
    case.mkdir()
    write_json(case / "handoff.json", handoff)
    log = case / "bombadil.log"
    container_name = f"qstack-bombadil-{uuid.uuid4().hex[:12]}"
    source = root / "browser-input"
    with docker_preview(case, source, faulty=faulty) as app:
        try:
            code = logged(["docker", "run", "--rm", "--name", container_name, "--network", f"container:{app}",
                           "--shm-size", "256m", *mount(source, "/pilot", readonly=True), *mount(case, "/artifacts"),
                           BOMBADIL, "browser", "test", "--headless", "--no-sandbox", "--time-limit=12s",
                           "--output-path", "/artifacts/trace",
                           ORIGIN, "/pilot/browser.ts"], log, timeout=75)
        except (subprocess.TimeoutExpired, KeyboardInterrupt):
            subprocess.run(["docker", "rm", "-f", container_name], capture_output=True, timeout=15)
            raise
    expected = 2 if faulty else 0
    require(code == expected, f"Bombadil returned {code}, expected {expected}. See {log}")
    state_count, observation, screenshot = read_browser_trace(case, faulty=faulty)
    journal = case / "events.json"
    require(journal.exists(), f"Bombadil did not drive the preview. See {log}")
    events = json.loads(journal.read_text(encoding="utf-8"))
    observed_steps = [event["action"] for event in events]
    require(observed_steps == handoff["steps"],
            f"Bombadil stopped on a different action sequence. See {journal}")
    require(events[-1]["attempt"] == 2 and events[-1]["status"] == ("failed" if faulty else "succeeded"),
            f"The browser did not reach the expected final attempt and status. See {journal}")
    return {"exit": code, "observedStates": state_count, "observation": observation,
            "events": events, "screenshot": screenshot}


def report(root, handoff, result, workflow):
    model_states = {state["action"]: state for state in handoff["modelStates"]}
    broken_events = {e["action"]: e for e in result["faultyBrowser"]["events"]}
    fixed_events = {e["action"]: e for e in result["fixedBrowser"]["events"]}

    def status(state):
        return f"Attempt {state['attempt']} · {state['status'].title()}" if state else "—"

    rows = "".join(
        f"<tr><td>{ACTIONS[action]}</td><td>{status(model_states.get(action))}</td>"
        f"<td>{status(broken_events.get(action))}</td><td>{status(fixed_events.get(action))}</td></tr>"
        for action in handoff["steps"]
    )
    captures = "".join(
        f'<figure><img src="{folder}/{escape(result[case]["screenshot"], quote=True)}" '
        f'alt="{title}" loading="lazy"><figcaption>{title}</figcaption></figure>'
        for folder, case, title in [
            ("faulty-browser", "faultyBrowser", "Fault injected · retry still failed after refresh"),
            ("fixed-browser", "fixedBrowser", "Protected · retry success survived refresh"),
        ]
    )
    stylesheet = (PILOT / "style.css").read_text(encoding="utf-8")
    workflow_section = ""
    if workflow:
        plan = json.loads((root / "plan.json").read_text(encoding="utf-8"))
        review = json.loads((root / "review.json").read_text(encoding="utf-8"))
        workflow_section = f"""
  <section class="panel"><h2>Plan and review</h2>
    <p>{escape(plan["behavior"])}</p>
    <p>{escape(review["summary"])}</p>
    <p class="files"><a href="plan.json">Plan and selected checks</a>
    <a href="review.json">Review findings</a> <a href="workflow.json">Workflow receipt</a></p>
  </section>"""
    body = f"""
<main>
  <header><p class="tag">QSTACK / VERIFICATION</p><span class="mode">TLC + Bombadil</span></header>
  <h1>Cancel and retry</h1>
  <p class="lead">TLC found an ordering that lets a late failure overwrite a successful retry.
  Bombadil ran that sequence in Chromium against both versions of the preview.</p>
  {workflow_section}
  <div class="two-up">
    <section class="panel"><h2>TLC model check</h2>
      <p class="caught">Faulty model violated its invariant.</p>
      <p class="pass">Protected model passed across {result['fixedModel']['distinctStates']} reachable states.</p>
    </section>
    <section class="panel"><h2>Bombadil browser check</h2>
      <p class="caught">Faulty preview violated its UI property.</p>
      <p class="pass">Protected preview showed attempt 2 as succeeded after refresh.</p>
    </section>
  </div>
  <section class="panel"><h2>From counterexample to browser</h2>
    <table><thead><tr><th scope="col">Action</th><th scope="col">Faulty model</th>
    <th scope="col">Faulty preview</th><th scope="col">Protected preview</th></tr></thead>
    <tbody>{rows}</tbody></table>
  </section>
  <section class="panel"><h2>Browser captures</h2><div class="two-up">{captures}</div></section>
  <section class="panel"><h2>Run evidence</h2><p class="files">
    <a href="handoff.json">TLC witness and browser steps</a>
    <a href="tlc-faulty.log">Faulty TLC log</a><a href="tlc-fixed.log">Protected TLC log</a>
    <a href="faulty-browser/bombadil.log">Faulty Bombadil log</a>
    <a href="fixed-browser/bombadil.log">Protected Bombadil log</a>
    <a href="faulty-browser/trace/trace.jsonl">Faulty browser trace</a>
    <a href="fixed-browser/trace/trace.jsonl">Protected browser trace</a>
    <a href="result.json">Run results</a>
  </p></section>
</main>"""
    (root / "report.html").write_text(page("Cancel and retry evidence · qstack", body, f"<style>{stylesheet}</style>"),
                                      encoding="utf-8")


def pilot(args):
    workspace = Path.cwd()
    parent = workspace / "qstack-runs"
    if args.out:
        root = args.out.resolve()
        root.mkdir(parents=True, exist_ok=False)
    else:
        parent.mkdir(exist_ok=True)
        root = Path(tempfile.mkdtemp(prefix="cancel-retry-", dir=parent))
    print(f"Evidence directory: {root}", flush=True)
    inputs = {}
    for dirname, filenames in [
        ("model", ("CancelRetry.tla", "Fixed.cfg", "Faulty.cfg")),
        ("browser-input", ("preview.py", "style.css", "browser.ts")),
    ]:
        (root / dirname).mkdir()
        for filename in filenames:
            path = root / dirname / filename
            shutil.copy2(PILOT / filename, path)
            inputs[path.relative_to(root).as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()

    workflow = Workflow(root, SKILLS, args, inputs) if args.command == "run" else None
    try:
        run_pilot(args, root, inputs, workflow)
    except (Exception, KeyboardInterrupt) as error:
        if workflow:
            workflow.fail(error)
        raise


def run_pilot(args, root, inputs, workflow):
    if workflow:
        workflow.plan()
    java = find_java(args.java)
    jar = args.tlc_jar.resolve() if args.tlc_jar else Path.cwd() / ".qstack-tools" / TLC_FILENAME
    require(not args.tlc_jar or jar.is_file(), f"The selected TLC jar does not exist: {jar}")
    ensure_tlc(jar)
    broken_model, counterexample = run_model(java, jar, root, faulty=True)
    fixed_model, _ = run_model(java, jar, root, faulty=False)
    handoff = extract_witness(counterexample)
    write_json(root / "handoff.json", handoff)
    print(f"TLC caught the fault and checked {fixed_model['distinctStates']} states in the fixed model.", flush=True)
    print("Browser handoff: " + " -> ".join(handoff["steps"]), flush=True)
    if workflow:
        workflow.complete("model", "tlc-fixed.log", "tlc-faulty.log", "handoff.json")
        preview = root / "browser-input" / "preview.py"
        compile(preview.read_bytes(), str(preview), "exec")
        write_json(root / "build.json", {"pythonSyntax": "passed", "inputs": inputs,
                                        "browserSpecCompilation": "runs inside Bombadil"})
        workflow.complete("build", "build.json")
        workflow.review(handoff)
        workflow.verify_inputs()
    broken_browser = run_browser(root, handoff, faulty=True)
    print("Bombadil caught the same defect in Chromium.", flush=True)
    fixed_browser = run_browser(root, handoff, faulty=False)
    result = {"faultyModel": broken_model, "fixedModel": fixed_model, "faultyBrowser": broken_browser,
              "fixedBrowser": fixed_browser, "inputs": inputs, "tlcJarSha256": TLC_SHA256, "bombadilImage": BOMBADIL}
    write_json(root / "result.json", result)
    report(root, handoff, result, workflow)
    if workflow:
        workflow.complete("verify", "result.json", "report.html", "faulty-browser/trace/trace.jsonl",
                          "fixed-browser/trace/trace.jsonl")
        workflow.finish()
    print("Bombadil confirmed attempt 2 still succeeded after refresh.", flush=True)
    print(f"Report: {root / 'report.html'}", flush=True)


def parse_agent_command(raw):
    try:
        argv = json.loads(raw)
    except ValueError as error:
        raise argparse.ArgumentTypeError("Expected a JSON array of command arguments.") from error
    if (not isinstance(argv, list) or not argv or any(not isinstance(token, str) for token in argv)
            or not argv[0].strip()):
        raise argparse.ArgumentTypeError("Expected a nonempty JSON array using an executable and string arguments.")
    return argv


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("plan", help="show the synthesized qstack method")
    runner = commands.add_parser("run", help="run the complete qstack workflow on the pilot")
    adapters = runner.add_mutually_exclusive_group()
    adapters.add_argument("--agent", choices=("codex", "claude", "bridge"), default="codex",
                          help="agent for planning and review (default: codex)")
    adapters.add_argument("--agent-command", type=parse_agent_command,
                          help="JSON argv for an agent that reads the request on stdin and writes its JSON reply")
    runner.add_argument("--model", help="override the Codex or Claude Code model")
    checks = commands.add_parser("pilot", help="run only the deterministic TLC and Bombadil checks")
    for command in (runner, checks):
        command.add_argument("--java", type=Path)
        command.add_argument("--tlc-jar", type=Path, help="use a local copy of the pinned TLC jar")
        command.add_argument("--out", type=Path, help="new directory for run evidence")
    preview = commands.add_parser("preview", help="open the pilot for manual interaction")
    preview.add_argument("--port", type=int, default=8765)
    preview.add_argument("--faulty", action="store_true")
    args = parser.parse_args()
    if args.command == "run" and args.model and (args.agent_command or args.agent == "bridge"):
        parser.error("--model applies to the Codex and Claude Code adapters")
    try:
        if args.command == "plan":
            print((SKILLS / "qstack" / "SKILL.md").read_text(encoding="utf-8"))
        elif args.command in ("run", "pilot"):
            pilot(args)
        else:
            serve(Scenario(PILOT_STEPS, args.faulty), args.port)
    except (OSError, RuntimeError, ValueError, subprocess.SubprocessError) as error:
        print(f"qstack: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
