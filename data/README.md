# Data

This project uses the **Open University Learning Analytics Dataset (OULAD)** — real,
anonymised student data from The Open University (UK), covering 7 subjects, each offered
2–4 times between 2013 and 2014 (22 course runs total).

- **License:** released under a license (Creative Commons Attribution 4.0) that permits free
  reuse as long as the source is credited.
- **Real or synthetic:** Real. Published as a peer-reviewed data descriptor: Kuzilek, J.,
  Hlosta, M., Zdrahal, Z. *Open University Learning Analytics dataset*. Sci Data 4, 170171
  (2017). https://doi.org/10.1038/sdata.2017.171
- **Source used here:** UCI Machine Learning Repository mirror —
  https://archive.ics.uci.edu/dataset/349/open+university+learning+analytics+dataset
- **Not included in this repo:** the raw CSVs are not committed (`studentVle.csv` alone is
  ~450 MB, and one file — `data/processed/` — is derived, not source data). Run the fetch
  script below to reproduce them locally.

## Reproduce

```bash
bash data/get_data.sh
```

This downloads and unzips the dataset into `data/oulad/` (~500 MB uncompressed). No account
or login is required. Re-running is safe — it skips the download if the files already exist.

## Why this dataset, and what it does not have

OULAD is used here as a stand-in for a SaaS (Software-as-a-Service) product's event data: it
has real signup dates, an engagement log (VLE = Virtual Learning Environment clicks), and a
real outcome (Pass / Distinction / Fail / Withdrawn). **It has no monetization stage** — it's a
free platform. Wherever this project's analysis would normally cover monetization, it uses
`final_result` as an explicitly labelled **value-outcome proxy**, not revenue. See the main
README for the full disclosure and the ADR for how this dataset was chosen.

**A genuine trade-off — a real con, and a real pro.** No monetization data
is a real gap — this project can't show a free-to-paid funnel, and that's a con, stated plainly.
But it isn't a pure loss: mapping a non-SaaS outcome onto a SaaS-shaped framework forced an
explicit, defended definition of what "value" means here (Pass/Distinction vs. Fail/Withdrawn) —
deciding what counts as the outcome that matters, and justifying it, rather than assuming it.
That definitional step is real analytical work, and this project shows it done.

## Files

| File | Grain | Notes |
|---|---|---|
| `courses.csv` | 1 row per course run (22) | Course-run length in days |
| `studentInfo.csv` | 1 row per student × presentation (= enrollment; 32,593) | Demographics + `final_result` |
| `studentRegistration.csv` | 1 row per student × presentation (= enrollment) | `date_registration` (days relative to course start, almost always negative i.e. before start), `date_unregistration` (withdrawal date, if any) |
| `studentVle.csv` | 1 row per student × site × day (10.66M) | `sum_click` — the engagement log |
| `vle.csv` | 1 row per VLE site (~6,300) | `activity_type` — the feature-usage taxonomy |
| `assessments.csv` | 1 row per assessment (206) | TMA (Tutor Marked Assessment) / CMA (Computer Marked Assessment) / Exam, due date, weight |
| `studentAssessment.csv` | 1 row per submission (173,912) | Score, submission date |
