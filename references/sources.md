# Where the rules come from

This file lists what the skill actually draws on. It cites only sources that were read while writing it; where a rule rests on general English usage or on the project's own testing, it says so.

## Public style guides

Read on 22 October 2026. `style.md` cites them by name for each rule taken from them; the wording in this skill is our own.

- **GOV.UK A to Z style guide** (UK Government Digital Service): abbreviations and acronyms, ampersands, bold, capitals and headings, contractions, dates, hyphens, "eg", "etc" and "ie", money, numbers, percentages, quotation marks, semicolons, times, job titles, and the list of words to avoid (deliver, facilitate, leverage, robust, going forward and others).
  https://guidance.publishing.service.gov.uk/writing-to-gov-uk-standards/style-guides/a-to-z-style-guide/
- **GOV.UK, Use clear language:** plain English, active voice, sentence and paragraph length, everyday words, "-ion" and "-ment" words, writing for specialists.
  https://guidance.publishing.service.gov.uk/writing-to-gov-uk-standards/writing-guidelines/clear-language/
- **Google developer documentation style guide:** the highlights page and the pages on contractions, dashes, numbers, dates and times, capitalization and serial commas.
  https://developers.google.com/style
- **digital.gov plain language guides** (US General Services Administration): "Writing for understanding" (active voice, present tense, hidden verbs), "Clear and short" (sentence and paragraph length), "Style" (wordy phrases, noun strings, abbreviations, "e.g." and "i.e.").
  https://digital.gov/guides/plain-language/writing

## Measurement

- **Flesch reading ease** and **Flesch–Kincaid grade level:** the two standard readability formulas for English, used in `audit.py`. Reading ease = 206.835 − 1.015 × (words per sentence) − 84.6 × (syllables per word); grade = 0.39 × (words per sentence) + 11.8 × (syllables per word) − 15.59. The script counts syllables with a vowel-group heuristic and a short list of exceptions, so its scores are close approximations, not exact values.
- **Sentence length variety** (coefficient of variation), runs of same-length sentences, sentence openers, dash density and the word lists in `audit.py` are this project's own measures. Their thresholds were set on the sample texts in `evals/` and are alarm bells, not a detector.

## General English usage

The flow rules (`flow.md`), the pattern catalog (`patterns.md`), the idioms (`idioms.md`) and the US/UK spelling table rest on general English usage and editing practice as it is commonly taught: active voice with a named actor, end focus, known-before-new, plain verbs over nominalisations, avoiding elegant variation, "said" as the default dialogue tag, and so on. They are written from scratch for this skill. All examples were written for this skill; none are quoted from published works.

## Field guides

`sectors.md` and `jargon.md` describe who reads texts in nine fields and which facts must not change. They rest on general knowledge of how these fields write, cross-checked against the plain-language guides above where those apply (public sector in particular). They are not legal, medical or financial advice: when a rewrite touches a regulated statement, the skill asks the text's owner.

## Usage and user feedback

Where a dictionary and real usage disagree, the skill follows usage: the term the audience actually says ("deploy" for engineers, "goes live" for customers). This principle comes from the user feedback that shaped this project's Turkish sibling skill and applies equally here.

## Our own test set

`evals/` holds eight sample texts (a LinkedIn post, a travel blog, an academic abstract, a short story scene, a genuinely human personal text, a developer wiki page, a bank e-mail, a patient leaflet) and the behaviour expected for each. They were written for this project.
