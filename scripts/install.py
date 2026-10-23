#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Still Human? · installer

Installs the skill into the agents on this computer and prepares the bridge between the
review page and the agent.

What it does:
  1. Checks the Python version and the skill files.
  2. Finds Claude Code, Codex, Gemini CLI and Antigravity and checks which bridge engines they support.
  3. Asks which of them to install into (the ones found are preselected). "Shared folder" installs
     through npx skills into ~/.agents/skills with the skills lock file, like other shared skills.
  4. Links the skill into Claude Code (~/.claude/skills), Codex (~/.codex/skills) and Antigravity
     (~/.gemini/config/skills, which npx skills leaves out), and writes the /still-human command for Gemini.
  5. Writes the bridge config to ~/.config/still-human/config.json.
  6. If asked (--permissions), lets Claude Code use the skill and run its scripts without asking every time.
     If asked (--codex-routing), adds a routing note to Codex's global instructions.
  7. Runs a short check.

Run from the copy that npx skills put into ~/.agents/skills, it installs nothing again: the skill is
already in place, so it only does the settings (Claude Code and Antigravity links, permissions, Codex routing,
Gemini command).

Usage:
  python3 ~/.agents/skills/still-human/scripts/install.py   # after npx skills add: settings only
  python3 scripts/install.py                  # asks which agents to install into, then before each step
  python3 scripts/install.py --targets claude,codex
  python3 scripts/install.py --yes            # installs without asking (leaves permissions alone)
  python3 scripts/install.py --yes --permissions
  python3 scripts/install.py --dry-run        # shows what it would do without changing anything
  python3 scripts/install.py --try-engine     # tries the suggestion engine with a real call (uses some quota)

Uses only the Python 3 standard library.
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time

NAME = "still-human"
VERSION = "1.4.1"
HERE = os.path.dirname(os.path.abspath(__file__))
SKILL_ROOT = os.path.dirname(HERE)
HOME = os.path.expanduser("~")
CONFIG_DIR = os.path.join(HOME, ".config", NAME)
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")
SCRIPTS = ("audit.py", "review.py", "bridge.py")

ARGS = None


def say(mark, text):
    print(f"{mark} {text}")


def ask(question, default=True):
    if ARGS.yes:
        return default
    if ARGS.dry_run or not sys.stdin.isatty():
        return False
    answer = input(f"? {question} [{'Y/n' if default else 'y/N'}] ").strip().lower()
    if not answer:
        return default
    return answer in ("y", "yes")


def run(cmd, timeout=20):
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return r.returncode, (r.stdout or "") + (r.stderr or "")
    except Exception as e:
        return 1, str(e)


# ---------------------------------------------------------------- 1. preflight

def preflight():
    if sys.version_info < (3, 8):
        sys.exit("Python 3.8 or newer is required.")
    say("✓", f"Python {sys.version.split()[0]}")
    missing = [p for p in ["SKILL.md", "notebook.json", "notebook/template.html", "notebook/page.py", "notebook/bridge.py"] + [f"scripts/{s}" for s in SCRIPTS]
               if not os.path.exists(os.path.join(SKILL_ROOT, p))]
    if missing:
        sys.exit("Skill files are missing: " + ", ".join(missing))
    say("✓", f"Skill files present ({SKILL_ROOT})")


# ---------------------------------------------------------------- 2. find agents

def find_agents():
    agents = {}
    path = shutil.which("claude")
    if path:
        _, version = run([path, "--version"])
        _, help_text = run([path, "--help"])
        agents["claude"] = {"path": path, "version": version.strip().splitlines()[0] if version.strip() else "?",
                            "fork": "--fork-session" in help_text, "stateless": "--print" in help_text}
    path = shutil.which("codex")
    if path:
        _, version = run([path, "--version"])
        code_fork, _ = run([path, "exec", "fork", "--help"])
        code_exec, _ = run([path, "exec", "--help"])
        agents["codex"] = {"path": path, "version": version.strip().splitlines()[0] if version.strip() else "?",
                           "fork": code_fork == 0, "stateless": code_exec == 0}
    path = shutil.which("gemini")
    if path:
        _, version = run([path, "--version"])
        _, help_text = run([path, "--help"])
        agents["gemini"] = {"path": path, "version": version.strip().splitlines()[0] if version.strip() else "?",
                            "fork": False, "stateless": "--prompt" in help_text}
    if not agents:
        say("!", "Claude Code, Codex and Gemini CLI were not found. The skill still installs, but the bridge has no suggestion engines.")
    for name, a in agents.items():
        engines = ["stateless" if a["stateless"] else None, "forked session" if a["fork"] else None]
        say("✓", f"{name} {a['version']} · bridge engines: {', '.join(e for e in engines if e) or 'none'}")
    return agents


