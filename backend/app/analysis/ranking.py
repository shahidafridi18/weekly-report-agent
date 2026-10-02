import pandas as pd


def rank_movements(
    variance_df: pd.DataFrame,
    numerical_columns: list[str],
    key_columns: list[str],
    top_n: int = 5,
) -> dict:
    """
    Find the largest absolute increases and decreases
    for each numerical metric.
    """

    rankings = {}

    for metric in numerical_columns:

        change_column = f"{metric}_change"

        if change_column not in variance_df.columns:
            continue

        columns = (
            key_columns
            + [
                f"{metric}_previous",
                f"{metric}_current",
                change_column,
                f"{metric}_change_pct",
            ]
        )

        metric_df = variance_df[columns].copy()

        gainers = (
            metric_df[
                metric_df[change_column] > 0
            ]
            .sort_values(
                by=change_column,
                ascending=False,
            )
            .head(top_n)
        )

        decliners = (
            metric_df[
                metric_df[change_column] < 0
            ]
            .sort_values(
                by=change_column,
                ascending=True,
            )
            .head(top_n)
        )

        rankings[metric] = {
            "top_gainers": gainers.to_dict(
                orient="records"
            ),
            "top_decliners": decliners.to_dict(
                orient="records"
            ),
        }

    return rankings