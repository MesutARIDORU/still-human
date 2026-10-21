# Pattern catalog, with examples

This file expands the short catalog in SKILL.md. For each pattern you get the sign, why it reads as machine-written, and a before/after example. Most patterns have two more lines:
- **In the field:** how the same pattern looks in one field: public sector, finance, health, education, HR, retail, software, law. The fields have their own guides in `sectors.md`.
- **False alarm:** a usage that looks like the pattern but is right in that genre or field. Leave it alone.

Every example follows the same rule: the **After** text adds no information that isn't in the **Before** text. Where information is missing, it leaves a placeholder in square brackets or drops the sentence. Do the same when you rewrite.

## Contents

- **S · Structure and rhythm:**
  - S1 Metronome sentences
  - S2 Staccato chains
  - S3 Same openers
  - S4 Name loop
  - S5 Paragraphs that summarise themselves
  - S6 Ending that replays the opening
  - S7 Threes everywhere
  - S8 Missing steps
  - S9 Participle tails
- **R · Rhetorical moves:**
  - R1 Contrast framing
  - R2 Announced reveals
  - R3 Asking and answering yourself
  - R4 False ranges
  - R5 Aphorisms and fake depth
  - R6 Significance inflation
  - R7 Empty truths
  - R8 Both-sides wrap-up
  - R9 Pattern in disguise
- **W · Words and register:**
  - W1 AI vocabulary
  - W2 Buzzwords
  - W3 Term drift
  - W4 Hidden verbs
  - W5 "Serves as" for "is"
  - W6 Filler and hedge stacks
  - W7 Agentless passive
  - W8 Register whiplash
  - W9 Brochure voice
  - W10 Always the likeliest word
  - W11 Inflated wording
- **T · Tone and chat:**
  - T1 Chat residue
  - T2 Sycophancy
  - T3 Therapist voice
  - T4 Fake candour
  - T5 Tour-guide voice
  - T6 Stock openings
  - T7 Stock closings
  - T8 E-mail formulas
- **P · Punctuation and format:**
  - P1 Em-dash habit
  - P2 Semicolon swap
  - P3 Bold sprinkling
  - P4 Labelled bullets
  - P5 Emoji decoration
  - P6 Heading case drift
  - P7 Over-explaining
  - P8 Consistency slips
- **E · Evidence and fiction:**
  - E1 Vague authority
  - E2 Invented cases and figures
  - E3 Gap filling
  - E4 Template challenges paragraph
  - E5 Fiction clichés
  - E6 Over-correction

---

## S · Structure and rhythm

The tells in this group survive from one model generation to the next. They are also what detectors lean on most: how sentence lengths are spread, and how predictably sentences are built.

### S1 · Metronome sentences
**Sign:** sentence after sentence of roughly the same length, usually 15 to 25 words, each with the same shape: subject, verb, object, a qualifying phrase. Paragraphs of the same height.
**Why it's a tell:** people don't measure sentences. If what they have to say is long, the sentence runs long; when it's done, it stops. So human prose puts a forty-word sentence next to a four-word one.

**Before:**
> The council began building the new cycle lanes last month. The first phase will add eight kilometres of track along the seafront. Some roads will be reduced to a single lane while the work is underway. Drivers are being asked to use alternative routes where possible.

**After:**
> The council started on the new cycle lanes last month. Phase one: eight kilometres along the seafront. While the work goes on, some roads will drop to a single lane, and the council is asking drivers to use other routes where they can.

**False alarm:** appointment reminders, delivery notices and outage updates are meant to be scanned, and short sentences of similar length are right there: "Your appointment is on 14 March at 10am. Bring photo ID." *(health)*

### S2 · Staccato chains
**Sign:** three or more short sentences in a row, each closed by a full stop, often fragments. The advertising beat: "Fast. Simple. Secure." Or the social-media version: "No fluff. No filler. Just results."
**Why it's a tell:** in running prose, a run of short actions usually joins into one sentence. Breaking every one off with a full stop builds false tension, and models reach for it whenever they want "punch".

**Before:**
> The meeting started. Nobody spoke. The numbers went up on the screen. Silence. Then the director stood up.

**After:**
> When the meeting started nobody spoke, not even when the numbers went up on the screen. Then the director stood up.

**Note:** the last sentence stayed short. It moves the scene on, so it earns it (F12).

**In the field:**
- *Software, release notes:* "Bug fixed. Faster loading. New look." → "We fixed [which] bug, pages load faster, and the interface has a new design."

