import pandas as pd


def classify_columns(df: pd.DataFrame) -> dict:
    """
    Classify DataFrame columns into numerical and non-numerical columns.
    """

    numerical_columns = df.select_dtypes(
        include="number"
    ).columns.tolist()

    non_numerical_columns = [
        column
        for column in df.columns
        if column not in numerical_columns
    ]

    return {
        "numerical_columns": numerical_columns,
        "non_numerical_columns": non_numerical_columns,
    }