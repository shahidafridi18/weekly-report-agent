import math

import numpy as np
import pandas as pd


def make_json_safe(value):
    """
    Convert Pandas / NumPy values into values that
    can safely be returned as JSON.
    """

    if isinstance(value, dict):
        return {str(key): make_json_safe(item) for key, item in value.items()}

    if isinstance(value, (list, tuple)):
        return [make_json_safe(item) for item in value]

    if value is None or value is pd.NA or value is pd.NaT:
        return None

    # bool is a subclass of int; preserve JSON true/false before integer conversion.
    if isinstance(value, (bool, np.bool_)):
        return bool(value)

    if isinstance(value, (float, np.floating)):
        if math.isnan(value) or math.isinf(value):
            return None

        return float(value)

    if isinstance(value, (int, np.integer)):
        return int(value)

    if isinstance(value, pd.Timestamp):
        return value.isoformat()

    return value


def dataframe_to_records(
    df: pd.DataFrame,
) -> list[dict]:
    """
    Convert a Pandas DataFrame into JSON-safe records.
    """

    records = df.to_dict(orient="records")

    safe_records = []

    for record in records:

        safe_record = {
            key: make_json_safe(value)
            for key, value in record.items()
        }

        safe_records.append(safe_record)

    return safe_records