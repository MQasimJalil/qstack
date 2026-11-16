#!/usr/bin/env node

const { spawnSync } = require("node:child_process");
const { createHash, randomUUID } = require("node:crypto");
const fs = require("node:fs");
const path = require("node:path");

const source = path.resolve(__dirname, "..");
const hosts = {
  codex: ".agents/skills",
  claude: ".claude/skills",
  cursor: ".cursor/skills",
  opencode: ".opencode/skills",
  gemini: ".gemini/skills",
};
const runtimeFiles = [
  "bin/qstack.cjs", "catalog/index.json", "docs/catalog.md", "docs/agent-capabilities.md",
  "docs/licenses/gstack.txt", "docs/licenses/pstack.txt", "docs/synthesis.md",
  "package.json", "README.md", "qstack.py", "qstack_workflow.py",
  "pilot/preview.py", "pilot/browser.ts", "pilot/style.css",
  "pilot/CancelRetry.tla", "pilot/Fixed.cfg", "pilot/Faulty.cfg",
];
const setupHelp = "qstack setup [--host codex|claude|cursor|opencode|gemini|all] [--dir WORKSPACE] [--skills-dir PATH]";

function digest(buf) {
  return createHash("sha256").update(buf).digest("hex");
}

function readRegularFile(file) {
  const stat = fs.lstatSync(file, { throwIfNoEntry: false });
  if (stat && !stat.isFile()) throw new Error(`Expected a regular file at ${file}`);
  return stat ? fs.readFileSync(file) : null;
}

function writeAtomic(file, content) {
  fs.mkdirSync(path.dirname(file), { recursive: true });
  const staged = `${file}.${randomUUID()}.tmp`;
  try {
    fs.writeFileSync(staged, content, { flag: "wx" });
    fs.renameSync(staged, file);
  } finally {
    fs.rmSync(staged, { force: true });
  }
}

function setup(args) {
  if (args.includes("--help")) {
    console.log(setupHelp);
    return;
  }
  const options = new Map();
  for (let i = 0; i < args.length; i += 2) {
    const [key, value] = args.slice(i, i + 2);
    if (!["--host", "--dir", "--skills-dir"].includes(key) || !value || value.startsWith("--") || options.has(key)) {
      throw new Error(setupHelp);
    }
    options.set(key, value);
  }
  const project = fs.realpathSync(path.resolve(options.get("--dir") ?? process.cwd()));
  const host = options.get("--host") ?? "codex";
  if (host !== "all" && !Object.hasOwn(hosts, host)) throw new Error(`Unknown host ${host}. ${setupHelp}`);
  const custom = options.get("--skills-dir");
  const destinations = custom
    ? [path.resolve(project, custom)]
    : (host === "all" ? Object.values(hosts) : [hosts[host]]).map((dir) => path.join(project, dir));
  const runtime = path.join(project, ".qstack", "runtime");
  const receipt = path.join(runtime, "install.json");
  const previous = readRegularFile(receipt);
  const owned = new Map(previous ? JSON.parse(previous.toString()).files : []);
  const skills = fs.readdirSync(path.join(source, "skills"), { withFileTypes: true })
    .filter((entry) => entry.isDirectory())
    .map((entry) => path.join(entry.name, "SKILL.md"));
  const files = new Map();
  const add = (relative, destination) => files.set(destination, fs.readFileSync(path.join(source, relative)));
  for (const relative of runtimeFiles) add(relative, path.join(runtime, relative));
  for (const skill of skills) {
    const relative = path.join("skills", skill);
    add(relative, path.join(runtime, relative));
    for (const destination of destinations) add(relative, path.join(destination, skill));
  }
  const changed = [];
  for (const [file, data] of files) {
    const existing = readRegularFile(file);
    const fingerprint = digest(data);
    if (!existing || digest(existing) !== fingerprint) {
      if (existing && owned.get(file) !== digest(existing)) {
        throw new Error(`Existing file has local changes. Move it before installing: ${file}`);
      }
      changed.push([file, data]);
    }
    owned.set(file, fingerprint);
  }
  for (const [file, data] of changed) writeAtomic(file, data);
  const tracked = Buffer.from(JSON.stringify({ version: require("../package.json").version, files: [...owned] }, null, 2) + "\n");
  if (!previous || !previous.equals(tracked)) writeAtomic(receipt, tracked);
  console.log(`Installed ${skills.length} qstack skills in ${destinations.join(", ")}`);
  const agent = host === "claude" ? "claude" : !custom && ["codex", "all"].includes(host) ? "codex" : "bridge";
  console.log(`Run: node "${path.join(runtime, "bin", "qstack.cjs")}" run --agent ${agent}`);
}

