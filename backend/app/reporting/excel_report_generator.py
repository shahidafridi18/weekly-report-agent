from pathlib import Path

from openpyxl import Workbook, load_workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter


NUMBER_FORMAT = '#,##0.00;[Red](#,##0.00);-'
PERCENT_FORMAT = '+0.00%;-0.00%;-'
HEADER_FILL = PatternFill("solid", fgColor="334155")
HEADER_FONT = Font(bold=True, color="FFFFFF")
HEADER_BORDER = Border(
    bottom=Side(style="thin", color="1F2937")
)
INSIGHT_HEADER_FILL = PatternFill("solid", fgColor="1E40AF")
INSIGHT_CONTENT_FILL = PatternFill("solid", fgColor="EFF6FF")


def _safe_cell_value(value):
    if isinstance(value, str) and value[:1] in ("=", "+", "-", "@"):
        return f"'{value}"
    return value


def _write_table(
    workbook: Workbook,
    title: str,
    headers: list[str],
    rows: list[list],
    widths: list[int] | None = None,
    percentage_columns: set[int] | None = None,
) -> None:
    worksheet = workbook.create_sheet(title)
    worksheet.append(headers)

    for row in rows:
        worksheet.append([_safe_cell_value(value) for value in row])

    worksheet.freeze_panes = "A2"
    worksheet.auto_filter.ref = worksheet.dimensions
    worksheet.sheet_view.showGridLines = False

    for cell in worksheet[1]:
        cell.fill = HEADER_FILL
        cell.font = HEADER_FONT
        cell.border = HEADER_BORDER
        cell.alignment = Alignment(vertical="center", wrap_text=True)
    worksheet.row_dimensions[1].height = 30

    for column_index in range(1, len(headers) + 1):
        if widths and column_index <= len(widths):
            width = widths[column_index - 1]
        else:
            width = min(
                max(
                    len(str(headers[column_index - 1])) + 2,
                    max(
                        (
                            len(str(worksheet.cell(row, column_index).value or ""))
                            for row in range(2, min(worksheet.max_row, 52) + 1)
                        ),
                        default=10,
                    ) + 2,
                ),
                42,
            )
        worksheet.column_dimensions[get_column_letter(column_index)].width = width

    percentage_columns = percentage_columns or set()
    for row in worksheet.iter_rows(min_row=2):
        for cell in row:
            if isinstance(cell.value, (int, float)):
                cell.number_format = (
                    PERCENT_FORMAT
                    if cell.column in percentage_columns
                    else NUMBER_FORMAT
                )


def _write_ai_insights(
    workbook: Workbook,
    ai_insights: str,
) -> None:
    """
    Create a dedicated sheet for AI insights
    with improved formatting and styling.
    """
    worksheet = workbook.create_sheet("AI Insights")
    worksheet.sheet_view.showGridLines = False
    
    # Add title
    worksheet.merge_cells("A1:B1")
    title_cell = worksheet["A1"]
    title_cell.value = "AI-Generated Business Insights"
    title_cell.font = Font(bold=True, color="FFFFFF", size=12)
    title_cell.fill = INSIGHT_HEADER_FILL
    title_cell.alignment = Alignment(
        vertical="center",
        horizontal="center",
        wrap_text=True
    )
    worksheet.row_dimensions[1].height = 28
    
    worksheet.append([])  # Empty row for spacing
    
    # Split insights by paragraphs and write them
    paragraphs = [
        para.strip() 
        for para in ai_insights.split("\n\n") 
        if para.strip()
    ]
    
    if not paragraphs:
        # Fallback: split by single newlines
        paragraphs = [
            line.strip() 
            for line in ai_insights.split("\n") 
            if line.strip()
        ]
    
    # Write each paragraph/insight
    for paragraph in paragraphs:
        row_num = worksheet.max_row + 1
        worksheet.merge_cells(f"A{row_num}:B{row_num}")
        
        cell = worksheet[f"A{row_num}"]
        cell.value = paragraph
        cell.font = Font(size=11, color="1F2937")
        cell.fill = INSIGHT_CONTENT_FILL
        cell.alignment = Alignment(
            vertical="top",
            horizontal="left",
            wrap_text=True
        )
        
        # Calculate appropriate row height based on text length
        lines = len(paragraph) // 80 + 1
        worksheet.row_dimensions[row_num].height = max(30, 20 * lines)
        
        # Add spacing row
        worksheet.append([])
    
    # Set column widths
    worksheet.column_dimensions["A"].width = 120
    worksheet.column_dimensions["B"].width = 2


