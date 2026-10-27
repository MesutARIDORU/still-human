# Changelog

## 1.5.0 · Daily update check

- **New-version check:** once a day, the first time it runs, the skill looks at the newest release on GitHub. If there's a new one, it asks in the chat after the delivery whether to update: "Update" or "Not now". After "Not now" it doesn't ask again the same day; it asks the next day, the first time it runs. The day it looked is kept in `~/.config/still-human/update.json`.
- **Long text, update first:** when the delivered text is longer than 250 characters, the skill updates without asking, then asks "OK" or "Go back". Without an answer the new version stays. "Go back" reinstalls the earlier release's tag, and a release the user went back from is never installed again unasked.
- **Clickable questions:** the preview and update questions come with options through AskUserQuestion in Claude Code, ask_user in Gemini CLI and request_user_input in Codex's Plan mode. In Codex's default mode the question stays written.
- **Updating itself:** on "Update", the skill runs `npx skills update -g still-human` if it was installed with `npx skills`, or `git pull --ff-only` if it runs from a git clone. A copy pinned to an older release is added again from the repository. The new version takes effect the next time it runs. Uploaded to Claude's chat as a zip, it gives the releases page to download the new zip from.
- **Asking in the chat:** ask "is there an update?" and the skill looks straight away, without waiting for the next day.
- **No internet:** if GitHub can't be reached, the skill says nothing. The request gives up after 4 seconds, and where Python from python.org lacks its certificates it tries again with the system's certificates or with `curl`.
- **Shared notebook 1.4.0:** the check comes from notebook-review as `bridge.py update`, and `notebook.json` now names the skill's GitHub repository (`repo`).

## 1.4.1 · In more tools

- **Description:** the skill's description now starts with its trigger words ("Humanizes English text") and ends with its name. With many skills installed, Codex shortens descriptions, and the trigger words were in the part that got cut. On a computer with 230 skills, Codex now picks the skill without being told its name.
- **Claude's chat:** every release gets a `still-human.zip`, which can be uploaded to Claude's desktop and web chat under Customize > Skills. In such an environment, where the user's browser can't reach the agent, the review page doesn't open live: it comes as a file to download, and the decisions come back by copy and paste.
- **Where it works:** a table in the README says what was tested in each tool: Claude Code, Codex CLI, Codex in the ChatGPT desktop app, Antigravity, Gemini CLI and Claude's chat. It also notes that Gemini CLI doesn't run on free individual accounts, since Google turned it off for them.
- **Update command:** `npx skills update -g still-human`. Without `-g` the command asks for a scope, Enter picks "Project", and the globally installed skill isn't updated.

## 1.4.0 · Preview on first use, Antigravity

- **Preview on first use:** the first time the skill is used, the review page opens without asking. A taped note on the page asks what should happen from then on: "Open it every time", "Ask me first" or "Only when I ask". With "Only when I ask", the note shows how to open the page with a chat box that types "preview", "show it on the page" and "open the changes on the page". In Claude Code and Codex it also offers "always open in this chat" and "don't open in this chat".
- **The choice lives in a file:** `~/.config/still-human/preferences.json`. Step 5 reads it with `bridge.py preview` before asking anything. With "Ask me first", a long text or one with many changes opens without asking. Change it on the Preview line in the page's settings, or by saying something like "always open the preview" in the chat.
- **Antigravity:** the setup script finds Antigravity and links the skill into `~/.gemini/config/skills`, where it reads skills. `npx skills` puts no link there, so the skill didn't show up. After installing with `npx skills`: `python3 ~/.agents/skills/still-human/scripts/install.py --targets antigravity`. Details in INSTALL.md.
- **Title:** "Still Human?" is back in Marker Felt, on the page, the cover and the screenshots.

## 1.3.1 · New cover

- **README cover:** the cover is redrawn in the review page's new look: a notebook sheet on a wooden desk, handwriting, green highlighter, the versions bubble and the taped card. The example is the same: "The new release isn't just an update — it's a transformative journey that doubles page speed." becomes "The new release makes pages twice as fast." The writing sits on the ruled lines.

## 1.3.0 · A notebook on the desk

