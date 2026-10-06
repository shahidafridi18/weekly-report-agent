from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from app.analysis.engine import run_analysis
from app.ingestion.excel_reader import read_excel_bytes
from app.insights.insight_generator import generate_weekly_insights
from app.insights.llm_service import GeminiService


router = APIRouter(
    prefix="/api",
    tags=["Comparison"],
)


@router.post("/compare")
async def compare_weekly_files(
    previous_file: UploadFile = File(...),
    current_file: UploadFile = File(...),
    key_columns: str = Form(
        "SIREN, Unique Identifier",
        description=(
            "Comma-separated business key columns. "
            "Counterparty reports default to SIREN and Unique Identifier."
        ),
    ),
    movement_threshold_pct: float = Form(20.0),
    minimum_absolute_change: float = Form(0.0),
    generate_ai_insights: bool = Form(True),
):
    """
    Compare two weekly Excel files.

    The endpoint:
    1. Validates the uploaded files.
    2. Reads both Excel files.
    3. Parses the business key columns.
    4. Runs deterministic Python analysis.
    5. Optionally generates AI business insights.
    6. Returns the complete comparison result.
    """

    try:
        # ---------------------------------------------------------
        # 1. Validate uploaded files
        # ---------------------------------------------------------

        for uploaded_file in [previous_file, current_file]:

            if not uploaded_file.filename:
                raise ValueError(
                    "Uploaded file must have a filename."
                )

            if not uploaded_file.filename.lower().endswith(".xlsx"):
                raise ValueError(
                    f"{uploaded_file.filename} is not an .xlsx file."
                )

        # ---------------------------------------------------------
        # 2. Read uploaded file contents
        # ---------------------------------------------------------

        previous_content = await previous_file.read()
        current_content = await current_file.read()

        previous_df = read_excel_bytes(
            previous_content
        )

        current_df = read_excel_bytes(
            current_content
        )

        # ---------------------------------------------------------
        # 3. Parse key columns
        #
        # Example input:
        # Product,Region
        #
        # Becomes:
        # ["Product", "Region"]
        # ---------------------------------------------------------

        parsed_key_columns = [
            column.strip()
            for column in key_columns.split(",")
            if column.strip()
        ]

        if not parsed_key_columns:
            raise ValueError(
                "At least one key column must be provided."
            )

        # ---------------------------------------------------------
        # 4. Run deterministic Python analysis
        # ---------------------------------------------------------

        result = run_analysis(
            previous_df=previous_df,
            current_df=current_df,
            key_columns=parsed_key_columns,
            movement_threshold_pct=movement_threshold_pct,
            minimum_absolute_change=minimum_absolute_change,
        )

        # ---------------------------------------------------------
        # 5. Generate optional AI insights
        #
        # AI failure must NOT cause the Excel comparison to fail.
        # ---------------------------------------------------------

        ai_insights = None
        ai_status = "not_requested"

        if generate_ai_insights:

            try:
                llm_service = GeminiService()

                ai_insights = generate_weekly_insights(
                    analysis=result,
                    llm_service=llm_service,
                )

                ai_status = "success"

            except Exception as exc:

                # For development, print the actual error
                # to the FastAPI terminal.
                print(
                    f"AI insight generation failed: {exc}"
                )

                ai_status = "unavailable"

        # ---------------------------------------------------------
        # 6. Return final response
        # ---------------------------------------------------------

        return {
            "comparison": {
                "previous_file": previous_file.filename,
                "current_file": current_file.filename,
                "key_columns": parsed_key_columns,
            },

            "analysis": result,

            "ai": {
                "status": ai_status,
                "insights": ai_insights,
            },
        }

    # -------------------------------------------------------------
    # Known validation/business errors
    # -------------------------------------------------------------

    except ValueError as exc:

        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    # -------------------------------------------------------------
    # Unexpected server errors
    # -------------------------------------------------------------

    except Exception as exc:

        print(
            f"Unexpected comparison error: {exc}"
        )

        raise HTTPException(
            status_code=500,
            detail=(
                "Unexpected error while comparing files."
            ),
        ) from exc