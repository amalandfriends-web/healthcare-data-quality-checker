import streamlit as st
import pandas as pd
import numpy as np

st.title("Healthcare Data Quality Checker")

# -----------------------------
# Step 1: Upload CSV
# -----------------------------
uploaded_file = st.file_uploader("Upload CSV file", type="csv")

# Optionally, load demo dataset
if st.checkbox("Load example demo dataset"):
    data = {
        'patient_id': [1,2,3,3,4,5],
        'age': [25,30,np.nan,45,150,40],
        'gender': ['F','M','F','F','M',np.nan],
        'admission_date': ['2023-01-01','2023-02-02','2023-02-03','2023-01-15','2023-03-01','2023-03-05'],
        'discharge_date': ['2023-01-10','2023-02-01','2023-02-05','2023-01-12','2023-03-02',np.nan],
        'lab_value': [4.5,np.nan,7.8,5.2,6.1,8.0]
    }
    df = pd.DataFrame(data)
elif uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
else:
    st.info("Please upload a CSV file or load the demo dataset to proceed.")
    st.stop()

# -----------------------------
# Step 2: Preview Data
# -----------------------------
st.subheader("Preview Data")
st.dataframe(df.head())

# -----------------------------
# Step 3: Column Summary
# -----------------------------
st.subheader("Column Summary")
col_summary = pd.DataFrame({
    'Column': df.columns,
    'Non-missing Count': df.notnull().sum().values,
    'Missing Count': df.isnull().sum().values,
    'Missing %': (df.isnull().sum().values / len(df) * 100)
})
st.dataframe(col_summary)

# -----------------------------
# Step 4: Missing Values Summary
# -----------------------------
st.subheader("Missing Values Summary")
missing_values = df.isnull().sum()
st.bar_chart(missing_values)

# Info for missing lab values
missing_lab_rows = df['lab_value'].isnull().sum()
if missing_lab_rows > 0:
    st.info(f"Lab values missing for {missing_lab_rows} rows (may be tests not yet done)")

# -----------------------------
# Step 5: Data Quality Score
# -----------------------------
dq_score = 100 - (df.isnull().sum().sum() / (df.shape[0]*df.shape[1]) * 100)
st.subheader("Data Quality Score")
st.progress(int(dq_score))
st.write(f"Overall Data Quality Score: {dq_score:.2f}%")

# -----------------------------
# Step 6: Rule Checks (Updated)
# -----------------------------
st.subheader("Rule Checks")
rule_violations = []

# Age check: must exist and 0-120
invalid_age_rows = df[(df['age'].isnull()) | (df['age'] < 0) | (df['age'] > 120)]
if not invalid_age_rows.empty:
    rule_violations.append(f"age: {len(invalid_age_rows)} rows with invalid or missing age (must be 0-120)")

# Admission/Discharge check: only if discharge_date exists
admission_discharge_rows = df[df['discharge_date'].notnull() & (df['admission_date'] > df['discharge_date'])]
if not admission_discharge_rows.empty:
    rule_violations.append(f"admission/discharge: {len(admission_discharge_rows)} rows where admission_date > discharge_date")

# Duplicate patient_id check
duplicate_patient_rows = df[df.duplicated(subset=['patient_id'], keep=False)]
if not duplicate_patient_rows.empty:
    rule_violations.append(f"duplicate patient_id: {len(duplicate_patient_rows)} rows")

# Display rule violations
if rule_violations:
    for rule in rule_violations:
        st.warning(rule)
else:
    st.success("All rules passed!")

# -----------------------------
# Step 7: Data Cleaning Options
# -----------------------------
st.subheader("Data Cleaning Options")

if st.button("Drop duplicates & Download"):
    cleaned_df = df.drop_duplicates(subset=['patient_id'])
    cleaned_df.to_csv("cleaned_data.csv", index=False)
    st.success("Duplicates dropped. CSV saved as cleaned_data.csv")

if st.button("Fill missing & Download"):
    cleaned_df = df.fillna("Missing")
    cleaned_df.to_csv("filled_data.csv", index=False)
    st.success("Missing values filled. CSV saved as filled_data.csv")

# -----------------------------
# Step 8: Visualize Duplicates / Missing
# -----------------------------
st.subheader("Duplicates & Missing Values Visualization")
dup_counts = df.duplicated(subset=['patient_id'], keep=False).sum()
st.write(f"Total duplicate patient_id rows: {dup_counts}")

st.bar_chart(df.isnull().sum())