**False alarm:** in a headline, a slogan or a product tagline the short beat is part of the genre. The tell is the same beat running through the body text.

### S3 · Same openers
**Sign:** sentence after sentence starts with the same word: the same subject ("This…", "It…", "We…") or the same connective ("Additionally", "Moreover", "Furthermore", "However").
**Why it's a tell:** detectors measure how varied sentence openings are, and connectives at the start of every sentence give prose the feel of lecture notes. People mostly link sentences through the ideas themselves.

**Before:**
> The new policy takes effect in May. Additionally, all staff must complete the training. Furthermore, managers will receive a separate briefing. Moreover, the old forms will no longer be accepted.

**After:**
> The new policy takes effect in May. Before then, all staff must complete the training; managers get a separate briefing as well. From May the old forms won't be accepted.

**In the field:**
- *Public sector:* "This service allows residents to… This means that… This ensures that…" → name the service once, then let the actions lead.

**False alarm:** numbered steps and checklists often start each line with a verb ("Open… Select… Save…"). That's the format, not a tell.

### S4 · Name loop
**Sign:** either the full name is rebuilt in every sentence ("Harbour Bank… Harbour Bank's… Harbour Bank also…"), or it rotates through synonyms to avoid repetition: "the company, the firm, the organisation, the business, the brand".
**Why it's a tell:** both are mechanical. The first ignores pronouns; the second, which English style teachers call elegant variation, makes the reader wonder whether "the firm" and "the brand" are different things.

**Before:**
> Northwind launched a new app in March. The company says the platform has 40,000 users. The firm plans to expand the solution to three more countries, and the brand expects the tool to break even next year.

**After:**
> Northwind launched a new app in March and says it already has 40,000 users. It plans to offer the app in three more countries and expects it to break even next year.

**False alarm:** contracts repeat defined terms ("the Supplier") on purpose, to avoid any doubt about who is meant. Leave them.

### S5 · Paragraphs that summarise themselves
**Sign:** every paragraph ends with its own moral: "In short, …", "Simply put, …", "The takeaway? …", or a line that restates the paragraph's first sentence.
**Why it's a tell:** a summary after every hundred words assumes the reader didn't follow. Human writers summarise when the argument has been long, not by reflex.

**Before:**
> The new rota gives each team two late shifts a month instead of four. Requests for swaps go through the shared calendar. In short, the new system is fairer and easier to manage.

**After:**
> The new rota gives each team two late shifts a month instead of four, and swap requests go through the shared calendar.

**False alarm:** a long report section can end with a one-line summary, and an executive summary is by definition a summary.

### S6 · Ending that replays the opening
**Sign:** the introduction announces what the text will cover; the conclusion lists the same points again, often with "In conclusion".
**Why it's a tell:** it's the school essay template. In a text of a few paragraphs, the reader remembers the opening.

**Before:**
> In this post we'll look at why onboarding matters, what makes it work and how to measure it. … In conclusion, onboarding matters, it works when it's structured, and it can be measured.

