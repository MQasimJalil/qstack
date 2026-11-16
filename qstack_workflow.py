"""Run the synthesized qstack skills through a host-independent reply contract."""

import hashlib
import json
import re
import shutil
import subprocess
import time
from pathlib import Path


PHASES = ("plan", "model", "build", "review", "verify")
PLAN_SHAPE = """Return an object with these keys:
{"behavior": string, "risk": string, "design": string, "acceptance": string,
 "checks": [{"tool": "tlc", "purpose": string}, {"tool": "bombadil", "purpose": string}]}"""
REVIEW_SHAPE = """Return an object with these keys:
{"summary": string, "findings": [{"file": string, "line": integer, "severity": "blocking" or "advisory",
 "trigger": string, "impact": string}]}"""
BRIEF = """Assess the bundled cancel-and-retry pilot. It starts with one running job, permits
one retry after cancellation, and controls when the two attempts' callbacks arrive.
After the retry succeeds, the cancelled attempt's late failure must leave the current result
successful, including after refresh. The run has one bounded TLC check and one live-browser
check, each with a deliberately broken control. The sources are already implemented. The
runtime will snapshot and check them without editing the implementation or publishing anything."""


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def text_fields(data, fields):
    return isinstance(data, dict) and all(
        isinstance(data.get(key), str) and data[key].strip() for key in fields
    )


def parse_reply(text):
    cleaned = text.strip()
    fence = re.fullmatch(r"```(?:json)?\s*(.*?)\s*```", cleaned, flags=re.S | re.I)
    answer = json.loads(fence[1] if fence else cleaned)
    if not isinstance(answer, dict):
        raise ValueError("expected one JSON object")
    return answer


class AgentTransport:
    def __init__(self, host, command=None, model=None, timeout=None):
        self.host = "command" if command else host
        self.command = command
        self.model = model
        self.timeout = timeout if timeout is not None else (300 if self.host == "bridge" else 180)
        self.codex_isolation = None

    def request(self, root, name, prompt):
        request = root / f"{name}.request.md"
        output = root / f"{name}.reply.json"
        request.write_text(prompt, encoding="utf-8")
        print(f"qstack {name}: {self.host}", flush=True)
        if self.host == "bridge":
            print(f"Read {request} and write the JSON reply to {output}", flush=True)
            return self.wait_for_reply(output)
        log = root / f"{name}.agent.log"
        command = self.agent_argv(name)
        try:
            result = subprocess.run(command, input=prompt.encode("utf-8"), capture_output=True,
                                    cwd=root, timeout=self.timeout)
        except subprocess.TimeoutExpired as error:
            log.write_bytes((error.stderr or b"") + (error.stdout or b""))
            raise RuntimeError(f"The {self.host} agent timed out during {name}. See {log}") from error
        log.write_bytes(result.stderr)
        if result.returncode != 0:
            with log.open("ab") as stream:
                stream.write(b"\n" + result.stdout)
            raise RuntimeError(f"The {self.host} agent failed during {name} (exit {result.returncode}). See {log}")
        if self.host == "claude":
            try:
                envelope = parse_reply(result.stdout.decode("utf-8-sig"))
                reply = envelope.get("result")
                if envelope.get("type") != "result" or envelope.get("is_error") or not isinstance(reply, str):
                    raise ValueError("Claude Code returned an unsuccessful result")
                output.write_text(reply, encoding="utf-8")
            except ValueError as error:
                with log.open("ab") as stream:
                    stream.write(b"\n" + result.stdout)
                raise RuntimeError(f"Invalid Claude Code result for {name}: {error}. See {log}") from error
        elif self.host == "command":
            output.write_bytes(result.stdout)
        try:
            return parse_reply(output.read_text(encoding="utf-8-sig"))
        except (OSError, ValueError) as error:
            raise RuntimeError(f"Invalid {name} reply in {output}: {error}") from error

    def wait_for_reply(self, output):
        last_error = None
        until = time.monotonic() + self.timeout
        while time.monotonic() < until:
            try:
                return parse_reply(output.read_text(encoding="utf-8-sig"))
            except FileNotFoundError:
                pass
            except (OSError, ValueError) as error:
                last_error = error
            time.sleep(0.25)
        reason = f": {last_error}" if last_error else ""
        raise RuntimeError(f"The agent did not supply a complete JSON reply at {output} within {self.timeout}s{reason}")

    def agent_argv(self, name):
        if self.host == "command":
            return self.command
        binary = shutil.which(f"{self.host}.exe") or shutil.which(f"{self.host}.cmd") or shutil.which(self.host)
        if not binary:
            raise RuntimeError(f"The {self.host} CLI is unavailable. Use --agent bridge or --agent-command.")
        model = ["--model", self.model] if self.model else []
        if self.host == "codex":
            if self.codex_isolation is None:
                help_text = subprocess.run([binary, "exec", "--help"], capture_output=True, timeout=15).stdout
                self.codex_isolation = [
                    flag for flag in ("--ignore-user-config", "--ephemeral") if flag.encode() in help_text
                ]
            return [binary, "exec", *self.codex_isolation, *model, "--skip-git-repo-check", "--sandbox", "read-only",
                    "--output-last-message", f"{name}.reply.json", "-"]
        return [binary, "--print", *model, "--output-format", "json", "--no-session-persistence", "--tools="]


