# CLAUDE.md — Product Analytics Case Study

## What this project is

A public portfolio piece demonstrating product analytics end to end: activation, engagement,
retention, and a monetization stage — on a real dataset. A recruiter should be able to open the
README and understand it in about 3 minutes. Full process and scope decisions: `ADR.md`.

**Dataset: OULAD** (Open University Learning Analytics Dataset). Real, released under a license
(Creative Commons Attribution 4.0) that permits free reuse as long as the source is credited.
It's an education platform, not SaaS, and it has **no monetization** — `final_result` (Pass/Distinction
vs Fail/Withdrawn) stands in as a labelled **value-outcome proxy**, never called revenue. See
`data/README.md` for the full disclosure and `ADR.md` for the dataset-selection reasoning.

## Environment — do not install without asking

- Use a Python 3.11 environment with `requirements.txt` installed.
- Run notebooks with: `jupyter nbconvert --to notebook --execute --inplace <notebook>`.
- **Any install / upgrade (conda, pip, kernel) is proposed as exact commands — never run
  unprompted.**
- **No statsmodels / scikit-learn**, by explicit decision (not installed in this env, and the
  user chose not to add them). Methodology uses stratified/cross-tab lift comparisons plus
  `scipy.stats` significance tests instead of regression or ML models. See `ADR.md`.

## Working rhythm

- **One notebook at a time**, in the order below. For each: write its cells, execute, export
  its PNGs to `images/`, self-check, then stop for the user's review before moving on.
- **Nothing is staged, committed, or pushed without the user's explicit review and approval.**
  At each checkpoint show `git status` + the diff and propose a commit message, then wait.
- Git: solo repo, direct-to-`main`, no branches, no PRs, no `gh` CLI.
- Gates (stop and wait): dataset choice — done; analysis plan — done; before the final
  narrative; before any commit.
- Escalate (don't fold in quietly) any finding that changes the analysis's scope.

## Notebook plan

| # | Notebook | Covers |
|---|---|---|
| 01 | `01_Data_Prep_and_Profile.ipynb` | Load, join, grain decisions, data-quality caveats surfaced up front |
| 02 | `02_Activation.ipynb` | Define activation from early engagement; test as a retention predictor |
| 03 | `03_Engagement_and_Retention.ipynb` | Funnel, weekly engagement, withdrawal/retention curves |
| 04 | `04_Feature_Adoption_and_Segmentation.ipynb` | VLE activity-type mix by segment |
| 05 | `05_Metrics_Framework_and_Synthesis.ipynb` | Primary metric + guardrails; headline synthesis |

## Conventions

- Files `NN_TitleCase.ipynb` at the repo root; `images/` at the repo root holds exported PNGs;
  notebooks are committed **executed, with outputs**.
- Shared loading/derivation logic lives in `prep.py` at the repo root (imported by every
  notebook) — mirrors `load_data.py` in The Seaborn Portfolio. Don't duplicate join/derivation
  logic inside individual notebooks.
- Every finding is tagged **[OBS]** (Observation) / **[HYP]** (Hypothesis) / **[CON]**
  (Conclusion). Correlation vs. causation is stated explicitly wherever it applies — this
  dataset especially: engagement correlating with success is confounded by student
  self-selection (motivated students both click more and pass more).
- Rate vs. mix is decomposed before attributing a change to one cause; correlated dimensions
  (e.g. module difficulty vs. engagement) are disentangled, not pooled blindly.

## QA

- `analysis-rigor-pass` runs before the final write-up.
- `independent-verification` runs on the headline activation finding.
- Single analyst throughout (not a multi-agent pipeline) — this is deliberate, see ADR.md.
- `ADR.md` follows the two-part format used in `AI Analyst Workspace/Reports/E11_03_Architecture_and_Evaluation_Report.md`:
  Part 1 architecture decision + alternatives considered, Part 2 self-evaluation (what QA
  caught, disagreements, AI-assisted workflow notes, what to do differently next time).
