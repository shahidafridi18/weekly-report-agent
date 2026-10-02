import pandas as pd

from app.processing.serializer import make_json_safe


def format_new_entities(
    new_df: pd.DataFrame,
    key_columns: list[str],
    numerical_columns: list[str],
) -> list[dict]:
    """
    Convert new rows into a clean business-friendly format.
    """

    entities = []

    for _, row in new_df.iterrows():

        entity = {
            key: make_json_safe(row[key])
            for key in key_columns
        }

        values = {}

        for metric in numerical_columns:

            current_column = f"{metric}_current"

            if current_column in row.index:
                values[metric] = make_json_safe(
                    row[current_column]
                )

        entities.append(
            {
                "entity": entity,
                "values": values,
            }
        )

    return entities


def format_removed_entities(
    removed_df: pd.DataFrame,
    key_columns: list[str],
    numerical_columns: list[str],
) -> list[dict]:
    """
    Convert removed rows into a clean business-friendly format.
    """

    entities = []

    for _, row in removed_df.iterrows():

        entity = {
            key: make_json_safe(row[key])
            for key in key_columns
        }

        previous_values = {}

        for metric in numerical_columns:

            previous_column = f"{metric}_previous"

            if previous_column in row.index:
                previous_values[metric] = make_json_safe(
                    row[previous_column]
                )

        entities.append(
            {
                "entity": entity,
                "previous_values": previous_values,
            }
        )

    return entities