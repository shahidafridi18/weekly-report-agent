import pandas as pd


def validate_columns(
    previous_df: pd.DataFrame,
    current_df: pd.DataFrame,
) -> dict:
    """
    Compare the columns available in two weekly datasets.
    """

    previous_columns = set(previous_df.columns)
    current_columns = set(current_df.columns)

    missing_columns = sorted(
        previous_columns - current_columns
    )

    new_columns = sorted(
        current_columns - previous_columns
    )

    common_columns = sorted(
        previous_columns & current_columns
    )

    return {
        "valid": not missing_columns and not new_columns,
        "missing_columns": missing_columns,
        "new_columns": new_columns,
        "common_columns": common_columns,
    }