# Product Analytics Case Study — Architecture Decision Record (ADR) & Self-Evaluation

An **Architecture Decision Record (ADR)** is a short document that captures one design choice:
what was decided, which alternatives were considered, why this one won, and what follows from
it. This one covers two decisions — the dataset, and the AI-assisted workflow shape — plus the
full QA trail and self-evaluation this project's scope required. Part 1 is the ADR proper; Part 2 is
the self-evaluation. The findings themselves are in `README.md` and the five notebooks.

---

## Part 1 — Architecture Decision Record

### Decision 1: the dataset

**Chosen: OULAD** (Open University Learning Analytics Dataset). Real, CC BY 4.0, 32,593
enrollments, no monetization stage.

**Alternatives considered, in the order they came up, and why each was rejected or replaced:**

| Candidate | What it offered | Why not chosen |
|---|---|---|
| **Sparkify mini** (Udacity, fictional music-streaming log) | Full SaaS-shaped journey: free/paid, upgrade, downgrade, cancel | Downloaded and profiled first. 220 of 225 users had already registered *before* the log's coverage window started — near-zero real signup cohorts. Activation would have been unmeasurable. Rejected at the profiling stage, before any analysis was built on it. |
| **GA4 sample e-commerce** (Google Merchandise Store, BigQuery public dataset) | Large N, real cohorts, revenue, CC BY 4.0 | Only reachable via BigQuery, which needs a Google Cloud account — no flat-file download existed the way Sparkify and OULAD had. Would have meant running SQL queries in an external console and pasting results back, a materially worse workflow than every prior exercise. Dropped for tooling-fit, not data quality, once a directly-downloadable alternative (OULAD) checked out. |
| **KKBox churn** (WSDM 2018 Kaggle competition) | Closest to real SaaS: actual subscription transactions, real churn | License/redistribution terms unverified, needs a Kaggle account. Not pursued once OULAD passed its own pre-lock check. |
| **Stack Exchange dump** | Real, CC BY-SA 4.0, multi-year cohorts | No monetization stage at all (raised, then dropped, before OULAD was even checked — see below) |
| **OULAD** — chosen | Real, CC BY 4.0, 32.6K enrollments, near-complete signup-to-outcome visibility (99.1% registered before course start), directly downloadable with no login | No monetization stage either — but this was the deliberate trade made over Sparkify's fake cohorts, after an explicit pre-lock check (profiling registration timing, cohort sizes, and outcome distribution *before* committing) |

**Why the trade was made explicitly, not assumed:** the user's own words mid-session — "the significance of 225 is very poor, i really hate it" — set the priority: real cohorts and adequate sample size over a literal monetization stage. The alternative (Stack Exchange, real cohorts, also no money) was on the table too; OULAD won because it also kept a rich, real, four-stage-mappable engagement log (VLE clicks, assessments, withdrawal dates), which Stack Exchange's Q&A structure doesn't offer as cleanly. This is disclosed prominently in `README.md` — the monetization stage is a labelled proxy throughout, never called revenue.

### Decision 2: the AI-assisted workflow shape

**Chosen: single analyst (me) + inline `analysis-rigor-pass` + one fresh `independent-verification` sub-agent on the headline claim.** Not a multi-agent pipeline.

**Alternatives considered:**

