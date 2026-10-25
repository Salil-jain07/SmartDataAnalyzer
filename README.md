# Smart Data Analyzer

A Python-based web application that helps users explore datasets, identify data quality issues, clean data, visualize relationships, and generate downloadable reports.

## Features

- **CSV and Excel Upload:** Upload and select datasets for analysis.
- **Data Quality Scan:** Identify missing values, duplicate rows, and potential data issues.
- **Data Quality Score:** Calculate a score based on missing values and duplicate rows.
- **Outlier Detection:** Identify potentially unusual numerical values.
- **Interactive Visualizations:** Generate histograms, bar charts, scatter plots, and interactive correlation heatmaps.
- **Data Cleaning:** Remove duplicates, remove rows with missing values, fill missing values using median or mode, and standardize text.
- **Undo and Reset:** Undo the last cleaning operation or restore the original dataset.
- **Dataset Comparison:** Compare the original dataset with the cleaned dataset.
- **Cleaning History:** Review the cleaning operations performed.
- **Download Cleaned Data:** Export the cleaned dataset as a CSV file.
- **PDF Reports:** Generate and download a data quality report.

## Technologies Used

- Python
- Streamlit
- Pandas and NumPy
- Matplotlib and Seaborn
- Plotly
- OpenPyXL
- ReportLab

## Project Structure

```text
SmartDataAnalyzer/
├── app.py
├── data_scanner.py
├── visualizations.py
├── pdf_report.py
├── requirements.txt
└── README.md
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd SmartDataAnalyzer
```

Replace `YOUR_GITHUB_REPOSITORY_URL` with your actual repository URL.

### 2. Create a virtual environment (recommended)

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the application

```bash
python -m streamlit run app.py
```

The application will open in your browser.

## How to Use

1. Upload a CSV or Excel dataset.
2. Review the dataset overview and quality metrics.
3. Run the data quality scan and outlier analysis.
4. Explore visualizations and column relationships.
5. Apply cleaning operations as needed.
6. Compare the original and current datasets.
7. Download the cleaned CSV or generate a PDF report.

## Data Quality Score

The score is calculated using missing-cell and duplicate-row ratios. It is a basic indicator of data completeness and duplication, not a comprehensive measure of all possible data quality problems.

## Future Improvements

- Add more data validation rules.
- Support larger datasets efficiently.
- Add customizable reports and visualizations.
- Improve data quality recommendations.

## Author

Developed as a Python data analysis project.