# ---------------------------------------------------------------- 3. choose the agents

TARGETS = [("claude", "Claude Code"), ("codex", "Codex"), ("gemini", "Gemini CLI"), ("antigravity", "Antigravity"),
           ("shared", "Shared folder")]
SHARED_DIR = os.path.join(HOME, ".agents", "skills")
SKILL_LOCK = os.path.join(HOME, ".agents", ".skill-lock.json")
DEFAULT_SOURCE = "MesutARIDORU/still-human"
CLI_AGENT_IDS = {"claude": "claude-code", "codex": "codex", "gemini": "gemini-cli"}
# running from the copy npx skills installed: the skill is already in place, only the settings are left
IN_SHARED = os.path.realpath(SKILL_ROOT) == os.path.realpath(os.path.join(SHARED_DIR, NAME))
# Antigravity has no command line to look for, only its app and its folder in ~/.gemini
ANTIGRAVITY_APPS = ("/Applications/Antigravity.app", "/Applications/Antigravity IDE.app")


def antigravity_found():
    return any(os.path.isdir(p) for p in ANTIGRAVITY_APPS) or os.path.isdir(os.path.join(HOME, ".gemini", "antigravity"))


def antigravity_skills_dir():
    """Where Antigravity reads global skills: ~/.gemini/config/skills; earlier versions read ~/.gemini/antigravity/skills.
    npx skills counts Antigravity among the agents that read ~/.agents/skills and links nothing there."""
    old = os.path.join(HOME, ".gemini", "antigravity", "skills")
    if os.path.isdir(old) and not os.path.isdir(os.path.join(HOME, ".gemini", "config")):
        return old
    return os.path.join(HOME, ".gemini", "config", "skills")


def present(key, agents):
    return key in agents or (key == "antigravity" and antigravity_found())
SETUP_STEPS = {"claude": "link and script permissions", "codex": "routing note", "gemini": f"/{NAME} command",
               "antigravity": "skill link"}


def shared_available():
    return bool(shutil.which("npx"))


def target_state(key, agents):
    if key == "shared":
        if not shared_available():
            return "npx not found (needs Node.js)"
        used = " · already in use on this computer" if os.path.exists(SKILL_LOCK) else ""
        return f"~/.agents/skills via npx skills, recorded in the lock file; other agents can be picked too{used}"
    if key == "antigravity":
        if not antigravity_found():
            return "not found on this computer"
        return "found · " + antigravity_skills_dir().replace(HOME, "~", 1) + (f" · {SETUP_STEPS[key]}" if IN_SHARED else "")
    if key not in agents:
        return "not found on this computer"
    return f"found · {agents[key]['version']}" + (f" · {SETUP_STEPS[key]}" if IN_SHARED else "")