- **New look:** the review page is a sheet of ruled paper with punched holes, lying on a wooden desk. The text, the title and the card are written in Patrick Hand. The font and the textures (paper, tape, highlighter, wood) are embedded in the page, so it makes no outside requests.
- **The text:** changed words sit on a green highlighter. Once a change is approved, its original stays readable, struck through, just above or before the new text.
- **The margin:** each change has a numbered circle at its middle, and a change over several lines gets an orange crayon brace. The first sentence of its reason is written in the right margin with a small arrow. Circles of changes that sit close together stack instead of covering each other.
- **The card:** a taped note card. "Apply the suggestion" (`1`) approves the change and opens the next one, with "Keep the original" (`2`) and "Edit it myself" (`3`) below it. Other versions are picked with the arrow beside them. A long card scrolls under its tape.
- **The versions bubble:** hovering over a change opens a hand-drawn speech bubble, written in the red of the title's underline. It names the version in the text and its place in the list. ‹ › step through the versions and ▾ lists them all. On a page opened with the live bridge and nothing to choose from, the list can ask the agent. The bubble shows in the final-text preview too.
- **Progress:** the last line counts the approved changes: "3 / 5 approved".
- **Preferences:** the type setting is stored under a new name and defaults to handwriting. An earlier setting is ignored, so everyone sees the new page once as it comes.
- **Reasons:** the first sentence of a reason is now a margin note, so SKILL.md asks for it to be short, with the detail in the second sentence.

## 1.2.0 · New touches on the page

- **Versions in place:** hover over a change and small arrows appear above its first word. They step through the suggestion, the shorter, more formal and warmer versions and the original, right in the text, and the version's name shows beside them for a moment. The arrows sit at the start of the part, so they stay put when the text gets longer or shorter.
- **Final text:** the eye button next to the title, or the `p` key, shows the text with your decisions applied, with no marks and no card. Hovering over a changed part there shows the same arrows.
- **Card at the top:** on a wide screen the card opens beside the page at the top and stays there while the page scrolls. The dashed line runs from the sentence into the gap and along it to the card.
- **The page's last line:** progress, open questions, "Keep the rest" and "Send to agent" moved from the floating bar onto the last line of the page. Click "1 open question" to go to the next question.
- **Divider:** a thin highlighter stroke separates the skill's notes from the text.
- **Readable card:** section names are clearer. The original is written in red pen, and the removed words are crossed out with a faint marker that runs behind the letters.
- The Edit menu's "preview" is now "show the feedback", so it isn't confused with the final text.

## 1.1.0 · New note card, shared notebook

