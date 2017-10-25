#!/usr/bin/env python
"""Provide functions for custom loading of files."""
from pathlib import Path
import gzip

import pandas as pd

from logzero import logger as log

from coordinator_data_tasks.utils import errors as e


def is_csv(path):
    """Return True if the path is probably a csv."""
    return 'csv' in Path(path).name.split('.')


def is_excel(path):
    """Return True if the path is probably an excel."""
    parts = Path(path).name.split('.')
    return any(["xls" in parts, "xlsx" in parts])


def load_table(path: str, **kwargs) -> pd.DataFrame:
    """Smartly load the table whether it's a csv or excel file."""
    if is_csv(path):
        return load_csv(str(path), **kwargs)
    elif is_excel(path):
        return load_xls(str(path), **kwargs)


def load_csv(path: str, **kwargs) -> pd.DataFrame:
    """Smartly load a csv whether it's gzipped or not."""
    fn = Path(path).name
    try:
        df = pd.read_csv(gzip.open(path), **kwargs)

    except (pd.io.common.CParserError, OSError):
        df = pd.read_csv(path, **kwargs)

    except pd.io.common.EmptyDataError:
        msg = f"File appears to be empty: {fn}."
        log.error(msg)
        raise

    if df.empty:
        msg = f"File appears to be empty: {fn}."
        log.error(msg)
        raise e.ValidationError(msg)

    return df


def load_xls(path: str, **kwargs) -> pd.DataFrame:
    """Load an excel table as DataFrame."""
    fn = Path(path).name
    try:
        df = pd.read_excel(path, **kwargs)

    except (UnicodeDecodeError, pd.errors.ParserError):
        msg = f"File appears to be empty: {fn}."
        log.error(msg)
        raise

    if df.empty:
        msg = f"File appears to be empty: {fn}."
        log.error(msg)
        raise e.ValidationError(msg)

    return df
