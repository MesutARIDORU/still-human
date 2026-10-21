# AGENTS.md snippet

For tools that read `AGENTS.md` (OpenCode, Amp, Jules and others), add the block below to the project's or the tool's `AGENTS.md`. Replace `<CLONE-PATH>` with the folder you cloned this repository into.

```markdown
## Still Human? (natural English rewriting)

When the user asks to humanize an English text, make it sound natural or less like AI,
remove AI writing patterns, or asks "was this written by AI?":

1. Read <CLONE-PATH>/SKILL.md and follow its steps.
2. Details are in <CLONE-PATH>/references, scripts in <CLONE-PATH>/scripts.
3. Add no information that is not in the text. Show every change with its reason in a table.
```
