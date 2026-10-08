from pathlib import Path

from app.analysis.engine import run_analysis
from app.ingestion.excel_reader import (
    read_excel_file,
)
from app.insights.insight_generator import (
    generate_weekly_insights,
)
from app.insights.llm_service import (
    GeminiService,
)
from app.reporting.chart_generator import (
    generate_kpi_change_chart,
    generate_movement_bridge_chart,
)
from app.reporting.pdf_generator import (
    generate_weekly_report_pdf,
)


BASE_DIR = Path(__file__).resolve().parent.parent

SAMPLE_DATA_DIR = (
    BASE_DIR / "sample_data"
)

REPORT_DIR = (
    BASE_DIR / "generated_reports"
)


# -----------------------------------------------------
# Read Excel files
# -----------------------------------------------------

week1 = read_excel_file(
    SAMPLE_DATA_DIR / "week1.xlsx"
)

week2 = read_excel_file(
    SAMPLE_DATA_DIR / "week2.xlsx"
)


# -----------------------------------------------------
# Run Python analysis
# -----------------------------------------------------

analysis = run_analysis(
    previous_df=week1,
    current_df=week2,
    key_columns=[
        "Product",
        "Region",
    ],
)


# -----------------------------------------------------
# Generate AI insights
# -----------------------------------------------------

ai_insights = None

try:

    llm_service = GeminiService()

    ai_insights = generate_weekly_insights(
        analysis=analysis,
        llm_service=llm_service,
    )

except Exception as exc:

    print(
        f"AI insights unavailable: {exc}"
    )


# -----------------------------------------------------
# Generate chart
# -----------------------------------------------------

chart_path = generate_kpi_change_chart(
    metric_summary=analysis[
        "metric_summary"
    ],
    output_path=(
        REPORT_DIR /
        "kpi_change_chart.png"
    ),
)

bridge_chart_path = generate_movement_bridge_chart(
    movement_bridge=analysis[
        "movement_bridge"
    ],
    output_path=(
        REPORT_DIR
        / "movement_bridge_chart.png"
    ),
)


# -----------------------------------------------------
# Generate PDF
# -----------------------------------------------------

pdf_path = generate_weekly_report_pdf(
    analysis=analysis,
    ai_insights=ai_insights,
    chart_path=chart_path,
    movement_bridge_chart_path=bridge_chart_path,
    output_path=(
        REPORT_DIR
        / "weekly_comparison_report.pdf"
    ),
    previous_file_name="week1.xlsx",
    current_file_name="week2.xlsx",
)

print(
    f"\nPDF created successfully: {pdf_path}"
)