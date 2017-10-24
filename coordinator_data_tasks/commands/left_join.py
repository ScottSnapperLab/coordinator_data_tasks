"""Left join excel sheets (left, right) on columns (join_on)."""
import typing as t
from pathlib import Path

import pandas as pd

from logzero import logger as log


def main(left_path: Path, right_path: Path, join_on: t.List[str], out: Path, indicator=True) -> None:
    """Left join excel sheets (left_path, right_path) on columns (join_on)."""
    if indicator:
        indicator = "FOUND_IN"

    # Load files
    left = pd.read_excel(str(left_path), sheetname=0)
    right = pd.read_excel(str(right_path), sheetname=0)

    # Do the Join
    result = left.merge(right=right, on=join_on, how='left', indicator=indicator)
    log.info(f"Results Digest:\n{result[indicator].value_counts()}")

    # Set join_on cols as index
    try:
        result = result.set_index(join_on).sort_index()
    except Exception as exc:
        log.warning(f"The index could not be sorted: {exc.args[0]}")
        result = result.set_index(join_on)

    # Set new Columns Index
    left_cols = [c for c in left.columns if c not in join_on]
    right_cols = [c for c in right.columns if c not in join_on]
    indicator_cols = [indicator]

    source_cols = ["left"] * len(left_cols) + ["right"] * len(right_cols) + ["indicator"] * len(indicator_cols)
    column_cols = left_cols + right_cols + indicator_cols

    result.columns = pd.MultiIndex.from_arrays([source_cols, column_cols], names=["Source", "Column"])

    # Write the results
    result.to_excel(str(out), index=True, sheet_name="Results")
