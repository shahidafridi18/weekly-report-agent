from io import BytesIO
from pathlib import Path
import re

import pandas as pd

from app.schema import (
    COUNTERPARTY_KEY_COLUMNS,
    COUNTERPARTY_METRIC_COLUMNS,
    COUNTERPARTY_TEXT_COLUMNS,
)


def _normalize_headers(df: pd.DataFrame) -> pd.DataFrame:
    df = df.dropna(axis="columns", how="all")
    df = df.loc[
        :,
        [
            column
            for column in df.columns
            if not str(column).startswith("Unnamed:")
        ],
    ]
    df.columns = [
        re.sub(r"\s+", " ", str(column).replace("\n", " ")).strip()
        for column in df.columns
    ]
    return df.dropna(axis="index", how="all").reset_index(drop=True)


def _find_header_row(raw_df: pd.DataFrame) -> int | None:
    required_headers = {
        "counterparty name",
        *(column.casefold() for column in COUNTERPARTY_KEY_COLUMNS),
    }

    for row_index, row in raw_df.iterrows():
        headers = {
            re.sub(r"\s+", " ", str(value).replace("\n", " ")).strip().casefold()
            for value in row
            if pd.notna(value)
        }
        if required_headers.issubset(headers):
            return int(row_index)

    return None


def _normalize_data(df: pd.DataFrame) -> pd.DataFrame:
    df = _normalize_headers(df)

    for column in COUNTERPARTY_TEXT_COLUMNS:
        if column in df.columns:
            df[column] = df[column].astype("string").str.strip()

    identity_columns = [
        column
        for column in ("Rank", *COUNTERPARTY_TEXT_COLUMNS)
        if column in df.columns
    ]
    if identity_columns:
        footer_mask = df[identity_columns].astype("string").apply(
            lambda column: column.str.contains(
                "TOTAL EXPOSURE",
                case=False,
                na=False,
            )
        ).any(axis="columns")
        df = df.loc[~footer_mask].copy()

    for column in COUNTERPARTY_METRIC_COLUMNS:
        if column not in df.columns:
            continue

        original_values = df[column]
        numeric_values = pd.to_numeric(original_values, errors="coerce")
        invalid_values = original_values.notna() & numeric_values.isna()
        if invalid_values.any():
            examples = original_values[invalid_values].astype(str).head(3).tolist()
            raise ValueError(
                f"Metric column '{column}' contains non-numeric values: {examples}."
            )
        df[column] = numeric_values

    if df.empty:
        raise ValueError("Excel sheet contains no counterparty data rows.")

    return df.reset_index(drop=True)


def _read_excel_source(
    source,
    sheet_name: str | None = None,
) -> pd.DataFrame:
    with pd.ExcelFile(source) as excel_file:
        return _read_excel_workbook(excel_file, sheet_name)


def _read_excel_workbook(
    excel_file: pd.ExcelFile,
    sheet_name: str | None = None,
) -> pd.DataFrame:
    sheet_names = excel_file.sheet_names

    if sheet_name is not None:
        if sheet_name not in sheet_names:
            raise ValueError(f"Excel sheet '{sheet_name}' was not found.")
        candidate_sheets = [sheet_name]
    elif "Analysis Data" in sheet_names:
        candidate_sheets = ["Analysis Data"]
    else:
        candidate_sheets = sheet_names

    fallback_df = None
    for candidate in candidate_sheets:
        raw_df = pd.read_excel(
            excel_file,
            sheet_name=candidate,
            header=None,
        )
        header_row = _find_header_row(raw_df.head(20))

        if header_row is None:
            df = pd.read_excel(excel_file, sheet_name=candidate)
        else:
            df = pd.read_excel(
                excel_file,
                sheet_name=candidate,
                header=header_row,
            )

        df = _normalize_data(df)
        if set(COUNTERPARTY_KEY_COLUMNS).issubset(df.columns):
            return df
        if fallback_df is None:
            fallback_df = df

    if fallback_df is not None:
        return fallback_df

    raise ValueError("Excel workbook contains no non-empty data sheet.")


def read_excel_file(
    file_path: str | Path,
    sheet_name: str | None = None,
) -> pd.DataFrame:
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

    return _read_excel_source(file_path, sheet_name=sheet_name)


def read_excel_bytes(
    file_content: bytes,
    sheet_name: str | None = None,
) -> pd.DataFrame:
    """
    Read Excel data directly from uploaded bytes.
    """

    if not file_content:
        raise ValueError(
            "Uploaded Excel file is empty."
        )

    try:
        return _read_excel_source(
            BytesIO(file_content),
            sheet_name=sheet_name,
        )

    except Exception as exc:
        raise ValueError(
            "Unable to read the uploaded Excel file."
        ) from exc
