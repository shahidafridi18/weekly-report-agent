from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from app.analysis.engine import run_analysis
from app.ingestion.excel_reader import read_excel_bytes


router = APIRouter(
    prefix="/api",
    tags=["Comparison"],
)


@router.post("/compare")
async def compare_weekly_files(
    previous_file: UploadFile = File(...),
    current_file: UploadFile = File(...),
    key_columns: str = Form(...),
    movement_threshold_pct: float = Form(20.0),
    minimum_absolute_change: float = Form(0.0),
):
    """
    Compare two weekly Excel files.
    """

    try:

        # Validate filenames
        for uploaded_file in [
            previous_file,
            current_file,
        ]:
            if not uploaded_file.filename:
                raise ValueError(
                    "Uploaded file must have a filename."
                )

            if not uploaded_file.filename.lower().endswith(
                ".xlsx"
            ):
                raise ValueError(
                    f"{uploaded_file.filename} is not an .xlsx file."
                )

        # Read uploaded bytes
        previous_content = await previous_file.read()
        current_content = await current_file.read()

        # Convert Excel -> Pandas
        previous_df = read_excel_bytes(
            previous_content
        )

        current_df = read_excel_bytes(
            current_content
        )

        # Convert:
        #
        # "Product,Region"
        #
        # into:
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

        # Run our existing analytical engine
        result = run_analysis(
            previous_df=previous_df,
            current_df=current_df,
            key_columns=parsed_key_columns,
            movement_threshold_pct=movement_threshold_pct,
            minimum_absolute_change=minimum_absolute_change,
        )

        return {
            "comparison": {
                "previous_file": previous_file.filename,
                "current_file": current_file.filename,
            },
            "analysis": result,
        }

    except ValueError as exc:

        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail="Unexpected error while comparing files.",
        ) from exc