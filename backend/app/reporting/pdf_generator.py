from __future__ import annotations

from datetime import datetime
from html import escape
from pathlib import Path
from typing import Any

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    Image,
    KeepTogether,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

# FCCR-inspired visual system. It borrows the compact hierarchy, classification
# strip, metadata grids, section bars and repeated footer, but is adapted to a
# weekly AI comparison report rather than reproducing the source report.
NAVY = colors.HexColor("#24364B")
BLUE = colors.HexColor("#315F8C")
MID_BLUE = colors.HexColor("#DCE8F2")
PALE_BLUE = colors.HexColor("#F3F7FA")
LIGHT_GREY = colors.HexColor("#F2F2F2")
MID_GREY = colors.HexColor("#D4D8DC")
DARK_GREY = colors.HexColor("#495057")
TEXT = colors.HexColor("#20252A")
GREEN = colors.HexColor("#2E7D32")
RED = colors.HexColor("#B3261E")
AMBER = colors.HexColor("#B26A00")
WHITE = colors.white


def format_number(value: Any) -> str:
    if value is None:
        return "N/A"
    try:
        return f"{float(value):,.2f}"
    except (TypeError, ValueError):
        return str(value)


def format_percentage(value: Any) -> str:
    if value is None:
        return "N/A"
    try:
        return f"{float(value):+.2f}%"
    except (TypeError, ValueError):
        return str(value)


def format_entity(entity: dict) -> str:
    return ", ".join(f"{key}: {value}" for key, value in entity.items()) or "N/A"


def _p(text: Any, style: ParagraphStyle) -> Paragraph:
    return Paragraph(escape(str(text or "")), style)


def _direction_color(direction: str):
    value = (direction or "").strip().lower()
    if value in {"increase", "increased", "up", "positive"}:
        return GREEN
    if value in {"decrease", "decreased", "down", "negative"}:
        return RED
    return DARK_GREY


def _table_style(header=True, numeric_from: int | None = None) -> TableStyle:
    commands = [
        ("GRID", (0, 0), (-1, -1), 0.35, MID_GREY),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("ROWBACKGROUNDS", (0, 1 if header else 0), (-1, -1), [WHITE, PALE_BLUE]),
    ]
    if header:
        commands += [
            ("BACKGROUND", (0, 0), (-1, 0), NAVY),
            ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("ALIGN", (0, 0), (-1, 0), "CENTER"),
        ]
    if numeric_from is not None:
        commands.append(("ALIGN", (numeric_from, 1 if header else 0), (-1, -1), "RIGHT"))
    return TableStyle(commands)


def _section_bar(title: str, styles: dict[str, ParagraphStyle]) -> Table:
    table = Table([[_p(title, styles["section_bar"]) ]], colWidths=[180 * mm])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), NAVY),
        ("BOX", (0, 0), (-1, -1), 0.5, NAVY),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    return table


def _classification_header_footer(canvas, doc):
    canvas.saveState()
    width, height = doc.pagesize

    # Top classification line, inspired by the reference report.
    canvas.setFillColor(NAVY)
    canvas.rect(doc.leftMargin, height - 19 * mm, doc.width, 5.5 * mm, fill=1, stroke=0)
    canvas.setFillColor(WHITE)
    canvas.setFont("Helvetica-Bold", 8)
    canvas.drawString(doc.leftMargin + 3 * mm, height - 17.1 * mm, "C2 - CONFIDENTIAL")
    canvas.drawRightString(width - doc.rightMargin - 3 * mm, height - 17.1 * mm, "WEEKLY AI COMPARISON REPORT")

    # Footer follows the source pattern: classification, page count, timestamp.
    footer_y = 10 * mm
    canvas.setStrokeColor(MID_GREY)
    canvas.setLineWidth(0.4)
    canvas.line(doc.leftMargin, footer_y + 4 * mm, width - doc.rightMargin, footer_y + 4 * mm)
    canvas.setFillColor(DARK_GREY)
    canvas.setFont("Helvetica", 7.5)
    canvas.drawString(doc.leftMargin, footer_y, "C2 - CONFIDENTIAL")
    canvas.drawCentredString(width / 2, footer_y, f"Page {doc.page}")
    canvas.drawRightString(
        width - doc.rightMargin,
        footer_y,
        f"Generated on {datetime.now().strftime('%Y-%m-%d %H:%M')}",
    )
    canvas.restoreState()


