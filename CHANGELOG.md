# Changelog

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
