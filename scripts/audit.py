#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Still Human? · numeric audit

Counts the measurable features of an English text that often show up in AI-written prose.
It does not give a verdict like a detector would. Thresholds are alarm bells, not targets.

Usage:
  python3 audit.py text.txt
  python3 audit.py new.txt --before old.txt     # before → after comparison
  python3 audit.py text.txt --json              # machine-readable output
  python3 audit.py text.txt --guide             # also print the writing guides for the guessed genre and sector
  python3 audit.py --guide "Poetry"             # print the writing guide for a given genre
  python3 audit.py --guide "Finance"            # ...or for a given sector

Texts can come from standard input and be kept under a short name, so the agent never has to
write files of its own (in Claude Code that would ask for approval every time):
  python3 audit.py - --save before --guide <<'TEXT'
  ...original text...
  TEXT
  python3 audit.py - --save after --before before <<'TEXT'
  ...rewritten text...
  TEXT

Uses only the Python 3 standard library.
"""

import argparse
import json
import os
import re
import statistics
import sys
import tempfile
from collections import Counter

# ---------------------------------------------------------------- helpers

def norm(s):
    """Lowercases and straightens curly apostrophes, so word lists match either kind."""
    return s.lower().replace("’", "'").replace("‘", "'")


WORD_RE = re.compile(r"[^\W\d_]+(?:[-'’][^\W\d_]+)*|\d+(?:[.,]\d+)*%?")
LETTER_RE = re.compile(r"[^\W\d_]")

ABBREVIATIONS = {
    "mr", "mrs", "ms", "dr", "prof", "sr", "jr", "st", "vs", "etc", "e.g", "i.e", "inc", "ltd", "co", "corp",
    "no", "fig", "approx", "dept", "est", "al", "cf", "ca", "u.s", "u.k", "a.m", "p.m", "ph.d", "jan", "feb",
    "mar", "apr", "jun", "jul", "aug", "sep", "sept", "oct", "nov", "dec", "mon", "tue", "wed", "thu", "fri",
    "vol", "pp", "p", "ed", "eds", "rev", "gen", "col", "lt", "sgt", "mt", "ft", "min", "max", "tel", "ext",
}


def words(s):
    return WORD_RE.findall(s)


# common words the vowel-group rule gets wrong
SYLLABLE_EXCEPTIONS = {
    "every": 2, "everything": 3, "everyone": 3, "everywhere": 3, "everybody": 4, "something": 2, "sometimes": 2,
    "someone": 2, "somewhere": 2, "somebody": 3, "business": 2, "businesses": 3, "people": 2, "peoples": 2,
    "science": 2, "friend": 1, "friends": 1, "via": 2, "being": 2, "idea": 3, "ideas": 3, "area": 3, "areas": 3,
    "real": 1, "really": 2, "create": 2, "created": 3, "creates": 2, "naive": 2, "lion": 2, "riot": 2, "fuel": 2,
    "cruel": 2, "fire": 1, "hour": 1, "hours": 1, "our": 1, "every day": 3, "toward": 2, "towards": 2,
}


def _syllables(w):
    """Syllables in one plain word. A heuristic: vowel groups with the usual English corrections."""
    w = re.sub(r"[^a-z]", "", w)
    if not w:
        return 0
    if w in SYLLABLE_EXCEPTIONS:
        return SYLLABLE_EXCEPTIONS[w]
    if len(w) <= 3:
        return 1
    if w.endswith("ed") and not w.endswith(("ted", "ded")):
        w = w[:-2]
    elif w.endswith("es") and not w.endswith(("ses", "zes", "ces", "ges", "shes", "ches", "xes", "ies")):
        w = w[:-2]
    elif w.endswith("e") and not w.endswith(("le", "ee", "ye", "ie")):
        w = w[:-1]
    n = len(re.findall(r"[aeiouy]+", w.lstrip("y")))
    # vowel pairs that are usually two syllables: tri-al, ra-di-o, ac-tu-al, vi-de-o, cre-ate
    n += len(re.findall(r"ia|(?<![tscg])io|ua|uo|eo|iu|ea(?=t|te|lit|lis)|(?<![ct])ie(?=[nt])|oe(?=[mt])", w))
    return max(1, n)


def count_syllables(word):
    if re.match(r"\d", word):
        return max(1, len(re.sub(r"\D", "", word)))  # a rough reading length for figures
    return max(1, sum(_syllables(part) for part in re.split(r"[-'’]", word.lower()) if part))


def count_terms(terms, lower_text):
    """Counts occurrences of each term that start at a word boundary."""
    found = Counter()
    for t in terms:
        n = len(re.findall(r"(?<![\w-])" + re.escape(t), lower_text))
        if n:
            found[t] = n
    return found


def count_patterns(patterns, lower_text):
    """Counts (label, regex) patterns; returns {label: count} for the ones found."""
    found = Counter()
    for label, rx in patterns:
        n = len(re.findall(rx, lower_text))
        if n:
            found[label] = n
    return found


# ---------------------------------------------------------------- word lists

AI_WORDS = [
    "delve", "delving", "delved", "tapestry", "testament to", "pivotal", "crucial", "intricate", "intricacies",
    "multifaceted", "realm", "landscape of", "evolving landscape", "ever-evolving", "ever-changing",
    "navigate the complexit", "navigating the complexit", "foster", "embark", "journey", "unlock the",
    "unlocking the", "unlocks the", "elevate your", "elevate the", "elevating", "showcas", "underscor", "boasts",
    "vibrant", "game-chang", "game chang", "holistic", "nuanced", "meticulous", "commendable",
    "paramount", "bustling", "myriad", "plethora", "beacon", "resonate", "resonates", "resonating",
    "transformative", "groundbreaking", "revolutioniz", "revolutionis", "harness the", "harnessing the",
    "the power of", "invaluable", "indelible", "enduring legacy", "captivat", "profound", "noteworthy",
    "symphony of", "dance of", "treasure trove", "labyrinth", "in the heart of", "embrace the", "rich history",
    "key takeaway", "deep understanding", "comprehensive", "nothing short of", "a tapestry",
]

BROCHURE = [
    "hidden gem", "breathtaking", "enchanting", "unforgettable", "must-visit", "must-see", "bucket list",
    "something for everyone", "stunning", "picturesque", "awe-inspiring", "world-renowned", "second to none",
    "feast for the senses", "nestled", "charming", "idyllic", "awaits", "look no further", "a true gem",
    "off the beaten path", "like no other", "sure to delight", "unrivalled", "unrivaled", "exquisite",
    "immerse yourself", "a haven", "a paradise", "truly unique", "one of a kind", "elevated experience",
]

TECH_BUZZWORDS = [
    "digital transformation", "end-to-end", "scalable", "scalability", "seamless", "robust", "cutting-edge",
    "state-of-the-art", "next-generation", "next-gen", "ai-powered", "ai-driven", "data-driven", "innovative",
    "synergy", "synergies", "ecosystem", "best-in-class", "world-class", "empower", "streamlin", "leverag",
    "future-proof", "mission-critical", "paradigm", "value proposition", "actionable insight", "frictionless",
    "turnkey", "disrupt", "revolutionary", "unparalleled", "optimize your", "optimise your", "one-stop shop",
    "supercharge", "best practices",
]

LATINATE = [
    "utiliz", "utilis", "facilitat", "commence", "endeavo", "in order to", "prior to", "subsequent to",
    "in the event that", "at this point in time", "is able to", "are able to", "on a daily basis",
    "on a weekly basis", "on a monthly basis", "on a regular basis", "with regard to", "with regards to",
    "in regard to", "with respect to", "due to the fact that", "for the purpose of", "in light of the fact",
    "ascertain", "a number of", "in terms of", "in close proximity", "the majority of", "in excess of",
    "has the ability to", "have the ability to", "in a timely manner",
]

SIGNIFICANCE = [
    "plays a pivotal role", "plays a crucial role", "plays a key role", "plays a vital role", "plays a significant role",
    "play a pivotal role", "play a crucial role", "play a key role", "play a vital role", "play a significant role",
    "a testament to", "marks a significant", "marking a significant", "a pivotal moment", "a significant milestone",
    "underscores the importance", "highlights the importance", "highlighting the importance", "cannot be overstated",
    "more important than ever", "now more than ever", "setting the stage", "sets the stage", "leaves a lasting",
    "left a lasting", "indelible mark", "shaping the future", "shape the future", "a new era", "redefine",
    "redefining", "reshape", "reshaping", "watershed moment", "turning point",
]

COPULA_DODGES = ["serves as", "serve as", "serving as", "stands as", "stand as", "functions as", "boasts a", "boasts an"]

FILLER = [
    "it's important to note", "it is important to note", "it's worth noting", "it is worth noting", "worth mentioning",
    "it should be noted", "needless to say", "it goes without saying", "it is essential to", "it's essential to",
    "it is crucial to", "it's crucial to", "in essence", "at its core", "the fact that", "it's important to remember",
    "it is important to remember", "it's important to understand", "it is important to understand",
    "may potentially", "could potentially", "might potentially", "can potentially", "could possibly",
    "may possibly", "might possibly", "to some extent", "generally speaking", "it can be argued",
    "it could be argued", "in many ways", "first and foremost", "last but not least", "each and every",
]

HEDGES = r"\b(may|might|could|possibly|potentially|perhaps|somewhat|arguably|likely|seems?|appears? to|tends? to|generally|relatively|to some extent|in some cases)\b"

CHAT_LEFTOVERS = [
    "as an ai", "as a language model", "as an ai language model", "i hope this helps", "hope this helps",
    "i hope that helps", "let me know if you", "feel free to ask", "feel free to let me know", "certainly!",
    "here's a revised", "here is a revised", "here's the rewritten", "here's an improved", "here is an improved",
    "here's a polished", "regenerate response", "as of my last", "knowledge cutoff", "i don't have access to real-time",
    "would you like me to", "if you'd like, i can", "is there anything else", "i can't browse",
    "[insert", "certainly, here", "sure, here's", "absolutely! here",
]

SYCOPHANCY = [
    "great question", "excellent question", "what a great question", "fantastic question", "you're absolutely right",
    "you are absolutely right", "what a fantastic", "what a wonderful", "that's a great point", "brilliant question",
    "i love this idea", "love this question",
]

# e-mail formulas that make a message read as generated when they pile up
MAIL_CLICHES = [
    ("hope this email finds you well", r"hope (this|my|the) (e-?mail|message|note|letter) finds you"),
    ("hope you're doing well", r"hope you('re| are) (doing well|having a (great|good|wonderful|lovely))"),
    ("wanted to reach out", r"(wanted|want|writing|am writing|i'm writing) to reach out|reaching out (to you )?(regarding|about|to)"),
    ("don't hesitate to contact", r"(do not|don't) hesitate to (contact|reach|get in touch|ask|let)"),
    ("please find attached", r"please find (attached|enclosed|below)|attached please find"),
    ("just following up", r"just (wanted to )?follow(ing)? up|just checking in|circling back on"),
    ("thank you for your consideration", r"thank you for your (time and )?consideration"),
    ("at your earliest convenience", r"at your earliest convenience"),
    ("i trust this message", r"i trust (this|that) (e-?mail|message|letter) "),
    ("as per", r"(?<!\w)as per (our|your|my|the) "),
]

STOCK_OPENINGS = [
    "in today's", "in an era", "in the ever-evolving", "in an ever-changing", "ever-changing world", "fast-paced",
    "rapidly evolving", "rapidly changing", "in the world of", "in the realm of", "when it comes to",
    "have you ever wondered", "imagine a world", "picture this", "in recent years", "now more than ever",
    "in an increasingly", "as technology continues", "it's no secret that", "it is no secret that", "let's face it",
    "in the digital age", "in this day and age", "in a world where",
]

STOCK_CLOSINGS = [
    "in conclusion", "in summary", "to sum up", "to summarize", "to summarise", "ultimately", "overall,",
    "all in all", "at the end of the day", "the future is bright", "the future looks bright",
    "the possibilities are endless", "what do you think", "let me know in the comments", "share your thoughts",
    "drop a comment", "here's to", "remember,", "remember:", "the choice is yours", "just beginning",
    "one thing is certain", "only time will tell", "stay tuned", "together, we can", "let's build",
    "the sky's the limit", "the rest is history", "a brighter future",
]

CONNECTIVE_OPENERS = [
    "additionally", "moreover", "furthermore", "in addition", "however", "therefore", "thus", "hence",
    "consequently", "ultimately", "overall", "notably", "importantly", "indeed", "in conclusion", "in summary",
    "as a result", "on the other hand", "that said", "with that in mind", "in essence", "essentially",
    "crucially", "interestingly", "similarly", "likewise", "in fact", "by doing so", "in doing so",
]

OFFICE_JARGON = [
    "circle back", "touch base", "bandwidth", "deep dive", "low-hanging fruit", "move the needle", "alignment",
    "align on", "take this offline", "take it offline", "double-click on", "action item", "actionable", "loop in",
    "looping in", "stakeholder", "deliverable", "boil the ocean", "north star", "pain point", "value-add",
    "quick win", "learnings", "ideate", "operationaliz", "socializ", "net-net", "hard stop", "eod", "asap",
    "per my last email", "going forward", "on my radar", "level set", "blocker", "sync up", "deck",
]

PARTICIPLE_TAIL = (r",\s+(highlighting|underscoring|emphasi[sz]ing|showcasing|reflecting|ensuring|making|allowing|"
                   r"enabling|fostering|providing|creating|offering|contributing|paving|solidifying|cementing|"
                   r"demonstrating|signal+ing|marking|reinforcing|illustrating|revealing|setting|positioning|"
                   r"leaving|helping|driving|shaping|transforming|bringing)\b")

CONTRAST_FRAMES = [
    r"\bnot (just|only|merely|simply) (a |an |the |about )?[^.!?\n]{1,70}?\b(but|it's|it is|they're|we're|this is)\b",
    r"\b(it|this|that)'s not (about )?[^.!?\n]{1,50}?[,;—–] ?(it|this|that)'s\b",
    r"\b(it|this|that) (is|was) not (about )?[^.!?\n]{1,50}?[,;—–] ?(it|this|that) (is|was)\b",
    r"\b(isn't|is not|wasn't|aren't|are not) (just|only|merely|simply) [^.!?\n]{1,50}[.!] (it's|it is|they're|this is|we're)\b",
    r"\bisn't (just )?about [^.!?\n]{1,60}?[,;.—–] ?(it's|it is) about\b",
    r"\bless about [^.!?\n]{1,50}? (and )?more about\b",
    r"\b(no|not) [^.!?\n]{1,30}[.] (no|not) [^.!?\n]{1,30}[.] (just|only)\b",
    r"\bisn't the (problem|point|issue|goal)[.,;] ?[^.!?\n]{1,40}? is\b",
]

LABEL_PATTERN = re.compile(
    r"(?:^|[.!?]\s+|\n)\s*(here's the (thing|kicker|catch|truth|deal|problem|reality|secret|twist|best part)|"
    r"the (truth|result|answer|catch|kicker|problem|bottom line|takeaway|lesson|reality|secret|key|difference|"
    r"reason|good news|bad news|best part|upshot|verdict)( is)?|the short answer|the real (question|problem|issue|answer)|"
    r"here's why|here's what|here's how|bottom line|spoiler( alert)?|plot twist)\s*[:?—]"
)

EMOJI_RE = re.compile(
    "[\U0001F300-\U0001FAFF\U00002600-\U000027BF\U0001F000-\U0001F2FF\U00002B00-\U00002BFF]"
)

CONTRACTION_RE = re.compile(r"\b\w+(n't|'re|'ll|'ve|'m|'d)\b|\b(it|that|there|here|what|who|he|she|let|where|how)'s\b")
FULL_FORM_RE = re.compile(
    r"\b(do not|does not|did not|is not|are not|was not|were not|cannot|can not|will not|would not|should not|"
    r"could not|have not|has not|had not|it is|that is|there is|we are|you are|they are|i am|we will|you will|"
    r"it will|we have|you have|i have|let us)\b"
)

PASSIVE_RE = re.compile(
    r"\b(is|are|was|were|be|been|being)\s+(?:\w+ly\s+)?(\w+ed|known|made|done|given|taken|seen|shown|written|built|"
    r"chosen|found|held|kept|left|lost|meant|paid|put|run|said|sent|set|sold|spent|told|understood|won|begun|broken|"
    r"brought|bought|caught|drawn|driven|fallen|felt|forgotten|frozen|grown|hidden|led|lent|risen|shut|spoken|"
    r"stolen|struck|taught|thrown|worn|drawn|chosen)\b(?![-\w])"
)
NOT_PASSIVE = {"interested", "excited", "tired", "worried", "pleased", "surprised", "concerned", "thrilled",
               "delighted", "bored", "scared", "married", "supposed", "used", "based", "located", "involved",
               "committed", "dedicated", "focused", "excited", "convinced", "determined", "satisfied", "disappointed",
               "embarrassed", "confused", "amazed", "annoyed", "exhausted", "frustrated", "relieved", "stressed",
               "need", "speed", "seed", "feed", "bed", "red", "shed", "bred", "fled", "led"}

HIDDEN_VERB_RE = re.compile(
    r"\b(make|makes|made|making|take|takes|took|taking|conduct\w*|perform\w*|carry out|carries out|carried out|"
    r"provide|provides|provided|give|gives|gave|given|reach|reached|reaches|undertake\w*|achieve\w*)\s+"
    r"(a |an |the |some |further |an initial |a thorough |a full )?"
    r"(\w+(?:tion|sion|ment|ance|ence|ysis|ison|sal|val))\b"
)
NOMINAL_RE = re.compile(r"\b\w{4,}(tion|sion|ment|ance|ence|ity|ness)s?\b")

ACRONYM_EXPANSION_RE = re.compile(r"\b[A-Z]{2,6}s?\s*\((?:[A-Z][a-z]+[\s-]?){2,6}\)|\((?:[A-Z][a-z]+[\s-]?){2,6}\)\s*[A-Z]{2,6}\b")

SENTENCE_START_ING_RE = re.compile(r"^[\"“‘(]?([A-Z][a-z]+ing)\b[^.!?]{0,80}?,")

# US and UK spellings of the same word: a text should keep to one side
US_UK_PAIRS = [
    ("color", "colour"), ("favor", "favour"), ("honor", "honour"), ("labor", "labour"), ("behavior", "behaviour"),
    ("neighbor", "neighbour"), ("flavor", "flavour"), ("humor", "humour"), ("rumor", "rumour"), ("harbor", "harbour"),
    ("center", "centre"), ("theater", "theatre"), ("fiber", "fibre"), ("liter", "litre"), ("catalog", "catalogue"),
    ("defense", "defence"), ("offense", "offence"), ("gray", "grey"), ("aging", "ageing"), ("judgment", "judgement"),
    ("acknowledgment", "acknowledgement"), ("skeptical", "sceptical"), ("aluminum", "aluminium"),
    ("pediatric", "paediatric"), ("anesthesia", "anaesthesia"), ("hemoglobin", "haemoglobin"),
    ("orthopedic", "orthopaedic"), ("diarrhea", "diarrhoea"), ("estrogen", "oestrogen"), ("enroll", "enrol"),
    ("fulfill", "fulfil"), ("percent", "per cent"), ("mold", "mould"), ("plow", "plough"), ("cozy", "cosy"),
    ("jewelry", "jewellery"), ("program", "programme"),
]
# words that double their final l in UK spelling when a suffix is added
DOUBLE_L = ["travel", "cancel", "model", "label", "signal", "fuel", "level", "total", "counsel", "marvel", "channel"]
# -ize / -ise verbs that really do vary (advertise, compromise, surprise and the like are -ise everywhere)
IZE = ["organiz", "realiz", "recogniz", "prioritiz", "optimiz", "customiz", "finaliz", "summariz", "emphasiz",
       "utiliz", "minimiz", "maximiz", "apologiz", "categoriz", "characteriz", "criticiz", "standardiz", "authoriz",
       "visualiz", "personaliz", "normaliz", "specializ", "stabiliz", "familiariz", "memoriz", "modernize",
       "monetiz", "mobiliz", "localiz", "initializ", "synchroniz", "digitiz", "capitaliz", "centraliz",
       "analyz", "paralyz", "catalyz"]
IZE_SUFFIXES = r"(e|es|ed|ing|er|ers|ation|ations)"


def us_uk_forms(lower):
    """Returns the distinct US-only and UK-only spellings found, and the -ize and -ise forms found.

    -ize is not a US marker on its own: British "Oxford spelling" pairs it with colour and centre.
    So a text mixes systems if it has US-only and UK-only forms, or both -ize and -ise forms.
    """
    us, uk, ize, ise = set(), set(), set(), set()
    for a, b in US_UK_PAIRS:
        for form, bucket in ((a, us), (b, uk)):
            for m in re.findall(r"(?<![\w-])" + re.escape(form) + r"(s|ed|ing|ful|ist|ists)?(?![\w-])", lower):
                bucket.add(form + m)
    for stem in IZE:
        base = stem[:-1]
        if stem == "modernize":
            base = "moderni"
        for m in re.finditer(r"(?<![\w-])" + base + r"([zs])" + IZE_SUFFIXES + r"(?![\w-])", lower):
            if base in ("analy", "paraly", "cataly"):
                # analyze / analyse is a US / UK pair, not an Oxford -ize choice
                (us if m.group(1) == "z" else uk).add(m.group(0))
            else:
                (ize if m.group(1) == "z" else ise).add(m.group(0))
    for w in DOUBLE_L:
        for m in re.finditer(r"(?<![\w-])" + w + r"(l?)(ed|ing|er|ers)(?![\w-])", lower):
            (uk if m.group(1) else us).add(m.group(0))
    # "program" is US for every sense, but UK writers use it for computer programs too: count only the UK-only form
    us.discard("program")
    us.discard("programs")
    return sorted(us), sorted(uk), sorted(ize), sorted(ise)


MINOR_WORDS = {"a", "an", "the", "and", "but", "or", "nor", "for", "so", "yet", "of", "in", "on", "at", "to", "by",
               "up", "as", "via", "with", "from", "into", "over"}


def heading_case(headings):
    """Classifies headings as title case or sentence case; lists minor words capitalized inside a heading."""
    title, sentence, minor_caps = 0, 0, []
    for h in headings:
        tokens = [t for t in re.findall(r"[A-Za-z][\w'’-]*", h)]
        if len(tokens) < 3:
            continue
        rest = tokens[1:]
        content = [t for t in rest if t.lower() not in MINOR_WORDS and not t.isupper()]
        if not content:
            continue
        capitalized = sum(1 for t in content if t[0].isupper())
        if capitalized == len(content):
            title += 1
            minor_caps += [t for t in rest if t.lower() in MINOR_WORDS and t[0].isupper()]
        elif capitalized <= len(content) / 3:
            sentence += 1
    return title, sentence, minor_caps


STOPWORDS = set("""a an the and or but if then so of to in on at by for with from as is are was were be been being it its
this that these those we you they he she i our your their his her my me us them not no yes do does did have has had will
would can could should may might must there here what which who whom when where why how all any each more most other some
such than too very just also only about into over after before up out""".split())


# ---------------------------------------------------------------- parsing

def parse(text):
    """Splits the text into headings, paragraphs and sentences; counts formatting marks."""
    raw = text
    text = re.sub(r"```.*?```", "\n", text, flags=re.S)

    headings = []
    dialogue_lines = 0
    blocks, block = [], []
    for line in text.splitlines():
        st = line.strip()
        if not st:
            if block:
                blocks.append(block)
                block = []
            continue
        if re.match(r"#{1,6}\s", st):
            headings.append(re.sub(r"^#{1,6}\s+", "", st))
            if block:
                blocks.append(block)
                block = []
            continue
        if re.match(r"^\|.*\|$", st) or re.match(r"^[-*_]{3,}$", st):
            continue  # table rows and horizontal rules are not prose
        st = re.sub(r"^>\s?", "", st)
        is_item = bool(re.match(r"^([-*+•]|\d+[.)])\s+", st))
        st = re.sub(r"^([-*+•]|\d+[.)])\s+", "", st)
        if re.match(r"^[\"“]", st):
            dialogue_lines += 1
        block.append((st, is_item))
    if block:
        blocks.append(block)
    kept, frame_lines = strip_correspondence_frame(blocks)
    frame_words = sum(len(words(line)) for b in blocks for line, _ in b) - sum(len(words(line)) for b in kept for line, _ in b)
    blocks = kept

    paragraphs, sentences, paragraph_sentences = [], [], []
    for b in blocks:
        if any(m for _, m in b) or len(b) > 1 and all(len(words(s)) < 12 for s, _ in b):
            parts = [s for s, _ in b]  # list or verse: every line is its own unit
        else:
            parts = [" ".join(s for s, _ in b)]
        paragraphs.append(" ".join(parts))
        ps = []
        for part in parts:
            ps.extend(split_sentences(part))
        paragraph_sentences.append(ps)
        sentences.extend(ps)

    return {
        "raw": raw,
        "plain": "\n\n".join(paragraphs),
        "headings": headings,
        "paragraphs": paragraphs,
        "paragraph_sentences": paragraph_sentences,
        "sentences": sentences,
        "dialogue_lines": dialogue_lines,
        "frame_lines": frame_lines,
        "frame_words": frame_words,
    }


GREETING_LINE_RE = re.compile(r"^(hi|hello|hey|dear|good morning|good afternoon|good evening|greetings|hiya)\b[^.!?]{0,60}[,!:]?$")
CLOSING_LINE_RE = re.compile(r"^(best|best regards|kind regards|warm regards|warmest regards|regards|thanks|thank you|many thanks|"
                             r"cheers|sincerely|yours sincerely|yours faithfully|yours truly|all the best|warmly|talk soon|"
                             r"thanks again|with thanks|respectfully)\b[^.!?]{0,30}[,.!]?$")


def strip_correspondence_frame(blocks):
    """Removes a letter's frame (greeting line, closing line and the signature below it).

    These short lines are conventions, not prose: counted as sentences they would trigger
    the short-sentence and same-opening alarms in every e-mail.
    """
    removed = 0
    if blocks and len(blocks[0]) == 1:
        first = norm(blocks[0][0][0])
        if len(words(first)) <= 8 and GREETING_LINE_RE.match(first):
            removed += 1
            blocks = blocks[1:]
    for b in range(max(0, len(blocks) - 2), len(blocks)):
        for i, (line, _) in enumerate(blocks[b]):
            if len(words(line)) <= 5 and CLOSING_LINE_RE.match(norm(line)):
                removed += len(blocks[b]) - i + sum(len(x) for x in blocks[b + 1:])
                blocks = blocks[:b] + ([blocks[b][:i]] if i else [])
                return blocks, removed
    return blocks, removed


END_RE = re.compile(r"([.!?…]+[\"”’»)]*)(\s+)")


def split_sentences(p):
    p = p.replace("**", "").replace("__", "")
    parts, start = [], 0
    for m in END_RE.finditer(p):
        following = p[m.end():m.end() + 1]
        mark = m.group(1)
        if following and following.islower():
            continue  # "e.g. the", "approx. ten", "wait... and"
        if mark == ".":
            previous = re.findall(r"[^\s(]+$", p[start:m.start(1)])
            if previous and previous[0].lower().strip(".") in ABBREVIATIONS:
                continue
            if previous and re.fullmatch(r"[A-Z]", previous[0]):
                continue  # an initial: "J. Smith"
        part = p[start:m.end(1)].strip()
        if part:
            parts.append(part)
        start = m.end()
    rest = p[start:].strip()
    if rest:
        parts.append(rest)
    return [s for s in parts if words(s)]


# ---------------------------------------------------------------- measurement

def longest_run(seq, cond):
    best, current = 0, 0
    for i in range(len(seq)):
        if cond(i):
            current += 1
            best = max(best, current)
        else:
            current = 0
    return best


def measure(text):
    a = parse(text)
    sentences = a["sentences"]
    paragraphs = a["paragraphs"]
    plain = a["plain"]
    lower = norm(plain)
    raw_lower = norm(a["raw"])
    all_words = words(plain)
    lettered = [w for w in all_words if LETTER_RE.search(w)]
    n_words = len(all_words) + a["frame_words"]  # the letter's frame is not prose but still part of the word count
    n_sentences = max(1, len(sentences))
    per_thousand = 1000 / max(1, n_words)

    lengths = [len(words(s)) for s in sentences] or [0]
    mean = statistics.mean(lengths)
    std = statistics.pstdev(lengths) if len(lengths) > 1 else 0.0
    cv = std / mean if mean else 0.0

    short_chain = longest_run(lengths, lambda i: lengths[i] <= 5)
    equal_run = 1
    current = 1
    for i in range(1, len(lengths)):
        if lengths[i] >= 10 and lengths[i - 1] >= 10 and abs(lengths[i] - lengths[i - 1]) <= 3:
            current += 1
            equal_run = max(equal_run, current)
        else:
            current = 1

    eligible_p, contrast_p = 0, 0
    for ps in a["paragraph_sentences"]:
        if len(ps) >= 3:
            eligible_p += 1
            pl = [len(words(s)) for s in ps]
            if min(pl) <= 8 and max(pl) >= 20:
                contrast_p += 1

    p_lengths = [len(words(p)) for p in paragraphs]
    p_cv = (statistics.pstdev(p_lengths) / statistics.mean(p_lengths)) if len(p_lengths) >= 4 and statistics.mean(p_lengths) else None

    # sentence openings
    openings = []
    for s in sentences:
        w = words(s)
        openings.append(norm(w[0]) if w else "")
    opening_counts = Counter(openings)
    top_opening, top_opening_n = (opening_counts.most_common(1)[0] if opening_counts else ("", 0))
    same_opening_run = longest_run(openings, lambda i: i > 0 and openings[i] == openings[i - 1]) + 1 if openings else 0
    connective_openers = 0
    for s in sentences:
        ls = norm(s).lstrip("\"“‘'( ")
        if any(re.match(re.escape(c) + r"(?!\w)", ls) for c in CONNECTIVE_OPENERS):
            connective_openers += 1
    ing_openers = sum(1 for s in sentences if SENTENCE_START_ING_RE.match(s.strip()))

    # participle tail: ", highlighting ..." in the second half of the sentence
    participle_tail = 0
    for s in sentences:
        ls = norm(s)
        for m in re.finditer(PARTICIPLE_TAIL, ls):
            if m.start() >= len(ls) * 0.35:
                participle_tail += 1
                break

    # punctuation: a pair of dashes around one aside counts as one use
    em_dash, dash_uses = 0, 0
    for s in sentences:
        body = re.sub(r"—(?=[\"”’'])", "", s)  # speech broken off: "I didn't—"
        n = body.count("—") + len(re.findall(r"\s–\s", body)) + len(re.findall(r"\s--\s|\w--\w", body))
        em_dash += n
        dash_uses += (n + 1) // 2
    semicolons = plain.count(";")
    colons = len(re.findall(r"(?<!\d):(?!\d)", plain))
    labeled_colons = len(LABEL_PATTERN.findall(lower))
    exclamations = plain.count("!")
    questions = plain.count("?")

    contrast_frames = sum(len(re.findall(rx, lower)) for rx in CONTRAST_FRAMES)

    triads = 0
    for m in re.finditer(r"([^\s,.;:!?]+(?: [^\s,.;:!?]+){0,2}), ([^\s,.;:!?]+(?: [^\s,.;:!?]+){0,2}),? (and|or) ([^\s,.;:!?]+)", lower):
        before = lower[max(0, m.start() - 2):m.start()]
        if not before.endswith(", "):
            triads += 1

    ai = count_terms(AI_WORDS, lower)
    buzz = count_terms(TECH_BUZZWORDS, lower)
    brochure = count_terms(BROCHURE, lower)
    latinate = count_terms(LATINATE, lower)
    significance = count_terms(SIGNIFICANCE, lower)
    copula = count_terms(COPULA_DODGES, lower)
    filler = count_terms(FILLER, lower)
    leftovers = count_terms(CHAT_LEFTOVERS, raw_lower)
    sycophancy = count_terms(SYCOPHANCY, raw_lower)
    mail = count_patterns(MAIL_CLICHES, raw_lower)
    office = count_terms(OFFICE_JARGON, lower)

    hedge_stacks = sum(1 for s in sentences if len(re.findall(HEDGES, norm(s))) >= 2)
    hidden_verbs = [m.group(0) for m in HIDDEN_VERB_RE.finditer(lower)]
    nominals = len(NOMINAL_RE.findall(lower))
    passive, agentless = 0, 0
    for s in sentences:
        ls = norm(s)
        found = [m for m in PASSIVE_RE.finditer(ls) if m.group(2) not in NOT_PASSIVE]
        if found:
            passive += 1
            tail = ls[found[0].end():found[0].end() + 60]
            if not re.match(r"[^.;]{0,40}\bby\b", tail):
                agentless += 1
    contractions = len(CONTRACTION_RE.findall(lower))
    full_forms = len(FULL_FORM_RE.findall(lower))
    acronym_expansions = len(ACRONYM_EXPANSION_RE.findall(plain))

    first_sentences = norm(" ".join(sentences[:2])) if sentences else ""
    opening_cliches = [t for t in STOCK_OPENINGS if re.search(r"(?<!\w)" + re.escape(t), first_sentences)]
    self_answer = 0  # a question immediately followed by its own short answer
    for i in range(len(sentences) - 1):
        if sentences[i].rstrip().rstrip("\"”’)").endswith("?"):
            nxt = norm(sentences[i + 1]).strip()
            answer_like = re.match(r"(because|simple|easy|the answer|it's simple|yes|no|not really|absolutely|exactly|"
                                   r"spoiler|turns out|short answer|nope|hardly)(?!\w)", nxt)
            short_verdict = len(words(nxt)) <= 4 and not nxt.endswith(("!", "?"))
            if answer_like or short_verdict:
                self_answer += 1
    last_p = norm(paragraphs[-1]) if paragraphs else ""
    closing_cliches = [t for t in STOCK_CLOSINGS if re.search(r"(?<!\w)" + re.escape(t), last_p)]
    question_ending = bool(sentences) and sentences[-1].rstrip().rstrip("\"”’)").endswith("?")

    # formatting
    bold = len(re.findall(r"\*\*[^*\n]+\*\*", a["raw"]))
    emoji = len(EMOJI_RE.findall(a["raw"]))
    us, uk, ize, ise = us_uk_forms(norm(re.sub(r"`[^`\n]*`|https?://\S+", " ", a["raw"])))
    title_headings, sentence_headings, minor_caps = heading_case(a["headings"])

    def stems(p):
        return {norm(w)[:6] for w in words(p) if len(w) >= 4 and norm(w) not in STOPWORDS and LETTER_RE.search(w)}
    overlap = None
    if len(paragraphs) >= 3:
        A, B = stems(paragraphs[0]), stems(paragraphs[-1])
        if min(len(A), len(B)) >= 5:  # a title line or a one-line sign-off says too little to compare
            overlap = len(A & B) / min(len(A), len(B))

    # readability (Flesch reading ease and Flesch-Kincaid grade)
    syllables = sum(count_syllables(w) for w in lettered)
    syl_per_word = syllables / max(1, len(lettered))
    words_per_sentence = len(all_words) / n_sentences  # prose only: the letter's frame has no sentences
    flesch = 206.835 - 1.015 * words_per_sentence - 84.6 * syl_per_word
    grade = 0.39 * words_per_sentence + 11.8 * syl_per_word - 15.59

    return {
        "words": n_words,
        "sentences": len(sentences),
        "paragraphs": len(paragraphs),
        "mean_sentence": round(mean, 1),
        "sentence_cv": round(cv, 2),
        "shortest": min(lengths),
        "longest": max(lengths),
        "short_chain": short_chain,
        "equal_length_run": equal_run,
        "contrast_paragraphs": f"{contrast_p}/{eligible_p}",
        "paragraph_cv": round(p_cv, 2) if p_cv is not None else None,
        "top_opening": top_opening,
        "top_opening_share": round(top_opening_n / n_sentences, 2),
        "same_opening_run": same_opening_run,
        "connective_opening_share": round(connective_openers / n_sentences, 2),
        "ing_openers": ing_openers,
        "ing_opener_share": round(ing_openers / n_sentences, 2),
        "participle_tails": participle_tail,
        "participle_tail_share": round(participle_tail / n_sentences, 2),
        "em_dash": em_dash,
        "dash_uses": dash_uses,
        "dash_uses_per_thousand": round(dash_uses * per_thousand, 1),
        "dialogue_lines": a["dialogue_lines"],
        "semicolons": semicolons,
        "colons": colons,
        "labeled_colons": labeled_colons,
        "exclamations": exclamations,
        "questions": questions,
        "contrast_frames": contrast_frames,
        "triads_per_thousand": round(triads * per_thousand, 1),
        "triads": triads,
        "ai_words": dict(ai),
        "tech_buzzwords": dict(buzz),
        "brochure": dict(brochure),
        "latinate": dict(latinate),
        "significance": dict(significance),
        "copula_dodges": dict(copula),
        "filler": dict(filler),
        "hedge_stacks": hedge_stacks,
        "hidden_verbs": hidden_verbs,
        "nominals_per_hundred": round(nominals * 100 / max(1, n_words), 1),
        "passive_sentences": passive,
        "agentless_passive_share": round(agentless / n_sentences, 2),
        "contractions": contractions,
        "full_forms": full_forms,
        "chat_leftovers": dict(leftovers),
        "sycophancy": dict(sycophancy),
        "mail_cliches": dict(mail),
        "frame_lines": a["frame_lines"],
        "cliche_opening": opening_cliches,
        "office_jargon": dict(office),
        "acronym_expansions": acronym_expansions,
        "self_answer": self_answer,
        "cliche_closing": closing_cliches,
        "question_ending": question_ending,
        "bold": bold,
        "emoji": emoji,
        "us_spellings": us,
        "uk_spellings": uk,
        "ize_spellings": ize,
        "ise_spellings": ise,
        "title_case_headings": title_headings,
        "sentence_case_headings": sentence_headings,
        "capitalized_minor_words": minor_caps,
        "first_last_overlap": round(overlap, 2) if overlap is not None else None,
        "syllables_per_word": round(syl_per_word, 2),
        "flesch": round(flesch, 1),
        "grade": round(grade, 1),
    }


# ---------------------------------------------------------------- text profile (genre and sector guess)

GENRE_LABELS = {
    "poetry": "Poetry",
    "literary": "Literary narrative",
    "essay": "Essay and opinion",
    "spec": "Technical specification",
    "docs": "Technical documentation",
    "corporate": "Business correspondence",
    "academic": "Academic writing",
    "legal": "Legal writing",
    "news": "News writing",
    "marketing": "Marketing copy",
    "social": "Social media",
    "personal": "Personal writing",
}

SECTOR_KEYWORDS = {
    "software and technology": ["software", "app", "apps", "application", "server", "api", "apis", "deploy", "release notes",
                                "new release", "codebase", "source code", "code review", "database", "cloud", "user interface",
                                "sprint", "backend", "frontend", "platform", "repository", "pull request", "npm", "git",
                                "bug", "bugs", "kubernetes", "latency", "endpoint", "saas", "outage", "downtime", "dashboard",
                                "engineer"],
    "finance": ["budget", "interest rate", "loan", "credit", "invest", "portfolio", "shares", "balance sheet", "cash flow",
                "invoice", "payment", "revenue", "earnings", "fiscal", "dividend", "mortgage", "apr", "fees", "annual fee",
                "savings", "bank", "overdraft", "tax"],
    "health": ["patient", "treatment", "clinic", "medication", "medicine", "doctor", "hospital", "diagnos", "symptom",
               "health", "dose", "nurse", "therapy", "prescri", "care team", "surgery", "appointment"],
    "education": ["student", "teacher", "lesson", "school", "curriculum", "exam", "courses", "course materials", "university",
                  "classroom", "learner", "pupil", "semester", "grades", "homework", "faculty"],
    "law": ["contract", "agreement", "the parties", "either party", "each party", "court", "lawsuit", "statute", "liable",
            "liability", "clause", "pursuant", "hereby", "indemnif", "jurisdiction", "gdpr", "compliance", "terminate"],
    "retail and e-commerce": ["orders", "your order", "order number", "shipping", "delivery", "cart", "checkout", "discount",
                              "in stock", "out of stock", "online store", "our store", "in-store", "returns", "refund",
                              "products", "basket", "promo code"],
    "public sector": ["council", "citizen", "resident", "government", "public service", "agency", "municipal",
                      "local authority", "permit", "federal", "ministry", "taxpayer", "constituent"],
    "human resources": ["employee", "hiring", "recruit", "annual leave", "sick leave", "parental leave", "payroll",
                        "performance review", "candidate", "interview", "onboarding", "benefits package", "pto",
                        "people team", "hr", "headcount"],
    "marketing and communications": ["brand", "campaign", "advert", "audience", "engagement", "social media", "content strategy",
                                     "launch", "newsletter", "conversion", "seo", "followers", "influencer"],
}
# Keywords match at the start of a word, so "patient" also finds "patients". Short ones match only as
# whole words: otherwise "app" is found in "apply" and "hr" in "three".
WHOLE_WORD_KEYWORDS = {"app", "apps", "api", "apis", "git", "npm", "apr", "hr", "pto", "seo", "gdpr", "saas", "bug",
                       "bugs", "tax", "bank", "brand", "launch"}
SECTOR_PATTERNS = {
    name: [re.compile(r"(?<!\w)" + re.escape(k) + (r"(?!\w)" if k in WHOLE_WORD_KEYWORDS else "")) for k in keys]
    for name, keys in SECTOR_KEYWORDS.items()
}

GREETING_RE = re.compile(r"^\s*(hi|hello|hey|dear|good morning|good afternoon|greetings)\b[^\n]{0,60}[,!:]?\s*$", re.M)
CLOSING_RE = re.compile(r"^\s*(best|best regards|kind regards|warm regards|regards|thanks|thank you|many thanks|cheers|"
                        r"sincerely|yours sincerely|yours faithfully|all the best|talk soon)\s*[,.!]?\s*$", re.M)
REQUIREMENT_RE = re.compile(r"\b(shall|must|must not|shall not|is required to|are required to|should)\b")
UNIT_RE = re.compile(r"\b\d+(?:[.,]\d+)?\s?(ms|s|sec|seconds|minutes|mb|gb|kb|tb|mbps|gbps|°c|°f|kg|mm|cm|kw|v|hz|px|rpm)\b", re.I)
NUMBERED_RE = re.compile(r"^\s*\d+(\.\d+)+\s", re.M)
IMPERATIVE_VERBS = {"run", "install", "open", "click", "select", "add", "create", "set", "use", "enter", "type", "go",
                    "copy", "paste", "configure", "check", "restart", "download", "update", "delete", "remove", "choose",
                    "save", "navigate", "make", "clone", "build", "start", "stop", "edit", "replace", "export", "import",
                    "upload", "sign", "log", "press", "tap", "enable", "disable", "change", "follow", "see", "read",
                    "take", "contact", "call", "keep", "avoid", "ask", "tell", "wait", "drink", "eat", "don't", "never",
                    "always", "try", "visit", "bring", "fill", "complete", "send", "write", "pay", "apply", "register",
                    "book", "remember", "swallow", "wash", "turn", "plug", "unplug", "attach", "connect", "place"}
PAST_RE = re.compile(r"\b(\w{3,}ed|was|were|had|said|went|came|saw|took|looked|turned|felt|knew|thought|told|stood|sat|"
                     r"left|found|made|got|ran|held|heard|began|kept|brought|asked|walked)\b")
FIRST_SINGULAR_RE = re.compile(r"\b(i|i'm|i've|i'd|i'll|me|my|mine|myself)\b")
FIRST_PLURAL_RE = re.compile(r"\b(we|we're|we've|we'll|our|ours|us)\b")
SECOND_RE = re.compile(r"\b(you|you're|you've|you'll|your|yours)\b")
THIRD_RE = re.compile(r"\b(he|she|they|him|her|his|them|their)\b")
CITATION_RE = re.compile(r"\([A-Z][A-Za-z'\-]+(?: (?:et al\.|and|&) [A-Z][A-Za-z'\-]+)?,? \d{4}[a-z]?(?:, p+\. ?\d+)?\)|\bet al\.|\[\d+(?:[,–-]\s?\d+)*\]")
DATELINE_RE = re.compile(r"^[A-Z][A-Z .]{2,}(?:,\s*[A-Za-z .]+)?\s*(?:\([A-Za-z .]+\))?\s*[—–-]\s")
SPEECH_RE = re.compile(r"[\"”’]\s*,?\s*(he|she|they|i|[A-Z][a-z]+)\s+(said|asked|whispered|shouted|replied|muttered|called|answered)\b|"
                       r"\b(said|asked|whispered|replied|muttered)\s*[,.]?\s*[\"“]", re.I)


def guess_profile(text):
    """Guesses the text's genre and sector from surface signals.

    It is a hint for the agent, not a verdict: the agent reads the text and decides.
    Returns {genre, label, sector, confidence, evidence, scores}.
    """
    a = parse(text)
    raw = a["raw"]
    lower = norm(raw)
    plain_lower = norm(a["plain"])
    sentences = a["sentences"]
    n_sent = max(1, len(sentences))
    lines = [l.strip() for l in re.sub(r"```.*?```", "", raw, flags=re.S).splitlines() if l.strip() and not l.strip().startswith("#")]
    score = {k: 0.0 for k in GENRE_LABELS}
    evidence = {k: [] for k in GENRE_LABELS}

    def add(genre, points, why):
        score[genre] += points
        if why and why not in evidence[genre]:
            evidence[genre].append(why)

    # poetry: many short lines that are not closed with sentence punctuation
    if len(lines) >= 4:
        short = sum(1 for l in lines if len(words(l)) <= 8)
        open_ended = sum(1 for l in lines if not re.search(r"[.!?…]$", l))
        if short / len(lines) >= 0.7 and open_ended / len(lines) >= 0.5:
            add("poetry", 4, "short lines without closing punctuation")
        stanzas = [b for b in re.split(r"\n\s*\n", raw.strip()) if b.strip()]
        if len(stanzas) >= 2 and all(2 <= len(b.strip().splitlines()) <= 8 for b in stanzas) and short / len(lines) >= 0.7:
            add("poetry", 2, "stanzas")

    # essay, column and personal writing: the writer speaks as "I"
    fs = len(FIRST_SINGULAR_RE.findall(plain_lower))
    we = len(FIRST_PLURAL_RE.findall(plain_lower))
    you = len(SECOND_RE.findall(plain_lower))
    third = len(THIRD_RE.findall(plain_lower))
    if fs >= 2:
        add("essay", min(fs, 8) * 0.35, "first-person view")
        add("personal", min(fs, 8) * 0.5, "first person singular")

    opinion = sum(1 for w in ("i think", "i believe", "i suspect", "in my view", "i'd argue", "i would argue",
                              "it seems to me", "the problem with", "we should", "why do we", "why we", "i have never understood")
                  if w in plain_lower)
    if opinion:
        add("essay", min(opinion, 4) * 0.7, "opinion markers")
    for w in ("i spent", "my trip", "i visited", "we visited", "itinerary", "bucket list", "destination", "my family",
              "my friends", "my kids", "last weekend", "last summer", "i remember"):
        if w in lower:
            add("personal", 0.6, "a lived experience")

    # an organisation speaking as "we" to the reader as "you": announcements and notices
    if we >= 2 and you >= 1:
        add("corporate", 1.0 + min(we + you, 6) * 0.15, "an organisation addressing the reader")
    elif we >= 3:
        add("corporate", 1.0, "an organisation speaking as we")

    # literary narrative: dialogue, third-person past tense
    dialogue = len(SPEECH_RE.findall(raw)) + (a["dialogue_lines"] if a["dialogue_lines"] >= 2 else 0)
    if dialogue >= 2:
        add("literary", 2 + min(dialogue, 6) * 0.5, "dialogue")
    past = sum(1 for s in sentences if PAST_RE.search(norm(s)))
    if past / n_sent >= 0.6 and len(sentences) >= 4 and third >= 2 and fs < 2 and we < 2 and you < 2:
        add("literary", 1.5, "third-person past narrative")

    # technical specification: requirement modals, numbering, units
    req = sum(1 for s in sentences if REQUIREMENT_RE.search(norm(s)))
    shall = len(re.findall(r"\bshall\b", lower))
    if req:
        add("spec", req / n_sent * 5, "requirement modals (shall, must)")
    if NUMBERED_RE.search(raw):
        add("spec", 1.5, "numbered clauses")
        add("legal", 0.5, "")
    units = len(UNIT_RE.findall(raw))
    if units:
        add("spec", min(units, 4) * 0.6, "units of measure")
    for w in ("requirement", "acceptance criteria", "at least", "no more than", "at most", "the system", "must support"):
        if w in lower:
            add("spec", 0.6, "")

    # technical documentation: code, commands, headings, imperative steps
    if "```" in raw or re.search(r"`[^`\n]+`", raw):
        add("docs", 2.5, "code and commands")
    if re.search(r"(?m)^\s*(\$ |npm |pip |git |python3? |brew |curl |npx |docker )", raw):
        add("docs", 1.5, "shell commands")
    if a["headings"]:
        add("docs", 1, "headings")
    imperative = sum(1 for s in sentences if (words(s) or [""])[0].lower() in IMPERATIVE_VERBS)
    if imperative >= 2:
        add("docs", min(imperative, 5) * 0.5, "step-by-step instructions")
    docs_terms = sum(1 for w in ("install", "configur", "dependenc", "repository", "branch", "command", "server",
                                 "environment", "version", "parameter", "run the", "click ") if w in lower)
    if docs_terms:
        add("docs", min(docs_terms, 5) * 0.5, "setup and development terms")
    if imperative >= 1 and you >= 2 and we < 2:
        add("docs", 1.0, "guiding the reader step by step")

    # business correspondence: greeting and closing
    greeting = GREETING_RE.search(lower[:200])
    closing = CLOSING_RE.search(lower[-250:])
    if greeting:
        add("corporate", 2.5, "greeting")
    if closing:
        add("corporate", 2.5, "sign-off")
    for w in ("attached", "meeting", "please let me know", "next steps", "all staff", "we are pleased", "the team",
              "our customers", "update on", "action required", "by friday", "deadline"):
        if w in lower:
            add("corporate", 0.6, "")

    # academic
    if CITATION_RE.search(raw):
        add("academic", 2.5, "citations")
    for w in ("this study", "this paper", "findings", "methodology", "participants", "literature", "hypothes",
              "statistically significant", "sample size", "results indicate", "results suggest", "p <"):
        if w in lower:
            add("academic", 0.8, "academic terms")

    # legal
    for w in ("hereinafter", "hereby", "herein", "whereas", "pursuant to", "notwithstanding", "indemnif", "the parties",
              "this agreement", "governing law", "liability", "jurisdiction"):
        if w in lower:
            add("legal", 1, "legal terms")
    if shall >= 2:
        add("legal", 1, "\"shall\" obligations")

    # news
    if DATELINE_RE.search(raw.strip()):
        add("news", 3, "dateline")
    reported = len(re.findall(r"\b(said on|said in a statement|told reporters|announced on|according to|officials said|"
                              r"a spokesperson|a spokesman|a spokeswoman|said (monday|tuesday|wednesday|thursday|friday|saturday|sunday))\b", lower))
    if reported:
        add("news", min(reported, 4) * 0.8, "reporting verbs")

    # marketing
    promo = len(re.findall(r"(?<!\w)(shop now|buy now|limited time|discover|don't miss|free shipping|sign up|get started|"
                           r"% off|exclusive|today only|order now|try it free|special offer|save up to|book now)", lower))
    if promo:
        add("marketing", min(promo, 6) * 0.7, "calls to buy")
    if raw.count("!") >= 2:
        add("marketing", 0.5, "")
        add("social", 0.3, "")

    # social media
    tags = len(re.findall(r"(?<![\w#])#[A-Za-z]\w+", raw)) + len(re.findall(r"(?<!\w)@\w+", raw))
    if tags:
        add("social", 2 + min(tags, 4) * 0.5, "hashtags and mentions")
    if len(EMOJI_RE.findall(raw)) >= 2:
        add("social", 1.5, "emoji")
    if "linkedin" in lower or re.search(r"thoughts\?|agree\?|comment below|in the comments|link in bio|follow for more|repost", lower):
        add("social", 2, "talking to followers")
    announce = len(re.findall(r"thrilled to|excited to (announce|share)|proud to (announce|share)|humbled|beyond grateful|"
                              r"big news|some personal news", lower))
    if announce:
        add("social", min(announce, 3) * 0.7, "post formulas")
    if re.search(r"(?m)^\s*[\U0001F300-\U0001FAFF\U00002600-\U000027BF]", raw):
        add("social", 0.8, "emoji at line starts")

    ranked = sorted(score.items(), key=lambda kv: kv[1], reverse=True)
    (best, s1), (_, s2) = ranked[0], ranked[1]
    if s1 < 1.5:
        best, label = None, "Unclear"
        confidence = "low"
    else:
        label = GENRE_LABELS[best]
        confidence = "high" if s1 >= 3 and s1 >= 2 * max(s2, 0.1) else "medium" if s1 - s2 >= 1.5 else "low"

    sector_scores = {name: sum(len(p.findall(lower)) for p in patterns) for name, patterns in SECTOR_PATTERNS.items()}
    sector, hits = max(sector_scores.items(), key=lambda kv: kv[1])
    if best in ("poetry", "literary"):
        sector = "literature"
    elif hits < 2:
        sector = "general"

    return {
        "genre": best,
        "label": label,
        "sector": sector,
        "confidence": confidence,
        "evidence": evidence[best][:3] if best else [],
        "scores": {k: round(v, 1) for k, v in ranked if v > 0},
    }


def profile_line(p):
    tail = f" [clues: {', '.join(p['evidence'])}]" if p["evidence"] else ""
    return f"Text type (guess): {p['label']} · Field: {p['sector']} · confidence: {p['confidence']}{tail}"


# ---------------------------------------------------------------- evaluation

def alarms(m):
    """Returns (label, value text, status, note) rows. status: 'ok' | 'warn' | 'alarm' | 'info'."""
    w = max(1, m["words"])
    pct = lambda x: f"{round(x * 100)}%"
    total = lambda d: sum(d.values())
    listed = lambda d: f"{total(d)} ({', '.join(d)})" if d else "0"
    rows = []

    def add(label, value, status, note=""):
        rows.append((label, value, status, note))

    if m["sentences"] >= 6:
        cv = m["sentence_cv"]
        add("Sentence length variety", f"{cv:.2f}",
            "alarm" if cv < 0.30 else "warn" if cv < 0.45 else "ok",
            "low means the sentences are all about the same length (alarm < 0.30)")
        add("Run of same-length sentences", f"{m['equal_length_run']} sentences",
            "alarm" if m["equal_length_run"] >= 5 else "warn" if m["equal_length_run"] == 4 else "ok",
            "medium or long sentences in a row, each within ±3 words of the last")
        add("Chain of short sentences", f"{m['short_chain']} sentences",
            "alarm" if m["short_chain"] >= 4 else "warn" if m["short_chain"] == 3 else "ok",
            "5 words or fewer, one after another")
        article = m["top_opening"] in ("the", "a", "an")
        limit = 0.40 if article else 0.25
        add("Most common opener", f"\"{m['top_opening']}\" {pct(m['top_opening_share'])}",
            "alarm" if m["top_opening_share"] > limit and m["sentences"] >= 8 else "ok",
            "more than a quarter of the sentences start with the same word")
        add("Sentences opened by a connective", pct(m["connective_opening_share"]),
            "alarm" if m["connective_opening_share"] > 0.25 else "warn" if m["connective_opening_share"] > 0.15 else "ok",
            "Additionally / Moreover / Furthermore ...")
        add("Opening -ing phrases", f"{m['ing_openers']} ({pct(m['ing_opener_share'])})",
            "alarm" if m["ing_opener_share"] > 0.2 and m["ing_openers"] >= 3 else "warn" if m["ing_openers"] >= 2 and m["ing_opener_share"] > 0.12 else "ok",
            "\"Building on this, ...\", \"Leveraging our expertise, ...\"")
    else:
        add("Rhythm measures", f"{m['sentences']} sentences", "info", "not measured below 6 sentences")
    add("Participle tails", f"{m['participle_tails']} ({pct(m['participle_tail_share'])})",
        "alarm" if m["participle_tail_share"] > 0.15 and m["participle_tails"] >= 2 else "warn" if m["participle_tails"] >= 1 else "ok",
        "\", highlighting ...\", \", ensuring ...\" tacked on at the end")

    uses, dash_rate = m["dash_uses"], m["dash_uses_per_thousand"]
    add("Em dashes", f"{m['em_dash']} ({uses} uses, {dash_rate}/1000 words)",
        "alarm" if (uses >= 2 and dash_rate >= 8) or (uses >= 4 and dash_rate >= 5)
        else "warn" if uses >= 1 and dash_rate >= 3 else "ok",
        "a legitimate mark; the tell is the density (a pair around one aside is one use)")
    semicolon_limit = max(2, w // 300)
    add("Semicolons", str(m["semicolons"]),
        "alarm" if m["semicolons"] > semicolon_limit + 1 else "warn" if m["semicolons"] > semicolon_limit else "ok",
        f"at most {semicolon_limit} at this length")
    add("Announced reveals", str(m["labeled_colons"]),
        "alarm" if m["labeled_colons"] >= 2 else "warn" if m["labeled_colons"] == 1 else "ok",
        "\"Here's the thing:\", \"The result?\"")
    add("Contrast framing", str(m["contrast_frames"]),
        "alarm" if m["contrast_frames"] >= 2 else "warn" if m["contrast_frames"] == 1 else "ok",
        "\"not just X, but Y\", \"it's not X, it's Y\"")
    add("Triads", f"{m['triads']} ({m['triads_per_thousand']}/1000 words)",
        "alarm" if m["triads_per_thousand"] > 4 and m["triads"] >= 3 else "warn" if m["triads_per_thousand"] > 3 and m["triads"] >= 2 else "ok",
        "\"X, Y and Z\"")
    n = total(m["ai_words"])
    add("AI vocabulary", listed(m["ai_words"]),
        "alarm" if n * 100 / w > 1.5 and n >= 2 else "warn" if n >= 2 else "ok", "")
    n = total(m["tech_buzzwords"])
    add("Buzzwords", listed(m["tech_buzzwords"]),
        "alarm" if n >= 3 else "warn" if n >= 1 else "ok", "seamless, robust, leverage ...")
    n = total(m["brochure"])
    add("Brochure language", listed(m["brochure"]),
        "alarm" if n >= 3 else "warn" if n >= 1 else "ok", "fine in moderation in ad copy; the tell is the pile-up")
    n = total(m["significance"])
    add("Significance inflation", listed(m["significance"]),
        "alarm" if n >= 2 else "warn" if n == 1 else "ok", "\"plays a pivotal role\", \"a testament to\"")
    n = total(m["copula_dodges"])
    add("\"Serves as\" for \"is\"", listed(m["copula_dodges"]),
        "alarm" if n >= 3 else "warn" if n >= 1 else "ok", "serves as, stands as, boasts")
    n = total(m["latinate"])
    add("Inflated wording", listed(m["latinate"]),
        "alarm" if n >= 3 and n * 100 / w > 1.2 else "warn" if n >= 2 else "ok", "utilize, in order to, prior to ...")
    n = len(m["hidden_verbs"])
    add("Hidden verbs", f"{n} ({', '.join(m['hidden_verbs'][:4])})" if n else "0",
        "alarm" if n >= 4 else "warn" if n >= 2 else "ok", "\"make a decision\" for \"decide\"")
    n = total(m["filler"])
    add("Filler phrases", listed(m["filler"]),
        "alarm" if n >= 2 else "warn" if n == 1 else "ok", "")
    add("Hedge stacks", str(m["hedge_stacks"]),
        "alarm" if m["hedge_stacks"] >= 2 else "warn" if m["hedge_stacks"] == 1 else "ok",
        "two or more hedges in one sentence")
    if m["sentences"] >= 6:
        add("Agentless passive", pct(m["agentless_passive_share"]),
            "alarm" if m["agentless_passive_share"] > 0.4 else "warn" if m["agentless_passive_share"] > 0.25 else "ok",
            "share of sentences; normal in academic, legal and spec writing")
    n = total(m["chat_leftovers"])
    add("Chat residue", listed(m["chat_leftovers"]), "alarm" if n else "ok", "conclusive on its own")
    n = total(m["sycophancy"])
    add("Sycophancy", listed(m["sycophancy"]), "alarm" if n else "ok", "")
    n = total(m["mail_cliches"])
    add("E-mail formulas", listed(m["mail_cliches"]),
        "alarm" if n >= 2 else "warn" if n == 1 else "ok", "one is a habit, several are a template")
    add("Asking and answering", str(m["self_answer"]),
        "alarm" if m["self_answer"] >= 2 else "warn" if m["self_answer"] == 1 else "ok", "\"Why? Because ...\"")
    n = total(m["office_jargon"])
    add("Office jargon", listed(m["office_jargon"]),
        "info" if n else "ok", "decide by audience, see references/jargon.md")
    if m["acronym_expansions"]:
        add("Spelled-out acronyms", str(m["acronym_expansions"]), "info",
            "right for general readers, noise for specialists")
    add("Stock opening", ", ".join(m["cliche_opening"]) or "none", "alarm" if m["cliche_opening"] else "ok", "first two sentences")
    add("Stock closing", ", ".join(m["cliche_closing"]) or "none", "alarm" if m["cliche_closing"] else "ok", "last paragraph")
    add("Ends on a question", "yes" if m["question_ending"] else "no", "warn" if m["question_ending"] else "ok",
        "fine once, a tell as a habit")
    if m["first_last_overlap"] is not None:
        add("First/last paragraph overlap", f"{m['first_last_overlap']:.2f}",
            "alarm" if m["first_last_overlap"] > 0.45 else "warn" if m["first_last_overlap"] > 0.30 else "ok",
            "does the ending repeat the opening?")
    if m["paragraph_cv"] is not None:
        add("Paragraph length variety", f"{m['paragraph_cv']:.2f}",
            "warn" if m["paragraph_cv"] < 0.20 else "ok", "are all the paragraphs the same height?")
    add("Bold", str(m["bold"]), "alarm" if m["bold"] > max(3, w // 150) else "ok", "")
    add("Emoji", str(m["emoji"]), "warn" if m["emoji"] else "ok", "")
    exclamation_limit = max(2, w // 100)
    add("Exclamation marks", str(m["exclamations"]), "warn" if m["exclamations"] > exclamation_limit else "ok",
        f"more than {exclamation_limit} at this length")
    us, uk, ize, ise = m["us_spellings"], m["uk_spellings"], m["ize_spellings"], m["ise_spellings"]
    if (us and uk) or (ize and ise) or (us and ise):
        parts = [f"{label}: {', '.join(forms[:4])}" for label, forms in (("US", us), ("UK", uk), ("-ize", ize), ("-ise", ise)) if forms]
        add("US/UK spelling", " · ".join(parts), "alarm", "pick one spelling system (-ize with UK spelling is fine: Oxford style)")
    else:
        side = ("US" if us else "UK, Oxford -ize" if uk and ize else "UK" if uk or ise else "US or Oxford -ize" if ize else "")
        add("US/UK spelling", f"consistent ({side})" if side else "no telling words", "ok", "")
    if m["title_case_headings"] or m["sentence_case_headings"]:
        mixed = m["title_case_headings"] and m["sentence_case_headings"]
        value = f"{m['title_case_headings']} title case, {m['sentence_case_headings']} sentence case"
        if m["capitalized_minor_words"]:
            value += f" · capitalized: {', '.join(m['capitalized_minor_words'][:4])}"
        add("Heading case", value, "alarm" if mixed else "warn" if m["capitalized_minor_words"] else "ok",
            "one style for every heading; and, of, the stay lowercase in title case")
    possible = m["contractions"] + m["full_forms"]
    if possible:
        add("Contractions", f"{m['contractions']} of {possible} ({pct(m['contractions'] / possible)})", "info",
            "none at all reads stiff in a blog or e-mail; legal, academic and spec texts skip them")
    fl = m["flesch"]
    band = ("very easy" if fl >= 90 else "easy" if fl >= 80 else "fairly easy" if fl >= 70 else "plain" if fl >= 60
            else "fairly difficult" if fl >= 50 else "difficult" if fl >= 30 else "very difficult")
    add("Readability (Flesch)", f"{fl} ({band}) · grade {m['grade']}", "info",
        f"avg. sentence {m['mean_sentence']} words, {m['syllables_per_word']} syllables/word")
    return rows


MARKS = {"ok": "✓", "warn": "~", "alarm": "!", "info": "·"}


def report(m, before=None, profile=None):
    lines = []
    lines.append("Still Human? · numeric audit")
    if profile:
        lines.append(profile_line(profile))
    if before:
        lines.append(f"Before: {before['words']} words, {before['sentences']} sentences, {before['paragraphs']} paragraphs")
        lines.append(f"After: {m['words']} words, {m['sentences']} sentences, {m['paragraphs']} paragraphs")
    else:
        lines.append(f"Text: {m['words']} words, {m['sentences']} sentences, {m['paragraphs']} paragraphs")
    lines.append("Thresholds are alarm bells, not verdicts. ✓ clean · ~ watch · ! alarm")
    lines.append("")
    new = alarms(m)
    old = {label: (value, status) for label, value, status, _ in alarms(before)} if before else {}
    width = max(len(label) for label, *_ in new) + 2
    for label, value, status, note in new:
        if before and label in old:
            old_value, old_status = old[label]
            line = f"{MARKS[status]} {label.ljust(width)}{MARKS[old_status]} {old_value}  →  {value}"
        else:
            line = f"{MARKS[status]} {label.ljust(width)}{value}"
        if note and status in ("warn", "alarm"):
            line += f"   [{note}]"
        lines.append(line)
    n_alarm = sum(1 for *_, s, _ in new if s == "alarm")
    n_warn = sum(1 for *_, s, _ in new if s == "warn")
    lines.append("")
    if before:
        old_alarm = sum(1 for *_, s, _ in alarms(before) if s == "alarm")
        lines.append(f"Alarms: {old_alarm} → {n_alarm} · Watch: {n_warn}")
    else:
        lines.append(f"Alarms: {n_alarm} · Watch: {n_warn}")
    return "\n".join(lines)


# ---------------------------------------------------------------- input, saved texts and the guides

SAVED_NAME_RE = re.compile(r"^[a-z0-9_-]{1,40}$")
GENRES_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "references", "genres.md")
SECTORS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "references", "sectors.md")


def saved_dir():
    root = os.environ.get("STILL_HUMAN_ROOT") or os.path.join(tempfile.gettempdir(), "still-human")
    folder = os.path.join(root, "texts")
    os.makedirs(folder, exist_ok=True)
    return folder


def save_text(name, text):
    if not SAVED_NAME_RE.match(name):
        sys.exit(f"Invalid name: {name!r}. Use lowercase letters, digits, - and _.")
    path = os.path.join(saved_dir(), name + ".txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    return path


def read(source):
    """Reads a text from standard input (-), a file, or a name saved earlier with --save."""
    if source == "-":
        return sys.stdin.read()
    # a short name without a dot or slash is a saved text first, a file in the current folder second
    if SAVED_NAME_RE.match(source) and os.path.exists(os.path.join(saved_dir(), source + ".txt")):
        with open(os.path.join(saved_dir(), source + ".txt"), encoding="utf-8") as f:
            return f.read()
    if os.path.exists(source):
        with open(source, encoding="utf-8") as f:
            return f.read()
    sys.exit(f"Text not found: {source!r} is neither a file nor a name saved with --save.")


def reference_section(path, label, exact=False):
    """The "## " section of a reference file whose title matches label, or None.
    Without exact, a title that starts with the label (or the other way round) also matches."""
    try:
        with open(path, encoding="utf-8") as f:
            guide = f.read()
    except OSError:
        return None
    sections = re.split(r"(?m)^## ", guide)
    wanted = (label or "").lower().strip()
    for sec in sections[1:]:
        title = sec.splitlines()[0].strip().lower()
        if wanted and (title == wanted or not exact and (title.startswith(wanted) or wanted.startswith(title))):
            return "## " + sec.strip().rstrip("-").strip()
    return None


def genre_guide(label, exact=False):
    """The section of references/genres.md for this genre label, or None."""
    return reference_section(GENRES_FILE, label, exact)


def sector_guide(label, exact=False):
    """The section of references/sectors.md for this sector, after the rules that hold in every sector."""
    section = reference_section(SECTORS_FILE, label, exact)
    if not section:
        return None
    common = reference_section(SECTORS_FILE, "Rules for every sector", exact=True)
    return f"{common}\n\n{section}" if common else section


def named_guide(label):
    """The guide for a genre or sector given by name: an exact title first, then a prefix."""
    return (genre_guide(label, exact=True) or sector_guide(label, exact=True)
            or genre_guide(label) or sector_guide(label))


def main(argv=None):
    ap = argparse.ArgumentParser(description="Still Human? · numeric audit for English text")
    ap.add_argument("text", nargs="?", help="text file, - for standard input, or a name saved with --save")
    ap.add_argument("--before", help="earlier version to compare against (file or saved name)")
    ap.add_argument("--save", metavar="NAME", help="keep the text under this name for later commands")
    ap.add_argument("--json", action="store_true", help="JSON output")
    ap.add_argument("--profile", action="store_true", help="print only the genre and sector guess")
    ap.add_argument("--guide", nargs="?", const="", metavar="GENRE_OR_SECTOR",
                    help="print the writing guides for the guessed genre and sector, or the guide for the genre or sector given")
    args = ap.parse_args(argv)

    if args.text is None:
        if args.guide:
            print(named_guide(args.guide) or f"No guide for this genre or sector: {args.guide}")
            return
        ap.error("a text is required")
    text = read(args.text)
    if args.save:
        save_text(args.save, text)
    # the genre is guessed from the original: with --before that is the earlier version
    profile = guess_profile(read(args.before) if args.before else text)
    if args.profile:
        print(json.dumps(profile, ensure_ascii=False, indent=1) if args.json else profile_line(profile))
        return
    m = measure(text)
    b = measure(read(args.before)) if args.before else None
    if args.json:
        out = {"after" if b else "measurement": m}
        if b:
            out["before"] = b
        out["profile"] = profile
        out["alarms"] = [{"label": l, "value": v, "status": s} for l, v, s, _ in alarms(m)]
        print(json.dumps(out, ensure_ascii=False, indent=1))
    else:
        print(report(m, b, profile))
    if args.guide is not None:
        if args.guide:
            guides = [named_guide(args.guide)]
        else:
            guides = [genre_guide(profile["label"]), sector_guide(profile["sector"])]
        for guide in guides:
            if guide:
                print("\n" + guide)


if __name__ == "__main__":
    main()
