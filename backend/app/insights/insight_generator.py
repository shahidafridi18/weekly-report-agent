from app.insights.context_builder import (
    build_insight_context,
)
from app.insights.llm_service import LLMService
from app.insights.prompts import (
    build_weekly_insight_prompt,
)


def generate_weekly_insights(
    analysis: dict,
    llm_service: LLMService,
) -> str:
    """
    Generate business insights from structured
    analytical results.
    """

    context = build_insight_context(
        analysis
    )

    prompt = build_weekly_insight_prompt(
        context
    )

    return llm_service.generate(
        prompt
    )