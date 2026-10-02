from pathlib import Path
from pprint import pprint
import json

from app.analysis.engine import run_analysis
from app.ingestion.excel_reader import read_excel_file


BASE_DIR = Path(__file__).resolve().parent.parent
SAMPLE_DATA_DIR = BASE_DIR / "sample_data"


week1 = read_excel_file(
    SAMPLE_DATA_DIR / "week1.xlsx"
)

week2 = read_excel_file(
    SAMPLE_DATA_DIR / "week2.xlsx"
)


result = run_analysis(
    previous_df=week1,
    current_df=week2,
    key_columns=["Product", "Region"],
    movement_threshold_pct=20,
)

print("\n========== VARIANCE DATA ==========")
pprint(result["variance_data"])


print("\n========== NEW ENTITIES ==========")
pprint(result["new_entities"])


print("\n========== REMOVED ENTITIES ==========")
pprint(result["removed_entities"])

print("\n========== JSON TEST ==========")

json_output = json.dumps(
    result,
    indent=2,
)

print(json_output)