import pandas as pd


def calculate_metric_summary(
    previous_df: pd.DataFrame,
    current_df: pd.DataFrame,
    numerical_columns: list[str],
) -> dict:
    """
    Calculate overall week-over-week totals and changes
    for every numerical metric.
    """

    summary = {}

    for column in numerical_columns:

        previous_total = previous_df[column].sum()
        current_total = current_df[column].sum()

        absolute_change = current_total - previous_total

        if previous_total != 0:
            percentage_change = (
                absolute_change / previous_total
            ) * 100
        else:
            percentage_change = None

        summary[column] = {
            "previous_total": float(previous_total),
            "current_total": float(current_total),
            "absolute_change": float(absolute_change),
            "percentage_change": (
                round(float(percentage_change), 2)
                if percentage_change is not None
                else None
            ),
            "direction": (
                "increase"
                if absolute_change > 0
                else "decrease"
                if absolute_change < 0
                else "unchanged"
            ),
        }

    return summary