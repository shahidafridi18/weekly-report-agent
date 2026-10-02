import pandas as pd


def calculate_contributions(
    variance_df: pd.DataFrame,
    numerical_columns: list[str],
    key_columns: list[str],
) -> dict:
    """
    Calculate how much each matched entity contributed
    to the net movement of each metric.

    This function only considers entities present
    in both periods.
    """

    results = {}

    for metric in numerical_columns:

        change_column = f"{metric}_change"

        if change_column not in variance_df.columns:
            continue

        total_matched_change = variance_df[
            change_column
        ].sum()

        contributions = []

        for _, row in variance_df.iterrows():

            entity = {
                key: row[key]
                for key in key_columns
            }

            absolute_change = row[change_column]

            if total_matched_change != 0:
                contribution_pct = (
                    absolute_change
                    / total_matched_change
                    * 100
                )
            else:
                contribution_pct = None

            contributions.append(
                {
                    "entity": entity,
                    "absolute_change": float(
                        absolute_change
                    ),
                    "contribution_to_net_change_pct": (
                        round(float(contribution_pct), 2)
                        if contribution_pct is not None
                        else None
                    ),
                }
            )

        contributions.sort(
            key=lambda item: abs(
                item["absolute_change"]
            ),
            reverse=True,
        )

        results[metric] = {
            "matched_entities_net_change": float(
                total_matched_change
            ),
            "contributors": contributions,
        }

    return results

def calculate_movement_bridge(
    previous_df: pd.DataFrame,
    current_df: pd.DataFrame,
    categories: dict[str, pd.DataFrame],
    numerical_columns: list[str],
) -> dict:
    """
    Explain total metric movement through:

    1. Matched entities
    2. New entities
    3. Removed entities
    """

    bridge = {}

    matched_df = categories["matched"]
    new_df = categories["new"]
    removed_df = categories["removed"]

    for metric in numerical_columns:

        previous_column = f"{metric}_previous"
        current_column = f"{metric}_current"

        matched_change = (
            matched_df[current_column].sum()
            - matched_df[previous_column].sum()
        )

        new_entity_impact = (
            new_df[current_column].sum()
            if current_column in new_df.columns
            else 0
        )

        removed_entity_impact = (
            -removed_df[previous_column].sum()
            if previous_column in removed_df.columns
            else 0
        )

        explained_change = (
            matched_change
            + new_entity_impact
            + removed_entity_impact
        )

        actual_change = (
            current_df[metric].sum()
            - previous_df[metric].sum()
        )

        bridge[metric] = {
            "matched_entity_change": float(
                matched_change
            ),
            "new_entity_impact": float(
                new_entity_impact
            ),
            "removed_entity_impact": float(
                removed_entity_impact
            ),
            "explained_change": float(
                explained_change
            ),
            "actual_total_change": float(
                actual_change
            ),
        }

    return bridge