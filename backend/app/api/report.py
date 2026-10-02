import shutil
import tempfile
from pathlib import Path

from fastapi import (
    APIRouter,
    BackgroundTasks,
    File,
    Form,
    HTTPException,
    UploadFile,
)
from fastapi.responses import FileResponse

from app.analysis.engine import run_analysis
from app.ingestion.excel_reader import read_excel_bytes
from app.insights.insight_generator import generate_weekly_insights
from app.insights.llm_service import GeminiService
from app.reporting.chart_generator import (
    generate_kpi_change_chart,
    generate_movement_bridge_chart,
)
from app.reporting.pdf_generator import generate_weekly_report_pdf


# ---------------------------------------------------------
# Router configuration
# ---------------------------------------------------------

router = APIRouter(
    prefix="/api",
    tags=["Reports"],
)


# ---------------------------------------------------------
# Helper: Clean filename
# ---------------------------------------------------------

def clean_filename(filename: str) -> str:
    """
    Convert an uploaded filename into a safe filename.

    Example:
        Week 1 Report.xlsx
        ->
        Week_1_Report
    """

    name = Path(filename).stem

    safe_name = "".join(
        character
        if character.isalnum()
        or character in ("-", "_")
        else "_"
        for character in name
    )

    return safe_name


# ---------------------------------------------------------
# Helper: Remove temporary report directory
# ---------------------------------------------------------

def cleanup_directory(directory: Path) -> None:
    """
    Remove temporary files after FastAPI finishes
    sending the PDF to the client.
    """

    shutil.rmtree(
        directory,
        ignore_errors=True,
    )


# ---------------------------------------------------------
# Generate report endpoint
# ---------------------------------------------------------

