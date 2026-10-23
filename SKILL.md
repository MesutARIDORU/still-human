---
name: still-human
description: >
  Still Human? Finds the marks that make English text read as AI-written and rewrites it in natural
  English without touching its facts or meaning. Explains every change in a table and, on request,
  opens a review page where each change can be kept, reverted or replaced. Use it when the user asks
  to "humanize", "make it sound human", "make it sound less like AI / ChatGPT", "de-AI", "it sounds
  robotic", "remove the AI tells", "rewrite this naturally", "tighten this up so it doesn't read like
  a bot"; when they want a LinkedIn post, blog post, e-mail, announcement, product copy, report,
  abstract or story to sound more human; when they ask "was this written by AI?"; when they want a
  text written from scratch in natural English; or when they paste a message that starts with
  "[Still Human? · feedback]". Do not use it for text in other languages (for Turkish text use
  insanlik-oldu-mu if it is installed) or when the user only wants a translation.
license: MIT
metadata:
  version: "1.3.1"
  display-name: "Still Human?"
compatibility: Any agent that can read files. The scripts need Python 3; without Python the measurements are made by hand.
allowed-tools:
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - AskUserQuestion
  - Bash(python3:*)
---

# Still Human?

This skill looks at an English text, finds what makes it read as machine-written, and rebuilds it the way a person who knows the subject would write it. Swapping words is not enough: it repairs the rhythm, the sentence skeletons and the line of reasoning. It shows every change with its reason and leaves the last word to the writer.

The name is always written **Still Human?**: two capitalised words and a question mark. Not "Still human", not "StillHuman", not "Still Human" without the question mark.

**Logo:** In the chat the skill signs as `💀 **Still Human❓**`: a skull at the front, a red question mark at the end. The review page carries the same pair in its title. The first line the user sees each time the skill runs, and the header line of the delivery, start with this logo. That is how the user knows the skill is at work. Use the logo on those two lines only, never inside the text.


## Three principles

**1. Fidelity to the facts.** Nothing goes in that is not in the source: no figures, percentages, dates, names of people or organisations, quotations, sources, anecdotes, and no opinion the writer does not hold. The most common mistake when humanizing AI text is to make it "concrete" by inventing numbers and stories. The reader publishes it and the invention goes out into the world. When the text needs to be concrete, there are four ways:
- Bring forward a fact that is already in the text.
- Make the claim smaller and plainer: "dropped" instead of "dropped significantly".
- Leave a placeholder: `[average reply time in the first week?]`.
- Ask the user at most three targeted questions.

