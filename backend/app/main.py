from fastapi import FastAPI

from app.api.comparison import router as comparison_router
from app.api.report import router as report_router
from app.api.agent import router as agent_router

app = FastAPI(
    title="Weekly Report Analysis Agent",
    description=(
        "Backend for automated week-over-week "
        "Excel comparison, AI insights, "
        "and PDF reporting."
    ),
    version="0.3.0",
)


app.include_router(comparison_router)
app.include_router(report_router)
app.include_router(agent_router)


@app.get("/")
def root():
    return {
        "message": (
            "Weekly Report Analysis Agent is running"
        )
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }