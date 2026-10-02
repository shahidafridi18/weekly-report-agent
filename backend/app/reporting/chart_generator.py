from pathlib import Path

import matplotlib.pyplot as plt


def generate_kpi_change_chart(
    metric_summary: dict,
    output_path: str | Path,
) -> Path:
    """
    Generate percentage change chart for all KPIs.
    """

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    metrics = []
    changes = []

    for metric, values in metric_summary.items():
        percentage_change = values.get("percentage_change")

        if percentage_change is None:
            continue

        metrics.append(metric)
        changes.append(percentage_change)

    if not metrics:
        raise ValueError(
            "No KPI percentage changes available."
        )

    fig, ax = plt.subplots(figsize=(10, 5))

    bars = ax.bar(
        metrics,
        changes,
    )

    ax.axhline(
        0,
        linewidth=1,
    )

    ax.set_title(
        "Week-over-Week KPI Change",
        fontsize=14,
        fontweight="bold",
    )

    ax.set_ylabel("Change (%)")

    ax.set_xlabel("")

    ax.tick_params(
        axis="x",
        rotation=25,
    )

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    for bar, value in zip(bars, changes):
        y_position = (
            value + 0.5
            if value >= 0
            else value - 0.5
        )

        vertical_alignment = (
            "bottom"
            if value >= 0
            else "top"
        )

        ax.text(
            bar.get_x() + bar.get_width() / 2,
            y_position,
            f"{value:+.2f}%",
            ha="center",
            va=vertical_alignment,
            fontsize=9,
        )

    fig.tight_layout()

    fig.savefig(
        output_path,
        dpi=160,
        bbox_inches="tight",
    )

    plt.close(fig)

    return output_path


def generate_movement_bridge_chart(
    movement_bridge: dict,
    output_path: str | Path,
    metric: str | None = None,
) -> Path | None:
    """
    Show how matched, new and removed entities explain
    the total change for one KPI.
    """

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if not movement_bridge:
        return None

    if metric is None:
        metric = next(
            iter(movement_bridge),
            None,
        )

    if not metric or metric not in movement_bridge:
        return None

    values = movement_bridge[metric]

    labels = [
        "Matched\nEntities",
        "New\nEntities",
        "Removed\nEntities",
        "Total\nChange",
    ]

    amounts = [
        values.get(
            "matched_entity_change",
            0,
        ),
        values.get(
            "new_entity_impact",
            0,
        ),
        values.get(
            "removed_entity_impact",
            0,
        ),
        values.get(
            "actual_total_change",
            0,
        ),
    ]

    fig, ax = plt.subplots(
        figsize=(9, 5)
    )

    bars = ax.bar(
        labels,
        amounts,
    )

    ax.axhline(
        0,
        linewidth=1,
    )

    ax.set_title(
        f"{metric} Movement Bridge",
        fontsize=14,
        fontweight="bold",
    )

    ax.set_ylabel(metric)

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    for bar, value in zip(
        bars,
        amounts,
    ):
        offset = max(
            abs(value) * 0.03,
            1,
        )

        y_position = (
            value + offset
            if value >= 0
            else value - offset
        )

        vertical_alignment = (
            "bottom"
            if value >= 0
            else "top"
        )

        ax.text(
            bar.get_x()
            + bar.get_width() / 2,
            y_position,
            f"{value:+,.0f}",
            ha="center",
            va=vertical_alignment,
            fontsize=9,
        )

    fig.tight_layout()

    fig.savefig(
        output_path,
        dpi=160,
        bbox_inches="tight",
    )

    plt.close(fig)

    return output_path