| Alternative | Why not chosen |
|---|---|
| Pure single-agent, no structural checks | This project has a known trap class — mechanically confounded metrics (tenure leaking into "engagement" measures) — that a single same-context pass is exactly the kind of thing to miss. This project's scope explicitly called for a rigor pass and independent verification; skipping either would have shipped at least one wrong headline number (see Part 2). |
| Sequential specialist pipeline (Explorer → Statistical Reviewer → Business Analyst) | This dataset is a handful of flat, well-understood tables with a canonical grain (one enrollment per subject×semester×student). There's no distinct "statistical reviewer" role to hand off to that the primary analyst can't do directly under this project's own rate-vs-mix/disentangling standards — the same reasoning that applies to similarly-shaped, single-table problems generally. |
| Parallel independent analysts (2–3, reconciled) | Worth it when a dataset supports genuinely different legitimate lenses (e.g. a dataset that could be read through price, reviews, host behaviour, or neighbourhood, with no single obvious throughline). OULAD's four-stage structure is closer to canonical — a second analyst would very likely re-derive the same headline story at several times the cost, not surface a materially different one. |
| **Chosen: single analyst + rigor-pass + one independent verifier** | Matches the actual risk shape: one well-bounded, four-stage analysis with a specific, identifiable class of trap (mechanical confounds from unequal tenure), which argues for a targeted, structural check exactly where the risk concentrates — not zero checking, not a full parallel pipeline. |

### Where QC actually occurred

1. **Rigor pass, before the write-up** — caught the exposure-matched lift correction (partial) and the whole-course tenure leakage in the feature-mix analysis (full rebuild of that section).
2. **Independent verification, after the rigor pass** — one fresh `general-purpose` sub-agent, given only the claim and pointers to the raw CSVs, explicitly told not to read any notebook, README, or prior reasoning. Verdict: HOLDS WITH CAVEAT — caught a date-boundary bug in the activation-window code (a missing
lower bound let pre-course browsing count as "first 14 days" activity) that the rigor pass's own
adversarial check had missed (see Part 2 for the full account).
3. **Gates with the user** — dataset choice (three rounds — see below), the analysis plan, then a skipped mid-review gate (the user asked for deliverables drafted first, review to follow top-to-bottom), before the eventual commit gate.
4. **<u>Attentive human review during the deliverable walkthrough</u>** — caught a definitional bug neither of the two structural QA layers above was scoped to find (see Part 2). Persistent terminology questions during final review forced a first-principles re-derivation of the project's grain, exposing a bug in the non-independence flag that a rigor-pass checklist and an independent sub-agent both structurally couldn't have caught, because neither was asking "what does this word actually mean."

---

## Part 2 — Self-evaluation

### The gates, and what was decided at each

| Gate | What happened |
|---|---|
| **Dataset choice** | Three rounds, not one. Round 1: proposed Sparkify/Stack Exchange/REES46 with trade-offs; the user picked Sparkify. Round 2: profiling Sparkify surfaced the near-zero-cohorts problem; escalated rather than folded in quietly, per this project's own scope-change rule. The user pushed back on all three reframing options offered and asked for a proper re-search. Round 3: GA4/OULAD/KKBox proposed; the user picked GA4; a tooling mismatch (BigQuery needing an external console) was caught before committing, flagged explicitly rather than quietly worked around, and OULAD was substituted and pre-checked before locking. |
| **Analysis plan** | Proposed mapping the four SaaS stages onto OULAD's actual tables (activation → early VLE engagement; engagement/retention → weekly clicks + withdrawal; feature adoption → VLE activity-type taxonomy; monetization → labelled value-outcome proxy), with the metrics-framework and rigor/verification plan stated up front. Approved without changes. |
| **Method (no statsmodels/scikit-learn)** | Neither library was already installed. Asked rather than assumed or auto-installed — and on review, stratified/cross-tab lift comparisons were judged sufficient for this analysis's actual questions (does a lift hold within every subgroup, not "fit the best-predicting model"), so the user chose not to add either dependency. This shaped every notebook's methodology (group-bys and lift tables instead of regression coefficients). |
| **Mid-project review** | Skipped by the user's explicit instruction to draft all deliverables first and review them top-to-bottom afterward, rather than the originally-planned "stop before the final narrative" checkpoint — noted here as a deviation from the original plan, made explicitly by the user, not assumed. |
| **Commit** | Carried out once the full top-to-bottom review was complete and every requested adjustment applied. |

### QA — rigor-pass findings and what was fixed

