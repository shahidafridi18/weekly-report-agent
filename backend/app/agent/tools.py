import logging
from pathlib import Path
import re
from tempfile import TemporaryDirectory
from threading import Lock

from app.agent.models import CompareRequest, FileRequest, ReportRequest
from app.agent.report_store import ReportStore
from app.analysis.engine import run_analysis
from app.ingestion.excel_reader import read_excel_bytes
from app.processing.normalizer import classify_columns
from app.processing.serializer import make_json_safe as json_safe
from app.sources.base import FileSource
from app.validation.data_validator import validate_columns


logger = logging.getLogger(__name__)
chart_lock = Lock()


class WeeklyTools:
    def __init__(self, source: FileSource, report_store: ReportStore):
        self.source = source
        self.report_store = report_store

    def list_weekly_files(self) -> dict:
        files = self.source.list_files()
        return {"files": files, "count": len(files)}

    def analyze_weekly_file(self, request: FileRequest) -> dict:
        info, content = self.source.read_file(request.file)
        frame = read_excel_bytes(content)
        validation = validate_columns(frame, frame, request.key_columns)
        if not validation["valid"]:
            raise ValueError(f"Weekly dataset validation failed: {validation}")
        metrics = classify_columns(frame)["numerical_columns"]
        statistics = {
            column: {
                "total": frame[column].sum(min_count=1),
                "mean": frame[column].mean(),
                "minimum": frame[column].min(),
                "maximum": frame[column].max(),
                "missing_count": int(frame[column].isna().sum()),
            }
            for column in metrics
        }
        return json_safe({
            "file": info,
            "row_count": len(frame),
            "column_count": len(frame.columns),
            "columns": frame.columns.tolist(),
            "key_columns": request.key_columns,
            "validation": validation,
            "metric_statistics": statistics,
        })

    def compare_weekly_files(self, request: CompareRequest) -> dict:
        previous, previous_content = self.source.read_file(request.previous_file)
        current, current_content = self.source.read_file(request.current_file)
        if previous["file_id"] == current["file_id"]:
            raise ValueError("Choose two different weekly input files.")
        result = run_analysis(
            previous_df=read_excel_bytes(previous_content),
            current_df=read_excel_bytes(current_content),
            key_columns=request.key_columns,
            movement_threshold_pct=request.movement_threshold_pct,
            minimum_absolute_change=request.minimum_absolute_change,
        )
        requested_metrics = request.metrics or list(result["metric_summary"])
        unknown = sorted(set(requested_metrics) - set(result["metric_summary"]))
        if unknown:
            raise ValueError(f"Unknown metrics: {unknown}. Use exact Excel column names.")
        ai = {"status": "not_requested", "insights": None}
        if request.generate_ai_insights:
            try:
                from app.insights.insight_generator import generate_weekly_insights
                from app.insights.llm_service import GeminiService
                ai = {"status": "success", "insights": generate_weekly_insights(result, GeminiService())}
            except Exception:
                logger.warning("AI insights unavailable; deterministic comparison remains available.", exc_info=True)
                ai["status"] = "unavailable"
        return json_safe({
            "comparison": {
                "previous_file": previous["file_id"],
                "current_file": current["file_id"],
                "key_columns": request.key_columns,
            },
            "analysis": result,
            "selected_metric_summary": {name: result["metric_summary"][name] for name in requested_metrics},
            "ai": ai,
        })

    def generate_weekly_reports(self, request: ReportRequest) -> dict:
        from app.reporting.chart_generator import generate_kpi_change_chart, generate_movement_bridge_chart
        from app.reporting.excel_report_generator import generate_weekly_report_excel
        from app.reporting.pdf_generator import generate_weekly_report_pdf

        result = self.compare_weekly_files(request)
        analysis = result["analysis"]
        ai_insights = result["ai"]["insights"]
        previous_name = Path(result["comparison"]["previous_file"]).name
        current_name = Path(result["comparison"]["current_file"]).name
        safe_stem = re.sub(r"[^\w-]", "_", f"{Path(previous_name).stem}_vs_{Path(current_name).stem}")[:150]
        artifacts = []
        # Generate all requested formats before publishing the persistent copies.
        with TemporaryDirectory(prefix="weekly_agent_") as temp:
            directory = Path(temp)
            pending = []
            if request.report_format in ("xlsx", "both"):
                path = directory / "report.xlsx"
                generate_weekly_report_excel(analysis, path, previous_name, current_name, ai_insights)
                pending.append((path, "xlsx"))
            if request.report_format in ("pdf", "both"):
                with chart_lock:
                    chart = generate_kpi_change_chart(analysis["metric_summary"], directory / "kpi.png")
                    bridge = generate_movement_bridge_chart(analysis["movement_bridge"], directory / "bridge.png")
                path = directory / "report.pdf"
                generate_weekly_report_pdf(
                    analysis=analysis, ai_insights=ai_insights, chart_path=chart,
                    movement_bridge_chart_path=bridge, output_path=path,
                    previous_file_name=previous_name, current_file_name=current_name,
                )
                pending.append((path, "pdf"))
            for path, report_format in pending:
                artifacts.append(self.report_store.save(path, report_format, f"{safe_stem}_report.{report_format}"))
        result["reports"] = artifacts
        return result
