from pathlib import Path
import json
import re
import shutil
from typing import Protocol
from uuid import uuid4

from app.agent.settings import AgentSettings


class ReportStore(Protocol):
    def save(self, source: Path, report_format: str, display_name: str) -> dict: ...


class LocalReportStore:
    def __init__(self, settings: AgentSettings):
        self.directories = {"xlsx": settings.excel_directory.resolve(), "pdf": settings.pdf_directory.resolve()}

    def save(self, source: Path, report_format: str, display_name: str) -> dict:
        directory = self.directories[report_format]
        directory.mkdir(parents=True, exist_ok=True)
        if not source.is_file() or source.stat().st_size == 0:
            raise RuntimeError("Report generator did not create a non-empty report.")
        report_id = f"report_{uuid4().hex}.{report_format}"
        target = directory / report_id
        staging = directory / f".{report_id}.tmp"
        metadata = directory / f".{report_id}.json"
        metadata_staging = directory / f".{report_id}.json.tmp"
        try:
            shutil.copyfile(source, staging)
            staging.replace(target)
            metadata_staging.write_text(json.dumps({"filename": display_name}), encoding="utf-8")
            metadata_staging.replace(metadata)
        finally:
            staging.unlink(missing_ok=True)
            metadata_staging.unlink(missing_ok=True)
        return {
            "report_id": report_id,
            "format": report_format,
            "filename": display_name,
            "download_url": f"/api/agent/reports/{report_format}/{report_id}",
        }

    def get_path(self, report_format: str, report_id: str) -> Path:
        if report_format not in self.directories or not re.fullmatch(r"report_[0-9a-f]{32}\.(?:pdf|xlsx)", report_id):
            raise FileNotFoundError("Report was not found.")
        if Path(report_id).suffix != f".{report_format}":
            raise FileNotFoundError("Report was not found.")
        directory = self.directories[report_format]
        path = (directory / report_id).resolve()
        if not path.is_relative_to(directory) or not path.is_file():
            raise FileNotFoundError("Report was not found.")
        return path

    def get_filename(self, report_format: str, report_id: str, hint: str | None = None) -> str:
        # get_path validates format, ID, and existence before we read metadata.
        path = self.get_path(report_format, report_id)
        metadata = path.parent / f".{report_id}.json"
        stored = None
        if metadata.is_file():
            try:
                stored = json.loads(metadata.read_text(encoding="utf-8")).get("filename")
            except (OSError, ValueError, AttributeError):
                stored = None
        for name in (stored, hint):
            if isinstance(name, str) and name:
                safe = re.sub(r"[^A-Za-z0-9._-]", "_", Path(name).name)[:200]
                if safe.lower().endswith(f".{report_format}"):
                    return safe
        return report_id