@router.post("/report")
async def generate_report(
    background_tasks: BackgroundTasks,

    previous_file: UploadFile = File(...),

    current_file: UploadFile = File(...),

    key_columns: str = Form(...),

    movement_threshold_pct: float = Form(20.0),

    minimum_absolute_change: float = Form(0.0),

    generate_ai_insights: bool = Form(True),
):
    """
    Compare two weekly Excel files and generate
    a downloadable PDF report.

    Processing flow:

        Excel files
            ↓
        Validation
            ↓
        Python analysis
            ↓
        Optional AI insights
            ↓
        Chart generation
            ↓
        PDF generation
            ↓
        PDF download
    """

    temp_directory = None

    try:

        # =========================================================
        # 1. Validate uploaded files
        # =========================================================

        uploaded_files = [
            previous_file,
            current_file,
        ]

        for uploaded_file in uploaded_files:

            if not uploaded_file.filename:

                raise ValueError(
                    "Uploaded file must have a filename."
                )

            if not uploaded_file.filename.lower().endswith(
                ".xlsx"
            ):

                raise ValueError(
                    f"{uploaded_file.filename} "
                    "is not an .xlsx file."
                )

        # =========================================================
        # 2. Read uploaded Excel file contents
        # =========================================================

        previous_content = await previous_file.read()

        current_content = await current_file.read()

        previous_df = read_excel_bytes(
            previous_content
        )

        current_df = read_excel_bytes(
            current_content
        )

        # =========================================================
        # 3. Parse business key columns
        # =========================================================

        # Example:
        #
        # Product,Region
        #
        # becomes:
        #
        # ["Product", "Region"]

        parsed_key_columns = [
            column.strip()
            for column in key_columns.split(",")
            if column.strip()
        ]

        if not parsed_key_columns:

            raise ValueError(
                "At least one key column must be provided."
            )

        # =========================================================
        # 4. Run deterministic Python analysis
        # =========================================================

        analysis = run_analysis(
            previous_df=previous_df,
            current_df=current_df,
            key_columns=parsed_key_columns,
            movement_threshold_pct=movement_threshold_pct,
            minimum_absolute_change=minimum_absolute_change,
        )

        # =========================================================
        # 5. Generate optional AI insights
        # =========================================================

        # Important:
        #
        # AI is NOT required for the report to work.
        #
        # If Gemini is unavailable, we still generate
        # the PDF using the deterministic Python analysis.

        ai_insights = None

        if generate_ai_insights:

            try:

                llm_service = GeminiService()

                ai_insights = generate_weekly_insights(
                    analysis=analysis,
                    llm_service=llm_service,
                )

            except Exception as exc:

                print(
                    "AI insight generation failed "
                    "during report generation: "
                    f"{exc}"
                )

                ai_insights = None

        # =========================================================
        # 6. Create temporary working directory
        # =========================================================

        # Every request gets its own directory.
        #
        # Example:
        #
        # /tmp/weekly_report_abcd1234/
        #
        # This prevents multiple users from overwriting
        # each other's charts or PDFs.

        temp_directory = Path(
            tempfile.mkdtemp(
                prefix="weekly_report_"
            )
        )

        # =========================================================
        # 7. Define temporary file paths
        # =========================================================

        chart_path = (
            temp_directory
            / "kpi_change_chart.png"
        )
        movement_bridge_chart_path = (
            temp_directory
            / "movement_bridge_chart.png"
        )

        pdf_path = (
            temp_directory
            / "weekly_comparison_report.pdf"
        )

        # =========================================================
        # 8. Generate KPI chart
        # =========================================================

        generate_kpi_change_chart(
            metric_summary=analysis[
                "metric_summary"
            ],
            output_path=chart_path,
        )

        generate_movement_bridge_chart(
            movement_bridge=analysis["movement_bridge"],
            output_path=movement_bridge_chart_path,
        )

        # =========================================================
        # 9. Generate PDF report
        # =========================================================

        generate_weekly_report_pdf(
            analysis=analysis,
            ai_insights=ai_insights,
            chart_path=chart_path,
            movement_bridge_chart_path=movement_bridge_chart_path,
            output_path=pdf_path,
            previous_file_name=previous_file.filename,
            current_file_name=current_file.filename,
        )

        # =========================================================
        # 10. Verify PDF was actually generated
        # =========================================================

        if not pdf_path.exists():

            raise RuntimeError(
                "PDF report was not generated."
            )

        if pdf_path.stat().st_size == 0:

            raise RuntimeError(
                "Generated PDF report is empty."
            )

        # =========================================================
        # 11. Generate download filename
        # =========================================================

        previous_name = clean_filename(
            previous_file.filename
        )

        current_name = clean_filename(
            current_file.filename
        )

        download_filename = (
            f"{previous_name}_vs_"
            f"{current_name}_report.pdf"
        )

        # Example:
        #
        # week1.xlsx
        # week2.xlsx
        #
        # becomes:
        #
        # week1_vs_week2_report.pdf

        # =========================================================
        # 12. Schedule temporary file cleanup
        # =========================================================

        # FileResponse needs the PDF to remain available
        # while FastAPI sends it.
        #
        # BackgroundTasks runs after the response has
        # finished sending.

        background_tasks.add_task(
            cleanup_directory,
            temp_directory,
        )

        # =========================================================
        # 13. Return PDF
        # =========================================================

        return FileResponse(
            path=str(pdf_path),
            media_type="application/pdf",
            filename=download_filename,
        )

    # =============================================================
    # Known validation errors
    # =============================================================

    except ValueError as exc:

        if temp_directory:

            cleanup_directory(
                temp_directory
            )

        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    # =============================================================
    # Unexpected errors
    # =============================================================

    except Exception as exc:

        if temp_directory:

            cleanup_directory(
                temp_directory
            )

        print(
            "Unexpected report generation error: "
            f"{exc}"
        )

        raise HTTPException(
            status_code=500,
            detail=(
                "Unexpected error while "
                "generating the PDF report."
            ),
        ) from exc