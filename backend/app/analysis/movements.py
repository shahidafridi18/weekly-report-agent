import pandas as pd


def detect_major_movements(
    variance_df: pd.DataFrame,
    numerical_columns: list[str],
    key_columns: list[str],
    threshold_pct: float = 20.0,
    minimum_absolute_change: float = 0.0,
) -> list[dict]:
    """
    Detect significant movements using both percentage
    and absolute-change thresholds.
    """

    movements = []

    for _, row in variance_df.iterrows():

        entity = {
            key: row[key]
            for key in key_columns
        }

        for metric in numerical_columns:

            previous_column = f"{metric}_previous"
            current_column = f"{metric}_current"
            change_column = f"{metric}_change"
            percentage_column = f"{metric}_change_pct"

            percentage_change = row[percentage_column]
            absolute_change = row[change_column]

            if pd.isna(percentage_change):
                continue

            percentage_significant = (
                abs(percentage_change)
                >= threshold_pct
            )

            absolute_significant = (
                abs(absolute_change)
                >= minimum_absolute_change
            )

            if (
                percentage_significant
                and absolute_significant
            ):

                movements.append(
                    {
                        "entity": entity,
                        "metric": metric,
                        "previous_value": float(
                            row[previous_column]
                        ),
                        "current_value": float(
                            row[current_column]
                        ),
                        "absolute_change": float(
                            absolute_change
                        ),
                        "percentage_change": round(
                            float(percentage_change),
                            2,
                        ),
                        "direction": (
                            "increase"
                            if absolute_change > 0
                            else "decrease"
                        ),
                    }
                )

    movements.sort(
        key=lambda item: abs(
            item["absolute_change"]
        ),
        reverse=True,
    )

    return movements