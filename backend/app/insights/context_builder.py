def build_insight_context(
    analysis: dict,
) -> dict:
    """
    Build a compact factual context for the LLM.

    The LLM receives calculated analytical facts,
    not raw Excel data.
    """

    return {
        "row_summary": analysis.get(
            "row_summary",
            {},
        ),

        "metric_summary": analysis.get(
            "metric_summary",
            {},
        ),

        "major_movements": analysis.get(
            "major_movements",
            [],
        )[:20],

        "movement_bridge": analysis.get(
            "movement_bridge",
            {},
        ),

        "new_entities": analysis.get(
            "new_entities",
            [],
        )[:10],

        "removed_entities": analysis.get(
            "removed_entities",
            [],
        )[:10],

        "zero_transitions": analysis.get(
            "zero_transitions",
            [],
        )[:10],
    }