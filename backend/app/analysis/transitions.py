import pandas as pd


def detect_zero_transitions(
    variance_df: pd.DataFrame,
    numerical_columns: list[str],
    key_columns: list[str],
) -> list[dict]:
    """
    Detect metrics that moved from zero to a value
    or from a value to zero.
    """

    transitions = []

    for _, row in variance_df.iterrows():

        entity = {
            key: row[key]
            for key in key_columns
        }

        for metric in numerical_columns:

            previous_column = f"{metric}_previous"
            current_column = f"{metric}_current"

            previous_value = row[previous_column]
            current_value = row[current_column]

            if pd.isna(previous_value) or pd.isna(current_value):
                continue

            if previous_value == 0 and current_value != 0:

                transitions.append(
                    {
                        "entity": entity,
                        "metric": metric,
                        "previous_value": 0,
                        "current_value": float(
                            current_value
                        ),
                        "transition": "started",
                    }
                )

            elif previous_value != 0 and current_value == 0:

                transitions.append(
                    {
                        "entity": entity,
                        "metric": metric,
                        "previous_value": float(
                            previous_value
                        ),
                        "current_value": 0,
                        "transition": "dropped_to_zero",
                    }
                )

    return transitions