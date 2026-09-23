# Product Analytics Case Study: Activation, Engagement, Retention & Value

An end-to-end product-analytics investigation — activation, engagement, retention, and a
monetization-analog "value" stage — on a real dataset, with the AI-assisted rigor process shown
alongside the findings. Built as a portfolio piece; read time ~3 minutes.

## TL;DR

Students who return to the platform on **3 or more separate days within their first 2 weeks**
("activation") go on to pass their course at a **24.5-point higher rate** than students who
don't, holding within every subject, education level, age band, and course-load tier tested —
and this is correlational, not proven causal. A real **22-point equity gap** by deprivation band
(a UK government measure of how disadvantaged someone's local area is) shows up in outcomes but
not in *how* engaged students use the platform, pointing at access and circumstance rather than
platform design.

## The data — read this before the findings

This project uses **OULAD** (Open University Learning Analytics Dataset): real, anonymised data
from 32,593 enrollments across 22 course runs (7 subjects, each a single continuous
~8–9 month course, offered twice a year) at The Open University (UK), 2013–2014, released under
a license (Creative Commons Attribution 4.0) that permits free reuse as long as the source is
credited. Citation: Kuzilek, Hlosta & Zdrahal, *Open University Learning Analytics dataset*, Sci
Data 4, 170171 (2017).

**It is not a SaaS product, and it has no monetization stage.** Most SaaS product analyses
follow a flow from activation → engagement → retention → monetization; this platform is free,
so there's no revenue stage in the data. OULAD is a free education platform, so:
- `final_result` stands in for "did the user get the value they came for" throughout: Pass or
  Distinction counts as yes, Fail or Withdrawn counts as no — a **labelled value-outcome
  proxy**, never called revenue.
- Everything downstream of that substitution (the metrics framework's guardrails, the
  recommendations) inherits this limitation.

**Coverage caveats, up front:** engagement time is measured in days relative to each course's own
start (day 0), not a shared calendar — so cohorts are the 22 course runs, not calendar
months. `imd_band` (the UK government's Index of Multiple Deprivation — ranks small residential
areas by income, employment, education, health, and other factors, grouped into ten bands from
most to least deprived) is missing for 3.4% of enrollments. 22.5% of
enrollments belong to a student who appears more than once (any subject, any semester — not
necessarily retaking one) — kept in the analysis, not statistically independent. See
`01_Data_Prep_and_Profile.ipynb` for the full data-quality pass.

## Process

One analyst (me, with Claude as an AI-assisted copilot), not a multi-agent pipeline — deliberate,
given the dataset's shape (see `ADR.md`). QA layers: `analysis-rigor-pass` (a 14-gate checklist,
same-context) before the write-up, then `independent-verification` (a genuinely fresh sub-agent,
zero exposure to this reasoning) on the headline claim. **The verification caught a real bug** — a
missing lower date-bound in the activation-window calculation, which inflated the activation rate
by ~3,700 enrollments before the fix. Every number below reflects the corrected pipeline. Full
account, including what was wrong and what would have caught it sooner: `ADR.md`.

## Findings

### 1. Activation, defined from the data

Three candidate signals (click volume, day-breadth, activity-type variety) were tested across
three windows (7/14/28 days). **Breadth — distinct active days — won**, and the relationship is a
smooth dose-response, not a clean cliff: the sharpest single jump is 0→1 active day (success
12.4%→35.8%). **Activation is defined as ≥3 distinct active days in the first 14 days** — past
the noisiest part of the curve, still inside an actionable window.

