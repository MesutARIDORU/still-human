# Writing by field

The text type (`genres.md`) tells you the form: an e-mail, a specification, a story. The field tells you the subject and the reader: the same e-mail reads differently from a bank and from a school. Once you've settled the field in step 1, read its section here. `audit.py --guide` prints the section for the field it guessed; for a particular field use, for example, `audit.py --guide "Finance"`.

Every section has the same headings:
- **Who reads it:** the field's readers and the register each one expects.
- **How models write here:** the AI tells typical of the field.
- **Don't touch:** facts that would do harm if they changed.
- **Style:** numbers, units, abbreviations and names common in the field (the rules are in `style.md`).
- **Before / After:** a short example. The after text adds nothing that isn't in the before text, and asks for missing facts in square brackets.

## Rules for every sector

- **Figures, dates, durations, amounts, doses and clause numbers** stay exactly as they are. Rounding, converting units or adding "about" is a change too.
- **Legal notices and required disclosures** are not shortened, simplified or deleted: risk warnings, side-effect warnings, cancellation rights, privacy notices, regulatory wording. Even if their language looks stiff, ask the text's owner.
- **The strength of a claim** stays. "May deliver higher returns" doesn't become "delivers higher returns"; "can help manage symptoms" doesn't become "treats".
- **Names of organisations, products and job titles** stay as the owner wrote them.

---

## Software and technology

**Who reads it:**
- The developer team: established terms stay (deploy, PR, release, staging).
- People who use the product: the words they use (update, sign in, goes live), not the team's slang.
- A customer's IT lead: technical, precise, without sales language.

**How models write here:**
- Release notes that open with excitement and emoji: "We're thrilled to unveil our most powerful release yet! 🚀" (T5, P5).
- Adjectives that don't say what changed: "powerful", "flexible", "seamless", "a more intuitive experience" (W2).
- Over-explaining for engineers: "Pull Request (PR)", "Continuous Integration and Continuous Deployment (CI/CD)" (P7).
- Incident notes in the agentless passive: "An issue was identified and has since been resolved." Nothing about what broke, for how long, or who was affected (W7).
- Error messages in therapist voice: "We understand how frustrating this can be." (T3)

**Don't touch:** code, commands, version numbers, error codes, API and library names, UI labels, CVE numbers and affected version ranges in a security notice, the times in an incident report.

**Style:** code, commands, file names and parameters go in code formatting. Version numbers stay as written: "version 4.2.1", not "v4.2". Product and API names keep their own capitalisation (GitHub, iOS, macOS, npm).

**Before:**
> We experienced a brief service disruption earlier today. Thanks to the tireless efforts of our dedicated engineering team, the issue was swiftly identified and resolved. We sincerely apologize for any inconvenience this may have caused.

**After:**
> Between [start time] and [end time] today, [which service] was unavailable. We've fixed it; the cause was [what?]. To stop it happening again, we're [doing what?]. We're sorry for the disruption.

**What changed:** the three things the reader of an incident note wants came first: when, what stopped working, why. They aren't in the text, so they're placeholders. "Tireless efforts of our dedicated engineering team" told the reader nothing, so it went.

## Finance

**Who reads it:**
- Retail customers: short, clear text with the figure up front.
- Investors and analysts: precise, numerate, no hype.
- Internal finance teams: their established terms (accruals, P&L, run rate, EBITDA).

**How models write here:**
- Comfort without content: "We are committed to providing you with the best possible value" around a rate cut (T3, R7).
- "In today's ever-changing financial landscape" (T6).
- Hedged promises that slide into guarantees in a rewrite: "could help you grow your savings" quietly becoming "will grow your savings". Don't let that happen.
- Significance inflation in reports: "delivered a robust performance underscoring our resilient business model" (R6, W2).

**Don't touch:** interest rates and their labels (APR, AER, APY), fees, dates when a change takes effect, notice periods, tax years, risk warnings ("the value of investments can go down as well as up"), regulator names, account and product names.

**Style:** keep the currency symbol and decimals as written (£75, £75.50, $1,250.00). Percentages stay numerals with "%". Don't turn "3.10% AER" into "about 3%". Write "million" and "billion" the way the text does; don't mix "m" and "million".

**Before:**
> In today's ever-changing financial landscape, we are committed to providing you with the best possible value. As part of our ongoing efforts to streamline our product offering, the interest rate on your account will change from 3.10% AER to 2.85% AER, effective 1 December 2026.

