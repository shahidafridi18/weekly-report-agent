from functools import lru_cache
import logging
from typing import Literal

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse

from app.agent.models import ChatRequest, CompareRequest, FileRequest, ReportRequest
from app.agent.orchestrator import AgentUnavailableError, WeeklyAgent
from app.agent.report_store import LocalReportStore
from app.agent.settings import AgentSettings
from app.agent.tools import WeeklyTools
from app.sources.base import AmbiguousFileError
from app.sources.local import LocalFileSource


router = APIRouter(prefix="/api/agent", tags=["Weekly file agent"])
logger = logging.getLogger(__name__)


@lru_cache(maxsize=1)
def get_agent() -> WeeklyAgent:
    settings = AgentSettings.from_env()
    return WeeklyAgent(WeeklyTools(LocalFileSource(settings.input_directory), LocalReportStore(settings)))


def invoke(operation):
    try:
        return operation()
    except AmbiguousFileError as exc:
        raise HTTPException(409, detail={"message": str(exc), "candidates": exc.candidates}) from exc
    except FileNotFoundError as exc:
        raise HTTPException(404, detail=str(exc)) from exc
    except AgentUnavailableError as exc:
        raise HTTPException(503, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(400, detail=str(exc)) from exc
    except Exception as exc:
        logger.exception("Weekly agent operation failed")
        raise HTTPException(500, detail="Weekly agent operation failed. Check the backend log.") from exc


# Synchronous routes run blocking Pandas, SDK, and reporting work in FastAPI's thread pool.
@router.get("/files")
def list_files(agent: WeeklyAgent = Depends(get_agent)):
    return invoke(agent.tools.list_weekly_files)


@router.post("/analyze")
def analyze_file(request: FileRequest, agent: WeeklyAgent = Depends(get_agent)):
    return invoke(lambda: agent.tools.analyze_weekly_file(request))


@router.post("/compare")
def compare_files(request: CompareRequest, agent: WeeklyAgent = Depends(get_agent)):
    return invoke(lambda: agent.tools.compare_weekly_files(request))


@router.post("/reports")
def create_reports(request: ReportRequest, agent: WeeklyAgent = Depends(get_agent)):
    return invoke(lambda: agent.tools.generate_weekly_reports(request))


@router.post("/chat")
def chat(request: ChatRequest, agent: WeeklyAgent = Depends(get_agent)):
    return invoke(lambda: agent.chat(request.message))


@router.get("/reports/{report_format}/{report_id}")
def download_report(report_format: Literal["pdf", "xlsx"], report_id: str, agent: WeeklyAgent = Depends(get_agent)):
    path = invoke(lambda: agent.tools.report_store.get_path(report_format, report_id))
    media_type = "application/pdf" if report_format == "pdf" else "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    return FileResponse(path, media_type=media_type, filename=report_id)