Ran the 14-gate checklist against all five notebooks. Full pass except:

- **Gate 7 (volume beside rate) — FIX, minor.** Notebook 02's within-education/age/first-timer lift
  tables printed only means, no group sizes. Fixed: added `n` columns throughout.
- **Gate 13 (leakage) — FIX, major.** Notebook 04's "engagement volume dominates feature mix"
  claim used whole-course click totals. Checked directly: whole-course `total_clicks` correlates
  0.43–0.48 with success, but *tenure-adjusted* (clicks per enrolled day) that collapses to
  0.02 — almost entirely a tenure artifact (a student who stays enrolled longer
  mechanically accumulates more clicks). **Fixed by rebuilding that entire section** on the same
  14-day early window as the activation signal, where exposure is comparable. A secondary
  finding built on the leaky version (light-engagement users showing a differentiating
  `quiz`-share correlation) **did not survive** the fix and was retracted, not softened — see
  below.
- **Gate 14 (internal consistency) — FIX, minor.** Notebook 05's Guardrail 1 ("submission rate
  confirms activation isn't hollow clicking") didn't originally acknowledge that non-activated
  enrollments overlap heavily with early-withdrawers, who mechanically can't submit later work
  regardless of engagement quality — the same underlying mechanism as the lift correction above,
  showing up a third time. Softened the framing rather than treating it as clean confirmation.

The rigor-pass process also closes with two checks that sit outside the 14 numbered gates:
arguing the opposite of the single highest-stakes conclusion, and (when a real methodological
choice was made) stress-testing it against an alternative. The first of those two is what
actually caught the mechanical lift inflation:

- **Adversarial "argue the opposite" check, applied to the headline claim — FIX, major.** Stress-tested
  it by excluding enrollments that withdrew within the 14-day activation window itself
  (mechanically unable to activate) — shrank the raw lift from 34.8pp to a more defensible
  24.5pp among 14-day survivors. Both numbers are kept, clearly labelled, with the smaller one
  used as the project's headline figure.

All other gates passed clean, including Gate 5 (rate-vs-mix), checked explicitly on the primary
metric itself: pooled activation rate (61.7%, post-fix) vs. subject-equal-weighted average
(computed separately) differ by ~1pp — not mix-driven.

### Independent verification result

**Claim tested:** "Among enrollments that survived at least 14 days, activated enrollments
(≥3 active days in the first 14) succeed at 59.5% vs. 33.8% for non-activated — a 25.7pp gap —
holding in all 7 subjects." (The rigor-pass-corrected figure at the time of the test.)

**Verdict: HOLDS WITH CAVEAT.** A fresh `general-purpose` sub-agent, given only the claim and
pointers to the raw CSVs — explicitly instructed not to read any notebook, README, or this
reasoning chain — independently computed 62.15% / 37.65% (24.49pp gap). The direction and the
7/7-subjects-positive pattern reproduced cleanly; the gap itself was within tolerance (1.2pp); but
**both group rates individually diverged by 2.65–3.85pp**, and the sub-agent's own activation
count (19,571) differed from mine (22,881 at the time) by 3,310 enrollments on an identical
28,128-person population — too large to be noise.

**Root cause, found by investigating the divergence rather than accepting "close enough":**
`prep.build_engagement`'s early-window filter was `date < early_window_days` with **no lower
bound**. `studentVle.csv` has pre-course rows (negative `date` — students browsing before their
own course's start), which were silently counting toward "first 14 days." This inflated the
activation classification by ~3,700 enrollments project-wide. **Fixed** (`0 <= date <
early_window_days` in both `build_engagement` and `build_activity_mix`), and every processed
table and all four downstream notebooks (02–05) were regenerated. The corrected numbers
(62.2% / 37.7%, 24.5pp) now match the independent sub-agent's figures almost exactly — confirming
the fix, not just patching the symptom.

### Where checks disagreed, and how it was resolved

Two distinct disagreements, at two different layers:

1. **Within the rigor pass itself:** the analysis's first-draft headline number (34.8pp raw lift,
   full population) disagreed with its own adversarial recheck (24.5pp, 14-day survivors only).
   Resolved by keeping both, clearly labelled, with the smaller number adopted as the headline
   claim — not by picking one and discarding the other.