**After:**
> From 1 December 2026, the interest rate on your account will change from 3.10% AER to 2.85% AER.

**What changed:** the change, the figures and the date came first, untouched. The opening and "streamline our product offering" carried no information for the customer. If the bank wants to give a reason for the change, it should be the real one: [reason for the change?].

## Health

**Who reads it:**
- Patients and carers: short sentences, everyday words, the action and its timing clear.
- Clinicians: precise terms, no simplification that loses meaning.
- Health administrators: the service's own terms.

**How models write here:**
- Therapist voice in a practical leaflet: "We understand that starting a new medication can feel overwhelming. You're not alone on this journey." (T3)
- Hedge stacks: "may potentially help", "could possibly improve" (W6).
- Significance inflation: "plays a crucial role in managing" (R6).
- A slogan ending: "Remember, your health is your most valuable asset!" (T7)

**Don't touch:** drug names, doses, units, frequency and timing ("twice a day with meals"), durations, side effects and warning signs, the instruction for what to do if they appear, contact numbers. Don't make a hedged clinical claim stronger, and don't make a warning weaker.

**Style:** keep units with a space as written ("500 mg"). Spell out frequencies the way the text does. Plain words help patients ("stomach pain" rather than "abdominal discomfort") unless the text is for clinicians.

**Before:**
> Metformin plays a crucial role in helping to manage blood sugar levels in people with type 2 diabetes. Your doctor may potentially increase your dose after two weeks. These effects could possibly improve over time as your body adjusts.

**After:**
> Metformin helps to control blood sugar in people with type 2 diabetes. Your doctor may increase your dose after two weeks. These side effects may get better as your body gets used to the medicine.

**What changed:** "plays a crucial role in" became the verb. Each stacked hedge became a single "may". The dose timing and the claim's strength stayed the same.

## Education

**Who reads it:**
- Students: direct, the task and the deadline clear.
- Parents and carers: plain, no school jargon.
- Teachers and staff: their professional terms (assessment criteria, scaffolding, differentiation).

**How models write here:**
- "Embark on an exciting learning journey" (W1, W9).
- Holistic, transformative, empowering learners to reach their full potential (W2).
- Rubrics full of untestable adjectives: "demonstrates a comprehensive and nuanced understanding".
- Letters home that bury the date of the trip under three paragraphs of values.

**Don't touch:** dates, deadlines, grade boundaries, assessment criteria, course codes, attendance rules, safeguarding wording.

**Style:** course and module names keep their capitalisation. Grade labels stay exactly as the school writes them.

**Before:**
> We are excited to embark on this enriching learning journey with your child as we explore the fascinating world of science through hands-on experiences that foster curiosity and critical thinking.

**After:**
> This term your child will do [how many?] practical science sessions [on what topics?].

**What changed:** the only fact in the sentence was that the science would be hands-on. The rest was brochure language. What a parent needs (how much, what topics) isn't in the text, so it's asked for.

## Law

**Who reads it:**
- Lawyers and the courts: precise terms, set phrases.
- Clients: plain English about what a clause means for them, without changing what it says.
- Staff following a policy: what they must and must not do.

**How models write here:**
- Friendly padding in a notice that must be exact.
- Marketing words in terms and conditions: "seamless", "hassle-free".
- Vague references: "in accordance with the relevant regulations".
- Over-hedging that blurs an obligation: "parties should endeavour to potentially…".

**Don't touch:** defined terms and their capitalisation, "shall", "must", "may", clause numbers and cross-references, statute names, notice periods, limitation and liability wording. Rewrite nothing with legal effect without asking.

**Style:** keep numbers as the document writes them, including the "thirty (30) days" form if it is used. Keep the document's own capitalisation of defined terms ("the Agreement", "the Supplier").

**Before:**
> We want to make cancelling as hassle-free as possible! Simply let us know within the cooling-off period and we'll take care of the rest.

**After:**
> You can cancel within the cooling-off period of [how many days?]. To cancel, [how: e-mail, form, phone?].

**What changed:** "hassle-free" and "we'll take care of the rest" hid the two things a customer has a right to know: the period and the method. Neither is in the text, so both are asked for. Check the legally required wording with the text's owner.

## Retail and e-commerce

