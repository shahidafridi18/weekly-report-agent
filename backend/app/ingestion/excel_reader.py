from pathlib import Path

import pandas as pd


def read_excel_file(file_path: str | Path) -> pd.DataFrame:
    """
    Read an Excel file and return its contents as a Pandas DataFrame.
    """

    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(
            f"Excel file not found: {file_path}"
        )

    if file_path.suffix.lower() != ".xlsx":
        raise ValueError(
            f"Unsupported file type: {file_path.suffix}. "
            "Only .xlsx files are currently supported."
        )

    df = pd.read_excel(file_path)

    if df.empty:
        raise ValueError(
            f"Excel file contains no data: {file_path.name}"
        )

    return df

from io import BytesIO

import pandas as pd


def read_excel_bytes(
    file_content: bytes,
) -> pd.DataFrame:
    """
    Read Excel data directly from uploaded bytes.
    """

    if not file_content:
        raise ValueError(
            "Uploaded Excel file is empty."
        )

    try:
        df = pd.read_excel(
            BytesIO(file_content)
        )

    except Exception as exc:
        raise ValueError(
            "Unable to read the uploaded Excel file."
        ) from exc

    if df.empty:
        raise ValueError(
            "Uploaded Excel file contains no data."
        )

    return df