# 🏥 Healthcare Data Quality Checker

A simple, interactive **Streamlit application** designed to automatically check and clean common data quality issues in tabular healthcare datasets (CSV files).

This tool is deployed live and ready to use!

## 🌐 Live Demo & Access

You can access the deployed application instantly without any installation:

👉 **Live App URL:** [https://amala-healthcare-data-quality-tool.streamlit.app/](https://amala-healthcare-data-quality-tool.streamlit.app/)

## ✨ Features

* **Quick Data Upload:** Easily upload a CSV file or use a built-in demo dataset.
* **Data Summary:** View missing counts, percentages, and data types for all columns.
* **Data Quality Score:** Get a simple overall quality score based on missing values.
* **Rule-Based Validation:** Automatically checks for critical, logic-based violations:
    * Invalid or out-of-range patient age (must be 0-120).
    * Admission Date occurring *after* Discharge Date.
    * Duplicate Patient IDs.
* **Basic Cleaning Options:** Download a cleaned version of the data after dropping duplicates or filling missing values.

## 🛠️ For Local Development (Optional)

If you are a developer who wants to clone the repository, modify the code, or run it in your local environment, follow these steps.

### Prerequisites

You need **Python** installed on your system.

1.  **Clone the Repository:**
    ```bash
    git clone [https://github.com/amalandfriends-web/healthcare-data-quality-checker.git](https://github.com/amalandfriends-web/healthcare-data-quality-checker.git)
    cd healthcare-data-quality-checker
    ```

2.  **Install Dependencies:**
    [cite_start]The required Python packages are listed in `requirements.txt` [cite: 1] (`streamlit`, `pandas`, `numpy`, etc.).
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the App Locally:**
    ```bash
    streamlit run app.py
    ```

4.  **Access:** The application will automatically open in your web browser, usually at `http://localhost:8501`.

## 📁 File Structure

| File | Description |
| :--- | :--- |
| `app.py` | [cite_start]The main Streamlit web application script, controlling the UI and workflow. [cite: 1] |
| `dq_checks.py` | [cite_start]Contains helper functions for core data quality logic and rule application. [cite: 1] |
| `requirements.txt` | Lists all necessary Python packages. |