2. **Between the rigor-pass-corrected analysis and independent verification:** my exposure-matched
   figures (59.5% / 33.8%) disagreed with the fresh sub-agent's (62.15% / 37.65%) by 2.65–3.85pp per
   group, despite an aligned gap. This is the more serious kind of disagreement — not "which
   number is more honest," but "these should be identical and aren't." Resolved by treating the
   divergence itself as a finding worth investigating rather than accepting the HOLDS WITH CAVEAT
   verdict at face value: traced to the date-boundary bug, fixed, and both sides' numbers now
   converge. **This is the single clearest value independent verification added in this project**
   — the rigor pass's own adversarial check (same author, same context) had already stress-tested
   this exact claim once and did not surface the boundary bug, because it never had a reason to
   write an independent line of code from raw data with no assumptions inherited from the first
   pass.

### AI-assisted workflow notes — where Claude was wrong or needed correcting

- **The date-boundary bug (above) is the clearest example.** It existed through three notebooks'
  worth of analysis and one full rigor pass before being caught — not because the rigor pass
  wasn't thorough, but because a same-context check inherits the same unstated assumption
  ("early window" obviously means days 0–13) that produced the bug in the first place. Only a
  fresh implementation, from raw data, with zero exposure to that assumption, was structurally
  positioned to catch it.
- **A plausible-looking secondary finding was wrong and got retracted, not softened.** The
  original notebook 04 reported that light-engagement students showed a strong positive
  correlation between quiz-usage share and success (+0.26), and proposed a targeted nudge as a
  recommendation. It was a pure artifact of the same tenure confound that inflated the
  headline volume correlation. Caught by the rigor pass's own Gate 13 check (not by independent
  verification, which wasn't scoped to this specific claim), and removed from the recommendations
  list with an explicit note rather than quietly dropped.
