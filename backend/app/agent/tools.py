import logging
import hashlib
from pathlib import Path
import re
from tempfile import TemporaryDirectory
from threading import Lock

from app.agent.models import CompareRequest, FileRequest, QueryRequest, ReportRequest
from app.agent.metric_resolver import MetricResolver, normalize
from app.agent.report_store import ReportStore
from app.analysis.engine import run_analysis
from app.ingestion.excel_reader import read_excel_bytes
from app.processing.normalizer import classify_columns
from app.processing.serializer import make_json_safe as json_safe
from app.sources.base import FileSource
from app.validation.data_validator import validate_columns


logger = logging.getLogger(__name__)
chart_lock = Lock()


class EntityMatchError(ValueError):
    def __init__(self, requested, candidates, ambiguous=False, source=None):
        self.requested = requested
        self.candidates = candidates
        self.ambiguous = ambiguous
        location = source or "the selected workbook(s)"
        message = (f"Entity '{requested}' matches multiple rows in {location}. Choose an exact business key."
                   if ambiguous else f"Entity '{requested}' was not found in {location}. Check the identifier and selected week.")
        super().__init__(message)


def entity_label(entity: dict) -> str:
    return ", ".join(f"{key}: {value}" for key, value in entity.items())


def entity_index(frames, key_columns):
    index = {}
    for frame in frames:
        for _, row in frame.iterrows():
            identity = json_safe({key: row[key] for key in key_columns})
            token = tuple(str(identity[key]) for key in key_columns)
            item = index.setdefault(token, {"entity": identity, "names": []})
            name = row.get("Counterparty Name")
            if isinstance(name, str) and name not in item["names"]:
                item["names"].append(name)
    return list(index.values())


def resolve_entity(requested: str, index: list[dict]) -> dict:
    label = normalize(requested)
    if not label:
        raise EntityMatchError(requested, [entity_label(item["entity"]) for item in index[:5]])
    def labels(item):
        return [normalize(text) for text in [*item["names"], *map(str, item["entity"].values()),
                entity_label(item["entity"]), " / ".join(map(str, item["entity"].values()))]]
    matches = [item for item in index if label in labels(item)]
    if not matches:
        matches = [item for item in index if any(f" {label} " in f" {candidate} " for candidate in labels(item))]
    if len(matches) != 1:
        raise EntityMatchError(requested, [entity_label(item["entity"]) for item in (matches or index)[:20]], ambiguous=len(matches) > 1)
    return matches[0]


