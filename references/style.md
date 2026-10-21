# Spelling, punctuation and style

English has no single authority. Publishers, governments, newspapers and companies each keep a house style, and they disagree on the serial comma, quotation marks, numbers and capitals. So the first rule is: **follow the text's own conventions, or the house style the writer names, and apply them consistently.** Mixing conventions inside one text is the tell (P8), not choosing one or the other.

Where this file says what a particular guide recommends, it cites a guide we actually read, listed at the end and in `sources.md`:
- **GOV.UK:** the UK government's A to Z style guide and its "Use clear language" guidance.
- **Google:** the Google developer documentation style guide.
- **digital.gov:** the US federal plain-language guidance.

Everything else is general English usage, given as such.

---

## Pick one spelling system

**US or UK, then stick to it.** Signs of each:

| US | UK |
|---|---|
| color, favor, behavior, neighbor | colour, favour, behaviour, neighbour |
| center, theater, fiber, liter | centre, theatre, fibre, litre |
| traveled, canceled, labeled, modeling | travelled, cancelled, labelled, modelling |
| defense, offense, license (noun and verb) | defence, offence, licence (noun) / license (verb) |
| analyze, catalog, gray, aging, judgment | analyse, catalogue, grey, ageing, judgement |
| percent | per cent (GOV.UK writes "per cent" in words) |
| program (all senses) | programme (TV, plan), program (software) |

**-ize or -ise:** US English uses -ize (organize, realize). British English uses both: -ise is more common, while "Oxford spelling" pairs -ize with other UK spellings (organize, colour). So "organize" in a UK text is not a mistake; "organize" and "organise" in the same text is. Some words take -ise everywhere: advertise, advise, compromise, exercise, surprise, supervise, televise.

**Leave alone:** proper names and quotations keep their own spelling: "World Health Organization" in a UK text, "Labour Party" in a US one.

`audit.py` lists the US and UK forms it finds and raises an alarm when a text mixes them.

## Dashes and hyphens

**Em dash (—).** A legitimate mark for a sharp break or an aside. Google's guide uses it without spaces on either side. In machine-written text it appears in nearly every paragraph, and as a drumroll before a reveal (P1). In a rewrite, prefer:
- a comma or a pair of commas for a light aside,
- parentheses for an aside the reader can skip,
- a colon when what follows explains or lists,
- a full stop when it's really a new sentence.

Keep a dash where nothing else works, keep the writer's own occasional dashes if their sample shows them, and keep a dash that breaks off speech in dialogue ("I didn't—").

**En dash (–).** Traditionally used for ranges (2019–2025) and in some UK styles, with spaces, in place of an em dash. Google's guide doesn't use en dashes at all and notes that a spaced en dash as an em dash isn't standard in US publishing. GOV.UK uses "to" instead of a dash for ranges of dates and times. Follow the text; never mix spaced en dashes and em dashes in one text.

**Hyphen (-).** Joins compound modifiers before a noun ("a well-known writer", "a two-week trial"), but usually not after it ("the writer is well known") and not after "-ly" adverbs ("a newly built road"). GOV.UK hyphenates only when the meaning would otherwise be unclear and lists words it writes solid: email, reuse, reopen.

## Commas

**Serial (Oxford) comma:** the comma before "and" or "or" at the end of a list: "red, white, and blue". Google's guide always uses it. Many news and some UK house styles leave it out unless it prevents ambiguity. Either is fine; mixing is not.

**After introductory phrases:** usual, especially when the phrase is long ("After the review closed, …"). Google's guide puts a comma after introductory words and phrases.

**Before "which":** use a comma for a non-restrictive clause ("The report, which came out on Monday, …"). US style often reserves "that" for restrictive clauses; UK style uses "which" for both.

## Semicolons and colons

**Semicolons** join two closely linked independent clauses, or separate list items that contain commas. GOV.UK avoids them and splits the sentence instead. The tell in machine text is a semicolon standing in for a deleted dash in a "statement; reveal" frame (P2).

**Colons** introduce an explanation, a list or a quotation. Google's guide lowercases the word after a colon unless it is a proper noun or starts a full quotation. The tell is the labelled colon: "Here's the thing:", "The result:" (R2).

## Quotation marks and apostrophes

- **US:** double quotation marks, single inside them; commas and full stops go inside the closing mark ("like this.").
- **UK:** often single quotation marks, double inside them; punctuation inside or outside according to sense. GOV.UK uses double quotes only for direct speech and quotations, and single quotes for unusual terms, titles and button labels.
- **Straight or curly:** pick one per text; don't mix " and ".
- **Apostrophes:** it's (it is) / its (belonging to it); plurals of acronyms and numbers take no apostrophe (PDFs, the 1990s).

## Capitals

**Headings:** sentence case ("How to reset your password") or title case ("How to Reset Your Password"). Google and GOV.UK both use sentence case for titles and headings; many publishers use title case. Choose one for the whole document. In title case, short articles, conjunctions and prepositions stay lowercase unless they're first: "The Rise and Fall of the Office", not "The Rise And Fall Of The Office" (P6).

**Job titles:** capitalised as part of a name or a specific title ("Chief Executive Jane Smith", "the Head of People"); lowercase when generic ("our engineers", "a head teacher"). GOV.UK follows this split.