def choose_targets(agents):
    """Which agents to install into (from the shared copy: which ones to set up). The ones found are preselected."""
    options = [(key, label) for key, label in TARGETS if not (IN_SHARED and key == "shared")]
    names = dict(TARGETS)
    found = [key for key, _ in options if present(key, agents)]
    if not IN_SHARED and shared_available() and os.path.exists(SKILL_LOCK):
        found.append("shared")  # skills on this computer are already installed this way
    if ARGS.targets == "all":
        return found
    if ARGS.targets != "ask":
        picked = [t.strip().lower() for t in ARGS.targets.split(",") if t.strip()]
        unknown = [t for t in picked if t not in names]
        if unknown:
            sys.exit(f"Unknown target: {', '.join(unknown)}. Valid targets: {', '.join(names)}")
        return [t for t in picked if t in dict(options)]
    if ARGS.yes or ARGS.dry_run or not sys.stdin.isatty():
        return found
    print("Which tools should be set up?" if IN_SHARED else "Which AI tools should it be installed into?")
    for i, (key, label) in enumerate(options, 1):
        print(f"  {i}) [{'x' if key in found else ' '}] {label:<13} {target_state(key, agents)}")
    while True:
        answer = input("? Type the numbers separated by commas (e.g. 1,2). Enter: the ticked ones, 0: none: ").strip().lower()
        if not answer:
            return found
        if answer == "0":
            return []
        picked, wrong = [], []
        for part in re.split(r"[,\s]+", answer):
            if part.isdigit() and 1 <= int(part) <= len(options):
                key = options[int(part) - 1][0]
            elif part in dict(options):
                key = part
            else:
                wrong.append(part)
                continue
            if key not in picked:
                picked.append(key)
        if not wrong:
            return picked
        print(f"  Not understood: {', '.join(wrong)}. Type numbers from 1 to {len(options)}.")


# ---------------------------------------------------------------- 4. link the skill

def link(target_dir, label, source=None):
    """Links (or with --copy, copies) the skill into an agent's skills folder: this copy, or source when given."""
    source = source or SKILL_ROOT
    target = os.path.join(target_dir, NAME)
    if os.path.islink(target) and os.path.realpath(target) == os.path.realpath(source):
        say("✓", f"{label}: already linked ({target})")
        return target
    if os.path.realpath(target) == os.path.realpath(source):
        say("✓", f"{label}: the skill is already here ({target})")
        return target
    if os.path.islink(target):
        # only a pointer: nothing to keep, and a renamed link would show up as a second skill
        if not ARGS.dry_run:
            os.unlink(target)
        say("·", f"{label}: old link ({os.path.realpath(target)}) {'would be replaced' if ARGS.dry_run else 'replaced'}")
    elif os.path.exists(target):
        if not ask(f"{label}: {target} already exists. Back it up and replace it?"):
            say("·", f"{label}: left alone")
            return target
        # the backup goes outside the skills folder, otherwise the agent loads it as a second skill
        backup = os.path.join(CONFIG_DIR, "backups", f"{label.lower().replace(' ', '-')}-{NAME}-{time.strftime('%Y%m%d-%H%M%S')}")
        if not ARGS.dry_run:
            os.makedirs(os.path.dirname(backup), exist_ok=True)
            shutil.move(target, backup)
        say("·", f"{label}: the old one {'would be kept (dry run)' if ARGS.dry_run else 'was kept'} at {backup}")
    if ARGS.dry_run:
        say("·", f"{label}: {target} would be {'copied' if ARGS.copy else 'linked'} (dry run)")
        return target
    os.makedirs(target_dir, exist_ok=True)
    if ARGS.copy:
        shutil.copytree(source, target, ignore=shutil.ignore_patterns(".git", ".github", "__pycache__", "evals", "*.pyc"))
        say("✓", f"{label}: copied ({target})")
    else:
        os.symlink(source, target)
        say("✓", f"{label}: linked ({target} → {source})")
    return target


def skill_source():
    """owner/repo of this checkout on GitHub, for npx skills; the published repository otherwise."""
    code, out = run(["git", "-C", SKILL_ROOT, "remote", "get-url", "origin"])
    m = re.search(r"github\.com[:/]([^/\s]+/[^/\s]+?)(?:\.git)?\s*$", out) if code == 0 else None
    return m.group(1) if m else DEFAULT_SOURCE


