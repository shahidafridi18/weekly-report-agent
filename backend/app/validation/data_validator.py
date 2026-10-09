import pandas as pd

from app.schema import (
    COUNTERPARTY_KEY_COLUMNS,
    COUNTERPARTY_METRIC_COLUMNS,
)


def validate_columns(
    previous_df: pd.DataFrame,
    current_df: pd.DataFrame,
    key_columns: list[str] | None = None,
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

    key_columns = key_columns or []
    missing_keys = {
        "previous": sorted(
            set(key_columns) - previous_columns
        ),
        "current": sorted(
            set(key_columns) - current_columns
        ),
    }

    blank_key_rows = {
        "previous": 0,
        "current": 0,
    }
    duplicate_key_rows = {
        "previous": 0,
        "current": 0,
    }
    if key_columns and not any(missing_keys.values()):
        for period, df in (
            ("previous", previous_df),
            ("current", current_df),
        ):
            blank_mask = df[key_columns].isna().any(axis="columns")
            for column in key_columns:
                blank_mask |= (
                    df[column]
                    .astype("string")
                    .str.strip()
                    .eq("")
                    .fillna(False)
                )
            blank_key_rows[period] = int(blank_mask.sum())
            duplicate_key_rows[period] = int(
                df.loc[~blank_mask].duplicated(
                    subset=key_columns,
                    keep=False,
                ).sum()
            )

    counterparty_workbook = bool(
        set(COUNTERPARTY_KEY_COLUMNS)
        & (previous_columns | current_columns)
    )
    missing_metrics = {
        "previous": sorted(
            set(COUNTERPARTY_METRIC_COLUMNS) - previous_columns
        ) if counterparty_workbook else [],
        "current": sorted(
            set(COUNTERPARTY_METRIC_COLUMNS) - current_columns
        ) if counterparty_workbook else [],
    }

    valid = (
        not missing_columns
        and not new_columns
        and not any(missing_keys.values())
        and not any(blank_key_rows.values())
        and not any(duplicate_key_rows.values())
        and not any(missing_metrics.values())
    )

    return {
        "valid": valid,
        "missing_columns": missing_columns,
        "new_columns": new_columns,
        "common_columns": common_columns,
        "missing_key_columns": missing_keys,
        "blank_key_rows": blank_key_rows,
        "duplicate_key_rows": duplicate_key_rows,
        "missing_metric_columns": missing_metrics,
    }