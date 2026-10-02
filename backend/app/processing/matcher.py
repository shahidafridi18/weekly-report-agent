import pandas as pd


def match_rows(
    previous_df: pd.DataFrame,
    current_df: pd.DataFrame,
    key_columns: list[str],
) -> pd.DataFrame:
    """
    Match rows between previous and current datasets
    using the supplied business key columns.
    """

    # Make sure all key columns exist in both datasets
    for column in key_columns:
        if column not in previous_df.columns:
            raise ValueError(
                f"Key column '{column}' is missing from previous dataset."
            )

        if column not in current_df.columns:
            raise ValueError(
                f"Key column '{column}' is missing from current dataset."
            )

    # Check for duplicate business keys
    previous_duplicates = previous_df.duplicated(
        subset=key_columns,
        keep=False,
    )

    current_duplicates = current_df.duplicated(
        subset=key_columns,
        keep=False,
    )

    if previous_duplicates.any():
        raise ValueError(
            "Duplicate business keys found in previous dataset."
        )

    if current_duplicates.any():
        raise ValueError(
            "Duplicate business keys found in current dataset."
        )

    # Merge the two datasets
    merged_df = previous_df.merge(
        current_df,
        on=key_columns,
        how="outer",
        suffixes=("_previous", "_current"),
        indicator=True,
    )

    return merged_df

def categorize_rows(
    merged_df: pd.DataFrame,
) -> dict[str, pd.DataFrame]:
    """
    Split merged data into matched, new, and removed rows.
    """

    matched_rows = merged_df[
        merged_df["_merge"] == "both"
    ].copy()

    removed_rows = merged_df[
        merged_df["_merge"] == "left_only"
    ].copy()

    new_rows = merged_df[
        merged_df["_merge"] == "right_only"
    ].copy()

    return {
        "matched": matched_rows,
        "new": new_rows,
        "removed": removed_rows,
    }