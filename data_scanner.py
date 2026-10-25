
import pandas as pd


def scan_dataset(df):
    """Identify potential data-quality issues without changing the data."""
    report = []

    # Missing values
    for column in df.columns:
        missing_count = int(df[column].isna().sum())

        if missing_count > 0:
            report.append({
                "Column": column,
                "Issue": "Missing values",
                "Count": missing_count,
                "Details": f"{missing_count} missing value(s)",
                "Suggested Fix": (
                    "Fill with median for numeric data, "
                    "mode for categorical data, or remove affected rows."
                )
            })

    # Duplicate rows
    duplicate_count = int(df.duplicated().sum())

    if duplicate_count > 0:
        report.append({
            "Column": "All columns",
            "Issue": "Duplicate rows",
            "Count": duplicate_count,
            "Details": f"{duplicate_count} exact duplicate row(s)",
            "Suggested Fix": ("Review and remove duplicate rows if they are unintended.")
        })

    # Numeric checks
    numeric_columns = df.select_dtypes(include="number").columns

    for column in numeric_columns:
        negative_count = int((df[column] < 0).sum())

        if negative_count > 0:
            report.append({
                "Column": column,
                "Issue": "Negative values",
                "Count": negative_count,
                "Details": (
                    f"{negative_count} negative value(s); "
                    "check whether these are valid"
                ),
                "Suggested Fix": ("Check whether negative values are valid for this column.")
            })

        # IQR-based outlier screening
        values = df[column].dropna()

        if len(values) >= 4:
            q1 = values.quantile(0.25)
            q3 = values.quantile(0.75)
            iqr = q3 - q1

            if iqr > 0:
                lower_bound = q1 - 1.5 * iqr
                upper_bound = q3 + 1.5 * iqr

                outlier_count = int(
                    ((values < lower_bound) |
                     (values > upper_bound)).sum()
                )

                if outlier_count > 0:
                    report.append({
                        "Column": column,
                        "Issue": "Potential outliers",
                        "Count": outlier_count,
                        "Details": (
                            f"Values outside {lower_bound:.2f} "
                            f"to {upper_bound:.2f}"
                        ),
                        "Suggested Fix":( "Inspect flagged values before deciding whether to correct or retain them.")
                    })

    # Inconsistent text formatting
    text_columns = df.select_dtypes(
        include=["object", "string"]
    ).columns

    for column in text_columns:
        values = df[column].dropna().astype(str)

        inconsistent_count = int(
            (
                (values != values.str.strip()) |
                (values != values.str.title())
            ).sum()
        )

        if inconsistent_count > 0:
            report.append({
                "Column": column,
                "Issue": "Inconsistent text formatting",
                "Count": inconsistent_count,
                "Details": (
                    "Some values have extra spaces or inconsistent "
                    "capitalization"
                ),
                "Suggested Fix":( "Trim extra spaces and standardize capitalization if appropriate.")
            })

    return pd.DataFrame(
        report,
        columns=[
            "Column",
            "Issue",
            "Count",
            "Details",
            "Suggested Fix"
        ]
    )


def detect_outliers(df):
    """Return the actual rows and values flagged as potential outliers."""
    outlier_rows = []
    numeric_columns = df.select_dtypes(include="number").columns

    for column in numeric_columns:
        values = df[column].dropna()

        if len(values) < 4:
            continue

        q1 = values.quantile(0.25)
        q3 = values.quantile(0.75)
        iqr = q3 - q1

        if iqr == 0:
            continue

        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr

        mask = (
            (df[column] < lower_bound) |
            (df[column] > upper_bound)
        )

        for index, value in df.loc[mask, column].items():
            outlier_rows.append({
                "Row Index": index,
                "Column": column,
                "Value": value,
                "Lower Bound": round(lower_bound, 2),
                "Upper Bound": round(upper_bound, 2)
            })

    return pd.DataFrame(
        outlier_rows,
        columns=[
            "Row Index", "Column", "Value",
            "Lower Bound", "Upper Bound"
        ]
    )

def analyze_relationships(df):
    """Analyze correlations between numeric columns."""

    numeric_df = df.select_dtypes(include="number")

    columns = [
        "Column 1", "Column 2",
        "Correlation", "Strength", "Direction"
    ]

    if numeric_df.shape[1] < 2:
        return pd.DataFrame(columns=columns)

    correlation_matrix = numeric_df.corr()
    results = []

    numeric_columns = correlation_matrix.columns

    for i in range(len(numeric_columns)):
        for j in range(i + 1, len(numeric_columns)):
            col1 = numeric_columns[i]
            col2 = numeric_columns[j]
            corr = correlation_matrix.loc[col1, col2]

            if pd.isna(corr):
                continue

            strength_value = abs(corr)

            if strength_value >= 0.7:
                strength = "Strong"
            elif strength_value >= 0.4:
                strength = "Moderate"
            else:
                strength = "Weak"

            if corr > 0:
                direction = "Positive"
            elif corr < 0:
                direction = "Negative"
            else:
                direction = "No linear relationship"
                results.append({
                    "Column 1": col1,
                    "Column 2": col2,
                    "Correlation": round(corr, 3),
                    "Strength": strength,
                    "Direction": direction
                })

            return pd.DataFrame(results, columns=columns)

def calculate_quality_score(df):
    """Calculate a basic data quality score out of 100."""

    if df.empty:
        return 0

    total_cells = df.shape[0] * df.shape[1]

    missing_ratio = df.isna().sum().sum() / total_cells
    duplicate_ratio = df.duplicated().sum() / len(df)

    score = 100
    score -= missing_ratio * 40
    score -= duplicate_ratio * 30

    return round(max(0, score), 2)