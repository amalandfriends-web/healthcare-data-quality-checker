# dq_checks.py
import pandas as pd
import numpy as np

def basic_summary(df):
    """Return basic summary metrics."""
    summary = {
        "rows": int(df.shape[0]),
        "columns": int(df.shape[1]),
        "missing_values": int(df.isna().sum().sum()),
        "duplicate_rows": int(df.duplicated().sum())
    }
    return summary

def column_summary(df):
    """Return column-wise summary for missing, unique, dtype."""
    cols = []
    for c in df.columns:
        col = {
            "column": c,
            "dtype": str(df[c].dtype),
            "missing": int(df[c].isna().sum()),
            "missing_pct": float(df[c].isna().mean()),
            "unique_values": int(df[c].nunique(dropna=True))
        }
        cols.append(col)
    return pd.DataFrame(cols)

def data_quality_score(df):
    """Simple heuristic for a data quality score 0-100."""
    rows, cols = df.shape
    missing_pct = df.isna().mean().mean()  # average missing per cell
    dup_pct = df.duplicated().mean()
    # Score reduces with missing and duplicates; basic example
    score = 100 - (missing_pct * 70 + dup_pct * 30)
    return max(0, round(score, 2))

def simple_type_checks(df, column_types):
    """
    column_types: dict e.g. {'age': 'int', 'dob': 'date', 'visit_date': 'date'}
    Returns a dict of columns that failed type conversion or had format issues.
    """
    issues = {}
    for col, expected in column_types.items():
        if col not in df.columns:
            issues[col] = f"Missing column"
            continue
        series = df[col].dropna()
        if expected == "int":
            invalid = series.apply(lambda x: not is_int_like(x))
            count = int(invalid.sum())
            issues[col] = f"{count} values not int-like"
        elif expected == "float":
            invalid = series.apply(lambda x: not is_float_like(x))
            count = int(invalid.sum())
            issues[col] = f"{count} values not float-like"
        elif expected == "date":
            invalid_count = 0
            try:
                pd.to_datetime(series, errors='coerce')
                invalid_count = int(pd.to_datetime(series, errors='coerce').isna().sum())
            except Exception:
                invalid_count = int(len(series))
            issues[col] = f"{invalid_count} values not parseable as date"
        else:
            issues[col] = "No check applied"
    return issues

def is_int_like(x):
    try:
        if pd.isna(x): return True
        int(float(x))
        return True
    except Exception:
        return False

def is_float_like(x):
    try:
        if pd.isna(x): return True
        float(x)
        return True
    except Exception:
        return False

def apply_basic_rules(df):
    """
    Example rules:
     - age must be between 0 and 120
     - admission_date <= discharge_date (if both exist)
    Returns list of rule failures.
    """
    failures = []
    if 'age' in df.columns:
        bad_age = df['age'].dropna().apply(lambda x: not is_int_like(x) or (int(float(x))<0) or (int(float(x))>120))
        count = int(bad_age.sum())
        if count>0:
            failures.append(f"age: {count} rows with invalid age (must be 0-120)")
    if 'admission_date' in df.columns and 'discharge_date' in df.columns:
        a = pd.to_datetime(df['admission_date'], errors='coerce')
        d = pd.to_datetime(df['discharge_date'], errors='coerce')
        invalid = a.notna() & d.notna() & (a > d)
        count = int(invalid.sum())
        if count>0:
            failures.append(f"admission/discharge: {count} rows where admission_date > discharge_date")
    return failures
