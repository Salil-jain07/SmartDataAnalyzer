
import streamlit as st
import pandas as pd
from backend.pdf_report import create_pdf_report
import os
import tempfile
from backend.visualizations import show_visualizations
from backend.data_scanner import (
    scan_dataset,
    detect_outliers,
    analyze_relationships,
    calculate_quality_score
)




st.set_page_config(
    page_title="Smart Data Analyzer",
    page_icon="📊",
    layout="wide"
)

if "pdf_bytes" not in st.session_state:
    st.session_state.pdf_bytes = None

st.title("Smart Data Analyzer")
st.write("Clean, compare, and analyze your datasets.")

uploaded_files = st.file_uploader(
    "Upload a CSV or Excel file",
    type=["csv", "xlsx"],
    accept_multiple_files=True,
    key="dataset_upload"
)


def initialize_dataset(df):
    st.session_state.original_df = df.copy(deep=True)
    st.session_state.current_df = df.copy(deep=True)
    st.session_state.undo_stack = []
    st.session_state.cleaning_history = []


def apply_cleaning(operation):
    current = st.session_state.current_df.copy(deep=True)

    # Save current state so the operation can be undone
    st.session_state.undo_stack.append(current.copy(deep=True))

    if operation == "Remove duplicate rows":
        before = len(current)
        current = current.drop_duplicates()
        changed = before - len(current)
        message = f"Removed {changed} duplicate row(s)."

    elif operation == "Remove rows with missing values":
        before = len(current)
        current = current.dropna()
        changed = before - len(current)
        message = f"Removed {changed} row(s) containing missing values."

    elif operation == "Fill numeric missing values with median":
        changed = 0

        for column in current.select_dtypes(include="number").columns:
            if current[column].isnull().any():
                median = current[column].median()

                if pd.notna(median):
                    count = int(current[column].isnull().sum())
                    current[column] = current[column].fillna(median)
                    changed += count

        message = f"Filled {changed} numeric missing value(s) with column medians."

    elif operation == "Fill missing values with mode":
        changed = 0

        for column in current.columns:
            if current[column].isnull().any():
                modes = current[column].mode(dropna=True)

                if not modes.empty:
                    count = int(current[column].isnull().sum())
                    current[column] = current[column].fillna(modes.iloc[0])
                    changed += count

        message = f"Filled {changed} missing value(s) with column modes."

    elif operation == "Standardize text":
        changed = 0

        for column in current.select_dtypes(include=["object", "string"]).columns:
            non_missing = current[column].dropna()
            cleaned = current[column].str.strip().str.replace(
                r"\s+", " ", regex=True
            ).str.title()

            changed += int(
                (current[column].fillna("\0") != cleaned.fillna("\0")).sum()
            )
            current[column] = cleaned

        message = f"Standardized text in {changed} cell(s)."

    else:
        # No supported operation selected
        st.session_state.undo_stack.pop()
        return

    st.session_state.current_df = current
    st.session_state.cleaning_history.append(message)


