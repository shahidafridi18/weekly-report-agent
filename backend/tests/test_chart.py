from pathlib import Path

from app.analysis.engine import run_analysis
from app.ingestion.excel_reader import (
    read_excel_file,
)
from app.reporting.chart_generator import (
    generate_kpi_change_chart,
)


BASE_DIR = Path(__file__).resolve().parent.parent

SAMPLE_DATA_DIR = (
    BASE_DIR / "sample_data"
)

REPORT_DIR = (
    BASE_DIR / "generated_reports"
)


week1 = read_excel_file(
    SAMPLE_DATA_DIR / "week1.xlsx"
)

week2 = read_excel_file(
    SAMPLE_DATA_DIR / "week2.xlsx"
)


analysis = run_analysis(
    previous_df=week1,
    current_df=week2,
    key_columns=[
        "Product",
        "Region",
    ],
)


chart_path = generate_kpi_change_chart(
    metric_summary=analysis[
        "metric_summary"
    ],
    output_path=(
        REPORT_DIR /
        "kpi_change_chart.png"
    ),
)


print(
    f"Chart created successfully: {chart_path}"
)