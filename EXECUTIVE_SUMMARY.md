# Executive Summary — Product Analytics Case Study

**The setting:** an online university (The Open University, UK) where students enroll in
courses, engage with course materials and discussion forums, and finish with a grade — Pass,
Distinction, Fail, or Withdrawn.

**The data:** 32,593 real student enrollments across **7 subjects**, each offered twice a year
(starting in February or October) across 2013 and 2014 — **22 subject-intake combinations** in
total, each a single continuous course run lasting about 8–9 months — released under a license
(Creative Commons Attribution 4.0) that permits free reuse as long as the source is credited.

**Important note:** most SaaS product analyses follow a flow from activation → engagement →
retention → monetization. This platform is free, so there's no revenue stage in the data. The
final grade stands in as a "did the user get what they came for" proxy throughout — clearly
labeled as a stand-in, never treated as real money.

## Headline finding

Students who return on **≥3 separate days in their first 2 weeks** ("activation," defined from
the data's own dose-response curve, not assumed) go on to succeed at a rate **24.5 points
higher** than students who don't — holding within every subject, education level, age band, and
course-load tier tested. **[HYP]** This is correlational: motivated or less-constrained students
plausibly both activate and succeed for reasons the data can't fully separate.

## The journey

| Stage | Result |
|---|---|
| Funnel | 100% register → 89.7% ever engage → 61.7% activate → 58.5% submit work → 37.3% succeed |
| Retention | 44.3% of all withdrawals happen by week 2; the activation retention-gap widens across the full term |
| Feature adoption | Core-vs-long-tail shape; *how much* someone engages predicts outcome more than *what* they touch |
| Equity | Feature-usage mix is flat by deprivation band (a UK measure of local-area disadvantage) — but success rate spans a real 22.4-point gap by that same band |

## Metrics framework

| Role | Metric | Current value |
|---|---|---|
| Primary | Week-2 Activation Rate | 61.7% |
| Guardrail | Assessment completion rate (share of available assessments submitted), activated vs. not | 67.7% vs. 32.1% |
| Guardrail | Activation-rate gap by deprivation band | 12.5pp |
| Guardrail | Activated-cohort active rate, week 20+ | ~52–64% |

## Recommendations

1. Week-1 return nudge for zero-activity enrollments — the steepest, most tractable drop point.
2. Targeted early support (not a feature change) for higher-deprivation enrollments — the outcome
   gap looks like access, not platform preference.
3. Any activation-boosting initiative needs a real holdout-group test before its outcome gain is
   credited to it — the self-selection confound means correlation alone isn't proof.

## Limitations

Correlational, not causal. Confounds checked one at a time, not jointly (confirming the lift
survives all of them at once would take a regression controlling for all of them together). No
real monetization data. 22.5% of enrollments belong to a student
who appears more than once, not separate people. One dataset, one platform, 2013–2014.

## Process

Single analyst + AI copilot, with a structured rigor pass and independent (fresh-context)
verification **built into the process** — which caught and fixed a real data error (inflating
the activation rate by ~3,700 enrollments) before it ever reached this summary. Full process
record: `ADR.md`.
