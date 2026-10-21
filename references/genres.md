# Text types

Every kind of text has its own right language. In a poem the line break is the writer's decision. In a specification "shall" states an obligation, and the "Kind regards" at the end of a business e-mail is there out of courtesy. Mistake them for AI tells and "fix" them, and you damage the text. For each type this file says:
- How do you recognise it?
- What do you leave alone?
- How does AI leave its mark in it?
- What language do you write in?

`audit.py --profile` makes a guess from surface clues. The guess is a hint; you read the text and decide. If a text sits between two types (a company announcement posted on LinkedIn, say), decide by the main reader and name both: "Social media · company announcement".

**Field** is the line of business the text is about: software, finance, health, law, education, public sector, retail, HR. The field decides the reader, the sensitive facts and the terms. Each field's guide is in `sectors.md` and its term tables are in `jargon.md`. For fiction and poetry the field is "literature".

---

## Poetry

**Clues:** short lines, little or no end-of-line punctuation, stanzas, sound patterns, rhyme.

**Don't touch:** line breaks, stanza shape, rhyme, metre, the poet's punctuation and capitalisation (or the lack of it), inverted word order. These are the poem.

**AI tells:**
- Images built from abstract nouns: "the tapestry of time", "whispers of hope", "the dance of light and shadow".
- Every stanza closing on comfort or uplift ("and still, I rise anew").
- Meaning bent to force a rhyme, especially a full rhyme on every second line.
- The vocabulary cluster: echoes, whispers, threshold, eternity, embrace, ethereal, tapestry.
- Every line the same length; rhyme so regular it sounds like a greeting card.

**How to write:** The default mode is **diagnose**. Don't rewrite a poem unless the user asks. Show the tells and say why without touching the lines. If the user asks for changes, use a light touch on the flagged lines only. Suggest a concrete object in place of an abstract image, but don't invent the object: ask. The flow rules (F1–F35) don't apply to poetry.

## Literary narrative

**Clues:** short story, novel, memoir. Dialogue in quotation marks, past-tense narration, named characters, scenes.

**Don't touch:** the characters' voices and registers, the dialogue and its punctuation (including a dash that breaks off speech), the writer's deliberate fragments and inversions, the narrator's person and tense, the plot.

**AI tells:** feelings named outright ("a wave of sadness washed over her"), two opposite feelings in the same eyes, every scene closing on a sentence of meaning ("In that moment, she knew everything would change"), fancy dialogue tags ("she breathed", "he husked"), stock atmosphere (a dog barking somewhere, rain hammering against the windows). See `patterns.md` E5.

**How to write:** the narrative rules (F20, F33–F35) do most of the work. List every physical detail you add to a scene in the table as "added detail". Leave the plot, the characters' decisions and the ending alone.

## Essay and opinion

**Clues:** a first-person view, an argument, questions to the reader, everyday examples, a column or op-ed format.

**Don't touch:** the writer's view and thesis, their irony, their personal examples.

**AI tells:** every paragraph ending on an aphorism, the "not X, but Y" frame, announced reveals ("Here's the uncomfortable truth:"), a conclusion that sees both sides and offends no one (R8).

**How to write:** if the writer has a voice, strengthen it; if not, don't invent one. Talking to the reader (F27), stance words (F28) and emphasis by position (F14) belong in this type.

## Personal writing

**Clues:** blog post, travel writing, a personal update. First person singular ("I went", "I realised"), a moment the writer lived through.

**Don't touch:** every detail of what the writer experienced, their own words, their jokes.

**AI tells:** brochure voice ("a breathtaking experience", "nestled in the heart of", "a hidden gem that awaits"), a stock opening and closing, generalisations that nobody lived ("there's something for everyone").

**How to write:** the concrete part is the writer's experience. If the experience isn't in the text, don't invent it: leave a placeholder or ask. A conversational tone is fine, but don't sprinkle slang (E6).

## Business correspondence

**Clues:** e-mail, memo, announcement, customer notice. A greeting ("Hi", "Dear"), a sign-off ("Best", "Kind regards"), an organisation speaking as "we" to the reader as "you".

**Don't touch:** the greeting and sign-off style (that's company culture), names and titles, dates, amounts, attachments, the action requested, any legally required wording.

**AI tells:**
- "I hope this email finds you well", "I hope you're doing well" as automatic openers.
- An opening that doesn't reach the point: "I'm reaching out to inform you of an important update regarding…".
- "Please don't hesitate to reach out if you have any questions or concerns."
- In an announcement, a stock opening ("In today's fast-paced business environment") and a slogan closing.
- Corporate warmth with nothing in it: "We truly value your loyalty", "our dedicated team is here to support you every step of the way".

**How to write:** the first sentence says why you're writing. The action needed and the deadline sit together in one clear sentence. The register is the organisation's. Internally, "Hi team" and contractions are natural; to a customer, follow the organisation's house style. No idioms or flourishes in a customer notice.