def install_shared(selected):
    """Installs through npx skills: one copy in ~/.agents/skills, recorded in the skills lock file,
    linked into the agents chosen there. This is how other shared skills on this computer are installed."""
    source = skill_source()
    cmd = ["npx", "-y", "skills", "add", source, "-g"]
    interactive = not ARGS.yes and sys.stdin.isatty()
    if not interactive:
        ids = [CLI_AGENT_IDS[t] for t in selected if t in CLI_AGENT_IDS]
        cmd += ["-y"] + (["-a"] + ids if ids else [])
    else:
        print("  npx skills will ask which agents to install into. Codex and Gemini CLI are always included.")
        print("  Claude Code is not ticked: type claude in the Search field, tick it with the space bar, then press Enter.")
    if ARGS.dry_run:
        say("·", "Shared folder: this command would run (dry run): " + " ".join(cmd))
        return os.path.join(SHARED_DIR, NAME)
    print("  $ " + " ".join(cmd))
    code = subprocess.run(cmd, cwd=HOME).returncode
    installed = os.path.exists(os.path.join(SHARED_DIR, NAME, "SKILL.md"))
    if code == 0 and installed:
        say("✓", f"Shared folder: installed ({os.path.join(SHARED_DIR, NAME)}) and recorded in the lock file. To update: npx skills update -g {NAME}")
    else:
        say("!", f"Shared folder: the npx skills install did not finish (exit code {code}). To try by hand: npx skills add {source} -g")
    return os.path.join(SHARED_DIR, NAME)


def write_gemini_command(skill_path):
    folder = os.path.join(HOME, ".gemini", "commands")
    target = os.path.join(folder, f"{NAME}.toml")
    content = f'''description = "Still Human? Finds and removes the marks of AI writing in English text"

prompt = """
First read {skill_path}/SKILL.md and follow its instructions. The scripts are in {skill_path}/scripts,
the reference files in {skill_path}/references. Handle the request below according to those instructions.

{{{{args}}}}
"""
'''
    if ARGS.dry_run:
        say("·", f"gemini: {target} would be written (dry run)")
        return
    os.makedirs(folder, exist_ok=True)
    with open(target, "w", encoding="utf-8") as f:
        f.write(content)
    say("✓", f"gemini: /{NAME} command written ({target})")


# ---------------------------------------------------------------- 5. bridge config

def write_config(agents, installs):
    config = {
        "version": VERSION,
        "skill_dir": SKILL_ROOT,
        "installs": installs,
        "agents": agents,
        "default_agent": next((a for a in ("claude", "codex", "gemini") if a in agents), None),
        "default_engine": "auto",
        "engine_order": ["agent", "fork", "stateless"],
        "updated": time.strftime("%Y-%m-%d %H:%M"),
    }
    if ARGS.dry_run:
        say("·", f"the bridge config would be written to {CONFIG_FILE} (dry run)")
        return
    os.makedirs(CONFIG_DIR, exist_ok=True)
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=1)
    say("✓", f"Bridge config written ({CONFIG_FILE})")


# ---------------------------------------------------------------- 6. permissions