- **A tooling mismatch was caught before it became the user's problem.** The first attempt at a
  post-Sparkify dataset (GA4 via BigQuery) would have required sending the user to an external SQL
  console to run queries and paste results back — a workflow regression from a normal setup
  where data lived in flat files Claude could query locally. Caught when the user questioned why
  manual SQL queries were needed at all — the honest answer was architecture (a hosted service
  needs cloud auth Claude can't supply alone), and the fix was finding a directly downloadable
  alternative (OULAD), not defending the original choice.
- **Positive: layered QA worked as designed, not redundantly.** The rigor pass's adversarial check
  caught part of the lift inflation (the within-window-withdrawal double-count) on its own, before
  independent verification ran. Independent verification then caught something structurally
  different — a code bug, not a statistical inference issue — that the same-context check could
  not have found regardless of how thorough it was. Neither layer subsumed the other.
- **A third definitional bug, caught by neither the rigor pass nor independent verification — by
  the user's own terminology questions during final review.** Notebook 01's non-independence flag
  (`repeat_student`) checked `nunique(code_presentation) > 1` — distinct semesters, not distinct
  subjects. This both over-counted (flagging students who simply took two different subjects in
  two different semesters as "repeat," when they'd never retaken anything) and under-counted
  (missing students who took two different subjects within the *same* semester, who still
  contribute two non-independent rows). Neither the rigor pass's 14-gate checklist nor the
  independent-verification sub-agent were scoped to check this specific flag — it surfaced only
  because the user kept asking what "module" vs. "subject" vs. "presentation" precisely meant during
  the README/notebook review, which forced a first-principles re-derivation of the grain and
  exposed the mismatch. Fixed to directly count enrollment rows per student
  (`multi_enrollment_student`): the correct figures are 3,538 students / 22.5% of enrollments, not
  2,589 / 16.7%, and the original "mostly re-attempts after a Fail or Withdrawn" framing was also
  corrected — only 1,259 of those 3,538 students are genuine same-subject retakers (86.5% of whom
  did have a Fail/Withdrawn first attempt); the rest simply took multiple different subjects,
  which isn't retaking anything. This is the clearest example in this project of a fourth QA
  layer — **<u>attentive human review during the deliverable walkthrough</u>** — catching something the
  other three structurally couldn't, because none of them were asking "what does this word
  actually mean."
- **The withdrawal figure never got the survivor-matching fix — caught by the user's review of
  notebook 05, not by any structural QA layer.** Enrollments that withdrew inside the 14-day
  window can't activate, so they inflate any activated-vs-not gap. That was corrected for the
  headline success lift (34.8pp → 24.5pp) but not for the parallel withdrawal-rate gap, which
  stayed on the full population at 27.7pp. Restricted to 14-day survivors it is **5.8pp** — most
  of the raw gap was the overlap. It surfaced when the user asked which period the withdrawal
  figure covered. The rigor pass and independent verification both missed it because both were
  scoped to the headline claim.
- **The same fix was also missing from the within-subgroup lifts — found while following up a
  fresh-context cold-read review.** The reviewer flagged that one quoted range rested on a
  ~50-person subgroup; checking it showed the lifts by subject, education, age band, first-timer
  status and credit tier were all on the full population too, quoted right beside the survivor-
  matched 24.5pp (e.g. subjects +20 to +45pp → +17 to +35pp; age bands +34 to +43pp → +24 to
  +28pp). Every group stays positive, so the qualitative conclusions held; the magnitudes had been
  overstated by ~10pp here and ~22pp for withdrawal. Lesson for both: when a correction is applied
  to a headline number, find every sibling figure computed on the same population and re-derive
  it on the same basis.

### What I'd do differently next time

1. **Add assertions inside `prep.py` itself**, not just downstream sanity checks — e.g. `assert
   (sv["date"] >= 0).all()` after applying an early-window filter, so a boundary-condition bug
   fails loudly at the source rather than silently propagating through four notebooks.
2. **Run the tenure-leakage check (effectively Gate 13) before building any
   whole-course-based analysis**, not after a notebook is already drafted — the fix would have
   been cheaper earlier, and the retracted quiz-nudge recommendation would never have been
   written in the first place.
3. **When mapping a non-native dataset onto a borrowed framework** (OULAD onto a SaaS
   activation/monetization shape), write the substitution decision down explicitly at the start
   of the affected notebook, not just in the dataset-choice gate — it surfaced correctly here, but
   late, and only because this project's scope demanded prominent disclosure.
4. **Consider a small synthetic fixture test for `prep.py`'s core functions** (a fake mini-dataset
   with a few known negative-date rows) — would have caught the date-boundary bug at write time,
   before any notebook ran on real data.
5. **Write out a precise data-dictionary / grain table before naming any derived flag**, not
   during a later terminology cleanup. `repeat_student`'s bug existed because "module,"
   "subject," "presentation," and "semester" were used loosely and interchangeably while writing
   the code — a five-minute table (subject / semester / course run / enrollment, each with its
   exact raw-column definition and count) would have made the `nunique(code_presentation)`
   mistake visually obvious immediately, the same way it became obvious once that table finally
   got written down under review pressure.

### Would a different architecture have caught this sooner?

Likely not through a different *agent* architecture — a parallel second analyst building the same
`build_engagement` function from the same ambiguous "first 14 days" framing would plausibly have
made the identical assumption. What would have caught it sooner is a **process** change (test
fixtures, in-code assertions), not more agents. The general pattern holds here too: additional
agents help most where genuine independence matters (as it did here, for the verification layer)
and add cost without benefit where the actual gap is code discipline, not reasoning diversity.
