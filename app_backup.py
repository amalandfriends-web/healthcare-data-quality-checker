# app.py
import streamlit as st
import pandas as pd
from dq_checks import basic_summary, column_summary, data_quality_score, simple_type_checks, apply_basic_rules

st.set_page_config(page_title="Healthcare Data Quality Checker", layout="wide")

st.title("Healthcare Data Quality Checker (Beginner friendly)")

st.markdown("""
Upload a CSV (patient register, visits, or other healthcare dataset). The app calculates basic data-quality metrics,
a column summary, a simple quality score, and lists common issues with easy export options.
""")

uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])
example_data = st.checkbox("Load example demo dataset")

if example_data and uploaded_file is None:
    # create a tiny sample demo
    df = pd.DataFrame({
        "patient_id": [1,2,3,3],
        "age": [25, "30", None, 45],
        "gender": ["F","M","F","F"],
        "admission_date": ["2023-01-01","2023-02-02","2023-02-03","2023-01-15"],
        "discharge_date": ["2023-01-10","2023-02-01","2023-02-05","2023-01-12"],
        "lab_value": [4.5, "NaN", 7.8, 5.2]
    })
elif uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
else:
    df = None

if df is not None:
    st.subheader("Preview data")
    st.dataframe(df.head(100))

    st.subheader("Basic summary")
    summary = basic_summary(df)
    st.json(summary)

    st.subheader("Column summary")
    cs = column_summary(df)
    st.dataframe(cs)

    st.subheader("Data Quality Score")
    score = data_quality_score(df)
    st.metric("DQ Score (0-100)", score)

    st.subheader("Type checks (optional)")
    st.markdown("Enter column:type pairs (comma separated). types: int,float,date. Example: age:int,admission_date:date")
    col_types_input = st.text_input("Column types", value="")
    if st.button("Run checks"):
        col_types = {}
        if col_types_input.strip():
            pairs = [p.strip() for p in col_types_input.split(",") if ":" in p]
            for pair in pairs:
                col,typ = pair.split(":")
                col_types[col.strip()] = typ.strip()
        issues = simple_type_checks(df, col_types)
        st.write(issues)

    st.subheader("Rule checks")
    rules = apply_basic_rules(df)
    if rules:
        for r in rules:
            st.warning(r)
    else:
        st.success("No rule failures detected")

    st.subheader("Duplicates and missing value visual")
    missing = df.isna().sum().sort_values(ascending=False)
    st.bar_chart(missing)

    st.subheader("Duplicates")
    st.write(f"Duplicate rows: {int(df.duplicated().sum())}")
    if int(df.duplicated().sum())>0:
        st.write(df[df.duplicated(keep=False)].head(50))

    st.subheader("Export cleaned dataset")
    st.markdown("Options: drop duplicates / fill missing with placeholders")
    if st.button("Drop duplicates and download cleaned CSV"):
        cleaned = df.drop_duplicates()
        st.download_button("Download cleaned CSV", cleaned.to_csv(index=False).encode('utf-8'), "cleaned.csv", "text/csv")
    if st.button("Fill missing with placeholders and download"):
        filled = df.fillna("MISSING")
        st.download_button("Download filled CSV", filled.to_csv(index=False).encode('utf-8'), "filled.csv", "text/csv")

    st.markdown("**Next steps:** use AI (Claude/Bolt) to suggest extra rules or create a model to auto-correct common formatting issues.")
else:
    st.info("Upload a CSV to get started, or check 'Load example demo dataset'.")