## Technical specification

**Clues:** numbered clauses, "shall", "must", "should", units of measure, "at least", "no more than", system and module names, acceptance criteria.

**Don't touch:** the modal verbs. "Shall" and "must" state an obligation, "should" a recommendation, "may" an option, and none of them can be swapped for another. Also clause numbers, figures, units, standard names (ISO 27001, AES-256, WCAG 2.2) and defined terms.

**AI tells:** untestable adjectives: "user-friendly", "seamless", "robust", "intuitive", "high-performance", "in appropriate formats". Decorative verbs: "shall facilitate", "will empower users to". Two requirements packed into one clause.

**How to write:** each clause states one testable requirement. Remove the vague adjective and put a criterion in its place. If the criterion isn't in the text, don't invent it; leave a placeholder: "The reporting module shall export reports in [which formats: PDF, CSV?]." No flow rules, idioms, contractions or varied rhythm here. Clauses that all have the same shape (S1) are not a tell in this type; that is how it should be.

## Technical documentation

**Clues:** installation guide, README, API reference, user guide, help article, patient or product instructions. Headings, code blocks, commands, imperative steps addressed to the reader ("Install", "Run", "Click").

**Don't touch:** code, commands, file paths, parameters, interface labels, version numbers, doses and safety warnings. They stay character for character.

**AI tells:** "In this comprehensive guide, we'll delve into…", "Let's get started!", emoji in headings, spelled-out acronyms for an expert reader (P7), three names for one concept (W3), "Happy coding! 🎉".

**How to write:** step by step, a short instruction and one reason (F31). One task per step. Terms stay the same throughout. Address the reader as "you" and use the imperative. If the readers are developers, the established terms stay as they are (see `jargon.md`).

## Academic writing

**Clues:** citations, "this study", methods, findings, hedged claims, passive voice in the methods.

**Don't touch:** careful hedging that reflects the evidence ("may", "is associated with"), the passive voice in methods, terms of art, citations, statistics and references to tables and figures.

**AI tells:** significance inflation ("plays a pivotal role", "underscores the critical importance"), the vocabulary cluster (W1: delve, multifaceted, intricate, landscape), vague authority (E1), a template "challenges and future directions" paragraph (E4), a closing sentence about "paving the way for future research".

**How to write:** the default mode is **light touch**. Keep the register; remove only the inflation and the filler. Never prop up an unsourced claim with an invented citation; ask the user. Don't turn "is associated with" into "causes".

## Legal writing

**Clues:** "hereby", "the Parties", "this Agreement", numbered clauses, "shall", "notwithstanding", names of statutes and regulations.

**Don't touch:** legal terms, set phrases, clause structure, capitalised defined terms, cross-references. Anything that could change the meaning.

**AI tells:** marketing or brochure language mixed into legal text, needless repetition, vague references ("the relevant provisions"), friendly padding in a notice that must be precise.

**How to write:** the default mode is **diagnose or light touch**. Put your suggestions in the table and ask the user before changing the text. Never make a change with legal consequences silently.

## News writing

**Clues:** a dateline ("LONDON (Reuters) –"), reporting verbs ("said", "announced", "according to"), names of organisations, figures, the most important fact first.

**Don't touch:** quotations, sources and their names, figures, dates and places.

**AI tells:** opinion and praise leaking in ("a landmark project that will transform the city"), brochure language, vague authority ("experts say"), a closing paragraph of significance.

**How to write:** a neutral voice. The most important fact in the first sentence. No first person and no addressing the reader. "Said" is the default reporting verb (F19).

## Marketing copy

**Clues:** a campaign, a discount, a call to action, exclamation marks, imperatives to the reader ("Discover", "Shop now", "Don't miss out").

**Don't touch:** the product's real features, prices, dates, conditions and legal small print, brand and product names.

**AI tells:** brochure voice (W9: unparalleled, exceptional, elevate your experience), piles of empty adjectives, an exclamation mark on every sentence, "Whether you're a… or a…, we've got you covered".

**How to write:** the call to action is legitimate in this type; keep it. But replace empty adjectives with a real feature of the product. If the feature isn't in the text, don't invent it; leave a placeholder.

## Social media

**Clues:** a LinkedIn, X or Instagram post. Emoji, hashtags, questions to followers ("Thoughts?"), very short paragraphs, "Excited to share…".

**Don't touch:** the writer's own emoji and hashtag habits, brand names, mentions.

**AI tells:** "Big news! 🚀", "I'm thrilled to announce…", asking and answering (R3), "not X, but Y" (R1), a slogan ending, every post closing with the same question to the audience (T7), "Let that sink in."

**How to write:** short, personal, one idea. If the audience is mixed, translate the team's jargon (see `jargon.md`).
