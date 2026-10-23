# Installation

Still Human? is plain Markdown plus a few small Python scripts. Any agent that can read files can follow the instructions in `SKILL.md`. The scripts (measurement, review page, live bridge) need Python 3.8 or newer and use only the standard library.

## With npx skills

The skill goes into the shared `~/.agents/skills` folder as a single copy and is recorded in the `~/.agents/.skill-lock.json` lock file. Codex and Gemini CLI read the skill from that folder. Claude Code looks in its own folder, so `npx skills` puts a link to the shared copy there. Antigravity reads its own folder too, but `npx skills` puts no link there. If you use Antigravity, run the setup script after installing (see Antigravity).

### One command

```bash
npx skills add MesutARIDORU/still-human -g -y -a claude-code codex gemini-cli
```

It installs into Claude Code, Codex and Gemini CLI without asking. At the end you see a summary like this:

```
◇  Installed 1 skill
│  ✓ ~/.agents/skills/still-human
│    universal: Codex, Gemini CLI
│    symlinked: Claude Code
```

With `-a`, the skill is installed only into the agents you name. If you write only `-a claude-code`, for example, the skill doesn't go into the shared folder; it's copied into Claude Code's folder. If you want Codex and Gemini CLI too, name all three.

### Picking from the list

```bash
npx skills add MesutARIDORU/still-human -g
```

The command first finds the skill and shows its description, then asks, in this order:

1. **Which agents do you want to install to?**
   - The "Universal (.agents/skills)" section at the top lists Codex, Gemini CLI and the other agents that read the shared folder. They're always included.
   - Claude Code is in the "Additional agents" section below and isn't ticked. Type `claude` in the "Search" field, tick Claude Code with the space bar, then press Enter.
   - If you just press Enter, the skill is installed into Codex and Gemini CLI but not into Claude Code.
2. **Installation method:** asked if you selected an extra agent. "Symlink (Recommended)" is preselected: the agent's folder gets a link to the shared copy, so an update reaches all of them at once. Press Enter.
3. **Proceed with installation?** It shows a summary and the skill's security scan. "Yes" is preselected; press Enter.

### Updating

```bash
npx skills update still-human
```

If you're in an agent-based tool, you can also just tell the agent "Install this skill: https://github.com/MesutARIDORU/still-human". The agent reads this file and runs the one command.

## Optional settings

`npx skills` installs the skill but doesn't touch your tools' settings. The skill works without any settings. If you want the following, run the setup script in the installed copy:

```bash
python3 ~/.agents/skills/still-human/scripts/install.py
```

The script doesn't install the skill again. In order, it:

1. Finds Claude Code, Codex, Gemini CLI and Antigravity on your computer, and checks which live-bridge engines each supports (forked session, stateless call).
2. Asks which tools to set up. The ones it found are ticked. Type the numbers separated by commas; Enter takes the ticked ones, 0 takes none:
   ```
   Which tools should be set up?
     1) [x] Claude Code   found · 2.1.300 (Claude Code) · link and script permissions
     2) [x] Codex         found · codex-cli 0.162.1 · routing note
     3) [x] Gemini CLI    found · 0.60.0 · /still-human command
     4) [x] Antigravity   found · ~/.gemini/config/skills · skill link
   ```
3. Checks whether Claude Code's skill folder (`~/.claude/skills/still-human`) has a link. If Claude Code wasn't selected during installation, it adds the link to the same copy. It doesn't add a link for Codex, which reads the shared folder itself; otherwise the skill would show up twice. For Antigravity it adds a link to the same copy at `~/.gemini/config/skills/still-human`, because `npx skills` leaves Antigravity out.
4. Writes the `~/.gemini/commands/still-human.toml` command for Gemini CLI.
5. Writes the bridge config to `~/.config/still-human/config.json`.
6. Asks whether Claude Code may run the skill and its scripts without asking each time: a `Skill(still-human)` rule and one `Bash(python3 …)` rule per script. If you agree, it backs up `~/.claude/settings.json` first. Without these permissions, Claude Code asks the first time the skill runs and before each script.
7. Asks whether to add a routing note to Codex's global instructions (see Codex below).
8. Runs a short check: a measurement, building a page, opening and closing the bridge.

Options:

| Option | What it does |
|---|---|
| `--dry-run` | Shows what it would do without changing anything |
| `--yes` | Runs without asking. Leaves the permissions and the Codex note alone |
| `--targets claude,codex` | Runs without asking, only for the tools named: `claude`, `codex`, `gemini`, `antigravity`. `all` means every tool found |
| `--permissions` | Adds the skill and script permissions to Claude Code |
| `--codex-routing` | Adds the routing note to Codex's global instructions (`~/.codex/AGENTS.override.md` if it exists, otherwise `~/.codex/AGENTS.md`) |
| `--try-engine` | Tries the stateless suggestion engine with a real call. Uses a little of your quota |
| `--no-check` | Skips the check at the end |

Every setting at once, without questions:

```bash
python3 ~/.agents/skills/still-human/scripts/install.py --targets claude,codex,gemini,antigravity --permissions --codex-routing
```

## Without Node.js

Clone the repository into a folder of your choice and run the setup script from there:

