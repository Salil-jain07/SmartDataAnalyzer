# Smart Data Analyzer

An interactive Python-based data analysis application that helps users inspect data quality, identify common data issues, clean datasets, visualize patterns, and export analysis results.

## Live Demo

[**Open Smart Data Analyzer**](https://smartdataanalyzer-fxahm82cz82ufuf884rwrf.streamlit.app/)

Upload a CSV or Excel file to explore dataset statistics, run data-quality checks, analyze outliers, create interactive visualizations, apply cleaning operations, and download cleaned data or a PDF report.

## Source Code

[**GitHub Repository — SmartDataAnalyzer**](https://github.com/Salil-jain07/SmartDataAnalyzer)

## Project Goals

- Simplify the initial process of exploring and understanding tabular datasets.
- Identify common data-quality issues such as missing values and duplicate records.
- Provide easy-to-use data-cleaning operations.
- Visualize data distributions and relationships between numeric variables.
- Compare original data with cleaned data.
- Maintain cleaning history and support undo and reset operations.
- Export cleaned datasets and generate downloadable PDF reports.
- Deploy the application online using Streamlit Community Cloud.

## Architecture

```text
         User
          |
          v
   Streamlit Web App
        app.py
          |
          v
   CSV / Excel Upload
          |
          v
    Pandas DataFrame
          |
          +----------------------+
          |                      |
          v                      v
   Data Quality Scan       Dataset Overview
   data_scanner.py         and Metrics
          |
          v
    Data Exploration
          |
          +----------------------+
          |                      |
          v                      v
   Visualizations         Data Cleaning
   visualizations.py      Operations
          |                      |
          |                      v
          |               Cleaning History
          |               Undo / Reset
          |                      |
          +-----------+----------+
                      |
                      v
               Export Results
                 /        \
                v          v
          Cleaned CSV   PDF Report
                        pdf_report.py
```

The architecture represents the main application flow. The project uses Pandas for data processing, Streamlit for the user interface, and separate Python modules for data scanning, visualizations, and PDF report generation.

## Technology Stack

- **Python** — Application logic and data processing.
- **Streamlit** — Interactive web application interface.
- **Pandas** — Dataset loading, inspection, cleaning, and transformation.
- **NumPy** — Numerical operations.
- **Plotly** — Interactive visualizations and correlation heatmaps.
- **Matplotlib and Seaborn** — Visualization libraries included in the project dependencies.
- **Openpyxl** — Excel `.xlsx` file support.
- **ReportLab** — PDF report generation.
- **Git** — Local version control.
- **GitHub** — Source code hosting.
- **Streamlit Community Cloud** — Application deployment.

## Supported Data Formats

The application supports:

- CSV files (`.csv`)
- Excel workbooks (`.xlsx`)

Users can upload datasets and select a dataset for analysis.

The application is designed for tabular data. The results depend on the quality, structure, data types, and size of the uploaded file.

## Application Features

### 1. Dataset Overview

- Display dataset dimensions.
- Show original and current row counts.
- Display the total number of columns.
- Track missing cells and duplicate rows.
- Show complete-cell percentage.
- Display a Data Quality Score.

### 2. Automated Data Quality Analysis

- Scan datasets for common data-quality issues.
- Identify missing values and duplicate records.
- Analyze potential outliers.
- Inspect relationships between numeric columns.
- Display findings and suggested fixes.

The suggested fixes are intended to help users investigate problems. Users should verify whether a proposed change is appropriate for their dataset.

### 3. Data Cleaning

The application supports common cleaning operations:

- Remove duplicate rows.
- Remove rows containing missing values.
- Fill missing numeric values using the median.
- Fill missing values using the mode.
- Standardize text values.

### 4. Cleaning History and Recovery

- Undo the last cleaning operation.
- Reset the dataset to its original state.
- Compare original and current datasets.
- Track cleaning actions through cleaning history.

These features help users understand how cleaning operations affect their data.

### 5. Interactive Visualizations

The application provides multiple visualization options:

- **Histogram:** Explore the distribution of numeric values.
- **Bar Chart:** Compare values across categories.
- **Scatter Plot:** Examine relationships between two numeric variables.
- **Correlation Heatmap:** Explore correlations between numeric columns.

The interactive correlation heatmap is built with Plotly and supports features such as hover information and zooming.

### 6. Data Export and Reporting

- Download the cleaned dataset as a CSV file.
- Generate a PDF report.
- Download the generated report for documentation or further review.

## Project Structure

```text
SmartDataAnalyzer/
│
├── app.py
├── data_scanner.py
├── visualizations.py
├── pdf_report.py
├── requirements.txt
├── README.md
├── .gitignore
└── .venv/                 # Local environment; not committed
```

### File Responsibilities

| File | Purpose |
|---|---|
| `app.py` | Main Streamlit application, user interface, dataset workflow, metrics, cleaning controls, charts, and downloads. |
| `data_scanner.py` | Data-quality scanning and issue identification. |
| `visualizations.py` | Visualization-related functions. |
| `pdf_report.py` | PDF report generation. |
| `requirements.txt` | Python package dependencies. |
| `README.md` | Project documentation and setup instructions. |
| `.gitignore` | Excludes selected local, generated, and sensitive files from Git. |

The `.venv/` directory is used for the local Python environment and should not be uploaded to GitHub.

## Installation and Setup

### Prerequisites

- Python installed on your system.
- Git, if you want to clone the repository.
- A code editor such as PyCharm.
- Basic familiarity with CSV or Excel datasets.

### 1. Clone the Repository

```bash
git clone https://github.com/Salil-jain07/SmartDataAnalyzer.git
cd SmartDataAnalyzer
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

### 3. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Run the Application

```bash
python -m streamlit run app.py
```

Streamlit will provide a local URL, usually:

```text
http://localhost:8501
```

Open the URL in your browser to use the application.

## How to Use the Application

1. Open the application.
2. Upload a CSV or Excel dataset.
3. Select the dataset you want to analyze.
4. Review the dataset overview and quality metrics.
5. Run the data-quality scan.
6. Explore outliers, relationships, and available charts.
7. Apply the required cleaning operations.
8. Use undo or reset if needed.
9. Compare the original and cleaned data.
10. Download the cleaned CSV or generate a PDF report.

## Data Quality Score

The application displays a Data Quality Score as a quick summary of dataset quality.

The score should be interpreted according to the formula implemented in the application. It is a project-specific indicator rather than a universally accepted data-quality standard.

A score alone cannot establish that a dataset is correct. The importance of missing values, duplicates, and unusual observations depends on the dataset's purpose and business rules.

## Deployment

The application is deployed using Streamlit Community Cloud and connected to GitHub.

- **Live application:** [Smart Data Analyzer](https://smartdataanalyzer-fxahm82cz82ufuf884rwrf.streamlit.app/)
- **Source repository:** [SmartDataAnalyzer](https://github.com/Salil-jain07/SmartDataAnalyzer)

The application source code is maintained in GitHub. Updates pushed to the connected repository can trigger a redeployment.

## Testing and Validation

Important checks when testing the application include:

- Uploading valid CSV and Excel files.
- Testing datasets containing missing values and duplicates.
- Verifying the results of each cleaning operation.
- Checking undo and reset functionality.
- Comparing original and cleaned data.
- Testing charts with suitable column types.
- Downloading the cleaned CSV.
- Generating and downloading a PDF report.
- Testing empty, malformed, or unsupported input files.
- Verifying the deployed application independently of the local environment.

## Current Limitations

- Cleaning operations are generic and may not suit every dataset.
- Outliers may be valid observations and require investigation before removal.
- Correlation analysis primarily describes linear relationships between numeric variables and does not establish causation.
- Very large datasets may require additional performance optimization.
- The Data Quality Score requires a clearly documented formula for consistent interpretation.
- The application is intended for interactive data exploration and preparation, not as a replacement for domain-specific validation or a full-scale data engineering platform.

## Future Improvements

- Add automated unit and integration tests.
- Introduce configurable data-quality rules.
- Improve validation and error handling for uploaded files.
- Add more file formats and customizable cleaning operations.
- Improve performance for large datasets.
- Expand PDF reports with more configurable summaries and visualizations.
- Add additional statistical analysis and data profiling features.
- Improve documentation of the Data Quality Score.
- Add more comprehensive logging and error diagnostics.
- Explore support for saving reusable cleaning workflows.

## Security and Data Handling

- Never commit passwords, API keys, cloud credentials, or other secrets.
- Do not upload confidential or personally identifiable data to a public demonstration.
- Review the hosting platform's data-handling behavior before uploading sensitive files.
- Avoid persistent storage of uploaded datasets unless it is explicitly required and appropriately secured.
- Validate uploaded files and handle parsing errors safely.

## Resume Description

**Smart Data Analyzer | Python, Streamlit, Pandas, Plotly, ReportLab**

- Developed an interactive data analysis application for CSV and Excel datasets with automated data-quality checks and common cleaning operations.
- Implemented interactive visualizations, original-versus-cleaned data comparison, cleaning history, undo/reset functionality, and CSV export.
- Integrated PDF report generation and deployed the application using Streamlit Community Cloud with GitHub version control.

## Author

**Salil Jain**

- GitHub: [Salil-jain07](https://github.com/Salil-jain07)
- Project Repository: [SmartDataAnalyzer](https://github.com/Salil-jain07/SmartDataAnalyzer)
- Live Demo: [Smart Data Analyzer](https://smartdataanalyzer-fxahm82cz82ufuf884rwrf.streamlit.app/)



