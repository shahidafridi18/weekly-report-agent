import pandas as pd

from app.analysis.aggregation import calculate_metric_summary
from app.analysis.contribution import (
    calculate_contributions,
    calculate_movement_bridge,
)
from app.analysis.movements import detect_major_movements
from app.analysis.ranking import rank_movements
from app.analysis.transitions import detect_zero_transitions
from app.analysis.variance import calculate_variances
from app.processing.matcher import categorize_rows, match_rows
from app.processing.normalizer import classify_columns
from app.validation.data_validator import validate_columns
from app.processing.serializer import dataframe_to_records
from app.analysis.entities import (
    format_new_entities,
    format_removed_entities,
)

def run_analysis(
    previous_df: pd.DataFrame,
    current_df: pd.DataFrame,
    key_columns: list[str],
    movement_threshold_pct: float = 20.0,
    minimum_absolute_change: float = 0.0,
) -> dict:
    """
    Run the complete week-over-week analysis pipeline.
    """

    # 1. Validate schemas
    validation = validate_columns(
        previous_df,
        current_df,
    )

    if not validation["valid"]:
        raise ValueError(
            "The weekly datasets do not have matching schemas."
        )

    # 2. Identify numerical columns
    classification = classify_columns(previous_df)

    numerical_columns = classification[
        "numerical_columns"
    ]

    # 3. Match rows
    merged_df = match_rows(
        previous_df,
        current_df,
        key_columns,
    )

    categories = categorize_rows(merged_df)

    # 4. Calculate row-level variances
    variance_df = calculate_variances(
        categories["matched"],
        numerical_columns,
    )

    # 5. Overall KPI analysis
    metric_summary = calculate_metric_summary(
        previous_df,
        current_df,
        numerical_columns,
    )

    # 6. Significant movements
    major_movements = detect_major_movements(
        variance_df,
        numerical_columns,
        key_columns,
        movement_threshold_pct,
        minimum_absolute_change,
    )

    # 7. Rankings
    rankings = rank_movements(
        variance_df,
        numerical_columns,
        key_columns,
    )

    # 8. Contribution analysis
    contributions = calculate_contributions(
        variance_df,
        numerical_columns,
        key_columns,
    )

    # 9. Reconcile total movement
    movement_bridge = calculate_movement_bridge(
        previous_df,
        current_df,
        categories,
        numerical_columns,
    )

    # 10. Detect zero transitions
    zero_transitions = detect_zero_transitions(
        variance_df,
        numerical_columns,
        key_columns,
    )

    new_entities = format_new_entities(
    categories["new"],
    key_columns,
    numerical_columns,
    )

    removed_entities = format_removed_entities(
    categories["removed"],
    key_columns,
    numerical_columns,
)



    return {
        "validation": validation,

        "columns": {
            "key_columns": key_columns,
            "numerical_columns": numerical_columns,
            "non_numerical_columns": classification[
                "non_numerical_columns"
            ],
        },

        "row_summary": {
            "previous_rows": len(previous_df),
            "current_rows": len(current_df),
            "matched_rows": len(categories["matched"]),
            "new_rows": len(categories["new"]),
            "removed_rows": len(categories["removed"]),
        },

        "metric_summary": metric_summary,

        "major_movements": major_movements,

        "rankings": rankings,

        "contributions": contributions,

        "movement_bridge": movement_bridge,

        "zero_transitions": zero_transitions,

        # Internal DataFrames for now
"variance_data": dataframe_to_records(
    variance_df
),

"new_entities": new_entities,

"removed_entities": removed_entities,

}