def _styles() -> dict[str, ParagraphStyle]:
    base = getSampleStyleSheet()
    return {
        "title": ParagraphStyle(
            "Title", parent=base["Title"], fontName="Helvetica-Bold",
            fontSize=18, leading=22, textColor=NAVY, alignment=TA_LEFT,
            spaceAfter=5,
        ),
        "subtitle": ParagraphStyle(
            "Subtitle", parent=base["Normal"], fontSize=8.5, leading=11,
            textColor=DARK_GREY, alignment=TA_LEFT,
        ),
        "section_bar": ParagraphStyle(
            "SectionBar", parent=base["Normal"], fontName="Helvetica-Bold",
            fontSize=9.5, leading=11, textColor=WHITE,
        ),
        "subheading": ParagraphStyle(
            "Subheading", parent=base["Heading3"], fontName="Helvetica-Bold",
            fontSize=10, leading=12, textColor=BLUE, spaceBefore=7, spaceAfter=5,
        ),
        "body": ParagraphStyle(
            "Body", parent=base["BodyText"], fontSize=8.5, leading=11.5,
            textColor=TEXT, spaceAfter=4,
        ),
        "small": ParagraphStyle(
            "Small", parent=base["BodyText"], fontSize=7.4, leading=9.2,
            textColor=TEXT,
        ),
        "small_center": ParagraphStyle(
            "SmallCenter", parent=base["BodyText"], fontSize=7.4, leading=9.2,
            textColor=TEXT, alignment=TA_CENTER,
        ),
        "small_right": ParagraphStyle(
            "SmallRight", parent=base["BodyText"], fontSize=7.4, leading=9.2,
            textColor=TEXT, alignment=TA_RIGHT,
        ),
        "label": ParagraphStyle(
            "Label", parent=base["BodyText"], fontName="Helvetica-Bold",
            fontSize=7.5, leading=9, textColor=NAVY,
        ),
        "value": ParagraphStyle(
            "Value", parent=base["BodyText"], fontSize=7.5, leading=9,
            textColor=TEXT,
        ),
        "insight": ParagraphStyle(
            "Insight", parent=base["BodyText"], fontSize=8.5, leading=12,
            textColor=TEXT, leftIndent=9, firstLineIndent=-6, spaceAfter=4,
        ),
    }


def _metadata_grid(analysis, previous_file_name, current_file_name, styles):
    columns = analysis.get("columns", {})
    key_columns = ", ".join(columns.get("key_columns", [])) or "N/A"
    numerical_columns = ", ".join(columns.get("numerical_columns", [])) or "N/A"
    rows = [
        [_p("Report type", styles["label"]), _p("Week-over-week business comparison", styles["value"]),
         _p("Status", styles["label"]), _p("Generated", styles["value"])],
        [_p("Previous source", styles["label"]), _p(previous_file_name, styles["value"]),
         _p("Current source", styles["label"]), _p(current_file_name, styles["value"])],
        [_p("Matching key(s)", styles["label"]), _p(key_columns, styles["value"]),
         _p("KPI field(s)", styles["label"]), _p(numerical_columns, styles["value"])],
    ]
    table = Table(rows, colWidths=[29 * mm, 61 * mm, 29 * mm, 61 * mm])
    table.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.4, MID_GREY),
        ("BACKGROUND", (0, 0), (0, -1), MID_BLUE),
        ("BACKGROUND", (2, 0), (2, -1), MID_BLUE),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    return table


