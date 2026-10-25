
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    LongTable
)
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import ParagraphStyle


def create_pdf_report(
    output_path,
    dataset,
    scan_report,
    outlier_report,
    relationship_report,
    cleaning_history
):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        rightMargin=30,
        leftMargin=30,
        topMargin=35,
        bottomMargin=35
    )

    styles = getSampleStyleSheet()
    content = []

    # Report title
    title_style = ParagraphStyle(
        "CustomTitle",
        parent=styles["Title"],
        alignment=TA_CENTER,
        textColor=colors.darkblue
    )

    content.append(
        Paragraph("Smart Data Analyzer Report", title_style)
    )
    content.append(Spacer(1, 0.2 * inch))

    # Calculate dataset metrics
    total_rows = len(dataset)
    total_columns = len(dataset.columns)
    missing_cells = int(dataset.isnull().sum().sum())
    duplicate_rows = int(dataset.duplicated().sum())
    total_cells = total_rows * total_columns

    complete_percentage = (
        ((total_cells - missing_cells) / total_cells) * 100
        if total_cells > 0 else 100
    )

    # Data Quality Score
    quality_score = 100

    if total_cells > 0:
        quality_score -= (missing_cells / total_cells) * 40

    if total_rows > 0:
        quality_score -= (duplicate_rows / total_rows) * 30

    quality_score = round(max(0, quality_score), 2)

    content.append(
        Paragraph("1. Dataset Overview", styles["Heading2"])
    )

    overview = [
        ["Metric", "Value"],
        ["Total Rows", str(total_rows)],
        ["Total Columns", str(total_columns)],
        ["Missing Cells", str(missing_cells)],
        ["Duplicate Rows", str(duplicate_rows)],
        ["Complete Cells", f"{complete_percentage:.2f}%"],
        ["Data Quality Score", f"{quality_score}/100"]
    ]

    table = Table(overview, colWidths=[240, 240])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("PADDING", (0, 0), (-1, -1), 7),
        ("VALIGN", (0, 0), (-1, -1), "TOP")
    ]))
    content.append(table)
    content.append(Spacer(1, 0.2 * inch))

    # Helper function for report tables
    def add_report_table(report):
        headers = list(report.columns)

        table_data = [
            [Paragraph(str(header), styles["Normal"])
             for header in headers]
        ]

        for row in report.fillna("").astype(str).values.tolist():
            table_data.append([
                Paragraph(str(value), styles["Normal"])
                for value in row
            ])

        available_width = A4[0] - 60
        column_width = available_width / max(1, len(headers))

        report_table = LongTable(
            table_data,
            colWidths=[column_width] * len(headers),
            repeatRows=1
        )

        report_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightblue),
            ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
            ("FONTSIZE", (0, 0), (-1, -1), 7),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 4),
            ("RIGHTPADDING", (0, 0), (-1, -1), 4),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5)
        ]))

        content.append(report_table)

    # Data Quality Scan
    content.append(
        Paragraph("2. Data Quality Scan", styles["Heading2"])
    )

    if scan_report is not None and not scan_report.empty:
        add_report_table(scan_report)
    else:
        content.append(
            Paragraph(
                "No scan findings available.",
                styles["Normal"]
            )
        )

    content.append(Spacer(1, 0.2 * inch))

    # Outlier report
    content.append(
        Paragraph("3. Potential Outliers", styles["Heading2"])
    )

    if outlier_report is not None and not outlier_report.empty:
        add_report_table(outlier_report)
    else:
        content.append(
            Paragraph(
                "No outlier findings available.",
                styles["Normal"]
            )
        )

    content.append(Spacer(1, 0.2 * inch))

    # Relationship report
    content.append(
        Paragraph("4. Column Relationships", styles["Heading2"])
    )

    if (
        relationship_report is not None
        and not relationship_report.empty
    ):
        add_report_table(relationship_report)
    else:
        content.append(
            Paragraph(
                "No relationship analysis available.",
                styles["Normal"]
            )
        )

    content.append(Spacer(1, 0.2 * inch))

    # Cleaning history
    content.append(
        Paragraph("5. Cleaning History", styles["Heading2"])
    )

    if cleaning_history:
        for number, entry in enumerate(cleaning_history, start=1):
            content.append(
                Paragraph(
                    f"{number}. {entry}",
                    styles["Normal"]
                )
            )
            content.append(Spacer(1, 4))
    else:
        content.append(
            Paragraph(
                "No cleaning operations have been recorded.",
                styles["Normal"]
            )
        )

    doc.build(content)