**Emphasis:** don't use capitals for emphasis. Google's guide reserves all caps for names, acronyms and code.

**Product and brand names:** as the owner writes them: iPhone, GitHub, eBay, npm.

## Numbers

Two common systems:
- **Google:** spell out zero to nine, numerals from 10, with exceptions for versions, measurements, prices and steps, and for any small number in the same sentence as a larger one.
- **GOV.UK:** "one" in words, numerals for 2 and above, including in running text.

Shared by both: spell out a number that starts a sentence (or reword the sentence); use commas in numbers of four or more digits (1,200; GOV.UK from 1,000 up); use a leading zero for decimals (0.5).

**Ordinals:** GOV.UK writes first to ninth in words, then 10th. Google spells ordinals out.

**Percentages:** numeral and % with no space (40%). In words, US "percent", UK "per cent".

**Money:** currency symbol before the figure with no space ($1,250, £75). GOV.UK drops ".00" from whole pounds (£75, not £75.00) and writes "million" and "billion" in full. In finance texts, keep every figure exactly as written.

**Never change a figure** to match a style rule if doing so could change its meaning: rates, doses, amounts and clause numbers stay as the source writes them.

## Dates and times

**Dates:**
- US: "January 19, 2027" (Google's format).
- UK: "19 January 2027", no ordinal ("19th") and no comma (GOV.UK's format).
- Avoid all-numeric dates like 04/05/27, which mean different days in the US and UK. If a numeric date is needed, Google recommends ISO 8601: 2027-01-19.

**Times:**
- Google: 12-hour clock, capital AM/PM with a space ("3:45 PM", "3 PM").
- GOV.UK: lowercase without a space ("5:30pm", "10am to 11am"), and "midday" and "midnight" instead of "12pm" and "12am".
- 24-hour times (17:30) are normal in many international and technical contexts.

**Ranges:** Google uses a hyphen without spaces (5-10 minutes); GOV.UK uses "to" (10am to 4pm, 2 to 4 June). Whichever the text uses, keep it.

## Abbreviations

- **First use:** spell out an abbreviation the reader may not know, then use the short form. Well-known ones need no expansion (GOV.UK gives NHS and MP as examples; in tech, PDF and USB). For specialists, don't expand their everyday acronyms (P7, `jargon.md`).
- **Full stops:** GOV.UK writes acronyms without full stops (BBC, not B.B.C.). US style often keeps them in a few (U.S., a.m.).
- **e.g., i.e., etc.:** GOV.UK and digital.gov both advise "for example", "such as", "that is" instead. In technical writing they are common; follow the house style, and never mix "e.g." and "eg".
- **Ampersand:** "and" in running text; "&" in names and logos (GOV.UK).

## Contractions

- Google's guide recommends common contractions, including negative ones ("don't", "can't"), because a scanning reader can miss a "not".
- GOV.UK avoids negative contractions ("cannot", not "can't") and complex ones like "should've".
- Generally: natural in e-mails, blogs, documentation, social posts and most business writing; absent from contracts, specifications, formal letters and much academic writing.
- Never invent non-standard contractions ("the system'll", "it'd've").

## Lists

- Introduce a list with a lead-in line that makes sense with each item.
- Keep items parallel: all sentences, or all fragments starting the same way.
- Punctuate consistently: either full sentences with full stops, or fragments without.
- Don't bullet an argument; reasoning belongs in sentences (P4).

## Emphasis and formatting

- **Bold:** GOV.UK uses bold only for interface labels in instructions, never for emphasis. In general prose, keep bold for one or two things a reader must not miss (P3).
- **Italics:** titles of books and publications in many styles; foreign words not yet naturalised; occasional emphasis.
- **Exclamation marks:** at most one in a short text; none in news, legal, academic or technical writing.
- **Emoji:** in social posts, if it's the writer's habit; not in documents, letters or reports (P5).

## Plain-language guidance in short

The government guides agree on a handful of habits that also happen to be the opposite of machine prose:
- Use active voice and say who does what; passive is fine when the action matters more than the actor (GOV.UK, digital.gov).
- Prefer everyday words: "buy" not "purchase", "help" not "assist" (GOV.UK).
- Watch for words ending in "-ion" and "-ment" and for "make", "take", "have" with a noun: they often hide a verb (digital.gov, GOV.UK).
- Keep sentences short; GOV.UK suggests splitting any sentence over 25 words and keeping paragraphs to five sentences or fewer. Use this as a check, not a rule: varied length is what makes prose read as human (S1, F11).
- Replace wordy phrases: "in order to" → "to", "a number of" → "several" or "many", "at this point in time" → "now", "is able to" → "can" (digital.gov).
- Explain specialist terms at first use, even for specialists, if they're not everyday words for them (GOV.UK).

## Guides cited in this file

- GOV.UK, A to Z style guide: https://guidance.publishing.service.gov.uk/writing-to-gov-uk-standards/style-guides/a-to-z-style-guide/
- GOV.UK, Use clear language: https://guidance.publishing.service.gov.uk/writing-to-gov-uk-standards/writing-guidelines/clear-language/
- Google developer documentation style guide: https://developers.google.com/style (pages on contractions, dashes, numbers, dates and times, capitalization, serial commas)
- digital.gov, plain language guides: https://digital.gov/guides/plain-language/writing (with its "Clear and short" and "Style" pages)