**[CON]** Activated enrollments succeed at a rate **24.5 points higher** than non-activated ones
(62.2% vs. 37.7%, measured only among enrollments that survived past the activation window
itself, to exclude students who couldn't have activated even if willing). This holds within
every one of the 7 subjects (+20 to +45pp), every education level, every age band, and every
course-load tier.

**[HYP] — correlation, not causation.** More engaged students are very likely also more
motivated or facing fewer outside barriers — either could independently drive success. This
can't be ruled out from observational data. Flagged explicitly, and it's the reason a metric
built on this finding needs guardrails, not just a target (see below).

### 2. The funnel and retention

100% register → 89.7% ever engage → 61.7% activate → 58.5% submit ≥1 assessment → 37.3% succeed.
The two real bottlenecks are never engaging at all, and engaging enough to activate — once
someone activates, 95% go on to submit something. Withdrawal is front-loaded: 44.3% of all
withdrawals happen by week 2 (including students who register and drop before the course even
starts), then a steadier trickle. The activation gap in the retention curve opens immediately and
**widens** across the full term — not a one-time effect.

### 3. Feature adoption

A clear core-vs-long-tail shape: 5 features near-universal (80–90% adoption), `quiz` common but
not universal (61%), then a long tail of niche tools. Feature *mix* (which features, exposure-
matched to volume) correlates with outcome far more weakly (+0.19) than raw engagement *volume*
— how much someone engages matters more than exactly what they touch.

### 4. Equity

**The project's clearest secondary finding.** Feature-usage mix is flat across deprivation band —
students from every socio-economic band use the platform the same way, once they engage. But
*outcome* is not flat: success rate rises from 35.2% (most deprived tenth) to 57.5% (least
deprived) — a 22.4-point gap — and activation rate from 54.8% to 67.3%, holding within every
subject. Since mix itself doesn't differ, this points more toward access/circumstance (time,
technology, competing demands) than platform design — the data can't confirm the mechanism
directly.

## Metrics framework

| Role | Metric | Current value | Guards against |
|---|---|---|---|
| **Primary** | Week-2 Activation Rate | 61.7% | — |
| Guardrail | Assessment submission rate, activated vs. not | 67.7% vs. 32.1% | Activation inflated by low-value clicking |
| Guardrail | Activation-rate gap by deprivation band | 12.5pp | Average gains masking a widening equity gap |
| Guardrail | Activated-cohort active rate, week 20+ | ~52–64% | A first-burst-only, unsustained "activation" |

## Recommendations, tied to evidence

1. **Build a week-1 return nudge** for enrollments with zero activity in week 1 — the single
   steepest point in both the funnel and the dose-response curve.
2. **Target early support (not a feature change) toward higher-deprivation enrollments** in the
   first two weeks — flexible deadlines, faster response — since feature-mix usage doesn't differ
   by band; the outcome gap looks like access, not preference.
3. **Don't credit an activation-boosting initiative with the outcome gain without a real
   holdout-group experiment.** The self-selection confound means a rising activation rate alone
   isn't evidence of causation.

*A fourth candidate recommendation (nudging light-engagement users toward quizzes) was retracted
during the rigor pass — it didn't survive an exposure-matched re-test. Recorded, not hidden: `ADR.md`.*

## Limitations

- Correlational throughout; the headline finding is not proven causal.
- No monetization stage exists in the source data — every "value" claim is a labelled proxy.
- 22.5% of enrollments belong to a student who appears more than once (not necessarily
  retaking — could be two different subjects) — the same person counted twice, not two
  separate people — so significance tests are approximate, not exact.
- `imd_band` (the equity dimension) is an area-level index, not individual income — a
  coarser proxy than ideal.
- One dataset, one platform, 2013–2014 — findings may not generalize to other education products
  or to real SaaS.

## Reproduce this

```bash
bash data/get_data.sh                 # downloads OULAD from UCI, no login needed
jupyter nbconvert --to notebook --execute --inplace 0*.ipynb   # inside an env with requirements.txt installed
```

Run notebooks in order (01 → 05); each depends on the previous one's cached tables in
`data/processed/`. See `requirements.txt` for exact package versions.

## Where to find more

- **`EXECUTIVE_SUMMARY.md`** — one-page version of this document.
- **`01`–`05_*.ipynb`** — the full analysis, executed with outputs, in order.
- **`ADR.md`** — architecture decisions, the full QA trail (rigor pass + independent
  verification, including the bug it caught), and AI-assisted-workflow notes.
- **`data/README.md`** — dataset provenance, license, and table schemas.

## AI-assisted workflow, in brief

Claude built the pipeline, ran the analysis, and caught two of its own errors via structured
QA — one in a same-context rigor pass (an inflated lift figure), one only via a fresh,
independent sub-agent (a date-boundary bug in the activation-window code that a same-context
check had missed twice). Both are documented with what was wrong and what was fixed, not
smoothed over. Full account, including where Claude needed correcting: `ADR.md`.