class WeeklyTools:
    def __init__(self, source: FileSource, report_store: ReportStore, metric_resolver: MetricResolver | None = None):
        self.source = source
        self.report_store = report_store
        self.metric_resolver = metric_resolver or MetricResolver()

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
        selected, matches = self.metric_resolver.resolve_many(request.metrics, metrics)
        dataset_rows = len(frame)
        selected_entity = None
        if request.entity:
            try:
                selected_entity = resolve_entity(request.entity, entity_index([frame], request.key_columns))
            except EntityMatchError as exc:
                raise EntityMatchError(exc.requested, exc.candidates, exc.ambiguous, info["file_id"]) from exc
            mask = frame[request.key_columns[0]].astype(str).eq(str(selected_entity["entity"][request.key_columns[0]]))
            for key in request.key_columns[1:]:
                mask &= frame[key].astype(str).eq(str(selected_entity["entity"][key]))
            frame = frame.loc[mask]
        statistics = {
            column: {
                "total": frame[column].sum(min_count=1),
                "mean": frame[column].mean(),
                "minimum": frame[column].min(),
                "maximum": frame[column].max(),
                "missing_count": int(frame[column].isna().sum()),
            }
            for column in selected
        }
        return json_safe({
            "file": info,
            "row_count": len(frame),
            "dataset_row_count": dataset_rows,
            "column_count": len(frame.columns),
            "columns": frame.columns.tolist(),
            "key_columns": request.key_columns,
            "validation": validation,
            "metric_statistics": statistics,
            "metric_values": {column: frame.iloc[0][column] for column in selected} if selected_entity else None,
            "metric_name_matches": matches,
            "available_metrics": metrics,
            "entity": selected_entity,
            "source_fingerprints": {info["file_id"]: hashlib.sha256(content).hexdigest()},
        })

    def compare_weekly_files(self, request: CompareRequest) -> dict:
        previous, previous_content = self.source.read_file(request.previous_file)
        current, current_content = self.source.read_file(request.current_file)
        if previous["file_id"] == current["file_id"]:
            raise ValueError("Choose two different weekly input files.")
        previous_frame = read_excel_bytes(previous_content)
        current_frame = read_excel_bytes(current_content)
        result = run_analysis(
            previous_df=previous_frame,
            current_df=current_frame,
            key_columns=request.key_columns,
            movement_threshold_pct=request.movement_threshold_pct,
            minimum_absolute_change=request.minimum_absolute_change,
        )
        requested_metrics, matches = self.metric_resolver.resolve_many(request.metrics, list(result["metric_summary"]))
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
            "metric_name_matches": matches,
            "entity_index": entity_index([previous_frame, current_frame], request.key_columns),
            "source_fingerprints": {
                previous["file_id"]: hashlib.sha256(previous_content).hexdigest(),
                current["file_id"]: hashlib.sha256(current_content).hexdigest(),
            },
            "ai": ai,
        })

    def _entity_changes(self, analysis: dict, metric: str) -> list[dict]:
        keys = analysis["columns"]["key_columns"]
        records = []
        for row in analysis["variance_data"]:
            records.append({
                "entity": {key: row[key] for key in keys}, "status": "matched",
                "previous": row.get(f"{metric}_previous"), "current": row.get(f"{metric}_current"),
                "absolute_change": row.get(f"{metric}_change"), "percentage_change": row.get(f"{metric}_change_pct"),
            })
        for row in analysis["new_entities"]:
            current = row["values"].get(metric)
            records.append({"entity": row["entity"], "status": "new", "previous": None,
                            "current": current, "absolute_change": current, "percentage_change": None})
        for row in analysis["removed_entities"]:
            previous = row["previous_values"].get(metric)
            records.append({"entity": row["entity"], "status": "removed", "previous": previous, "current": None,
                            "absolute_change": -previous if previous is not None else None,
                            "percentage_change": -100.0 if previous is not None and previous != 0 else None})
        return records

    def query_comparison(self, request: QueryRequest) -> dict:
        # Queries are deterministic; do not call the optional insight generator here.
        compare = request.model_dump(exclude={"question", "entity", "direction", "limit"})
        compare["generate_ai_insights"] = False
        base = self.compare_weekly_files(CompareRequest.model_validate(compare))
        analysis = base["analysis"]
        metrics = list(base["selected_metric_summary"])
        data = {
            "comparison": base["comparison"], "question": request.question,
            "row_summary": analysis["row_summary"], "metric_name_matches": base["metric_name_matches"],
            "metric_summary": base["selected_metric_summary"],
            "source_fingerprints": base["source_fingerprints"],
        }
        if request.question == "contributors":
            if len(metrics) > 3:
                from app.agent.metric_resolver import MetricMatchError
                raise MetricMatchError("contributors metric selection", metrics, True)
            results = {}
            for metric in metrics:
                all_records = self._entity_changes(analysis, metric)
                net = analysis["metric_summary"][metric]["absolute_change"]
                unknown = sum(item["absolute_change"] is None for item in all_records)
                records = [item for item in all_records if item["absolute_change"] is not None and item["absolute_change"] != 0]
                if request.direction == "increase":
                    records = [item for item in records if item["absolute_change"] > 0]
                elif request.direction == "decrease":
                    records = [item for item in records if item["absolute_change"] < 0]
                records.sort(key=lambda item: (-abs(item["absolute_change"]), entity_label(item["entity"])))
                for item in records:
                    item["contribution_to_net_change_pct"] = item["absolute_change"] / net * 100 if net else None
                results[metric] = {"direction": request.direction, "movement_bridge": analysis["movement_bridge"][metric],
                                   "top_contributors": records[:request.limit], "matching_entities": len(records),
                                   "entities_with_missing_change": unknown}
            data["contributors"] = results
        elif request.question == "entity":
            if not request.entity:
                raise EntityMatchError("unspecified", [entity_label(item["entity"]) for item in base["entity_index"][:20]])
            entity = resolve_entity(request.entity, base["entity_index"])
            changes = {}
            for metric in metrics:
                for item in self._entity_changes(analysis, metric):
                    if item["entity"] == entity["entity"]:
                        changes[metric] = {key: value for key, value in item.items() if key != "entity"}
                        break
            data["entity"] = entity
            data["metric_changes"] = changes
        elif request.question == "entities":
            data["new_entities"] = [{"entity": row["entity"], "values": {metric: row["values"].get(metric) for metric in metrics}} for row in analysis["new_entities"][:request.limit]]
            data["removed_entities"] = [{"entity": row["entity"], "previous_values": {metric: row["previous_values"].get(metric) for metric in metrics}} for row in analysis["removed_entities"][:request.limit]]
            data["limit"] = request.limit
        elif request.question == "zero_transitions":
            records = [row for row in analysis["zero_transitions"] if row.get("metric") in metrics]
            data["zero_transitions"] = records[:request.limit]
            data["matching_transitions"] = len(records)
        return json_safe(data)

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
