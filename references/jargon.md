# Field terms and business jargon

The yardstick is the language the reader actually uses, not the dictionary and not the writer's team. A word can be correct and still sound wrong for the audience: "deploy" is right in an engineering channel and odd in a customer e-mail; "go live" is right for customers and slightly vague for engineers.

## Six rules

1. **Decide the audience first.** The same fact is "we merged the fix and deployed it to production" for developers and "the fix is live" for customers.
2. **One term per concept.** Pick the reader's term and keep it (W3). If the product calls it a "workspace", don't also call it a "project", "space" and "environment".
3. **Don't explain what the reader knows.** Spelled-out acronyms and glossed terms for specialists are a tell (P7). For general readers, explain a term once, at first use.
4. **Buzzwords are the real tell.** Seamless, robust, end-to-end, empower, leverage, synergy: words that make a text sound technical or strategic without saying anything (W2). Replace them with what the thing does.
5. **Office jargon depends on the room.** "Circle back" and "bandwidth" are normal inside some teams. In a customer letter, a job ad or anything public, they sound like a template.
6. **Never change** code, commands, file names, product names, UI labels, quoted text, or a term that has a defined meaning in a contract, a regulation or a clinical guideline.

---

## Software and product development

| Concept | Developer team | General readers | Avoid |
|---|---|---|---|
| Putting a change live | deploy, ship, release, push to prod | goes live, is now available, update | "rolled out a game-changing update" |
| Code review request | PR, pull request, merge request (GitLab) | (rarely needed) | "Pull Request (PR)" spelled out for engineers |
| Automated build and test | CI, the pipeline, CI/CD | (rarely needed) | "Continuous Integration and Continuous Deployment (CI/CD)" for engineers |
| Test environment | staging, dev, preview | test version | "pre-production environment" in a team chat |
| A fault | bug, regression, incident | problem, issue, outage | "an unexpected anomaly" |
| Fix | patch, hotfix, fix | fix, update | "remediation" outside a security report |
| Feature that is hidden until ready | feature flag, behind a flag | (not mentioned) | "toggled capability" |
| Signing in | auth, SSO, log in | sign in, log in (pick one and keep it) | mixing "sign in", "log in" and "login" in one text |
| Product's settings | config, settings | settings | "configuration preferences" |
| Something blocking progress | blocked on, blocker | delayed, waiting for | team slang in a customer note |

**In release notes for users:** say what changed and what the user can now do: "You can now export reports as CSV." Not "Enhanced reporting capabilities."

## Finance

| Concept | Industry and internal | Retail customers | Avoid |
|---|---|---|---|
| Yearly interest on savings | AER (UK), APY (US) | the interest rate, AER/APY as written | changing the label or rounding the figure |
| Yearly cost of borrowing | APR | APR, as written | "competitive rates" without the figure |
| Money in and out over time | cash flow | money coming in and going out | "liquidity dynamics" |
| Profit and loss | P&L | profit (or loss) | "bottom-line performance" |
| Earnings before interest, tax, depreciation and amortisation | EBITDA | (explain once, or avoid) | spelling it out for analysts |
| Charges | fees, charges | fees, as listed | "small administrative considerations" |
| Risk warnings | as required by the regulator | exactly as written | shortening or softening them |

**Customer letters:** the figure, the date and the action come first. "Your rate will change from 3.10% AER to 2.85% AER on 1 December 2026" is the sentence; everything else supports it.

## Health

| Concept | Clinicians | Patients and carers | Avoid |
|---|---|---|---|
| Stomach | abdomen, abdominal | stomach, tummy (for children) | "gastrointestinal discomfort" in a leaflet |
| High blood pressure | hypertension | high blood pressure | switching between the two in one leaflet |
| Medicine | medication, drug, the drug's name | medicine, tablets, the medicine's name | "pharmaceutical intervention" |
| How often | b.d., t.d.s. (prescriptions) | twice a day, three times a day | abbreviations in patient material |
| Side effects | adverse effects | side effects | "you may experience some unwanted sensations" |
| Get help urgently | escalate | call 999 / 911 / your doctor (as written) | "reach out to a healthcare professional" when the text names a number |

**Never change** a dose, a unit, a frequency, a duration, a warning sign or what to do about it. Keep the hedging of a clinical claim exactly as strong as the source.

## Law

| Concept | Legal drafting | Plain-English summary for clients | Avoid |
|---|---|---|---|
| Obligation | shall, must | must, have to | turning "shall" into "will" or "should" in the clause itself |
| Permission | may | can, may | "is empowered to" |
| End a contract | terminate | end, cancel | "sunset the agreement" |
| Make good a loss | indemnify | pay for losses caused by | "make you whole" (idiom) in a contract |
| Despite | notwithstanding | despite, even if | dropping it when it changes priority between clauses |
| The parties | the Parties (defined) | you and us | redefining terms in a summary |

**Rule:** a plain-English summary sits next to the legal text; it doesn't replace it. Rewrite clauses only when the user asks and has checked with whoever owns the document.

## Public sector and local government

