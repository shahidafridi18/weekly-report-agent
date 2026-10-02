import json


def build_weekly_insight_prompt(
    context: dict,
) -> str:
    """
    Build the prompt used to generate weekly
    business insights.
    """

    context_json = json.dumps(
        context,
        indent=2,
    )

    return f"""
You are a business reporting analyst.

Your task is to explain a week-over-week comparison
using ONLY the calculated facts supplied below.

IMPORTANT RULES:

1. Do not invent facts.
2. Do not invent business reasons or causes.
3. Do not recalculate values.
4. Do not assume why a metric increased or decreased.
5. Use only the supplied analysis data.
6. Clearly distinguish facts from possible areas
   that require investigation.
7. If the data does not explain why something happened,
   say that the underlying cause requires investigation.
8. Prioritize material movements rather than describing
   every small change.
9. Pay attention to new and removed entities.
10. Pay attention to the movement bridge when explaining
    overall metric changes.

ANALYSIS DATA:

{context_json}

Generate a concise but useful weekly business analysis
with the following sections:

## Executive Summary

Summarize the most important overall changes.

## Key Positive Movements

Identify the most important positive movements supported
by the supplied data.

## Key Negative Movements

Identify the most important negative movements supported
by the supplied data.

## Main Drivers

Explain which entities contributed most to the overall
metric movements.

Do not invent causal explanations.

## New and Removed Entities

Explain important new or removed entities and their
measured impact.

## Risks and Items to Investigate

Highlight unusual or material changes that may deserve
further investigation.

Do not claim a cause unless the supplied data proves it.

## Key Takeaways

Provide a short list of the most important factual
takeaways for management.
"""