```bash
git clone https://github.com/MesutARIDORU/still-human.git ~/still-human
```

```bash
python3 ~/still-human/scripts/install.py
```

Run from the repository, the script asks which tools to install into and links the skill there itself: `~/.claude/skills/still-human` for Claude Code, `~/.codex/skills/still-human` for Codex, `~/.gemini/config/skills/still-human` for Antigravity. Because it's a link, updating the repository with `git pull` updates the skill too. Add `--copy` to copy instead of linking. The other steps are the same as the settings above.

## Notes by tool

### Claude Code

The skill loads from `~/.claude/skills/still-human`. `npx skills` puts a link to the shared copy there. If you used the one command or ticked Claude Code in the list, the link is there; otherwise the setup script adds it.

Usage: give it a text and say "humanize this", or use the `/still-human` command.

### Codex

Codex reads skills from the shared `~/.agents/skills` folder; if you installed with `npx skills`, nothing else is needed. Don't also put the skill under `~/.codex/skills`, or Codex will see it twice.

**Name and icon:** Codex reads the skill's display name and icon from `agents/openai.yaml`. The skill shows up as "Still Human?" with a skull icon.

**Picking the skill:** with many skills installed, Codex may not pick this one by itself. The setup script offers to add a three-line routing note to Codex's global instructions for that (`--codex-routing`). If you'd rather not, start your request with `$still-human`.

**Live bridge:** the bridge opens a local server on 127.0.0.1 only. If your sandbox settings are strict and Codex asks before running the command, allowing it for that session is enough. Suggestion calls run in a read-only sandbox.

### Gemini CLI

`npx skills` installs the skill into the shared folder that Gemini CLI reads. The setup script also writes the `~/.gemini/commands/still-human.toml` command, so you can call the skill by name: `/still-human [text]`. To add the command by hand, copy [adapters/gemini/still-human.toml](adapters/gemini/still-human.toml) into that folder and replace `<SKILL-PATH>` with `~/.agents/skills/still-human`.

In Gemini, "Suggest another" works only through the stateless call, since Gemini CLI can't fork a session. The stateless call also needs an account that can use Gemini CLI.

### Antigravity

Antigravity reads global skills from `~/.gemini/config/skills`; earlier versions looked in `~/.gemini/antigravity/skills`, and the setup script uses whichever is there. `npx skills` counts Antigravity among the agents that read the shared folder, so it puts no link there and the skill doesn't show up in Antigravity. After installing with `npx skills`, run:

```bash
python3 ~/.agents/skills/still-human/scripts/install.py --targets antigravity
```

The script links `~/.gemini/config/skills/still-human` to the shared copy, so `npx skills update` updates the skill in Antigravity too. Open a new chat in Antigravity and type `/still`: the skill shows up in the list. If it doesn't, restart Antigravity. On a version that doesn't follow the link, run the script with `--copy`, and run it again after every update.

On the live bridge, the listening agent works in Antigravity too. The forked session doesn't, and the stateless call goes through Claude Code, Codex or Gemini CLI if one is installed. A preview choice "just for this chat" can't be saved by the bridge, since it can't identify an Antigravity chat; the agent remembers that choice for the rest of the chat itself.

### Other tools that read AGENTS.md

For tools that don't read the shared folder, first clone the repository. Then add the block in [adapters/agents-md-snippet.md](adapters/agents-md-snippet.md) to the project's or the tool's `AGENTS.md`, replacing `<CLONE-PATH>` with the repository folder.

### Web chat interfaces

If the web interface of ChatGPT, Claude.ai or Gemini can't read files or run scripts, you can paste the contents of `SKILL.md` into the custom instructions, a Project or a Gem. Two things are then missing:
- The measurements are made by hand.
- There's no review page.

The change table still comes.

## Checking the installation

Tell your agent:

```
Humanize this: In today's fast-paced digital landscape, our team has developed an innovative, end-to-end solution that seamlessly transforms the customer experience.
```

If it's installed correctly, the answer looks like this:
- The line `💀 Still Human❓ · Text type: …` appears in the chat first, then the agent carries on.
- The delivery starts with the same logo.
- It notices the stock opening and the buzzwords ("innovative", "end-to-end", "seamlessly").
- It doesn't invent what the solution is. The text doesn't say, so it leaves a placeholder or asks.
- It gives a change table.

If the agent only swaps in synonyms, or adds a feature of its own, it hasn't read the instructions.

## Removing

If you installed with `npx skills`:

```bash
npx skills remove still-human -g
```

If you ran the setup script, remove what it wrote too:
- `~/.gemini/commands/still-human.toml`
- The Antigravity link: `~/.gemini/config/skills/still-human`
- `~/.config/still-human`
- If you added Claude Code permissions: the `Skill(still-human)` and `still-human/scripts` lines in `~/.claude/settings.json`.
- If you added the Codex routing note: the block between `still-human:start` and `still-human:end` in `~/.codex/AGENTS.override.md` (or `AGENTS.md`).

Before changing `settings.json` and the Codex instructions file, the setup script saved backups of them in the same folder.

If you installed by hand from the repository, delete the `~/.claude/skills/still-human` and `~/.codex/skills/still-human` links and the folder you cloned.