| Concept | Internal and policy | Residents and citizens | Avoid |
|---|---|---|---|
| Make or provide a service | deliver, roll out | run, provide, start, offer | "deliver" for everything |
| Work with | collaborate, partner with, engage | work with, talk to | "engage stakeholders" in a public notice |
| Push something forward | drive, progress, advance | start, speed up, do | "drive forward the agenda" |
| Help someone do something | facilitate, enable, empower | help, let | "empower residents to" |
| Important | key, critical, robust | important (or just say why) | "key" and "robust" as filler |
| From now on | going forward | from now on, from [date] | "going forward" |
| Website or system | portal, hub, one-stop shop | website, online service, the service's name | "digital hub" |

Several of these words appear on the GOV.UK list of words to avoid (`style.md`, `sources.md`). They are the plain-language community's own catalogue of bureaucratic tells.

## Retail and e-commerce

| Concept | Internal | Shoppers | Avoid |
|---|---|---|---|
| Order delivery | fulfilment, last mile | delivery, shipping | "fulfilment journey" |
| Item out of stock | OOS, stock-out | out of stock, sold out | "currently unavailable at this point in time" |
| Returns | reverse logistics, RMA | returns, refund | "hassle-free returns" without the period and method |
| Basket | cart (US), basket (UK) | the site's own word | switching between the two |
| Discount | markdown, promo | discount, sale, X% off, as stated | "unbeatable savings" without the figure |

## Human resources

| Concept | HR team | Employees and candidates | Avoid |
|---|---|---|---|
| Joining process | onboarding | your first weeks, induction | "onboarding journey" |
| Leaving | offboarding, attrition | leaving | "transitioning out" |
| Time off | PTO, annual leave, leave entitlement | holiday (UK), vacation/PTO (US), as in the policy | mixing the two in one policy |
| Pay | compensation, total reward | pay, salary, benefits | "competitive compensation package" without a range |
| Staff numbers | headcount, FTE | number of people | FTE in a message to staff without explaining it |

**Job ads:** rockstar, ninja, guru, self-starter, fast-paced environment, work hard play hard, "we're a family". All tells, and some put people off applying. Replace them with what the job involves.

## Education

| Concept | Teachers and staff | Students and parents | Avoid |
|---|---|---|---|
| Support for different levels | differentiation, scaffolding | extra help, harder tasks for those who want them | "personalised learning journey" |
| Assessment | formative / summative assessment | quizzes, tests, exams, coursework | "holistic evaluation" |
| Goals of a lesson | learning objectives, outcomes | what you'll learn | "empowering learners to unlock their potential" |
| Term | term, semester (as the school uses) | term, semester | switching between the two |

## Marketing and communications

| Concept | Marketing team | Customers and press | Avoid |
|---|---|---|---|
| The audience | target audience, persona, segment | (not mentioned) | "our valued community" |
| How people respond | engagement, CTR, conversion | (not mentioned) | metrics in customer copy |
| New product | launch, GTM | new, now available | "thrilled to unveil our groundbreaking" |
| A company's offering | proposition, solution | the product's name, what it does | "innovative solutions" |
| Brand qualities | brand pillars, tone of voice | (shown, not stated) | "we are passionate about excellence" |

---

## Office jargon: what to say instead

Normal in some teams; a tell in public and customer-facing text, and in any text when it piles up.

| Jargon | Plainer |
|---|---|
| circle back | come back to, reply |
| touch base | talk, check in, call |
| bandwidth | time, capacity |
| deep dive | close look, detailed review |
| low-hanging fruit | easy wins, the simplest fixes |
| move the needle | make a difference, change [the figure] |
| take this offline | talk about it separately |
| action items | next steps, to-dos |
| align on | agree on |
| learnings | lessons, what we learned |
| going forward | from now on, from [date] |
| leverage (verb) | use |
| socialise (an idea) | share, run past people |
| ideate | come up with ideas |
| per my last email | as I said, as in my e-mail of [date] |
| reach out | contact, write to, call |

## Buzzwords: what to say instead

The replacement is almost never another word; it's the fact the buzzword was hiding.

| Buzzword | Ask instead |
|---|---|
| seamless, frictionless | What doesn't the user have to do any more? |
| robust | What load, failure or misuse does it survive? |
| cutting-edge, state-of-the-art, next-generation | What does it do that the previous version didn't? |
| scalable | Up to what number of users, requests, sites? |
| end-to-end | Which steps, from where to where? |
| AI-powered, data-driven | What does the AI or the data actually decide or do? |
| innovative, transformative, game-changing | What changed, for whom? |
| empower, enable | Who can now do what? |
| streamline | Which step is gone or shorter? |
| holistic | Which parts are now considered together? |
| best-in-class, world-class | Compared with whom, by what measure? |
| synergy | What will the two teams or companies do together? |

If the text doesn't contain the answer, leave a placeholder with the question; don't make the answer up.

## Over-explaining for specialists

For readers in the field, these are words, not acronyms. Don't spell them out unless the text is for general readers or the house style requires it.

- **Software:** API, SDK, CI, CD, PR, URL, HTTP, JSON, CSV, UI, UX, SSO, SQL, DNS, VPN, CPU, RAM, SaaS.
- **Finance:** APR, AER, APY, ROI, P&L, EBITDA, KPI, FX, ETF, IPO.
- **Health:** GP, A&E (UK), ER (US), NHS, MRI, ECG, BMI.
- **HR:** PTO, FTE, KPI, L&D.
- **Marketing:** SEO, CTR, CRM, B2B, B2C.

For a general audience, spell an acronym out once at first use, then use the short form, unless it's better known than its expansion (BBC, NASA, PDF, USB).
