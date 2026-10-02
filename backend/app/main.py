from fastapi import FastAPI

from app.api.comparison import router as comparison_router


app = FastAPI(
    title="Weekly Report Analysis Agent",
    description=(
        "Backend for automated week-over-week "
        "Excel comparison and AI reporting."
    ),
    version="0.2.0",
)


app.include_router(
    comparison_router
)


@app.get("/")
def root():
    return {
        "message": "Weekly Report Analysis Agent is running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }