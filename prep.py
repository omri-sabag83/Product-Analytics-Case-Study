"""
Shared loading and derivation logic for the OULAD-based Product Analytics Case Study.
Every notebook imports from here rather than repeating join/derivation logic — mirrors
load_data.py in The Seaborn Portfolio.

Grain: one "enrollment" = one (code_module, code_presentation, id_student) triple. A student
who takes two module presentations contributes two enrollments (see NON_INDEPENDENCE_NOTE).
"""

from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).parent
RAW_DIR = ROOT / "data" / "oulad"
PROCESSED_DIR = ROOT / "data" / "processed"
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

ENROLL_KEY = ["code_module", "code_presentation", "id_student"]
PRESENTATION_KEY = ["code_module", "code_presentation"]

NON_INDEPENDENCE_NOTE = (
    "2,589 of 28,785 students appear in more than one module presentation. Enrollments, not "
    "students, are the analysis grain throughout; repeat enrollments are not de-duplicated by "
    "default. Treat significance tests as approximate where this matters."
)

# Rare VLE activity types are collapsed into 'other' for the feature-adoption mix (notebook 04).
# Threshold and the resulting bucket list are computed data-driven in build_activity_mix(),
# not hardcoded here.


def _to_numeric_or_missing(s: pd.Series) -> pd.Series:
    """OULAD encodes some missing numerics as the literal string '?'."""
    return pd.to_numeric(s.replace("?", np.nan), errors="coerce")


def load_raw(data_dir: Path = RAW_DIR) -> dict[str, pd.DataFrame]:
    """Load all seven OULAD CSVs with minimal type cleanup. Run data/get_data.sh first."""
    if not (data_dir / "studentVle.csv").exists():
        raise FileNotFoundError(
            f"{data_dir} is empty. Run `bash data/get_data.sh` first (see data/README.md)."
        )
    courses = pd.read_csv(data_dir / "courses.csv")
    info = pd.read_csv(data_dir / "studentInfo.csv")
    info["imd_band"] = info["imd_band"].replace("?", np.nan)
    reg = pd.read_csv(data_dir / "studentRegistration.csv")
    reg["date_registration"] = _to_numeric_or_missing(reg["date_registration"])
    reg["date_unregistration"] = _to_numeric_or_missing(reg["date_unregistration"])
    vle_sites = pd.read_csv(data_dir / "vle.csv")
    student_vle = pd.read_csv(
        data_dir / "studentVle.csv",
        dtype={"id_site": "int32", "id_student": "int32", "date": "int16", "sum_click": "int16"},
    )
    assessments = pd.read_csv(data_dir / "assessments.csv")
    assessments["date"] = _to_numeric_or_missing(assessments["date"])
    student_assessment = pd.read_csv(data_dir / "studentAssessment.csv")
    student_assessment["score"] = _to_numeric_or_missing(student_assessment["score"])
    return {
        "courses": courses,
        "info": info,
        "reg": reg,
        "vle_sites": vle_sites,
        "student_vle": student_vle,
        "assessments": assessments,
        "student_assessment": student_assessment,
    }


def build_enrollments(raw: dict[str, pd.DataFrame]) -> pd.DataFrame:
    """One row per (subject, semester, student) — one enrollment: demographics + registration + outcome."""
    e = raw["info"].merge(raw["reg"], on=ENROLL_KEY, how="left")
    e = e.merge(raw["courses"], on=PRESENTATION_KEY, how="left")

    e["registered_before_start"] = e["date_registration"] < 0
    e["withdrew"] = e["date_unregistration"].notna()
    e["success"] = e["final_result"].isin(["Pass", "Distinction"])
    e["distinction"] = e["final_result"].eq("Distinction")

    # A student contributes more than one row (any subject, any semester) — the actual
    # statistical-independence concern, not specifically "retook the same subject." An earlier
    # version checked nunique(code_presentation) > 1, which both over-counted (flagged students
    # who took two different subjects in different semesters, never repeating anything) and
    # under-counted (missed students taking two different subjects in the *same* semester, since
    # they'd share one code_presentation value). Caught during terminology review — see ADR.md.
    enrollments_per_student = e.groupby("id_student")["id_student"].transform("size")
    e["multi_enrollment_student"] = enrollments_per_student > 1

    return e


def build_engagement(
    raw: dict[str, pd.DataFrame], early_window_days: int = 14
) -> pd.DataFrame:
    """
    Per-enrollment engagement summary, both early-window (activation candidate signals) and
    whole-course. The early window is [0, early_window_days) — day 0 is module start, a shared
    clock across a cohort's students since registration happens before day 0 for ~99% of
    enrollments. The lower bound matters: studentVle.csv has pre-course rows (negative `date`,
    students browsing before their course starts) — an earlier version of this function used
    `date < early_window_days` with no lower bound, silently folding pre-course browsing into
    the "first 14 days" signal and inflating the activation rate by ~3,700 enrollments (caught
    by independent verification on the headline claim — see ADR.md).
    """
    sv = raw["student_vle"].merge(
        raw["vle_sites"][["id_site"] + PRESENTATION_KEY + ["activity_type"]],
        on=["id_site"] + PRESENTATION_KEY,
        how="left",
    )

    full = (
        sv.groupby(ENROLL_KEY)
        .agg(
            total_clicks=("sum_click", "sum"),
            active_days=("date", "nunique"),
            first_click_day=("date", "min"),
            last_click_day=("date", "max"),
        )
        .reset_index()
    )

    early = sv[(sv["date"] >= 0) & (sv["date"] < early_window_days)]
    early_agg = (
        early.groupby(ENROLL_KEY)
        .agg(
            early_clicks=("sum_click", "sum"),
            early_active_days=("date", "nunique"),
            early_distinct_activity_types=("activity_type", "nunique"),
        )
        .reset_index()
    )

    out = full.merge(early_agg, on=ENROLL_KEY, how="left")
    for col in ["early_clicks", "early_active_days", "early_distinct_activity_types"]:
        out[col] = out[col].fillna(0)
    return out