def claude_permissions(skill_path):
    settings = os.path.join(HOME, ".claude", "settings.json")
    # the skill itself also needs a rule: without it Claude Code asks before every use of the skill
    rules = [f"Skill({NAME})"] + [f"Bash(python3 {skill_path}/scripts/{s}:*)" for s in SCRIPTS]
    try:
        with open(settings, encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {}
    except Exception as e:
        say("!", f"Could not read the Claude settings file ({e}); permissions left alone.")
        return
    allow = data.setdefault("permissions", {}).setdefault("allow", [])
    added = [r for r in rules if r not in allow]
    if not added:
        say("✓", "Claude Code: the skill and script permissions are already there")
        return
    print("  Change to the Claude Code settings:")
    for r in added:
        print(f"    + {r}")
    if not ARGS.permissions and not ask("Apply this change to ~/.claude/settings.json?", default=False):
        say("·", "Claude Code: permissions left alone. Claude will ask before running the skill and each script.")
        return
    if ARGS.dry_run:
        say("·", "Claude Code: permissions would be updated (dry run)")
        return
    if os.path.exists(settings):
        shutil.copy2(settings, f"{settings}.backup-{time.strftime('%Y%m%d-%H%M%S')}")
    allow.extend(added)
    os.makedirs(os.path.dirname(settings), exist_ok=True)
    with open(settings, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    say("✓", "Claude Code: skill and script permissions added (a backup of the old settings is next to it)")


ROUTING_START = f"<!-- {NAME}:start -->"
ROUTING_END = f"<!-- {NAME}:end -->"
CODEX_ROUTING = f"""{ROUTING_START}
## Still Human?

When the user wants an English text humanized, made to sound natural or less robotic, cleaned of AI writing patterns, or asks "was this written by AI?", use the `{NAME}` skill.
{ROUTING_END}
"""


def codex_routing():
    """Adds a short routing note to Codex's global instructions.

    With many skills installed Codex may not pick this one by itself; the note makes it use the skill
    without the user typing $still-human. Codex reads AGENTS.override.md instead of AGENTS.md when
    the override exists, so the note goes there.
    """
    home = os.path.join(HOME, ".codex")
    override = os.path.join(home, "AGENTS.override.md")
    target = override if os.path.exists(override) and os.path.getsize(override) > 0 else os.path.join(home, "AGENTS.md")
    try:
        with open(target, encoding="utf-8") as f:
            current = f.read()
    except FileNotFoundError:
        current = ""
    if ROUTING_START in current:
        say("✓", f"Codex: the routing note is already there ({target})")
        return
    print("  With many skills installed, Codex may not pick this skill by itself.")
    print(f"  A three-line routing note at the end of {target} sends English rewriting requests to this skill.")
    if not ARGS.codex_routing and not ask("Add the note?", default=False):
        say("·", f"Codex: no routing note added. You can call the skill with ${NAME} whenever you want it.")
        return
    if ARGS.dry_run:
        say("·", f"Codex: the routing note would be added to {target} (dry run)")
        return
    if current:
        shutil.copy2(target, f"{target}.backup-{time.strftime('%Y%m%d-%H%M%S')}")
    os.makedirs(home, exist_ok=True)
    with open(target, "a", encoding="utf-8") as f:
        f.write(("\n\n" if current and not current.endswith("\n\n") else "") + CODEX_ROUTING)
    say("✓", f"Codex: routing note added ({target}){' · a backup of the old file is next to it' if current else ''}")


def codex_note():
    say("·", "Codex: the live bridge opens a local server on 127.0.0.1 only. If your sandbox settings are strict,")
    print("    Codex may ask before running the command; allowing it for that session is enough. Suggestion calls run in a read-only sandbox.")


# ---------------------------------------------------------------- 7. check

SAMPLE = """In today's fast-paced world, artificial intelligence has become an indispensable part of every business. Our company has embarked on a comprehensive transformation journey. This isn't just a technology investment, it's a cultural shift. Ultimately, the future is bright."""
SAMPLE_REWRITE = """We are investing heavily in AI. It will change how we work, not only which tools we use."""


def check(agents):
    tmp = tempfile.mkdtemp(prefix="still-human-install-")
    old, new = os.path.join(tmp, "old.txt"), os.path.join(tmp, "new.txt")
    with open(old, "w", encoding="utf-8") as f:
        f.write(SAMPLE)
    with open(new, "w", encoding="utf-8") as f:
        f.write(SAMPLE_REWRITE)
    code, out = run([sys.executable, os.path.join(HERE, "audit.py"), old])
    say("✓" if code == 0 and "Alarms:" in out else "!", "Numeric audit " + ("works" if code == 0 else "failed: " + out[-200:]))
    page = os.path.join(tmp, "review.html")
    code, out = run([sys.executable, os.path.join(HERE, "review.py"), "--before", old, "--after", new, "--output", page])
    say("✓" if code == 0 and os.path.exists(page) else "!", "Review page " + ("builds" if code == 0 else "failed: " + out[-200:]))
    sys.path.insert(0, HERE)
    try:
        import bridge
        info, _ = bridge.start(page, agent=next(iter(agents), None))
        status = bridge.call(info, "/api/status")
        labels = {"agent": "listening agent", "fork": "forked session", "stateless": "stateless call"}
        engines = [labels[e] for e, ok in status["engines"].items() if ok]
        say("✓", f"Live bridge opens and closes · engines available in this folder: {', '.join(engines) or 'none (they appear while an agent listens)'}")
        if ARGS.try_engine and status["engines"].get("stateless"):
            no = bridge.call(info, "/api/suggest", {"part": 1, "before": "This isn't just a technology investment, it's a cultural shift.",
                                                    "after": "It will change how we work, not only which tools we use.", "request": "", "engine": "stateless"})["request"]
            for _ in range(90):
                r = bridge.call(info, f"/api/suggestions/{no}")
                if r["status"] != "pending":
                    break
                time.sleep(2)
            say("✓" if r["status"] == "ready" else "!", "Stateless suggestion engine: " + ("; ".join(r["suggestions"]) if r["status"] == "ready" else r.get("error") or "no answer"))
        bridge.call(info, "/api/close", {})
    except Exception as e:
        say("!", f"The live bridge could not start ({e}). The page still works as a file; feedback comes back by copy and paste.")
    shutil.rmtree(tmp, ignore_errors=True)


# ---------------------------------------------------------------- main

def main(argv=None):
    global ARGS
    ap = argparse.ArgumentParser(description="Still Human? · installer")
    ap.add_argument("--targets", default="ask",
                    help="claude,codex,gemini,antigravity,shared, or all for every agent found (default: ask; without a terminal, every agent found). "
                         "shared installs through npx skills into ~/.agents/skills")
    ap.add_argument("--copy", action="store_true", help="copy instead of linking")
    ap.add_argument("--permissions", action="store_true", help="let Claude Code use the skill and its scripts without asking")
    ap.add_argument("--codex-routing", action="store_true", help="add a note to Codex's global instructions so Codex picks this skill by itself")
    ap.add_argument("--yes", action="store_true", help="install with defaults, without asking")
    ap.add_argument("--dry-run", action="store_true", help="show what would be done without changing anything")
    ap.add_argument("--no-check", action="store_true", help="skip the final check")
    ap.add_argument("--try-engine", action="store_true", help="try the stateless suggestion engine with a real call")
    ARGS = ap.parse_args(argv)

    print("Still Human? · setup\n")
    preflight()
    agents = find_agents()
    print()
    if IN_SHARED:
        print(f"· The skill is installed in the shared folder and will not be installed again. To update: npx skills update -g {NAME}\n")
    targets = choose_targets(agents)
    labels = dict(TARGETS)
    if not targets:
        print("· No tool picked; only the config file will be written.")
    else:
        print(("· To set up: " if IN_SHARED else "· To install: ") + ", ".join(labels[t] for t in targets))
        for t in targets:
            if t != "shared" and not present(t, agents):
                print(f"  {labels[t]} was not found on this computer. The skill still installs and will be ready once {labels[t]} is installed.")
    installs = {}
    if IN_SHARED:
        installs["shared"] = SKILL_ROOT
        if "claude" in targets:
            # npx skills has usually linked it already; if not, the link points at this same copy
            installs["claude"] = link(os.path.join(HOME, ".claude", "skills"), "Claude Code")
        if "codex" in targets:
            installs["codex"] = SKILL_ROOT  # Codex reads ~/.agents/skills itself; a second link would show the skill twice
    elif "shared" in targets:
        # npx skills links the agents itself; linking them here too would give Codex the skill twice
        installs["shared"] = install_shared(targets)
        for key, folder in (("claude", ".claude"), ("codex", ".codex")):
            if key in targets:
                installs[key] = os.path.join(HOME, folder, "skills", NAME)
    else:
        if "claude" in targets:
            installs["claude"] = link(os.path.join(HOME, ".claude", "skills"), "Claude Code")
        if "codex" in targets:
            installs["codex"] = link(os.path.join(HOME, ".codex", "skills"), "Codex")
    if "antigravity" in targets:
        # npx skills leaves Antigravity out, so it is linked here in every case, to the shared copy when there is one
        installs["antigravity"] = link(antigravity_skills_dir(), "Antigravity", installs.get("shared"))
    if "gemini" in targets:
        # with the shared folder, Gemini reads the same copy as the other agents
        write_gemini_command(installs.get("shared") or SKILL_ROOT)
        installs["gemini"] = os.path.join(HOME, ".gemini", "commands", f"{NAME}.toml")
    print()
    write_config(agents, installs)
    if "claude" in installs:
        claude_permissions(installs["claude"])
    if "codex" in installs:
        codex_routing()
        codex_note()
    if not ARGS.no_check and not ARGS.dry_run:
        print()
        check(agents)
    print("\nDone. To try it, tell your agent: \"Make this sound human: In today's fast-paced world, AI has become an indispensable part of our lives.\"")


if __name__ == "__main__":
    main()
