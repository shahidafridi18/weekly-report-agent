from pathlib import Path

from app.ingestion.excel_reader import read_excel_file
from app.processing.normalizer import classify_columns
from app.validation.data_validator import validate_columns
from app.processing.matcher import match_rows, categorize_rows
from app.analysis.variance import calculate_variances
from app.analysis.movements import detect_major_movements
BASE_DIR = Path(__file__).resolve().parent.parent
SAMPLE_DATA_DIR = BASE_DIR / "sample_data"


week1 = read_excel_file(
    SAMPLE_DATA_DIR / "week1.xlsx"
)

week2 = read_excel_file(
    SAMPLE_DATA_DIR / "week2.xlsx"
)


print("\n========== WEEK 1 ==========")
print(week1)

print("\n========== WEEK 2 ==========")
print(week2)


print("\nWeek 1 shape:")
print(week1.shape)

print("\nWeek 1 columns:")
print(week1.columns.tolist())

print("\nWeek 1 data types:")
print(week1.dtypes)

classification = classify_columns(week1)

print("\n========== COLUMN CLASSIFICATION ==========")

print("Numerical columns:")
print(classification["numerical_columns"])

print("\nNon-numerical columns:")
print(classification["non_numerical_columns"])

validation = validate_columns(
    week1,
    week2,
)

print("\n========== SCHEMA VALIDATION ==========")
print(validation)

key_columns = ["Product", "Region"]

matched_df = match_rows(
    week1,
    week2,
    key_columns,
)

print("\n========== MATCHED DATA ==========")
print(matched_df.to_string(index=False))

categories = categorize_rows(matched_df)

print("\n========== ROW SUMMARY ==========")

print("Matched rows:", len(categories["matched"]))
print("New rows:", len(categories["new"]))
print("Removed rows:", len(categories["removed"]))

matched_only = categories["matched"]

numerical_columns = classification["numerical_columns"]

variance_df = calculate_variances(
    matched_only,
    numerical_columns,
)

print("\n========== VARIANCE ANALYSIS ==========")

columns_to_show = [
    "Product",
    "Region",
    "Revenue_previous",
    "Revenue_current",
    "Revenue_change",
    "Revenue_change_pct",
]

print(
    variance_df[columns_to_show].to_string(index=False)
)

major_movements = detect_major_movements(
    variance_df,
    numerical_columns,
    key_columns,
    threshold_pct=20,
)

print("\n========== MAJOR MOVEMENTS ==========")

for movement in major_movements:
    print(movement)