**Who reads it:**
- Shoppers: the price, the delivery date, the return terms.
- Marketplace sellers: the platform's rules and fees.

**How models write here:**
- Brochure voice on product pages: "elevate your everyday with our exquisitely crafted…" (W9).
- "Whether you're a seasoned chef or a kitchen novice, we've got you covered" (R4).
- Order e-mails padded with thanks before the tracking number.

**Don't touch:** prices, discounts and their conditions, dates of a sale, delivery times, return and refund periods, sizes and materials, safety information.

**Style:** prices keep their currency and decimals. "Free delivery over £50" stays exactly that; "free delivery" alone would change the offer.

**Before:**
> Elevate your morning ritual with the Aurora kettle — a masterpiece of design that effortlessly combines style and functionality. Whether you're a tea lover or a coffee connoisseur, it's the perfect addition to any kitchen.

**After:**
> The Aurora kettle [capacity?] boils [how fast?]. [Material and finish?]

**What changed:** the text named the product and nothing else about it. Every claim was brochure voice. A shopper wants capacity, speed and materials, and none of them is in the text.

## Public sector and local government

**Who reads it:**
- Residents and citizens, many of them reading under pressure or in their second language.
- Businesses dealing with a regulator.
- Other public bodies.

**How models write here:**
- "We are committed to delivering high-quality, resident-focused services" (W2, R7).
- Agentless passives: "Applications will be processed and decisions communicated in due course" (W7).
- Words from the buzzword lists of plain-language guides: deliver, drive, facilitate, robust, key, going forward, empower (see `jargon.md`).

**Don't touch:** eligibility rules, deadlines, amounts, legal duties, opening hours, phone numbers and addresses, the names of schemes, forms and acts.

**Style:** many public bodies use sentence case everywhere, numerals for numbers, and "to" for ranges ("10am to 4pm"). Follow the organisation's own style guide if it has one (`style.md`).

**Before:**
> Residents are advised that applications will be processed in due course and outcomes will be communicated via the appropriate channels.

**After:**
> We'll look at your application and tell you our decision [by when?] [by letter, e-mail or text?].

**What changed:** the council became "we", the resident became "you". "In due course" and "the appropriate channels" are the two facts a resident wants, so they are placeholders.

## Human resources

**Who reads it:**
- Employees: what changes for them, from when, what they need to do.
- Candidates: the job, the pay, the process.
- Managers: the policy and their part in it.

**How models write here:**
- Job ads full of "rockstar", "ninja", "fast-paced environment", "passionate self-starter" (W2, T6).
- "We're a family" and "our people are our greatest asset" (R7).
- Policy announcements in therapist voice: "We understand change can be difficult" (T3).

**Don't touch:** salaries and ranges, leave allowances, notice periods, dates a policy starts, eligibility rules, legally required statements (equal opportunities, right to work).

**Style:** job titles are capitalised when they are titles ("Head of People") and lowercase when they describe ("our people team").

**Before:**
> We're looking for a passionate, results-driven rockstar to join our fast-paced, dynamic team and help us take things to the next level!

**After:**
> We're hiring a [job title] to [main responsibility?]. You'll report to [whom?].

**What changed:** none of the adjectives said what the job is. The ad needs the title, the work and the reporting line; they're not in the text, so they're asked for.

## Marketing and communications

**Who reads it:**
- Customers and prospects.
- Journalists reading a press release.
- Followers on social media.

**How models write here:**
- Press releases with "is thrilled to announce" and "a leading provider of innovative solutions" (T5, W2).
- Campaign copy built from triads and contrast frames: "Bold. Fresh. Unstoppable." "It's not just a drink, it's a lifestyle." (S2, R1).
- Quotes from executives that no person would say: "We are incredibly excited about this transformative partnership." (W1)

**Don't touch:** names, dates, prices, the offer's conditions, quotes attributed to a named person (suggest edits; don't rewrite them yourself), trademarks and their symbols.

**Style:** keep brand names exactly as the brand writes them, including unusual capitalisation. In a press release, keep the dateline and the "About" section as written.

**Before:**
> Northwind is thrilled to announce a groundbreaking partnership with Contoso that will revolutionise the way businesses manage their data.

**After:**
> Northwind and Contoso are working together on [what, exactly?], starting [when?].

**What changed:** "thrilled", "groundbreaking" and "revolutionise" carried no facts. What the partnership is and when it starts are the news, and neither is in the text.
