"""Provide functions to recode a dataframe column.

Each function should be in a form that can be handed to df[column_name].apply(func).
"""


import pandas as pd


def recode_dates(x):
    """Return `x` recast as datetime[ns], or `NaT`."""
    try:
        return pd.to_datetime(x)
    except ValueError:
        return pd.NaT