- **Note card:** a plain card with three parts: "Original" (removed words struck through), "Suggested" (added words in bold) and "Other options" (the same sentence shorter, more formal and warmer). You decide with "Keep", "Revert", "Use" next to an option, or "Write my own". Arrows at the top move between changes, and the card names the pattern.
- **Responsive layout:** on a wide screen the card opens beside the page, level with the sentence and joined to it by a dashed line. In a narrow window it opens under the sentence; on a phone, from the bottom of the screen. In a narrow window a small note suggests opening the page in the browser.
- **Margin marks and progress bar:** each changed line shows its state in the margin: not reviewed, kept, reverted, your own. The bar at the bottom shows progress and open questions, and "Keep the rest" accepts every change not yet looked at.
- **Options in the notes:** the agent writes an `alternatives` field for each change. When the bridge is open and there are no options, the card asks the agent for the three versions, and the user can ask for something else.
- **Shared notebook:** the review page and the live bridge moved to [notebook-review](https://github.com/MesutARIDORU/notebook-review), shared with the Turkish skill İnsanlık öldü mü?. A copy lives in `notebook/`, the skill's identity (name, language, pattern names) in `notebook.json`. `scripts/review.py` and `scripts/bridge.py` are now short scripts that call it; their commands and options are unchanged. `assets/review.html` is gone. A daily GitHub workflow (`.github/workflows/sync-notebook.yml`) keeps `notebook/` up to date.

## 1.0.0 · First release

An agent skill that finds the marks of AI writing in English text and rewrites it in natural English without touching its facts. It works in Claude Code, Codex and Gemini CLI and installs with `npx skills`. It is the English counterpart of the Turkish skill [İnsanlık öldü mü?](https://github.com/MesutARIDORU/insanlik-oldu-mu), written for English from the ground up rather than translated.

**Writing**
- **Fidelity to the facts:** no figure, organisation, source, anecdote or opinion that isn't in the source goes into the text. Missing information is marked with a placeholder or asked for. The strength of every claim is kept. In fiction, details added to a scene are listed in the table as "added detail".
- **Five modes:** diagnose, light touch, full rewrite, write from scratch and feedback round.
- **Text type and field:** the skill recognises the type (12 types, `references/genres.md`) and the field (9 fields, `references/sectors.md`) and works in their language. The field guides list the readers, the field's typical tells and the facts that would do harm if they changed (doses, rates, deadlines, legal notices).
- **Pattern catalog:** 51 coded patterns in six families (S structure and rhythm, R rhetorical moves, W words and register, T tone and chat, P punctuation and format, E evidence and fiction). Each has a before/after example, most have a field example, and each says when it is not a tell ("False alarm"), in `references/patterns.md`.
- **Flow rules:** 35 rules (F1–F35) built on English writing craft: sentence building, linking, rhythm, emphasis, certainty, word texture, the reader, instructions and narrative.
- **Idioms:** idioms grouped by work situation, each with the stiff phrasing it replaces; dose by text type, dead clichés, mangled idioms and confused pairs.
- **Jargon:** term tables for software, finance, health, law, public sector, e-commerce, HR, education and marketing, plus office jargon and buzzwords with what to say instead. The yardstick is the reader's actual usage.
- **Style:** dashes, commas, quotation marks, capitals, numbers, money, dates, times, abbreviations, contractions and US/UK spelling, citing the GOV.UK, Google developer documentation and digital.gov guides where the rule comes from them.

**Delivery**
- **Announcement in the chat:** as it starts, the skill writes `💀 Still Human❓ · Text type: … · Field: … · Approach: …` and carries on without waiting.
- **Delivery format:** a header line with the logo, the final text, a "What I changed and why" table, a measures line and at most three questions.
- **Preview question:** after delivering, the skill asks in the chat, with options, whether to show the changes on the review page. The text never waits for the answer.
- **Voice from a sample:** if the user gives a sample of their own writing, sentence length, register, address and word choice come from it; none of its facts do.

**Scripts**
- **Numeric audit (`scripts/audit.py`):** sentence length variety, runs of same-length sentences, repeated openers, opening -ing phrases, participle tails, em-dash density, semicolons, announced reveals, contrast framing, triads, AI vocabulary, buzzwords, brochure language, significance inflation, "serves as" for "is", inflated wording, hidden verbs, filler and hedge stacks, agentless passive, chat residue, sycophancy, e-mail formulas, office jargon, stock openings and closings, US/UK spelling mixes (Oxford -ize counts as UK), heading case, contractions, and Flesch reading ease with Flesch–Kincaid grade. Before and after values side by side. Guesses the type and field and prints the matching guides with `--guide`.
- **Review page (`scripts/review.py`):** a single-file, notebook-style page. Only the changed words are marked: medium weight with a very faint yellow highlighter. Clicking a change shows the earlier version, the reason and the options: keep, revert, "Suggest another", add a note. The agent's notes anchor each changed sentence, including deleted and inserted ones, so the page lines old and new sentences up even after a heavy rewrite.
- **Live bridge (`scripts/bridge.py`):** the page asks the agent for suggestions and sends the decisions straight to it. Three engines: the listening agent, a forked session (Claude Code and Codex) and a stateless call (Claude Code, Codex, Gemini CLI). The server listens on 127.0.0.1 only and needs a per-session token.
- **Setup script (`scripts/install.py`):** run from the copy `npx skills` installed, it does only the settings: Claude Code permissions, the Codex routing note, the Gemini CLI command and the bridge config. Run from a clone on a computer without Node.js, it links the skill into the chosen tools itself.

**Look**
- **Logo:** a skull and a red question mark. `💀 Still Human❓` in the chat, a hand-drawn skull on the review page.
- **Codex:** `agents/openai.yaml` gives the display name ("Still Human?"), the skull icon and a short description.