Do not reverse the meaning, do not change the strength of a claim ("will" into "may", "may" into "will"), and never drop an item of information silently. The one exception is fiction: small physical and scene details added to show a feeling (a hand that won't keep still, keys dropped on the counter) belong to the storytelling. List them in the change table as "added detail" so the writer can take them out.

**2. The skeleton matters more than the words.** Word-level tells go stale within a year or two; models drop whatever word gets famous. Structural tells stay: sentences of the same length, the "not X, but Y" frame, everything in threes, a participle tail on every other sentence. If you repaint a pattern with synonyms and keep its skeleton, the pattern is still there. When you rewrite, change the skeleton first.

**3. Measure.** Humanizing leaves marks of its own: forced fragments, fake slips, slang sprinkled on every paragraph, lowercase affectation. Don't break sound human writing. Passive voice in a methods section is the right register there. A clean text that went through an editor is not AI-written. Look for clusters, not single words.


## Which job, which mode

| What the user says | Mode | What happens |
|---|---|---|
| "Was this written by AI?", "check it", "score it", "don't change anything, just tell me" | **Diagnose** | The text is not touched. The tells, their weight and the human marks are reported. |
| "Don't change too much", "just fix it", "light edit". Also academic, legal and official texts, and texts with strong human marks | **Light touch** | Only the flagged sentences change. Paragraph order, sequence and register stay. |
| "Humanize", "make it sound natural", "rewrite", "make it flow" | **Full rewrite** (default) | The skeleton is rebuilt; the facts and the order of the argument stay. |
| "Write this in natural English", "write a LinkedIn post about…" | **Write from scratch** | Written without falling into the patterns. No review page; a short note instead. |
| The message starts with "[Still Human? · feedback]" | **Feedback round** | The user's decisions are applied (see Feedback round). |

If the mode is unclear, use the default mode of the text type (see Text types). If that is unclear too, do a full rewrite. Say the mode at the start of the delivery. If the user wants a different one, switch in the second round.


## Workflow

**Command rules.** Run each script on its own; never chain it to another command with `;`, `&&` or `|`. To read files in the skill folder use the Read tool, not `cat`, `grep` or `sed`. Pass texts to the scripts on standard input instead of writing files; the script keeps them under a short name. Claude Code runs commands that follow these rules without asking; for the rest it asks the user every time.

**1. Identify and announce.** Read the text and decide:
- **Text type:** poetry, literary narrative, essay and opinion, personal writing, business correspondence, technical specification, technical documentation, academic writing, legal writing, news writing, marketing copy or social media. Add a subtype if it helps: "business correspondence · internal announcement".
- **Field:** the line of business the text is about: software, finance, health, education, law, public sector, retail...
- **Audience and register:** a developer team, the general public, customers? Formal or relaxed? US or UK spelling?
- **The writer's voice and human marks:** first person, humour, odd but specific details, fragments that do work, a regional idiom. If the human marks are strong, lean towards a light touch.
- **Writing sample:** if the user gave a sample of their own writing, take the voice from it: sentence length, register, how they address the reader, the words they reach for, their punctuation habits (do they use em dashes, semicolons, contractions?). Carry over no facts or sentences from the sample, only the voice. If the sample has AI tells of its own, don't count them as voice.

If the user named the text type, theirs stands. If the mode is unclear, use the type's default mode (see Text types).

Before calling any tool, write one line in the chat, then carry on without waiting:
```
💀 **Still Human❓** · Text type: literary narrative (short story) · Field: literature · Approach: light touch, dialogue and speech punctuation kept
```
In the approach, give the mode and what you will keep or focus on for this type. Keep the line short; the explanation comes with the delivery. The user knows the skill is at work from this line, so don't skip it.

**Measure.** Pass the text to the script on standard input:
```bash
python3 <skill-dir>/scripts/audit.py - --save before --guide <<'TEXT'
[the text itself, as it is]
TEXT
```
The script keeps the text as "before", prints the numeric audit and appends the guides for the genre and field it guessed. The first line of the report is the script's guess at the text type. The guess comes from surface clues. If it differs from your decision, look at the text again. If your decision changes, get the guide for the right type or field and use the new type in the delivery:
```bash
python3 <skill-dir>/scripts/audit.py --guide "Technical specification"
```
```bash
python3 <skill-dir>/scripts/audit.py --guide "Finance"
```
The genre guide says what not to touch, how AI leaves its mark in that genre and what language to write in. The field guide (`references/sectors.md`) says who reads the text, which facts would do harm if they changed (doses, rates, deadlines, legal notices) and the field's typical tells.

If Python is not available, estimate the measures and the type by hand. Remember that models are bad at counting: don't put a number in the report you are not sure of.

**2. Diagnose.** Mark the tells in the text using the pattern catalog below and weigh them:
- **Conclusive:** enough on its own, such as chat residue (T1).
- **Strong:** structural patterns, such as S1, S9, R1.
- **Weak:** proves nothing alone and matters only in a cluster, such as a single "crucial".

**3. Write.** Rebuild according to the mode and the text type. For each sentence, ask first: what information does it carry? If none (an empty truth, a stock opening, a template closing), cut it. If it carries information, give it the plainest skeleton, then build it in the language of the text type. The flow rules (F1–F35) do not all apply everywhere: the rhythm rules don't apply to poetry, specifications or legal text (see `references/genres.md`). Decide jargon, spelling and contractions by field and audience.

**4. Check.** Measure the new text against the old one:
```bash
python3 <skill-dir>/scripts/audit.py - --save after --before before <<'TEXT'
[the new text]
TEXT
```
Then ask yourself two questions:
- "What still makes this read as machine-written?"
- "Did I remove the pattern, or just change its clothes?" (R9)

Look for your own tics too:
- Does every paragraph end on a neat line?
- Did "Here's the thing:" or a colon reveal creep in?
- Does every closing land on a question?
- Did you add anything that breaks fidelity to the facts?

**5. Deliver, then ask about the preview.** Deliver the text first, in the output format below. Don't make the user wait for anything: the text and the table always come straight away.

After a light touch or a full rewrite, ask in the chat, with options, whether the user wants to see the review page:
- **If you have a multiple-choice question tool** (AskUserQuestion in Claude Code), use it. Question: "Do you want to see the changes on the review page?" Options, in this order:
  - "Preview (Recommended)": the review page opens in the browser and the decisions are made there.
  - "No thanks": the text stays as it is.
- **If there is no such tool** (Codex, Gemini CLI), end the delivery with: "Shall I open the review page? Just type **preview** or **no thanks**."

If the user picks "Preview", or types "preview" later, open the page live (see Review page), put its address in the chat, then start listening. If they pick "No thanks" or move on to something else, don't ask again.

Don't ask when:
- The user already asked for the page ("show me on the page", "preview"). Deliver with the page.
- The user said they don't want the page, or only wants the text.
- The mode is diagnose, write from scratch or feedback round.


## Text types

Each type has its own right language. The details, the clues and the AI tells of each type are in `references/genres.md`. The `audit.py --guide` command in step 1 prints the relevant section; read it before you start writing.

| Text type | Default mode | Don't touch | Focus |
|---|---|---|---|
| Poetry | Diagnose | Line breaks, stanzas, rhyme, metre, punctuation | Abstract imagery, consoling final lines. Rewrite only on request |
| Literary narrative | Light touch | Character voice, dialogue and its punctuation, plot | Named emotions, fiction clichés (E5), the narrative rules (F33–F35) |
| Essay and opinion | Full rewrite | The writer's view, thesis, irony | Aphorism endings, "not X, but Y", announced reveals |
| Personal writing | Full rewrite | What the writer lived through, their own words | Brochure voice, stock openings and closings, invented experience |
| Business correspondence | Full rewrite | Greeting and sign-off, names, titles, dates, amounts, the action asked for | Openings that don't get to the point, "I hope this email finds you well", "don't hesitate to reach out" |
| Technical specification | Light touch | "Shall / must / should", clause numbers, figures, units, standards | Untestable adjectives ("user-friendly", "seamless"), one requirement per clause |
| Technical documentation | Full rewrite | Code, commands, paths, parameters, UI labels | Promotional intros, over-explained terms (P7), step-by-step imperative |
| Academic writing | Light touch | Hedged claims, passive in methods, terms, citations | Significance inflation (R6), vocabulary cluster (W1), vague authority (E1) |
| Legal writing | Diagnose or light touch | Legal terms, clause structure, anything that could change meaning | Marketing voice mixed in. Ask before applying changes |
| News writing | Full rewrite | Quotes, sources, figures, dates, places | Opinion and praise leaking in, vague authority |
| Marketing copy | Full rewrite | The product's real features, prices, dates, conditions | Empty adjective piles (W9). A call to action is legitimate |
| Social media | Full rewrite | The writer's own emoji and hashtag habits | Announcement voice (T5), asking and answering (R3), slogan endings (T7) |


## Pattern catalog

The code, the sign and the remedy of each pattern are below. Longer before/after examples, field examples and false-alarm notes are in `references/patterns.md`. Read it when you are unsure about a pattern or want a good remedy.

### S · Structure and rhythm (the most durable tells)
- **S1 Metronome sentences.** Sentence after sentence of 15 to 25 words; paragraphs of the same height. Remedy: put a short sentence next to a long one (F11).
- **S2 Staccato chains.** "Fast. Simple. Secure." or "No fluff. No filler. Just results." in running prose. Remedy: join with commas and "and"; save a lone short sentence for real emphasis.
- **S3 Same openers.** "Additionally", "Moreover", "Furthermore" in a row, or "This…" / "It…" opening sentence after sentence. Remedy: let the idea make the transition (F7).
- **S4 Name loop.** The full name rebuilt in every sentence, or rotated through synonyms: "the company, the firm, the organisation, the brand". Remedy: introduce once, then refer (F9).
- **S5 Paragraphs that summarise themselves.** Every paragraph closes with "In short…" or a one-line moral. Remedy: end on the last real point and move on.
- **S6 Ending that replays the opening.** The intro lists what's coming and the conclusion lists it again. Remedy: end on something new, a next step, or the last idea.
- **S7 Threes everywhere.** Adjectives, examples and benefits always arrive in threes. Remedy: give as many as there are; don't round lists to three (F29).
- **S8 Missing steps.** Every sentence is fine alone but the bridge between them is missing. Remedy: write the step.
- **S9 Participle tails.** A clause of commentary hung on the end: ", highlighting the importance of…", ", ensuring a seamless…", ", underscoring its commitment to…". Remedy: cut the tail, or make it its own sentence with a subject who does something.

### R · Rhetorical moves
- **R1 Contrast framing.** "It's not X, it's Y", "not just X, but Y", "less about X and more about Y", "X isn't the problem. Y is." Remedy: say the positive thing plainly.
- **R2 Announced reveals.** "Here's the thing:", "The result?", "The truth is:", "Bottom line:". Remedy: say it first, name it afterwards if you must (F15).
- **R3 Asking and answering yourself.** "Why does this matter? Because…", "The answer? Simple." Remedy: state the point, or leave the question open (F16).
- **R4 False ranges.** "From small startups to global enterprises", "from your morning coffee to your evening commute". Remedy: list what is actually covered.
- **R5 Aphorisms and fake depth.** "Design is the language of trust." "And that makes all the difference." Remedy: write the concrete claim the aphorism is pointing at.
- **R6 Significance inflation.** "Plays a pivotal role", "a testament to", "marks a significant milestone", "now more than ever". Remedy: say what happened and let the reader judge its weight.
- **R7 Empty truths.** "Communication is key." "Trust takes time to build." Remedy: cut it, or turn it into a claim someone could disagree with.
- **R8 Both-sides wrap-up.** "While challenges remain, the opportunities are immense." Remedy: say which way the evidence points, or what is still unknown.
- **R9 Pattern in disguise.** The words changed but the skeleton didn't: "Rather than X, it's Y", "X? Hardly. Y." Remedy: pick one wing and drop the frame.

### W · Words and register
- **W1 AI vocabulary.** Delve, tapestry, testament, pivotal, crucial, intricate, multifaceted, realm, landscape, foster, embark, journey, showcase, underscore, vibrant, holistic, nuanced. One or two are normal; the tell is the cluster.
- **W2 Buzzwords.** Seamless, robust, cutting-edge, scalable, end-to-end, AI-powered, synergy, ecosystem, empower, leverage, streamline, best-in-class. Remedy: say what the product actually does (see Jargon).
- **W3 Term drift.** Three names for one thing, or the wrong audience's terms: spelled-out acronyms for engineers, team slang for customers. Remedy: the reader's term, and only one.
- **W4 Hidden verbs.** "Make a decision", "conduct an analysis", "the implementation of". Remedy: decide, analyse, implement (F3).
- **W5 "Serves as" for "is".** "Serves as", "stands as", "functions as", "boasts". Remedy: "is", "has".
- **W6 Filler and hedge stacks.** "It's important to note that", "it's worth mentioning", "may potentially", "could possibly help to". Remedy: cut it; one hedge is enough (F18).
- **W7 Agentless passive.** "Mistakes were made", "it was decided that", "priorities are set automatically". Remedy: name who does it; if nobody knows, don't invent someone (F2).
- **W8 Register whiplash.** "Hey folks!" next to "we hereby endeavour to". Remedy: one register.
- **W9 Brochure voice.** Hidden gem, breathtaking, nestled, unforgettable experience, awaits you, something for everyone. Remedy: give information.
- **W10 Always the likeliest word.** Every word is the first one that comes to mind; nothing surprises. Remedy: a few unexpected but exact choices. Don't reach for exotic words; reach for specific details.
- **W11 Inflated wording.** Utilise, facilitate, commence, endeavour, in order to, prior to, a myriad of, due to the fact that. Remedy: use, help, start, try, to, before, many, because (F21).

### T · Tone and chat
- **T1 Chat residue.** "I hope this helps!", "Certainly!", "As an AI language model", "Here's a revised version:", "Let me know if you'd like…". Conclusive. Remedy: delete it all.
- **T2 Sycophancy.** "Great question!", "You're absolutely right!" Remedy: start with the answer.
- **T3 Therapist voice.** "It's completely understandable to feel…", "You're not alone" in a text that isn't about feelings. Remedy: cut it.
- **T4 Fake candour.** "Let's be honest:", "I'll be real with you", "Let that sink in." Remedy: just say it.
- **T5 Tour-guide voice.** "Let's dive in", "In this article, we'll explore", "Buckle up", "Everything you need to know about". Remedy: start with the content.
- **T6 Stock openings.** "In today's fast-paced world", "In the ever-evolving landscape of", "In an era where", "Have you ever wondered". Remedy: make the first sentence carry information.
- **T7 Stock closings.** "In conclusion", "Ultimately", "The future is bright", "What do you think? Let me know in the comments." Remedy: end on new information, a plan or a scene; vary the ending from text to text.
- **T8 E-mail formulas.** "I hope this email finds you well", "I wanted to reach out", "Please don't hesitate to contact me", "Please find attached", "Just circling back". One may be the writer's habit; several are a template. Remedy: open with the purpose, close with the action.

### P · Punctuation and format
- **P1 Em-dash habit.** Dashes for asides and drama in every paragraph: "— and the results speak for themselves". The em dash is a proper English mark; the tell is the density. Remedy: comma, parentheses, colon or full stop; keep a dash only where it does work nothing else can. A dash that breaks off speech in dialogue stays.
- **P2 Semicolon swap.** The semicolon that replaced a removed dash, keeping the same two-beat frame. Remedy: break the frame itself.
- **P3 Bold sprinkling.** Every key term in bold. Remedy: keep bold for one or two things, or for UI labels in instructions.
- **P4 Labelled bullets.** "**Scalability:** It scales." or bullets for ideas that are not a list. Remedy: prose.
- **P5 Emoji decoration.** An emoji on every heading or bullet. Remedy: remove; if it's the writer's own habit, keep it sparing.
- **P6 Heading case drift.** Title Case in one heading and sentence case in the next, or "The Rise And Fall Of" with capitalised minor words. Remedy: one style; in title case, "and", "of", "the" stay lowercase.
- **P7 Over-explaining.** "API (Application Programming Interface)" for engineers; a gloss on every term. Remedy: don't explain what the reader knows.
- **P8 Consistency slips.** "Color" and "colour", "organize" and "organise" in one text; serial comma in one list and not the next; straight and curly quotes mixed. Remedy: one system, applied throughout.

### E · Evidence and fiction
- **E1 Vague authority.** "Experts say", "studies show", "research suggests". Remedy: name the source if it's in the text; otherwise own the claim or leave a placeholder. Never invent a source.
- **E2 Invented cases and figures.** "One client tripled their sales in two weeks." Remedy: remove it unless it's real, or say plainly that it's hypothetical.
- **E3 Gap filling.** "While specific details are limited, it is likely that…", "as of my last update". Remedy: say what isn't known, or cut the sentence.
- **E4 Template challenges paragraph.** "Despite these successes, X faces several challenges…" followed by "However, with continued…". Remedy: describe the real problem with the facts in the text.
- **E5 Fiction clichés.** "A wave of nostalgia washed over her", "a breath she didn't know she'd been holding", eyes holding "a mixture of grief and determination", "somewhere, a dog barked". Remedy: show the feeling through body and scene (F33).
- **E6 Over-correction.** Forced fragments, fake typos, slang on every line, lowercase affectation. The signature of humanizers themselves. Remedy: restraint.


## Tech and business jargon

The yardstick is the language the audience actually uses. Dictionary-correct alternatives that nobody says make a text sound artificial. Detailed tables are in `references/jargon.md`: software, finance, health, law, public sector, e-commerce, HR, education and marketing. Read it whenever you edit a technical or business text.

- **Developer and internal team text:** established terms stay: deploy, PR, merge, commit, sprint, backlog, release, staging. Spelling them out ("Pull Request (PR)", "Continuous Integration and Continuous Deployment (CI/CD)") for engineers is a tell (P7).
- **General readers:** the words people use: "goes live", "update", "sign in", "deadline". Not the team's slang: "shipped to prod", "we're blocked on infra".
- **Official and public-sector text:** plain English; short, common words over formal ones, with the reader as "you" where the house style allows.
- **Tells in any text:** buzzwords (W2), several names for one idea (W3), office jargon for the wrong audience ("circle back", "move the needle", "bandwidth" in a customer letter).
- **Never change:** code, commands, file and product names, interface labels, quotations.


## Flow rules

Removing a pattern is half the job. The space it leaves needs English's own tools. Each rule's explanation, the genres it suits and examples from different fields are in `references/flow.md`. Read it for any text with narrative or dialogue.

- **Building sentences:**
  - F1 Put the news first.
  - F2 Name the actor, then the action.
  - F3 Use the verb, not the noun made from it.
  - F4 Keep the subject close to its verb.
  - F5 Save the end of the sentence for what matters.
- **Linking sentences:**
  - F6 Start from what the reader already knows.
  - F7 Let the idea make the transition, not "Moreover".
  - F8 "And", "but" and "so" can start a sentence.
  - F9 Introduce once, then refer: full name, short name, pronoun.
  - F10 Join actions that belong together.
- **Rhythm:**
  - F11 Put a short sentence next to a long one.
  - F12 Let sentence length follow the tension.
  - F13 Vary the shape, not just the length.
- **Emphasis:**
  - F14 Let structure carry the emphasis: position, repetition, a short sentence.
  - F15 Say it first, name it afterwards.
  - F16 Don't ask what you're about to answer.
- **Certainty:**
  - F17 Match certainty to the evidence: will, should, may, might. Never turn one into another.
  - F18 One hedge per claim.
  - F19 Pick the reporting verb that is true: said, claimed, admitted, argued.
  - F20 Use the past perfect to step back in time, then return to the simple past.
- **Word texture:**
  - F21 Short plain verbs: use, help, start, buy, need.
  - F22 Phrasal verbs where the register allows: set up, find out, roll out.
  - F23 Contractions where the register allows.
  - F24 Name the concrete thing.
  - F25 Cut what changes nothing.
- **The reader:**
  - F26 Fix the address: "you", "we" or the organisation's name, and keep it.
  - F27 Talk to the reader where the genre lets you.
  - F28 Stance words, sparingly: frankly, admittedly, still, at least.
  - F29 Count honestly: "two or three people", not a tidy three.
- **Instructions and business text:**
  - F30 Put an example next to a rule.
  - F31 Short instruction, one reason.
  - F32 Lead with what the reader came for: what, when, where, how much.
- **Narrative and dialogue:**
  - F33 Show the feeling; don't name it.
  - F34 Let a character's thought slip into the narration.
  - F35 Keep dialogue tags plain: "said", "asked", or an action beat.

Idioms also add texture, with their own dose: at most one per paragraph, and only from `references/idioms.md` or ones you know for certain. The file groups idioms by work situation and text type, and lists the dead clichés and mangled idioms to avoid.


## Spelling, punctuation and style

Pick one spelling system (US or UK) and one set of conventions per text, following the writer, the house style or the audience. Consistency matters more than which convention you choose. Details, with the public style guides they come from, are in `references/style.md`.

- **Em dash (—):** a legitimate mark, and the most famous AI tell when it shows up in every paragraph (P1). In a rewrite, use commas, parentheses, colons or full stops for asides; keep a dash only where nothing else works, and keep a writer's dashes if their own sample uses them. In dialogue, a dash for speech that breaks off stays.
- **Serial comma:** some house styles always use it, others only to avoid ambiguity. Follow the text; the tell is mixing both.
- **Quotation marks:** US double with punctuation inside; UK often single, with punctuation placed by sense. Follow the text.
- **Headings:** sentence case or title case, one style per document (P6).
- **Contractions:** natural in e-mails, blogs, docs, social posts and most business writing; usually absent from legal text, specifications and much academic writing. Their total absence in a relaxed text is a mild tell.


## Leave-alone list

Touch the text less when you see these:
- **Things that are not AI tells:**
  - Flawless grammar.
  - Formal and academic registers.
  - An occasional "additionally" or "crucial".
  - A single punchy short sentence.
  - A casual "maybe" or "I think".
  - Unsourced but ordinary claims.
  - Patterns inside quotations, titles and proper names.
- **Human errors:** dangling modifiers, subject-verb disagreement, a logic slip, a missing word. People make these; models rarely do. Don't count them as tells; point them out separately and gently as grammar notes.
- **Human marks:**
  - Specific details that are hard to invent.
  - Mixed feelings.
  - References tied to a time, a place or a subculture.
  - The writer interrupting themselves.
  - Emotion leaking into punctuation (an ellipsis, an exclamation).
  - Fragments that do real work.
  - Regional spelling and idiom.

Detectors often mistake clean, plain human writing for AI. This skill's job is good English, not fooling a detector.


## Output format

The default delivery is below. If the user wants only the text, give only the text.

```
💀 **Still Human❓** · Full rewrite · Social media · 158 → 74 words

[final text]

**What I changed and why**

| # | Before | After | Why |
|---|--------|-------|-----|
| 1 | "In today's fast-paced digital landscape..." | (removed) | Stock opening; carries no information (T6) |
| 2 | "This isn't just a tool. It's a game-changer..." | (removed) | Contrast framing with nothing behind it (R1) |

**Measures:** sentence length variety 0.24 → 0.57 · em dashes 3 → 0 · alarms 6 → 0
**Questions for you:** [the placeholders you left and targeted questions, three at most]
**Review page:** [address] (only if the user asked for the page)
```

- **Header line:** the logo, the mode, the text type and the word count. The announcement line from step 1 stays where it was; don't repeat it in the delivery.
- **Table:** at most eight rows, the most important changes. Group repeated changes into one row ("passive → named actor, in 5 places"). Write the Why column in plain English and put the code in brackets.
- **Measures line:** only if the script ran. Take the numbers from the script; never make them up.
- **Questions line:** only if you left placeholders.
- **Diagnose mode:** instead of the final text, a "Verdict" line: strong tells / mixed / weak tells. Then a table of tells (tell, short quote, weight), the human marks and the measures. End with "I can do a light touch or a full rewrite if you like."
- **Write from scratch:** the text and a two- or three-sentence note saying which patterns you avoided on purpose and which facts you left as placeholders.


## Review page

If the user picked "Preview" after the delivery, asked for the page, or typed "preview" later, build an interactive review page. You need to be able to run Python and write files.

The page is a single HTML file that looks like a notebook sheet on a wooden desk:
- In the text, changed words sit on a green highlighter. Once the user approves a change, its original stays above the new text, struck through. Where something was deleted, a small "[deleted]" note sits. Questions in square brackets are orange.
- Each change has a numbered circle in the margin. The first sentence of its reason is written in the right margin as a short note.
- Clicking a change opens a taped note card with three parts: "Original" (the old sentence, struck through), "Suggested" (the new one and its reason) and "Other options" (the same sentence shorter, more formal and warmer). The user decides with "Apply the suggestion", "Keep the original", "Edit it myself" or the arrow next to an option, and can add a note.
- On a wide screen the card opens beside the page at the top, in a narrow window under the sentence, on a phone from the bottom of the screen. The last line of the page counts the approved changes.
- Hovering over a change opens a bubble that switches between its versions in place. The eye button (or the `p` key) shows the final text with the decisions applied and no marks.
- The user makes their decisions and presses "Send to agent". If the page was opened without the bridge, the button reads "Copy feedback" and the user pastes the message into the chat.

Building the page takes two steps. The original text was saved as "before" in step 1 and the final text as "after" in step 4; you don't need to write any files.
1. Prepare the reasons as JSON. The page splits changes sentence by sentence, so make **one entry per changed sentence**. Put the sentences into "before" and "after" exactly as they appear in the texts, character for character, in the order they occur. The page uses these entries as anchors, so even in a heavy rewrite every old sentence lines up with its new one. For a deleted sentence, leave "after" empty. The first sentence of a reason is written in the page's margin, so keep it short and put the detail in the second: "Contrast framing. The facts stayed, the pattern went."

   For every sentence that isn't deleted, write three more versions in "alternatives": shorter, more formal and warmer. The card shows them under "Other options" and the user picks one with a click. The options follow the same rules: no facts that aren't in the source, the claim keeps its strength, placeholders stay where they are. If a version doesn't suit the text type ("warmer" in a specification, say), leave it out.
   ```json
   {
     "title": "LinkedIn announcement",
     "mode": "Full rewrite",
     "profile": {
       "label": "Social media",
       "subtype": "company announcement",
       "sector": "software and technology",
       "audience": "general readers",
       "approach": "Announcement voice and slogan ending removed; the missing figure is asked for."
     },
     "changes": [
       {"before": "sentence in the original", "after": "sentence that replaced it", "reason": "short reason", "pattern": "R1",
        "alternatives": [
          {"kind": "Shorter", "text": "the sentence, shorter"},
          {"kind": "More formal", "text": "the sentence, more formal"},
          {"kind": "Warmer", "text": "the sentence, warmer"}
        ]}
     ]
   }
   ```
2. Run the script with the JSON on standard input:
   ```bash
   python3 <skill-dir>/scripts/review.py --before before --after after --notes - --live --open <<'JSON'
   {...notes in the format above...}
   JSON
   ```
   In "profile", write the decision you made in step 1. The page shows it at the top of the notebook as the "Text type". If you leave it out, the page uses the script's guess.

   `--live` serves the page through a local bridge, so the page can talk to you (see Live review). `--open` opens it in the browser. If the bridge can't start, the script says so and the page opens as a file. Put the address the script prints into the "Review page" line of the delivery.


## Live review

A page opened with `--live` has two extra features:
- **Ask for other options:** on the card, the user types a request such as "more casual" or "with an idiom" and asks the agent for two or three options. If the notes have no "alternatives", the card asks for the shorter, more formal and warmer versions this way too.
- **Send to agent:** the user sends their decisions straight to you instead of copying and pasting.

The bridge answers a suggestion request in one of three ways. The user picks the engine in Settings. With "auto", the order is:
1. **Listening agent:** if you are waiting with `bridge.py wait`, the request comes to you. This is the way with the most context.
2. **Forked session:** a copy of the chat that cannot use tools. It knows all the context, but in long chats it is slow and costly.
3. **Stateless call:** `claude -p`, `codex exec` or `gemini -p` without the chat history.

After opening the page and delivering, start listening:
```bash
python3 <skill-dir>/scripts/bridge.py wait
```
The command waits for an event (up to 9 minutes) and prints it:
- **Suggestion request:** write two or three options that follow the rules (fidelity to the facts, no patterns, fitting the text around them) and send them. If the request is "Write three options, in this order: shorter, more formal, warmer.", write exactly three, in that order: the card labels them by position. Then `wait` again.
  ```bash
  python3 <skill-dir>/scripts/bridge.py reply --request 4 --suggestion "..." --suggestion "..." --suggestion "..."
  ```
- **The user sent their decisions:** handle the text with the Feedback round steps. Then close the bridge: `bridge.py close`.
- **Timeout:** stop listening and tell the user. From now on suggestions come from a forked session or a stateless call. Once they've sent their decisions, typing "continue" in the chat is enough. When "continue" arrives, read the decisions:
  ```bash
  python3 <skill-dir>/scripts/bridge.py status
  ```

Where shell commands have a short time limit (Codex, for example), listen in a loop with `wait --timeout 50`, for about 9 minutes in total.

If the user picks one of the suggestions on the page, it arrives in the feedback as "SUGGEST ANOTHER" with the chosen text. Use it unchanged, like the user's own version.


## Feedback round

When the user pastes a message that starts with "[Still Human? · feedback]", handle the decisions like this:

- `#n REVERT`: bring back the original for that part.
- `#n SUGGEST ANOTHER`: use the text in the "user's version" line exactly as it is. If you see a pattern in it, mention it gently in a note, but don't change the user's choice.
- `#n KEEP, WITH NOTE`: keep the change. Read the note and, if needed, fine-tune that sentence in its direction.
- `General note`: apply it to the whole text, such as tone, length or register.
- `[Text with decisions applied] ... [/text]`: if this block is there, it is the basis of the second round. The decisions are already in it; apply only the notes on top.

Then measure again and deliver in the same output format. This time the table shows only the changes of this round. If the user is working with the review page and this round has more than three changes, build the page again. Don't ask the preview question again in this round.


## Example

**Before** (internal announcement, mixed audience):

> Hi team,
>
> In today's fast-paced business environment, efficiency is more important than ever. With that in mind, I'm thrilled to announce that we've officially rolled out our new expense platform — a game-changer for how we manage spending!
>
> This isn't just a new tool; it's a fundamental shift in how we work. Receipts can now be uploaded from your phone, approvals are routed automatically, and reimbursements are processed significantly faster.
>
> Ultimately, this is about empowering every one of you to focus on what truly matters. Thank you for being part of this exciting journey! 🚀

**First line in the chat** (step 1, then the work goes on):

💀 **Still Human❓** · Text type: business correspondence (internal announcement) · Field: finance · Approach: full rewrite, greeting kept, the missing figure asked for

**Delivery:**

💀 **Still Human❓** · Full rewrite · Business correspondence · 93 → 30 words

> Hi team,
>
> Our new expense platform is live.
>
> You can upload receipts from your phone, the platform routes approvals for you, and reimbursements are faster [by how much?].
>
> Thanks, everyone.

**What I changed and why**

| # | Before | After | Why |
|---|------|-------|-------|
| 1 | "In today's fast-paced business environment, efficiency is more important than ever." | (removed) | Stock opening and significance inflation; tells the reader nothing (T6, R6) |
| 2 | "I'm thrilled to announce that we've officially rolled out… — a game-changer…!" | "Our new expense platform is live." | The news first; the dash aside and the buzzword go (F1, P1, W2) |
| 3 | "This isn't just a new tool; it's a fundamental shift in how we work." | (removed) | Contrast framing with no fact behind it (R1) |
| 4 | "Receipts can now be uploaded…, approvals are routed automatically" | "You can upload receipts…, the platform routes approvals for you" | Named actors instead of agentless passives (W7, F2) |
| 5 | "processed significantly faster" | "faster [by how much?]" | No figure in the source, so it's asked for, not invented (E2) |
| 6 | "Ultimately, this is about empowering… exciting journey! 🚀" | "Thanks, everyone." | Stock closing, buzzword, journey metaphor and emoji (T7, W2, P5) |

**Questions for you:** If you know how much faster reimbursements are now, I'll put the figure in the brackets. If not, I'll drop that part.

The greeting "Hi team," stays as it was. It's the writer's choice, not a tell.


## Files

| File | When to read or run it |
|---|---|
| `references/genres.md` | The genre guides. `audit.py --guide` prints the relevant section, so you don't need to read the file separately |
| `references/sectors.md` | The field guides: readers, facts not to touch, typical tells, a before/after example. `audit.py --guide` prints the guessed field's section too |
| `references/patterns.md` | When you're unsure about a pattern, want an example remedy, or need to know whether a usage counts as a tell in this genre ("False alarm" notes) |
| `references/flow.md` | The flow rules in detail, and which rules suit which genre. Always for narrative and dialogue |
| `references/jargon.md` | Always for technical, software or field-specific business text |
| `references/style.md` | Dashes, commas, quotation marks, capitals, numbers, money, dates, times, abbreviations, US/UK spelling, contractions |
| `references/idioms.md` | Before using an idiom, or when you spot a dead cliché or a mangled idiom |
| `references/sources.md` | To show a user where the rules come from |
| `scripts/audit.py` | Measurement, text type guess, genre and field guides (step 1), before/after comparison (step 4). `--save` keeps the text, `--guide` prints guides, `--profile` prints only the guess |
| `scripts/review.py` | The interactive review page (if the user says "Preview" in step 5), with the bridge through `--live` |
| `scripts/bridge.py` | The live bridge: `wait`, `reply`, `status`, `close` |
| `scripts/install.py` | Setup: links the skill into agents, configures the bridge, runs a check |
| `notebook/`, `notebook.json` | The shared core of the review page and the bridge, and the skill's identity. Copied from the notebook-review repository; you don't need to read or change them. `review.py` and `bridge.py` use them |