if uploaded_files:
    selected_file_name = st.selectbox(
        "Choose a dataset to analyze",
        [file.name for file in uploaded_files]
    )

    uploaded_file = next(
        file for file in uploaded_files
        if file.name == selected_file_name
    )

    file_signature = (
        uploaded_file.name,
        uploaded_file.size
    )

    # Store each dataset's state separately
    if "datasets" not in st.session_state:
        st.session_state.datasets = {}

    # Save the previously active dataset before switching
    previous_signature = st.session_state.get("active_file_signature")

    if previous_signature is not None:
        st.session_state.datasets[previous_signature] = {
            "original_df": st.session_state.original_df.copy(deep=True),
            "current_df": st.session_state.current_df.copy(deep=True),
            "undo_stack": [
                df.copy(deep=True)
                for df in st.session_state.undo_stack
            ],
            "cleaning_history": st.session_state.cleaning_history.copy(),
            "scan_report": st.session_state.get("scan_report"),
            "outlier_report": st.session_state.get("outlier_report"),
            "relationship_report": st.session_state.get("relationship_report"),
            "pdf_bytes": st.session_state.get("pdf_bytes")
        }

    # Restore saved state or initialize a new dataset
    if (
        previous_signature != file_signature
        or "current_df" not in st.session_state
    ):
        if file_signature in st.session_state.datasets:
            saved = st.session_state.datasets[file_signature]

            for key, value in saved.items():
                st.session_state[key] = value
        else:
            try:
                if uploaded_file.name.lower().endswith(".csv"):
                    df = pd.read_csv(uploaded_file)
                else:
                    df = pd.read_excel(uploaded_file)

                initialize_dataset(df)

                for key in [
                    "scan_report",
                    "outlier_report",
                    "relationship_report",
                    "pdf_bytes"
                ]:
                    st.session_state.pop(key, None)

            except Exception as e:
                st.error(f"Could not read the file: {e}")
                st.stop()

        st.session_state.active_file_signature = file_signature

    original = st.session_state.original_df
    current = st.session_state.current_df




    st.subheader("Automatic Data Quality Scan")

    if st.button("Scan Current Dataset"):
        st.session_state.scan_report = scan_dataset(
            st.session_state.current_df
        )

    report = st.session_state.get("scan_report")

    if report is not None:
        if report.empty:
            st.success("No issues detected by the current scanner.")
        else:
            st.warning(f"Potential issues found: {len(report)}")
            st.dataframe(report, use_container_width=True)

            st.download_button(
                "Download Scan Report",
                data=report.to_csv(index=False).encode("utf-8"),
                file_name="data_quality_scan.csv",
                mime="text/csv"
            )

    # Detailed Outlier Analysis
    st.markdown("### Outlier Analysis")

    if st.button("View Outlier Details"):
        st.session_state.outlier_report = detect_outliers(
            st.session_state.current_df
        )

    if st.session_state.get("outlier_report") is not None:
        outlier_report = st.session_state.outlier_report

        if outlier_report.empty:
            st.success("No potential outliers detected.")
        else:
            st.warning(
                f"Potential outlier values found: {len(outlier_report)}"
            )

            st.dataframe(
                outlier_report,
                use_container_width=True
            )

            st.download_button(
                "Download Outlier Report",
                data=outlier_report.to_csv(index=False).encode("utf-8"),
                file_name="outlier_report.csv",
                mime="text/csv"
            )

    st.success("Dataset ready.")

    st.subheader("6. Explore Your Data")

    show_visualizations(st.session_state.current_df)

    # Column Relationship Analysis
    st.markdown("### Column Relationship Analysis")

    if st.button("Analyze Column Relationships"):
        st.session_state.relationship_report = analyze_relationships(
            st.session_state.current_df
        )

    if st.session_state.get("relationship_report") is not None:
        relationship_report = st.session_state.relationship_report

        if relationship_report.empty:
            st.info(
                "At least two numeric columns with valid correlations "
                "are needed for relationship analysis."
            )
        else:
            st.dataframe(
                relationship_report,
                use_container_width=True
            )

            st.download_button(
                "Download Relationship Report",
                data=relationship_report.to_csv(index=False).encode("utf-8"),
                file_name="column_relationships.csv",
                mime="text/csv"
            )

    # Overview

    # Overview
    st.subheader("1. Dataset Overview")

    col1, col2, col3 = st.columns(3)

    col1.metric("Original Rows", len(original))
    col2.metric("Current Rows", len(current))
    col3.metric("Total Columns", len(current.columns))

    col4, col5, col6 = st.columns(3)

    missing_cells = int(current.isnull().sum().sum())
    duplicate_rows = int(current.duplicated().sum())
    total_cells = current.shape[0] * current.shape[1]

    complete_percentage = (
        ((total_cells - missing_cells) / total_cells) * 100
        if total_cells > 0 else 100
    )

    col4.metric("Missing Cells", missing_cells)
    col5.metric("Duplicate Rows", duplicate_rows)
    col6.metric("Complete Cells", f"{complete_percentage:.2f}%")

    # Data Quality Score
    quality_score = calculate_quality_score(current)

    st.subheader("Data Quality Score")
    st.metric("Quality Score", f"{quality_score}/100")
    # Cleaning controls
    st.subheader("2. Cleaning Operations")

    operation = st.selectbox(
        "Choose a cleaning operation",
        [
            "Remove duplicate rows",
            "Remove rows with missing values",
            "Fill numeric missing values with median",
            "Fill missing values with mode",
            "Standardize text"
        ]
    )

    if st.button("Apply Cleaning", type="primary"):
        apply_cleaning(operation)
        st.rerun()

    col_undo, col_reset = st.columns(2)

    with col_undo:
        if st.button(
            "Undo Last Step",
            disabled=not st.session_state.undo_stack,
            use_container_width=True
        ):
            st.session_state.current_df = (
                st.session_state.undo_stack.pop()
            )

            if st.session_state.cleaning_history:
                st.session_state.cleaning_history.pop()

            st.rerun()

    with col_reset:
        if st.button("Reset to Original", use_container_width=True):
            st.session_state.current_df = original.copy(deep=True)
            st.session_state.undo_stack = []
            st.session_state.cleaning_history = []
            st.rerun()

    # Before-and-after comparison
    st.subheader("3. Original vs Current Dataset")

    left, right = st.columns(2)

    with left:
        st.markdown("**Original Dataset**")
        st.write(f"Rows: {len(original)}")
        st.write(f"Columns: {len(original.columns)}")
        st.write(f"Missing cells: {int(original.isnull().sum().sum())}")
        st.write(f"Duplicate rows: {int(original.duplicated().sum())}")
        st.dataframe(original.head(10), use_container_width=True)

    with right:
        st.markdown("**Current Dataset**")
        st.write(f"Rows: {len(current)}")
        st.write(f"Columns: {len(current.columns)}")
        st.write(f"Missing cells: {int(current.isnull().sum().sum())}")
        st.write(f"Duplicate rows: {int(current.duplicated().sum())}")
        st.dataframe(current.head(10), use_container_width=True)

    # History
    st.subheader("4. Cleaning History")

    if st.session_state.cleaning_history:
        for number, entry in enumerate(
            st.session_state.cleaning_history, start=1
        ):
            st.write(f"{number}. {entry}")
    else:
        st.info("No cleaning operations applied yet.")

    # Downloads
    st.subheader("5. Download Results")

    csv_data = current.to_csv(index=False).encode("utf-8")

    st.download_button(
        "Download Current Cleaned CSV",
        data=csv_data,
        file_name="cleaned_dataset.csv",
        mime="text/csv"
    )


    st.subheader("6. Download PDF Report")

    if st.button("Generate PDF Report"):
        try:
            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=".pdf"
            ) as temp_file:
                pdf_path = temp_file.name

            create_pdf_report(
                output_path=pdf_path,
                dataset=st.session_state.current_df,
                scan_report=st.session_state.get("scan_report"),
                outlier_report=st.session_state.get("outlier_report"),
                relationship_report=st.session_state.get(
                    "relationship_report"
                ),
                cleaning_history=st.session_state.cleaning_history
            )

            with open(pdf_path, "rb") as file:
                pdf_bytes = file.read()

            st.session_state.pdf_bytes = pdf_bytes
            os.remove(pdf_path)

        except Exception as e:
            st.error(f"Could not generate PDF report: {e}")

    if st.session_state.get("pdf_bytes") is not None:
        st.download_button(
            "Download PDF Report",
            data=st.session_state.pdf_bytes,
            file_name="smart_data_quality_report.pdf",
            mime="application/pdf"
        )


else:
    st.info("Upload a CSV or Excel file to get started.")

