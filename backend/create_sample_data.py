import pandas as pd
from pathlib import Path


# Find the root project directory
BASE_DIR = Path(__file__).resolve().parent.parent

# sample_data folder is outside backend
SAMPLE_DATA_DIR = BASE_DIR / "sample_data"

# Make sure the folder exists
SAMPLE_DATA_DIR.mkdir(exist_ok=True)


week1_data = [
    {
        "Product": "Product A",
        "Region": "North",
        "Revenue": 100000,
        "Cost": 70000,
        "Profit": 30000,
        "Orders": 100,
    },
    {
        "Product": "Product B",
        "Region": "South",
        "Revenue": 150000,
        "Cost": 100000,
        "Profit": 50000,
        "Orders": 140,
    },
    {
        "Product": "Product C",
        "Region": "East",
        "Revenue": 80000,
        "Cost": 55000,
        "Profit": 25000,
        "Orders": 80,
    },
    {
        "Product": "Product D",
        "Region": "West",
        "Revenue": 200000,
        "Cost": 150000,
        "Profit": 50000,
        "Orders": 190,
    },
]


week2_data = [
    {
        "Product": "Product C",
        "Region": "East",
        "Revenue": 90000,
        "Cost": 60000,
        "Profit": 30000,
        "Orders": 92,
    },
    {
        "Product": "Product A",
        "Region": "North",
        "Revenue": 135000,
        "Cost": 85000,
        "Profit": 50000,
        "Orders": 125,
    },
    {
        "Product": "Product B",
        "Region": "South",
        "Revenue": 110000,
        "Cost": 90000,
        "Profit": 20000,
        "Orders": 105,
    },
    {
        "Product": "Product E",
        "Region": "Central",
        "Revenue": 75000,
        "Cost": 50000,
        "Profit": 25000,
        "Orders": 70,
    },
]


week1_df = pd.DataFrame(week1_data)
week2_df = pd.DataFrame(week2_data)


week1_path = SAMPLE_DATA_DIR / "week1.xlsx"
week2_path = SAMPLE_DATA_DIR / "week2.xlsx"


week1_df.to_excel(week1_path, index=False)
week2_df.to_excel(week2_path, index=False)


print("Sample Excel files created successfully.")
print(f"Week 1: {week1_path}")
print(f"Week 2: {week2_path}")