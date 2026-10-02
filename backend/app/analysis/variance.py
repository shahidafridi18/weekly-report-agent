import pandas as pd


def calculate_variances(
    matched_df: pd.DataFrame,
    numerical_columns: list[str],
) -> pd.DataFrame:
    """
    Calculate absolute and percentage changes
    for each numerical column.
    """

    result_df = matched_df.copy()

    for column in numerical_columns:

        previous_column = f"{column}_previous"
        current_column = f"{column}_current"

        if previous_column not in result_df.columns:
            continue

        if current_column not in result_df.columns:
            continue

        change_column = f"{column}_change"
        percentage_column = f"{column}_change_pct"

        result_df[change_column] = (
            result_df[current_column]
            - result_df[previous_column]
        )

        previous_values = result_df[previous_column]

        result_df[percentage_column] = (
            result_df[change_column]
            .div(previous_values.where(previous_values != 0))
            .mul(100)
        )

    return result_df