function skillCatalog() {
  return require("../catalog/index.json");
}

function showSkills(args) {
  const { skills, sources } = skillCatalog();
  const query = args.filter((arg) => arg !== "--json").join(" ").trim().toLowerCase();
  const matches = skills.filter((entry) => {
    const matchingSources = sources.filter((row) => row.target === entry.id);
    if (!query) return true;
    return [
      entry.id, entry.description, entry.category,
      ...matchingSources.flatMap((row) => [row.path, row.name, `${row.repo}:${row.name}`]),
    ].some((text) => text.toLowerCase().includes(query));
  });
  if (args.includes("--json")) {
    console.log(JSON.stringify(matches, null, 2));
  } else {
    for (const skill of matches) console.log(`${skill.id}\t${skill.category}\t${skill.description}`);
    console.log(`${matches.length} of ${skills.length} skills`);
  }
}

function showSkill(args) {
  if (args.length !== 1) throw new Error("Usage: qstack skill <name>");
  const { skills, sources } = skillCatalog();
  const name = args[0].replace(/^\//, "").toLowerCase();
  const direct = skills.find((skill) => skill.id === name);
  const matches = sources.filter((row) =>
    row.path.toLowerCase() === name || row.name.toLowerCase() === name || `${row.repo}:${row.name.toLowerCase()}` === name);
  const primary = matches.filter((row) => row.status !== "host edition");
  const targets = new Set((primary.length ? primary : matches).map((row) => row.target).filter(Boolean));
  if (!direct && targets.size !== 1) {
    if (targets.size) throw new Error(`Ambiguous skill ${name}. Use ${[...targets].join(" or ")}.`);
    throw new Error(`Unknown installable skill ${name}. Use qstack skills to search.`);
  }
  const id = direct?.id ?? [...targets][0];
  process.stdout.write(fs.readFileSync(path.join(source, "skills", id, "SKILL.md"), "utf8"));
  const mode = !direct && (primary.length ? primary : matches).find((row) => row.target === id && row.mode);
  if (mode) process.stdout.write(`\n## Invocation mode\n\n${mode.mode}\n`);
}

function main(args) {
  if (!args.length || args[0] === "--help" || args[0] === "-h") {
    console.log("qstack setup | skills [search] [--json] | skill <name> | run | plan | pilot | preview");
    console.log("Use qstack setup --help or qstack run --help for options.");
    return 0;
  }
  if (args[0] === "setup") {
    setup(args.slice(1));
    return 0;
  }
  if (args[0] === "skills") {
    showSkills(args.slice(1));
    return 0;
  }
  if (args[0] === "skill") {
    showSkill(args.slice(1));
    return 0;
  }
  const python = process.env.QSTACK_PYTHON
    ? [process.env.QSTACK_PYTHON]
    : process.platform === "win32" ? ["python", "python3"] : ["python3", "python"];
  for (const program of python) {
    const result = spawnSync(program, [path.join(source, "qstack.py"), ...args], { stdio: "inherit" });
    if (result.error?.code === "ENOENT") continue;
    if (result.error) throw result.error;
    return result.status ?? 1;
  }
  throw new Error("Python 3.10 or newer was not found. Set QSTACK_PYTHON to its executable.");
}

try {
  process.exitCode = main(process.argv.slice(2));
} catch (error) {
  console.error(`qstack: ${error.message}`);
  process.exitCode = 1;
}