**After:**
> *(opening)* [Start with the first real point instead of the menu.] … *(closing)* [End on the last point or the next step; don't list the three topics again.]

**Note:** the placeholders are deliberate. A stronger opening needs a fact or a view from the writer, and none is in the text.

**False alarm:** long technical documents and reports often restate the scope at the end for readers who skip to it. That's fine.

### S7 · Threes everywhere
**Sign:** adjectives, examples and benefits always come in threes: "fast, reliable and secure", "for students, teachers and parents". Several triads per paragraph.
**Why it's a tell:** three feels complete, so models round every list to three. Real lists have as many items as there are.

**Before:**
> Our platform is fast, reliable and secure. It helps teams plan, track and deliver their work, and it's loved by startups, agencies and enterprises.

**After:**
> The platform helps teams plan and track their work. [Which claim about speed or security can we back with a fact?]

**In the field:**
- *HR, job ad:* "We're looking for someone curious, driven and collaborative." → name the one quality the job really needs.

**False alarm:** a list that really has three items, like three dates or three locations, is just a list.

### S8 · Missing steps
**Sign:** each sentence is fine on its own, but the reasoning between them is missing; the text jumps from cause to conclusion.
**Why it's a tell:** models produce locally fluent sentences and leave the logic to the reader.

**Before:**
> Customers are using the mobile app more than the website. We are therefore closing the phone line.

**After:**
> Customers are using the mobile app more than the website [and calling less? source?]. We are therefore closing the phone line.

**Note:** the missing step can't be invented: if the text doesn't say that phone calls fell, ask.

### S9 · Participle tails
**Sign:** a clause of commentary hung on the end of a sentence with an -ing verb: ", highlighting the importance of collaboration", ", ensuring a seamless experience", ", underscoring our commitment to quality", ", paving the way for future growth".
**Why it's a tell:** the tail claims a significance the sentence hasn't earned. It has no subject who does anything; it just comments. It's among the most frequent machine habits in English.

**Before:**
> The library extended its weekend opening hours, reflecting its commitment to serving the community and fostering a love of reading.

**After:**
> The library is now open longer at weekends [new hours?].

**In the field:**
- *Finance, annual report:* "Revenue rose 4%, underscoring the resilience of our business model." → "Revenue rose 4%."
- *Software:* "The update adds offline mode, ensuring a seamless experience for users." → "The update adds offline mode, so the app works without a connection."

**False alarm:** an -ing clause that adds a fact, not a comment, is normal English: "She left the meeting early, taking the report with her."

---

## R · Rhetorical moves

### R1 · Contrast framing
**Sign:** "It's not X, it's Y", "This isn't just X. It's Y.", "not only X but also Y", "less about X and more about Y", "X isn't the problem. Y is." Three or more in one text and it's a skeleton.
**Why it's a tell:** the frame invents an opponent (who said it was "just a tool"?) to make the real claim sound bigger. Models use it constantly because it imitates insight.

**Before:**
> This isn't just a software update. It's a whole new way of working.

**After:**
> The update changes [what, in practice?].

**In the field:**
- *Education:* "Homework isn't about grades; it's about building habits." → "Homework is there to build study habits."
- *Marketing:* "It's not just coffee. It's a ritual." → say what's different about the coffee.

**False alarm:** a genuine correction of a real misunderstanding is fine: "The fee isn't charged monthly; it's charged once a year." The reader might really think it was monthly.

### R2 · Announced reveals
**Sign:** "Here's the thing:", "The truth is:", "The result?", "The kicker?", "Bottom line:", "Here's why that matters:", "Spoiler:". A label, a colon or question mark, then the point.
**Why it's a tell:** the drumroll is there because the point alone isn't dramatic. Once per text can be a voice; three times is a template.

**Before:**
> We tested both versions for a month. The result? Version B won by a mile.

**After:**
> We tested both versions for a month, and version B won clearly [by how much?].

**False alarm:** "Note:" and "Warning:" in documentation are labels with a job. So are "Q:" and "A:" in a FAQ.

### R3 · Asking and answering yourself
**Sign:** "Why does this matter? Because…", "So what changed? Everything.", "The answer? Simple."
**Why it's a tell:** the question isn't one the reader asked. It's a device to stretch one statement into two beats.

**Before:**
> Why does this matter? Because every customer deserves a fast answer.

**After:**
> Every customer should get a fast answer.

**False alarm:** a FAQ asks and answers by design, and a question the reader really has ("Do I need to reapply?") is fine as a heading.

### R4 · False ranges
**Sign:** "From X to Y" where X and Y aren't ends of a real scale: "from small startups to global enterprises", "from your morning coffee to your evening commute", "from beginners to experts".
**Why it's a tell:** the range pretends to cover everything between two points; usually it means "everyone" and says nothing.

**Before:**
> From first-time buyers to seasoned investors, our app has something for everyone.

**After:**
> The app is built for [which users, specifically?].

**False alarm:** a real range is fine: "for children from 4 to 11", "prices from £8 to £25".

### R5 · Aphorisms and fake depth
**Sign:** a quotable one-liner at the end of a paragraph: "Design is the language of trust." "Data tells a story." "And that makes all the difference." "Perhaps the real question was never asked."
**Why it's a tell:** it sounds wise and claims nothing that can be checked. Models close paragraphs with them by reflex.

**Before:**
> We rebuilt the checkout so it needs one page instead of three. Because in the end, simplicity is the ultimate form of respect.

**After:**
> We rebuilt the checkout so it needs one page instead of three.

**False alarm:** an essayist's own line, earned by the argument before it, is voice. The tell is a moral at the end of every paragraph.

### R6 · Significance inflation
**Sign:** "plays a pivotal role", "is a testament to", "marks a significant milestone", "underscores the importance of", "cannot be overstated", "more important than ever", "a watershed moment", "shaping the future of".
**Why it's a tell:** the text tells the reader how important something is instead of showing what happened. Models inflate by default.

**Before:**
> The opening of the new clinic marks a significant milestone in the city's healthcare journey and underscores the vital importance of accessible care.

**After:**
> The new clinic opened on [date] in [where?] and sees [which patients?].

**In the field:**
- *Academic:* "Social media plays a pivotal role in adolescent wellbeing." → "Social media use is associated with adolescent wellbeing [as found in…?]."

**False alarm:** "a key factor" in a statistical sense, backed by the analysis, is a finding, not inflation.

### R7 · Empty truths
**Sign:** a general statement no one would argue with: "Communication is key." "Every business is different." "Trust takes time to build." "Change can be challenging."
**Why it's a tell:** it fills space with agreement. A claim with content can be disagreed with.

**Before:**
> Communication is key to any successful project. That's why we hold a short stand-up every morning.

**After:**
> We hold a short stand-up every morning.

**False alarm:** in children's material or a policy statement of values, a plain general principle can be the point.

### R8 · Both-sides wrap-up
**Sign:** a closing that balances everything and decides nothing: "While challenges remain, the opportunities are immense." "Ultimately, the right choice depends on your individual needs."
**Why it's a tell:** it avoids committing to the conclusion the evidence supports.

**Before:**
> While remote work has its challenges, it also offers numerous benefits. Ultimately, the best approach depends on each organisation's unique needs.

**After:**
> [What does the evidence in the text point to? Say that, or say what's still unknown.]

**False alarm:** "it depends" is right when the text has just explained what it depends on.

### R9 · Pattern in disguise
**Sign:** the words of a known pattern have changed but its skeleton stays: "Rather than a tool, it's a movement", "Forget X. Think Y.", "X? Hardly. Y." The contrast frame and the reveal survive the paint job.
**Why it's a tell:** this is what a rewrite leaves behind when it swaps words instead of rebuilding. Check your own rewrite for it.

**Before (after a lazy rewrite):**
> Rather than simply a platform, it's a new way of collaborating.

**After:**
> Teams use the platform to [do what?].

---

## W · Words and register

### W1 · AI vocabulary
**Sign:** a cluster of words that models overuse: delve, tapestry, testament, pivotal, crucial, intricate, multifaceted, realm, landscape, navigate (the complexities), foster, embark, journey, showcase, underscore, boast, vibrant, holistic, nuanced, meticulous, invaluable, transformative, resonate, ever-evolving.
**Why it's a tell:** each word is fine on its own. Four in a paragraph is a fingerprint, and readers have learned to spot them.

**Before:**
> This study delves into the multifaceted landscape of remote learning, shedding light on the intricate interplay between engagement and outcomes.

**After:**
> This study looks at how engagement in remote learning relates to students' results.

**False alarm:** a geologist's "landscape", a ship that "navigates", a "crucial" step in a procedure that really fails without it. Count clusters, not words.

### W2 · Buzzwords
**Sign:** seamless, robust, cutting-edge, state-of-the-art, scalable, end-to-end, AI-powered, data-driven, innovative, synergy, ecosystem, best-in-class, empower, leverage, streamline, unlock value, next-generation, future-proof.
**Why it's a tell:** the words make a product sound technical without saying what it does. Plain-language guides for government writing list several of them as words to avoid (`style.md`).

**Before:**
> Our AI-powered, end-to-end solution seamlessly empowers teams to streamline their workflows.

**After:**
> The software [does what? e.g. assigns incoming requests to the right person].

**In the field:**
- *Public sector:* "We will leverage our robust digital ecosystem to drive transformation." → "We will [do what, with which service?]."

**False alarm:** in engineering, "scalable" and "robust" can be measurable claims ("scales to 10,000 concurrent users"). Keep them when the number is there.

### W3 · Term drift
**Sign:** one concept with three names in the same text (account, profile, workspace), or the terms of the wrong audience: spelled-out acronyms for engineers, team slang ("prod", "infra", "blocked on") for customers.
**Why it's a tell:** models vary words for style and don't track what the reader knows. Readers assume a new word means a new thing.

**Before:**
> Log in to your account. From your profile, open your workspace settings, then return to your dashboard.

**After:**
> Sign in, open [the one term the product uses] settings, then go back to the dashboard.

**False alarm:** a glossary or a "terms we use" section introduces synonyms on purpose.

### W4 · Hidden verbs
**Sign:** the action is turned into a noun and propped up by a weak verb: "make a decision", "conduct an analysis", "carry out an assessment", "provide assistance", "the implementation of the policy".
**Why it's a tell:** nominalisations stack up in machine prose and in bureaucratic prose alike; they make sentences longer and hide who does what. US plain-language guidance calls them hidden verbs (`sources.md`).

**Before:**
> The committee will make a decision following the completion of a review of the applications.

**After:**
> The committee will decide once it has reviewed the applications.

**False alarm:** some nouns are terms of art: "a risk assessment" is a named document in health and safety; "the implementation phase" can be a project stage.

### W5 · "Serves as" for "is"
**Sign:** "serves as", "stands as", "functions as", "acts as", "boasts", "features" where "is" or "has" would do.
**Why it's a tell:** models avoid the plain copula as if it were weak. People don't.

**Before:**
> The old station now serves as a community centre and boasts a café and a small library.

**After:**
> The old station is now a community centre with a café and a small library.

**False alarm:** "serves as" is right when something has a different main job: "the spare room serves as an office on Fridays".

### W6 · Filler and hedge stacks
**Sign:** "It's important to note that", "It's worth mentioning that", "It should be noted that", "In essence", "At its core"; and hedges piled up: "may potentially", "could possibly help to", "might arguably be seen as".
**Why it's a tell:** filler delays the point; stacked hedges show the writer won't commit even to uncertainty.

**Before:**
> It is important to note that this treatment may potentially help to reduce symptoms in some patients.

**After:**
> This treatment may reduce symptoms in some patients.

**In the field:**
- *Health:* keep exactly one hedge if the source hedges. "May reduce" must not become "reduces" (F17).

**False alarm:** academic writing hedges on purpose; one careful hedge per claim is good practice there.

### W7 · Agentless passive
**Sign:** "mistakes were made", "it was decided that", "priorities are set automatically", "applications will be processed", "an issue was identified". No one does anything.
**Why it's a tell:** the passive hides who is responsible, and models use it to sound formal. Plain-language guides ask writers to say who does what.

**Before:**
> It has been decided that the office will be closed on Fridays.

**After:**
> [Who?] has decided to close the office on Fridays.

**Note:** if the text doesn't say who decided, don't invent someone; ask, or keep the passive.

**False alarm:** in a methods section ("samples were stored at −20 °C") or when the actor really doesn't matter ("the building was finished in 1902"), the passive is right.

### W8 · Register whiplash
**Sign:** chummy and stiff in the same text: "Hey folks! 👋 We hereby wish to inform you that…", or "pursuant to" in a friendly team update.
**Why it's a tell:** models mix registers from different training texts; a person writing to a known audience keeps one.

**Before:**
> Hey everyone! 🎉 Please be advised that, pursuant to the updated policy, desks must be cleared prior to departure.

**After:**
> Hi everyone, quick reminder: under the new policy, please clear your desk before you leave.

**False alarm:** a deliberately comic contrast in an essay or a column is a choice, not a slip.

### W9 · Brochure voice
**Sign:** hidden gem, breathtaking, nestled, picturesque, unforgettable experience, awaits you, something for everyone, a must-visit, look no further, immerse yourself.
**Why it's a tell:** it's the default register for anything with a location or a product. It gives impressions, not information.

**Before:**
> Nestled in the heart of the Highlands, this hidden gem offers breathtaking views and an unforgettable experience for every traveller.

**After:**
> The village is in the Highlands [where exactly?]. [What can you see or do there that the writer saw or did?]

**False alarm:** marketing copy can sell, and a single "stunning" in a real estate listing is the genre. The tell is the pile-up, and brochure voice in a personal blog where the writer's own experience should be.

### W10 · Always the likeliest word
**Sign:** every word is the first that comes to mind ("plays an important role", "a wide range of", "in today's world", "take it to the next level"); nothing in the text surprises.
**Why it's a tell:** language models pick probable words. Human writers make some choices only they would make, mostly through specific details.

**Before:**
> The café offers a wide range of delicious food and drinks in a cosy atmosphere.

**After:**
> [What does the café actually serve that the writer remembers?]

**False alarm:** plain, common wording is not a tell by itself, and an instruction should be predictable. Only flag this when the whole text is made of stock phrases.

### W11 · Inflated wording
**Sign:** utilise, facilitate, commence, endeavour, ascertain, in order to, prior to, subsequent to, a number of, due to the fact that, in the event that, at this point in time, on a daily basis, has the ability to.
**Why it's a tell:** formal Latin-derived words and padded phrases where short ones do the same job. Government style guides in the UK and US give lists of these with plain replacements (`sources.md`).

**Before:**
> In order to commence the process, please utilise the form prior to submitting your application.

**After:**
> To start, use the form before you apply.

**False alarm:** some long words are the right term: "facilitator" is a job title; "commencement" is a ceremony; legal text keeps "prior" if the contract defines it.

---

## T · Tone and chat

### T1 · Chat residue
**Sign:** "I hope this helps!", "Certainly!", "Sure, here's a revised version:", "As an AI language model", "Let me know if you'd like me to adjust the tone", "Regenerate response", "[Insert name here]".
**Why it's a tell:** it's the assistant talking to its user, pasted into the final text. Conclusive on its own.

**Before:**
> Certainly! Here's a polished version of your announcement: We are pleased to share…

**After:**
> We are pleased to share…

**False alarm:** none in the final text. Placeholders that *you* leave on purpose (`[date?]`) are different: they're questions for the writer, named as such in the delivery.

### T2 · Sycophancy
**Sign:** "Great question!", "What a fantastic idea!", "You're absolutely right", "I love this".
**Why it's a tell:** praise before every answer is the chatbot's tic. In a published text it makes no sense.

**Before:**
> Great question! The deadline for applications is 30 June.

**After:**
> The deadline for applications is 30 June.

### T3 · Therapist voice
**Sign:** "It's completely understandable to feel overwhelmed", "You're not alone", "It's okay to take things one step at a time", "We hear you" in a text that isn't about feelings.
**Why it's a tell:** models soften every message as if the reader were distressed. In a leaflet or a notice it reads as condescending.

**Before:**
> We understand that changes to your account can feel overwhelming, and that's completely okay. You're not alone.

**After:**
> [Delete. The next sentence should say what changes.]

**False alarm:** in mental-health resources, bereavement letters or support services, acknowledging feelings is the content.

### T4 · Fake candour
**Sign:** "Let's be honest:", "I'll be real with you", "Here's the uncomfortable truth", "Let that sink in.", "Read that again."
**Why it's a tell:** it announces honesty instead of being direct.

**Before:**
> Let's be honest: most meetings could be an e-mail.

**After:**
> Most of our meetings could be an e-mail.

### T5 · Tour-guide voice
**Sign:** "Let's dive in", "In this article, we'll explore", "Buckle up", "Let's unpack this", "Without further ado", "Everything you need to know about", "Big news! 🚀", "I'm thrilled to announce".
**Why it's a tell:** the text describes itself instead of starting.

**Before:**
> In this comprehensive guide, we'll dive into everything you need to know about setting up your account. Let's get started!

**After:**
> To set up your account, you need [what?].

**False alarm:** a long manual can have a one-line "This guide covers X and Y" for readers deciding whether they're in the right place.

### T6 · Stock openings
**Sign:** "In today's fast-paced world", "In the ever-evolving landscape of", "In an era where", "In the digital age", "Have you ever wondered", "Imagine a world where", "It's no secret that".
**Why it's a tell:** it warms up instead of starting. The first sentence carries no information.

**Before:**
> In today's fast-paced business environment, customer experience is more important than ever. That's why we've launched a new support portal.

**After:**
> We've launched a new support portal.

**In the field:**
- *Finance:* "In today's ever-changing financial landscape, we're committed to value." → start with the change to the account.

### T7 · Stock closings
**Sign:** "In conclusion", "Ultimately", "At the end of the day", "The future is bright", "The possibilities are endless", "Here's to…", "Remember: …", "What do you think? Let me know in the comments!"
**Why it's a tell:** the ending summarises, cheers or asks for engagement instead of finishing. Every model post ends the same way.

**Before:**
> Ultimately, it's about working smarter, not harder. What's your favourite productivity tip? Let me know below! 👇

**After:**
> [End on the last real point, or on the next step: what should the reader do or expect?]

**False alarm:** a genuine question to readers once in a while is fine on social media. The tell is a question at the end of every post.

### T8 · E-mail formulas
**Sign:** "I hope this email finds you well", "I hope you're doing well", "I wanted to reach out", "Just circling back", "Please find attached", "Please don't hesitate to reach out", "Thank you for your time and consideration", "at your earliest convenience".
**Why it's a tell:** one of them may be the writer's habit or company style. Three in one short e-mail is a template, and generated e-mails use them all.

**Before:**
> I hope this email finds you well. I wanted to reach out regarding the invoice. Please find attached a copy. Please don't hesitate to reach out if you have any questions.

**After:**
> I've attached a copy of the invoice [number?]. [What do you need the reader to do, and by when?]

**False alarm:** "Please find attached" is still normal in some formal and international business correspondence. Leave a single formula alone if it's the writer's style.

---

## P · Punctuation and format

### P1 · Em-dash habit
**Sign:** em dashes for asides, drama and afterthoughts in nearly every paragraph: "— and the results speak for themselves", "— not just X, but Y —". Spaced en dashes or double hyphens doing the same job.
**Why it's a tell:** the em dash is a real English mark with real uses, and many good writers love it. What gives machine text away is the density, and the dash used as a drumroll before a reveal.

**Before:**
> The new dashboard went live on Friday — and the early feedback has been incredible. It brings everything together — tickets, chats, and e-mails — in one place.

**After:**
> The new dashboard went live on Friday, and the early feedback has been good [any specifics?]. It puts tickets, chats and e-mails in one place.

**False alarm:** a dash that breaks off speech in dialogue ("I didn't—") stays. A writer whose own sample uses dashes now and then can keep one where it works. In fiction and essays an occasional dash is voice.

### P2 · Semicolon swap
**Sign:** the semicolon that replaced a removed dash, keeping the same two-beat "statement; reveal" frame: "It's not a tool; it's a movement."
**Why it's a tell:** the punctuation changed, the skeleton didn't (R9).

**Before:**
> This isn't just a policy change; it's a cultural shift.

**After:**
> The policy changes [what?].

**False alarm:** semicolons that separate list items containing commas, or two closely linked clauses in careful prose, are standard. Some house styles avoid them entirely (`style.md`).

### P3 · Bold sprinkling
**Sign:** every key term in bold, several times a paragraph.
**Why it's a tell:** chat interfaces render markdown, so models bold for skimmability. In a document, bold everywhere means emphasis nowhere.

**Before:**
> Our **mission** is to deliver **value** through **innovation** and **collaboration**.

**After:**
> [Say what the organisation does; no bold needed.]

**False alarm:** bold for UI labels in instructions ("Select **Save**") is a common convention.

### P4 · Labelled bullets
**Sign:** bullets that start with a bold label and then repeat it: "**Scalability:** The platform scales with your needs." Or bullet points for ideas that are really an argument.
**Why it's a tell:** the label-colon-sentence list is a chatbot format. It chops reasoning into slogans.

**Before:**
> - **Speed:** The new process is faster.
> - **Simplicity:** It's simpler to use.
> - **Savings:** It saves money.

**After:**
> The new process is faster and simpler, and it costs less [how much less?].

**False alarm:** reference material, a glossary, a feature comparison table or real parallel items can be a labelled list.

### P5 · Emoji decoration
**Sign:** 🚀 on every announcement, ✅ on every bullet, 💡 before every tip, 👇 before the call to comment.
**Why it's a tell:** it's a template of a social post, applied to texts where emoji don't belong.

**Before:**
> 🚀 Big news! ✅ Faster loading ✅ New design 💡 Smarter search

**After:**
> The new version loads faster, has a new design and improves search [in what way?].

**False alarm:** the writer's own emoji habit on social media is their voice. Keep it, but sparingly.

### P6 · Heading case drift
**Sign:** "Key Steps For Deploying" in one heading and "How to roll back" in the next; title case with capitalised minor words ("The Rise And Fall Of…").
**Why it's a tell:** models switch between styles from different sources. Real documents follow one house style.

**Before:**
> ## Getting Started With The API
> ## How to authenticate
> ## Rate Limits And Quotas

**After:**
> ## Getting started with the API
> ## How to authenticate
> ## Rate limits and quotas

**False alarm:** title case is a legitimate house style (many publishers and US organisations use it). The tell is mixing styles, or capitalising "and", "of", "the" inside a title-case heading.

### P7 · Over-explaining
**Sign:** every acronym spelled out and every term glossed, even for readers who use them daily: "CI/CD (Continuous Integration and Continuous Deployment)", "API (Application Programming Interface)", "ROI (return on investment)" for a finance team.
**Why it's a tell:** models explain for an imaginary general reader. A colleague writing to colleagues doesn't.

**Before:**
> Submit a Pull Request (PR) and wait for the CI/CD (Continuous Integration and Continuous Deployment) pipeline to pass.

**After:**
> Open a PR and wait for CI to pass.

**False alarm:** for a general audience, spelling out an acronym on first use is good practice (`style.md`).

### P8 · Consistency slips
**Sign:** "color" and "colour", "organize" and "organise" in one text; a serial comma in one list and not the next; straight and curly quotes mixed; "e-mail" and "email"; "10am" and "10:00 AM".
**Why it's a tell:** generated text stitches together conventions from different sources. A person or a house style picks one.

**Before:**
> Our organisation will prioritize the new color scheme in the autumn.

**After (UK):**
> Our organisation will prioritise the new colour scheme in the autumn.

**False alarm:** a quotation or a proper name keeps its own spelling ("World Health Organization" in a UK text).

---

## E · Evidence and fiction

### E1 · Vague authority
**Sign:** "Experts say", "Studies show", "Research suggests", "According to industry reports", "Many believe".
**Why it's a tell:** it borrows authority without a source, and models produce it whenever a claim needs support.

**Before:**
> Studies show that remote workers are more productive.

**After:**
> [Which study? If the text has none, write "We've found that…" if it's the writer's own experience, or cut the claim.]

**False alarm:** a news report can say "officials said" when the source is in the next sentence. A review article can summarise a literature it then cites.

### E2 · Invented cases and figures
**Sign:** "One client increased sales by 300% in two weeks." "Over 90% of users report higher satisfaction." Precise, flattering numbers with no source.
**Why it's a tell:** models generate plausible specifics to sound concrete. This is also the most harmful habit of humanizing tools: an invented figure in a published text.

**Before:**
> Response times have dropped significantly.

**After:**
> Response times have dropped [by how much, over what period?].

**False alarm:** a figure that's in the source stays, word for word. An example clearly marked as hypothetical ("Say you earn £30,000…") is fine.

### E3 · Gap filling
**Sign:** "While specific details are limited, it is likely that…", "As of my last update…", "Although information is scarce, it can be inferred that…".
**Why it's a tell:** the model fills a gap with speculation, and the hedge admits it.

**Before:**
> While specific details about the merger are limited, it is likely that both companies will benefit from increased market share.

**After:**
> The details of the merger haven't been announced [or: what's known so far?].

### E4 · Template challenges paragraph
**Sign:** "Despite its successes, X faces several challenges, including…" followed by "However, with continued investment and innovation, X is well positioned to…".
**Why it's a tell:** it's the encyclopedic template every model learned: praise, challenges, hopeful future.

**Before:**
> Despite these achievements, the programme faces several challenges, including funding constraints and staffing shortages. However, with continued commitment, it is well positioned for future success.

**After:**
> The programme is short of [money, staff, both? figures?].

### E5 · Fiction clichés
**Sign:** "A wave of nostalgia washed over her", "a breath she didn't know she'd been holding", "eyes that held a mixture of grief and determination", "the silence was deafening", "somewhere in the distance, a dog barked", "In that moment, she knew everything would change", "his voice barely above a whisper".
**Why it's a tell:** models name feelings and reach for the stock image. They also end scenes on a sentence of meaning.

**Before:**
> A wave of sadness washed over Clara as she stood in the kitchen, looking at the chipped blue mugs. Her eyes held a mixture of grief and determination.

**After:**
> Clara stood in the kitchen. She picked up one of the chipped blue mugs, put it down, picked it up again. *(added detail: her hands)*

**Note:** the mugs are in the source; the repeated movement is an added detail, listed in the table so the writer can remove it.

**False alarm:** a writer's deliberate pastiche, or a character who talks in clichés, is voice.

### E6 · Over-correction
**Sign:** the marks humanizing tools leave: forced fragments ("Weird. But true."), fake typos, slang on every line ("ngl", "lowkey"), random lowercase, swearing for authenticity, "honestly" and "literally" sprinkled in.
**Why it's a tell:** it imitates human mess without a human reason. Readers and detectors both learn this signature.

**Before (an over-corrected rewrite):**
> ok so. the new app? honestly kinda wild. like, it just… works?? lol

**After:**
> The new app works better than I expected. [In what way, for the writer?]

**False alarm:** a writer whose own voice is like that, as shown by their sample, keeps it.
