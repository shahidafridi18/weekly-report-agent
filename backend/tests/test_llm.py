from pathlib import Path

from app.analysis.engine import run_analysis
from app.ingestion.excel_reader import read_excel_file
from app.insights.insight_generator import (
    generate_weekly_insights,
)
from app.insights.llm_service import GeminiService


BASE_DIR = Path(__file__).resolve().parent.parent
SAMPLE_DATA_DIR = BASE_DIR / "sample_data"


week1 = read_excel_file(
    SAMPLE_DATA_DIR / "counterparty_week1_formatted.xlsx"
)

week2 = read_excel_file(
    SAMPLE_DATA_DIR / "counterparty_week2_formatted.xlsx"
)


analysis = run_analysis(
    previous_df=week1,
    current_df=week2,
    key_columns=[
        "SIREN",
        "Unique Identifier",
    ],
)


llm_service = GeminiService()


insights = generate_weekly_insights(
    analysis=analysis,
    llm_service=llm_service,
)


print("\n========== AI INSIGHTS ==========\n")

print(insights)