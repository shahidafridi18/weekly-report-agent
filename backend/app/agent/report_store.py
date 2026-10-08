from pathlib import Path
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
        try:
            shutil.copyfile(source, staging)
            staging.replace(target)
        finally:
            staging.unlink(missing_ok=True)
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