def to_display_week(date: pd.Series) -> pd.Series:
    """
    Convert a day-relative-to-course-start value into a 1-indexed "week" label: week 1 = days
    0-6 (the first week), week 2 = days 7-13, etc. — ordinary calendar counting, no "week 0".
    Negative weeks (pre-course activity) keep plain floor-division numbering, e.g. week -1 =
    days -7 to -1, the week immediately before the course started; there's no week 0 to bridge
    the two, the same way the BC/AD calendar has no year 0. Relabeling only — doesn't change
    which enrollment falls in which bucket, only what that bucket is called.
    """
    floor_week = date // 7
    return floor_week.where(date < 0, floor_week + 1)


def build_weekly_activity(raw: dict[str, pd.DataFrame]) -> pd.DataFrame:
    """Per-enrollment, per-week-since-start click totals — for retention/engagement curves."""
    sv = raw["student_vle"]
    sv = sv.assign(week=to_display_week(sv["date"]))
    return (
        sv.groupby(ENROLL_KEY + ["week"])
        .agg(clicks=("sum_click", "sum"))
        .reset_index()
    )


def build_activity_mix(
    raw: dict[str, pd.DataFrame], min_share: float = 0.01, window_days: int | None = None
) -> pd.DataFrame:
    """
    Per-enrollment share of clicks by activity_type (feature-adoption mix, notebook 04).

    `window_days`, if set, restricts to clicks with 0 <= date < window_days — use this (matching
    build_engagement's early window) when comparing mix/volume against an outcome. Without
    it, whole-course totals mechanically favor enrollments with longer tenure (a student who
    stays enrolled longer simply accumulates more clicks), which confounds any volume/mix-vs-
    outcome comparison — caught in the rigor pass (Gate 13, leakage): whole-course total_clicks
    correlates ~0.43-0.48 with success, but tenure-adjusted (clicks per enrolled day) that drops
    to ~0.02. Whole-course mode is still fine for descriptive adoption-rate questions (notebook
    04's "did they ever use X" section), just not for predicting outcome.
    """
    sv = raw["student_vle"].merge(
        raw["vle_sites"][["id_site"] + PRESENTATION_KEY + ["activity_type"]],
        on=["id_site"] + PRESENTATION_KEY,
        how="left",
    )
    if window_days is not None:
        sv = sv[(sv["date"] >= 0) & (sv["date"] < window_days)]
    overall_share = sv.groupby("activity_type")["sum_click"].sum()
    overall_share = overall_share / overall_share.sum()
    keep_types = overall_share[overall_share >= min_share].index
    sv = sv.assign(
        activity_bucket=np.where(sv["activity_type"].isin(keep_types), sv["activity_type"], "other")
    )
    by_type = (
        sv.groupby(ENROLL_KEY + ["activity_bucket"])["sum_click"].sum().unstack(fill_value=0)
    )
    shares = by_type.div(by_type.sum(axis=1), axis=0)
    shares.columns = [f"share_{c}" for c in shares.columns]
    return shares.reset_index()


def build_assessment_features(raw: dict[str, pd.DataFrame]) -> pd.DataFrame:
    """Per-enrollment assessment engagement: submission rate, timeliness, average score."""
    a = raw["assessments"]
    sa = raw["student_assessment"].merge(
        a[["id_assessment"] + PRESENTATION_KEY + ["date", "assessment_type"]],
        on="id_assessment",
        how="left",
    )
    sa["on_time"] = sa["date_submitted"] <= sa["date"]

    assessments_per_presentation = a.groupby(PRESENTATION_KEY)["id_assessment"].nunique()
    assessments_per_presentation.name = "n_assessments_available"

    per_enroll = (
        sa.groupby(ENROLL_KEY)
        .agg(
            n_submissions=("id_assessment", "nunique"),
            avg_score=("score", "mean"),
            on_time_rate=("on_time", "mean"),
        )
        .reset_index()
    )
    per_enroll = per_enroll.merge(
        assessments_per_presentation, on=PRESENTATION_KEY, how="left"
    )
    per_enroll["submission_rate"] = (
        per_enroll["n_submissions"] / per_enroll["n_assessments_available"]
    )
    return per_enroll


def save_processed(df: pd.DataFrame, name: str) -> Path:
    path = PROCESSED_DIR / f"{name}.parquet"
    df.to_parquet(path, index=False)
    return path


def load_processed(name: str) -> pd.DataFrame:
    return pd.read_parquet(PROCESSED_DIR / f"{name}.parquet")