def generate_weekly_report_excel(
    analysis: dict,
    output_path: str | Path,
    previous_file_name: str,
    current_file_name: str,
    ai_insights: str | None = None,
) -> Path:
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Load existing workbook if it exists, otherwise create new one
    if output_path.exists():
        workbook = load_workbook(output_path)
        # Remove AI Insights sheet if it exists (will be recreated with new data)
        if "AI Insights" in workbook.sheetnames:
            workbook.remove(workbook["AI Insights"])
        # Skip recreating analysis sheets if they already exist
        # Just update AI Insights and save
        if ai_insights:
            _write_ai_insights(workbook, ai_insights)
        workbook.save(output_path)
        return output_path
    
    # Create new workbook if file doesn't exist
    workbook = Workbook()
    workbook.remove(workbook.active)

    columns = analysis.get("columns", {})
    key_columns = columns.get("key_columns", [])
    metric_columns = columns.get("numerical_columns", [])
    row_summary = analysis.get("row_summary", {})

    summary = workbook.create_sheet("Summary")
    summary.sheet_view.showGridLines = False
    summary.merge_cells("A1:F1")
    summary["A1"] = "Weekly Business Comparison Report"
    summary["A1"].font = Font(bold=True, color="FFFFFF", size=15)
    summary["A1"].fill = HEADER_FILL
    summary["A1"].alignment = Alignment(vertical="center")
    summary.row_dimensions[1].height = 32
    summary.append([])
    summary.append(["Previous file", previous_file_name])
    summary.append(["Current file", current_file_name])
    summary.append(["Matching keys", ", ".join(key_columns)])
    summary.append([])
    summary.append(["Previous rows", "Current rows", "Matched", "New", "Removed"])
    summary.append(
        [
            row_summary.get("previous_rows", 0),
            row_summary.get("current_rows", 0),
            row_summary.get("matched_rows", 0),
            row_summary.get("new_rows", 0),
            row_summary.get("removed_rows", 0),
        ]
    )
    for cell in summary[7]:
        cell.fill = HEADER_FILL
        cell.font = HEADER_FONT
    for column, width in {"A": 28, "B": 42, "C": 16, "D": 16, "E": 16, "F": 16}.items():
        summary.column_dimensions[column].width = width

    # Add AI Insights sheet right after Summary for visibility
    if ai_insights:
        _write_ai_insights(
            workbook,
            ai_insights,
        )

    metric_summary = analysis.get("metric_summary", {})
    _write_table(
        workbook,
        "Metric Summary",
        ["Metric", "Previous", "Current", "Change", "Change %", "Direction"],
        [
            [
                metric,
                values.get("previous_total"),
                values.get("current_total"),
                values.get("absolute_change"),
                (values["percentage_change"] / 100)
                if values.get("percentage_change") is not None
                else None,
                values.get("direction", "").title(),
            ]
            for metric, values in metric_summary.items()
        ],
        widths=[38, 16, 16, 16, 14, 16],
        percentage_columns={5},
    )

    movement_bridge = analysis.get("movement_bridge", {})
    _write_table(
        workbook,
        "Movement Bridge",
        ["Metric", "Matched change", "New impact", "Removed impact", "Explained change", "Actual change"],
        [
            [
                metric,
                values.get("matched_entity_change"),
                values.get("new_entity_impact"),
                values.get("removed_entity_impact"),
                values.get("explained_change"),
                values.get("actual_total_change"),
            ]
            for metric, values in movement_bridge.items()
        ],
        widths=[38, 18, 16, 18, 18, 16],
    )

    variance_headers = [*key_columns, "Metric", "Previous", "Current", "Change", "Change %"]
    variance_rows = []
    for record in analysis.get("variance_data", []):
        entity = [record.get(key) for key in key_columns]
        for metric in metric_columns:
            percentage = record.get(f"{metric}_change_pct")
            variance_rows.append(
                entity
                + [
                    metric,
                    record.get(f"{metric}_previous"),
                    record.get(f"{metric}_current"),
                    record.get(f"{metric}_change"),
                    (percentage / 100) if percentage is not None else None,
                ]
            )
    _write_table(
        workbook,
        "Entity Variances",
        variance_headers,
        variance_rows,
        widths=[22] * len(key_columns) + [38, 16, 16, 16, 14],
        percentage_columns={len(variance_headers)},
    )

    new_headers = [*key_columns, "Metric", "Current value"]
    new_rows = [
        [item.get("entity", {}).get(key) for key in key_columns]
        + [metric, value]
        for item in analysis.get("new_entities", [])
        for metric, value in item.get("values", {}).items()
    ]
    _write_table(
        workbook,
        "New Entities",
        new_headers,
        new_rows,
        widths=[22] * len(key_columns) + [38, 18],
    )

    removed_headers = [*key_columns, "Metric", "Previous value"]
    removed_rows = [
        [item.get("entity", {}).get(key) for key in key_columns]
        + [metric, value]
        for item in analysis.get("removed_entities", [])
        for metric, value in item.get("previous_values", {}).items()
    ]
    _write_table(
        workbook,
        "Removed Entities",
        removed_headers,
        removed_rows,
        widths=[22] * len(key_columns) + [38, 18],
    )

    movement_headers = [*key_columns, "Metric", "Previous", "Current", "Change", "Change %", "Direction"]
    movement_rows = [
        [item.get("entity", {}).get(key) for key in key_columns]
        + [
            item.get("metric"),
            item.get("previous_value"),
            item.get("current_value"),
            item.get("absolute_change"),
            (item["percentage_change"] / 100)
            if item.get("percentage_change") is not None
            else None,
            item.get("direction"),
        ]
        for item in analysis.get("major_movements", [])
    ]
    _write_table(
        workbook,
        "Major Movements",
        movement_headers,
        movement_rows,
        widths=[22] * len(key_columns) + [38, 16, 16, 16, 14, 16],
        percentage_columns={len(movement_headers) - 1},
    )

    transition_headers = [*key_columns, "Metric", "Previous", "Current", "Transition"]
    transition_rows = [
        [item.get("entity", {}).get(key) for key in key_columns]
        + [
            item.get("metric"),
            item.get("previous_value"),
            item.get("current_value"),
            item.get("transition"),
        ]
        for item in analysis.get("zero_transitions", [])
    ]
    _write_table(
        workbook,
        "Zero Transitions",
        transition_headers,
        transition_rows,
        widths=[22] * len(key_columns) + [38, 16, 16, 20],
    )

    workbook.save(output_path)
    return output_path