def _add_ai_insights(story, ai_insights: str, styles):
    for raw in ai_insights.splitlines():
        line = raw.strip()
        if not line:
            story.append(Spacer(1, 2.5 * mm))
        elif line.startswith("## "):
            story.append(_p(line[3:].replace("**", ""), styles["subheading"]))
        elif line.startswith("# "):
            story.append(_p(line[2:].replace("**", ""), styles["subheading"]))
        elif line.startswith("- "):
            story.append(Paragraph(f"&#8226;&nbsp;&nbsp;{escape(line[2:].replace('**', ''))}", styles["insight"]))
        else:
            story.append(_p(line.replace("**", ""), styles["body"]))


def generate_weekly_report_pdf(
    analysis: dict,
    ai_insights: str | None,
    chart_path: str | Path | None,
    output_path: str | Path,
    previous_file_name: str,
    current_file_name: str,
    movement_bridge_chart_path: str | Path | None = None,
) -> Path:
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    chart_path = Path(chart_path) if chart_path else None
    bridge_chart = Path(movement_bridge_chart_path) if movement_bridge_chart_path else None
    styles = _styles()

    document = SimpleDocTemplate(
        str(output_path), pagesize=A4,
        leftMargin=15 * mm, rightMargin=15 * mm,
        topMargin=25 * mm, bottomMargin=18 * mm,
        title="Weekly AI Comparison Report",
        author="Weekly Report Analysis Agent",
    )
    story = []

    # 1. Compact identity area, replacing the FCCR third-party identity block.
    story.append(_p("Weekly Business Comparison Report", styles["title"]))
    story.append(_p(
        "AI-assisted comparison of source files, KPI movements, entity changes and management insights.",
        styles["subtitle"],
    ))
    story.append(Spacer(1, 4 * mm))
    story.append(_metadata_grid(analysis, previous_file_name, current_file_name, styles))
    story.append(Spacer(1, 5 * mm))

    # 2. Rating-result-style executive result panel.
    story.append(_section_bar("Comparison Result", styles))
    row_summary = analysis.get("row_summary", {})
    overview = [
        ["Previous rows", "Current rows", "Matched", "New", "Removed"],
        [
            row_summary.get("previous_rows", 0), row_summary.get("current_rows", 0),
            row_summary.get("matched_rows", 0), row_summary.get("new_rows", 0),
            row_summary.get("removed_rows", 0),
        ],
    ]
    overview_table = Table(overview, colWidths=[36 * mm] * 5)
    overview_table.setStyle(_table_style(header=True))
    story += [Spacer(1, 2 * mm), overview_table, Spacer(1, 5 * mm)]

    # 3. KPI table mirrors the source report's dense risk-factor grid.
    story.append(_section_bar("KPI Performance", styles))
    metric_data = [["Metric", "Previous", "Current", "Change", "Change %", "Direction"]]
    directions = []
    for i, (metric, values) in enumerate(analysis.get("metric_summary", {}).items(), start=1):
        direction = str(values.get("direction", "")).title()
        directions.append((i, _direction_color(direction)))
        metric_data.append([
            _p(metric, styles["small"]), format_number(values.get("previous_total")),
            format_number(values.get("current_total")), format_number(values.get("absolute_change")),
            format_percentage(values.get("percentage_change")), direction,
        ])
    metric_table = Table(metric_data, repeatRows=1, colWidths=[48*mm, 27*mm, 27*mm, 27*mm, 24*mm, 27*mm])
    metric_style = _table_style(header=True, numeric_from=1)
    metric_style.add("ALIGN", (-1, 1), (-1, -1), "CENTER")
    for row, color in directions:
        metric_style.add("TEXTCOLOR", (-1, row), (-1, row), color)
        metric_style.add("FONTNAME", (-1, row), (-1, row), "Helvetica-Bold")
    metric_table.setStyle(metric_style)
    story += [Spacer(1, 2 * mm), metric_table]

    if chart_path and chart_path.exists():
        story += [Spacer(1, 4 * mm), KeepTogether([
            _p("KPI Change Chart", styles["subheading"]),
            Image(str(chart_path), width=170 * mm, height=92 * mm),
        ])]

    story.append(PageBreak())
    story.append(_section_bar("Movement Bridge", styles))
    story.append(Spacer(1, 2 * mm))
    story.append(_p(
        "Reconciliation of total KPI change across continuing, new and removed entities.",
        styles["body"],
    ))
    bridge_data = [["Metric", "Matched change", "New impact", "Removed impact", "Explained", "Actual"]]
    for metric, values in analysis.get("movement_bridge", {}).items():
        bridge_data.append([
            _p(metric, styles["small"]), format_number(values.get("matched_entity_change")),
            format_number(values.get("new_entity_impact")), format_number(values.get("removed_entity_impact")),
            format_number(values.get("explained_change")), format_number(values.get("actual_total_change")),
        ])
    bridge_table = Table(bridge_data, repeatRows=1, colWidths=[48*mm, 28*mm, 25*mm, 28*mm, 26*mm, 25*mm])
    bridge_table.setStyle(_table_style(header=True, numeric_from=1))
    story.append(bridge_table)
    if bridge_chart and bridge_chart.exists():
        story += [Spacer(1, 4 * mm), Image(str(bridge_chart), width=170 * mm, height=80 * mm)]

    story += [Spacer(1, 5 * mm), _section_bar("Major Movements", styles), Spacer(1, 2 * mm)]
    movements = analysis.get("major_movements", [])
    if movements:
        movement_data = [["Entity", "Metric", "Previous", "Current", "Change", "Change %"]]
        for item in movements[:30]:
            movement_data.append([
                _p(format_entity(item.get("entity", {})), styles["small"]),
                _p(item.get("metric", ""), styles["small"]),
                format_number(item.get("previous_value")), format_number(item.get("current_value")),
                format_number(item.get("absolute_change")), format_percentage(item.get("percentage_change")),
            ])
        movement_table = Table(
            movement_data, repeatRows=1,
            colWidths=[47*mm, 35*mm, 25*mm, 25*mm, 25*mm, 23*mm],
        )
        movement_table.setStyle(_table_style(header=True, numeric_from=2))
        story.append(movement_table)
    else:
        story.append(_p("No major movements were detected using the configured thresholds.", styles["body"]))

    story.append(PageBreak())
    story.append(_section_bar("Entity Changes", styles))
    for heading, key, values_key, empty_text in [
        ("New Entities", "new_entities", "values", "No new entities were detected."),
        ("Removed Entities", "removed_entities", "previous_values", "No removed entities were detected."),
    ]:
        story.append(_p(heading, styles["subheading"]))
        items = analysis.get(key, [])
        if not items:
            story.append(_p(empty_text, styles["body"]))
            continue
        data = [["Entity", "Metric values"]]
        for item in items[:30]:
            values = ", ".join(
                f"{metric}: {format_number(value)}" for metric, value in item.get(values_key, {}).items()
            )
            data.append([
                _p(format_entity(item.get("entity", {})), styles["small"]),
                _p(values, styles["small"]),
            ])
        table = Table(data, repeatRows=1, colWidths=[72 * mm, 108 * mm])
        table.setStyle(_table_style(header=True))
        story.append(table)
        story.append(Spacer(1, 3 * mm))

    story.append(PageBreak())
    story.append(_section_bar("AI Business Insights", styles))
    story.append(Spacer(1, 3 * mm))
    if ai_insights:
        _add_ai_insights(story, ai_insights, styles)
    else:
        story.append(_p("AI-generated business insights were not requested or were unavailable.", styles["body"]))

    document.build(story, onFirstPage=_classification_header_footer, onLaterPages=_classification_header_footer)
    return output_path
