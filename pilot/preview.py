"""The cancel-and-retry preview and its deterministic callback fixture."""

import argparse
import json
from dataclasses import dataclass, field
from html import escape
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Lock
from urllib.parse import parse_qs


HERE = Path(__file__).resolve().parent
ACTIONS = {
    "cancel": "Cancel attempt 1",
    "retry": "Retry job",
    "deliver-retry": "Deliver attempt 2 success",
    "deliver-original": "Deliver late attempt 1 failure",
    "refresh": "Refresh job",
}
PILOT_STEPS = tuple(ACTIONS)


@dataclass
class Job:
    accept_stale: bool
    attempt: int = 1
    status: str = "running"
    pending: set[int] = field(default_factory=lambda: {1})

    def cancel(self):
        if self.status != "running":
            raise ValueError("Only a running job can be cancelled.")
        self.status = "cancelled"

    def retry(self):
        if self.status != "cancelled":
            raise ValueError("Only a cancelled job can be retried.")
        self.attempt += 1
        self.pending.add(self.attempt)
        self.status = "running"

    def complete(self, attempt, status):
        if attempt not in self.pending:
            return "duplicate callback ignored"
        self.pending.remove(attempt)
        if attempt == self.attempt and self.status == "running":
            self.status = status
            return "current callback applied"
        if self.accept_stale and attempt < self.attempt and self.status == "succeeded":
            self.status = status
            return "stale callback applied"
        return "stale or cancelled callback ignored"


class Scenario:
    def __init__(self, steps, accept_stale=False, journal=None):
        self.steps = tuple(steps)
        if self.steps != PILOT_STEPS:
            raise ValueError("The handoff must contain the cancel-and-retry witness and a refresh.")
        self.job = Job(accept_stale)
        self.journal = journal
        self.events = []
        self.lock = Lock()

    @property
    def next_action(self):
        return self.steps[len(self.events)] if len(self.events) < len(self.steps) else None

    def advance(self, action):
        if action is None or action != self.next_action:
            raise ValueError("That action is out of sequence. Reload to see the current step.")
        match action:
            case "cancel":
                self.job.cancel()
                effect = "cancellation recorded"
            case "retry":
                self.job.retry()
                effect = "retry started"
            case "deliver-retry":
                effect = self.job.complete(2, "succeeded")
            case "deliver-original":
                effect = self.job.complete(1, "failed")
            case "refresh":
                effect = "fresh HTTP read of job state"
        self.events.append({
            "action": action, "attempt": self.job.attempt, "status": self.job.status, "effect": effect,
        })
        if self.journal:
            staged = self.journal.with_suffix(".tmp")
            staged.write_text(json.dumps(self.events, indent=2) + "\n", encoding="utf-8")
            staged.replace(self.journal)


def page(title, body, stylesheet):
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(title)}</title>{stylesheet}</head>
<body>{body}</body></html>"""


def render(scenario):
    job = scenario.job
    stage = len(scenario.events)
    next_action = scenario.next_action
    stale = "true" if any(e["action"] == "deliver-original" for e in scenario.events) else "false"
    refreshed = "true" if stage == len(scenario.steps) else "false"
    mode = "Fault injected" if job.accept_stale else "Protected"
    pending = ", ".join(str(number) for number in sorted(job.pending)) or "None"
    steps = "".join(
        f'<li class="{"done" if i < stage else "current" if i == stage else ""}">{title}</li>'
        for i, title in enumerate(ACTIONS.values())
    )
    if next_action == "refresh":
        action = '<a class="button" data-next href="/refresh">Refresh job</a>'
    elif next_action:
        action = (
            '<form action="/action" method="post">'
            f'<button class="button" data-next name="action" value="{next_action}">{ACTIONS[next_action]}</button>'
            '</form>'
        )
    else:
        action = '<a class="button" data-next href="/">Read job status again</a>'
    event_log = "".join(
        f"<tr><td>{ACTIONS[event['action']]}</td><td>{escape(event['effect'])}</td></tr>"
        for event in scenario.events
    ) or '<tr><td colspan="2">Waiting for the first action.</td></tr>'
    return page("Cancel and retry · qstack", f"""
<main id="pilot" data-stale-delivered="{stale}" data-refreshed="{refreshed}">
  <header><p class="tag">QSTACK / PILOT</p><span class="mode">{mode}</span></header>
  <h1>Cancel and retry</h1>
  <p class="lead">Retry a job while the first attempt still has a callback in flight.</p>
  <div class="two-up">
    <section class="panel" aria-labelledby="job-title">
      <h2 id="job-title">Job status</h2>
      <p id="job-status" class="state {job.status}">{job.status.title()}</p>
      <dl><div><dt>Current attempt</dt><dd id="job-attempt">{job.attempt}</dd></div>
      <div><dt>Pending callbacks</dt><dd>{pending}</dd></div></dl>
    </section>
    <section class="panel" aria-labelledby="steps-title">
      <h2 id="steps-title">Scenario</h2>
      <ol>{steps}</ol>
      {action}
    </section>
  </div>
  <section class="panel" aria-labelledby="history-title">
    <h2 id="history-title">Event history</h2>
    <table><thead><tr><th scope="col">Step</th><th scope="col">Effect</th></tr></thead>
    <tbody>{event_log}</tbody></table>
  </section>
</main>""", '<link rel="stylesheet" href="/style.css">')


def new_server(scenario, port=0):
    class Handler(BaseHTTPRequestHandler):
        def reply(self, status, body, content_type="text/plain; charset=utf-8"):
            data = body.encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(data)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(data)

        def do_GET(self):
            if self.path == "/health":
                self.reply(200, "ready")
            elif self.path == "/style.css":
                self.reply(200, (HERE / "style.css").read_text(encoding="utf-8"), "text/css; charset=utf-8")
            elif self.path in {"/", "/refresh"}:
                with scenario.lock:
                    if self.path == "/refresh" and scenario.next_action == "refresh":
                        scenario.advance("refresh")
                    body = render(scenario)
                self.reply(200, body, "text/html; charset=utf-8")
            else:
                self.reply(404, "Page not found")

        def do_POST(self):
            if self.path != "/action":
                self.reply(404, "Page not found")
                return
            try:
                length = int(self.headers.get("Content-Length", "0"))
                if not 0 < length <= 1024:
                    raise ValueError("Expected a short form body.")
                form = parse_qs(self.rfile.read(length).decode("utf-8"), strict_parsing=True)
                action, = form.get("action", [])
                if action not in ACTIONS or action == "refresh":
                    raise ValueError("Unknown action.")
                with scenario.lock:
                    scenario.advance(action)
            except ValueError as error:
                self.reply(400, str(error))
                return
            self.send_response(303)
            self.send_header("Location", "/")
            self.send_header("Content-Length", "0")
            self.end_headers()

        def log_message(self, *_):
            pass

    return ThreadingHTTPServer(("127.0.0.1", port), Handler)


def serve(scenario, port):
    with new_server(scenario, port) as server:
        print(f"Preview at http://127.0.0.1:{server.server_port}", flush=True)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--handoff", type=Path, required=True)
    parser.add_argument("--journal", type=Path, required=True)
    parser.add_argument("--port", type=int, required=True)
    parser.add_argument("--faulty", action="store_true")
    args = parser.parse_args()
    handoff = json.loads(args.handoff.read_text(encoding="utf-8"))
    serve(Scenario(handoff["steps"], args.faulty, args.journal), args.port)