class Workflow:
    def __init__(self, root, skill_root, args, inputs):
        self.root = root
        self.inputs = inputs
        self.agent = AgentTransport(args.agent, args.agent_command, args.model)
        self.skills = {}
        for name in ("qstack", "qstack-plan", "qstack-model", "qstack-review", "qstack-verify"):
            source = (skill_root / name / "SKILL.md").read_text(encoding="utf-8")
            self.skills[name] = source
        self.receipt = {
            "status": "running", "agent": self.agent.host, "phases": [], "inputs": inputs,
            "skills": {name: hashlib.sha256(body.encode("utf-8")).hexdigest() for name, body in self.skills.items()},
        }
        self.save()

    def save(self):
        write_json(self.root / "workflow.json", self.receipt)

    def complete(self, phase, *evidence):
        seen = self.receipt["phases"]
        if len(seen) >= len(PHASES) or PHASES[len(seen)] != phase:
            raise RuntimeError(f"Unexpected or duplicate workflow phase {phase}.")
        if any(not (self.root / artifact).is_file() for artifact in evidence):
            raise RuntimeError(f"Missing {phase} evidence.")
        skill = f"qstack-{phase}" if phase != "build" else "qstack"
        seen.append({"name": phase, "skill": skill, "evidence": evidence,
                     "executor": self.agent.host if phase in ("plan", "review") else "qstack"})
        self.save()

    def verify_inputs(self):
        for relative, expected in self.inputs.items():
            if hashlib.sha256((self.root / relative).read_bytes()).hexdigest() != expected:
                raise RuntimeError(f"Reviewed input changed during the workflow: {relative}")

    def finish(self):
        self.verify_inputs()
        if [phase["name"] for phase in self.receipt["phases"]] != list(PHASES):
            raise RuntimeError("Some workflow phases did not finish.")
        self.receipt["status"] = "verified"
        self.save()

    def fail(self, error):
        self.receipt.update(status="incomplete", error=str(error))
        self.save()

    def source_context(self, *selected):
        blocks = []
        for relative in self.inputs:
            if selected and relative not in selected:
                continue
            source = (self.root / relative).read_text(encoding="utf-8")
            numbered = "\n".join(f"{line}: {text}" for line, text in enumerate(source.splitlines(), 1))
            blocks.append(f"### {relative}\n\n{numbered}")
        return "\n\n".join(blocks)

    def reply(self, phase, context, shape):
        prompt = (
            f"# qstack {phase}\n\n{self.skills[f'qstack-{phase}']}\n\n"
            f"## Task\n\n{BRIEF}\n\n{context}\n\n"
            f"## Reply\n\n{shape}\n"
            "Use only the supplied task and evidence. Return one JSON object, without Markdown. "
            "Act as a read-only analyst. qstack will execute the tool phases.\n"
        )
        return self.agent.request(self.root, phase, prompt)

    def plan(self):
        plan = self.reply("plan", self.source_context("model/CancelRetry.tla", "browser-input/preview.py"), PLAN_SHAPE)
        if not text_fields(plan, ("behavior", "risk", "design", "acceptance")):
            raise RuntimeError("The plan must specify the behavior, risk, design, and acceptance.")
        checks = plan.get("checks")
        if (not isinstance(checks, list) or len(checks) != 2
                or any(not text_fields(item, ("tool", "purpose")) for item in checks)
                or {item["tool"] for item in checks} != {"tlc", "bombadil"}):
            raise RuntimeError("The pilot plan must select TLC and Bombadil exactly once each.")
        write_json(self.root / "plan.json", plan)
        self.complete("plan", "plan.json", "plan.reply.json")

    def review(self, handoff):
        plan = (self.root / "plan.json").read_text(encoding="utf-8")
        context = (
            f"## Accepted plan\n\n{plan}\n\n## TLC witness\n\n{json.dumps(handoff, indent=2)}\n\n"
            "The deliberately faulty branch is the test control. Assess the protected implementation "
            "and check that its browser property observes the actual contract.\n\n"
            + self.source_context("model/CancelRetry.tla", "browser-input/preview.py", "browser-input/browser.ts")
        )
        review = self.reply("review", context, REVIEW_SHAPE)
        if not text_fields(review, ("summary",)) or not isinstance(review.get("findings"), list):
            raise RuntimeError("The review must contain a summary and a findings array.")
        for item in review["findings"]:
            if (not text_fields(item, ("file", "severity", "trigger", "impact"))
                    or item["severity"] not in ("blocking", "advisory")
                    or item["file"] not in self.inputs or type(item.get("line")) is not int
                    or not 1 <= item["line"] <= len((self.root / item["file"]).read_text(encoding="utf-8").splitlines())):
                raise RuntimeError("Each finding needs an in-scope file and line, trigger, impact, and valid severity.")
        write_json(self.root / "review.json", review)
        if any(item["severity"] == "blocking" for item in review["findings"]):
            raise RuntimeError(f"The review found a blocker. See {self.root / 'review.json'}")
        self.complete("review", "review.json", "review.reply.json")
