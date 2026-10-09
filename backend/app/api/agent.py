from functools import lru_cache
import logging
from typing import Literal

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse

from app.agent.models import ChatRequest, CompareRequest, FileRequest, QueryRequest, ReportRequest
from app.agent.metric_resolver import MetricMatchError, MetricResolver
from app.agent.orchestrator import AgentUnavailableError, WeeklyAgent
from app.agent.report_store import LocalReportStore
from app.agent.settings import AgentSettings
from app.agent.sessions import SessionConflictError, SessionNotFoundError, SessionStore
from app.agent.tools import EntityMatchError, WeeklyTools
from app.sources.base import AmbiguousFileError
from app.sources.local import LocalFileSource


router = APIRouter(prefix="/api/agent", tags=["Weekly file agent"])
logger = logging.getLogger(__name__)


@lru_cache(maxsize=1)
def get_agent() -> WeeklyAgent:
    settings = AgentSettings.from_env()
    return WeeklyAgent(
        WeeklyTools(LocalFileSource(settings.input_directory), LocalReportStore(settings), MetricResolver(settings.metric_aliases)),
        sessions=SessionStore(settings.session_database),
    )


def invoke(operation):
    try:
        return operation()
    except AmbiguousFileError as exc:
        raise HTTPException(409, detail={"message": str(exc), "candidates": exc.candidates}) from exc
    except MetricMatchError as exc:
        raise HTTPException(409 if exc.ambiguous else 400, detail={"message": str(exc), "candidates": exc.candidates}) from exc
    except EntityMatchError as exc:
        raise HTTPException(409, detail={"message": str(exc), "candidates": exc.candidates}) from exc
    except SessionNotFoundError as exc:
        raise HTTPException(404, detail=str(exc)) from exc
    except SessionConflictError as exc:
        raise HTTPException(409, detail=str(exc)) from exc
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
    return invoke(lambda: agent.chat(
        message=request.message,
        session_id=request.session_id,
        include_details=request.include_details,
    ))


@router.post("/query")
def query_comparison(request: QueryRequest, agent: WeeklyAgent = Depends(get_agent)):
    return invoke(lambda: agent.tools.query_comparison(request))


@router.post("/sessions")
def create_session(agent: WeeklyAgent = Depends(get_agent)):
    return invoke(agent.sessions.create)


@router.get("/sessions")
def list_sessions(agent: WeeklyAgent = Depends(get_agent)):
    return invoke(agent.sessions.list_sessions)


@router.get("/sessions/{session_id}")
def get_session(session_id: str, agent: WeeklyAgent = Depends(get_agent)):
    def read_session():
        session = agent.sessions.get(session_id)
        session["turns"] = agent.sessions.get_turns(session_id)
        return session
    return invoke(read_session)


@router.delete("/sessions/{session_id}")
def delete_session(session_id: str, agent: WeeklyAgent = Depends(get_agent)):
    invoke(lambda: agent.sessions.delete(session_id))
    return {"status": "deleted", "session_id": session_id}


@router.get("/reports/{report_format}/{report_id}")
def download_report(report_format: Literal["pdf", "xlsx"], report_id: str, filename: str | None = None, agent: WeeklyAgent = Depends(get_agent)):
    path = invoke(lambda: agent.tools.report_store.get_path(report_format, report_id))
    readable_name = invoke(lambda: agent.tools.report_store.get_filename(report_format, report_id, filename))
    media_type = "application/pdf" if report_format == "pdf" else "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    return FileResponse(path, media_type=media_type, filename=readable_name)
