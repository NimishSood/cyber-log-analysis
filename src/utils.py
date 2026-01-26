# src/utils.py
"""
Utility functions for CIC-IDS-2017 exploration.

Design goals:
- Keep notebooks clean and focused on storytelling.
- Make common inspections reusable and reproducible.
- Avoid hardcoded absolute paths; use Path objects.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Optional

import numpy as np
import pandas as pd


# -----------------------------
# File discovery / acquisition
# -----------------------------

def list_csv_files(data_raw_dir: Path) -> pd.DataFrame:
    """
    Discover CSV files in a directory and return a table with file names and sizes (MB).
    """
    if not data_raw_dir.exists():
        raise FileNotFoundError(f"Raw data directory not found: {data_raw_dir.resolve()}")

    csv_files = sorted(data_raw_dir.glob("*.csv"))
    if not csv_files:
        raise FileNotFoundError(f"No CSV files found in: {data_raw_dir.resolve()}")

    return pd.DataFrame({
        "file": [f.name for f in csv_files],
        "size_mb": [round(f.stat().st_size / (1024**2), 2) for f in csv_files],
    })


def pick_file(data_raw_dir: Path, preferred_name: Optional[str] = None) -> Path:
    """
    Pick a file for analysis. If preferred_name exists, return it; otherwise return the first CSV.
    """
    csv_files = sorted(data_raw_dir.glob("*.csv"))
    if not csv_files:
        raise FileNotFoundError(f"No CSV files found in: {data_raw_dir.resolve()}")

    if preferred_name:
        candidate = data_raw_dir / preferred_name
        if candidate.exists():
            return candidate

    return csv_files[0]


# -----------------------------
# Loading helpers
# -----------------------------

def load_peek(csv_path: Path, nrows: int = 5000) -> pd.DataFrame:
    """
    Fast peek load for schema inspection.
    """
    if not csv_path.exists():
        raise FileNotFoundError(f"CSV not found: {csv_path.resolve()}")

    df = pd.read_csv(csv_path, nrows=nrows)
    df.columns = df.columns.str.strip()  # crucial hygiene step
    return df


def load_full(csv_path: Path) -> pd.DataFrame:
    """
    Full load. Keep separate from peek so you can control memory/time during demos.
    """
    if not csv_path.exists():
        raise FileNotFoundError(f"CSV not found: {csv_path.resolve()}")

    df = pd.read_csv(csv_path)
    df.columns = df.columns.str.strip()
    return df


# -----------------------------
# Audit / understanding helpers
# -----------------------------

@dataclass
class AuditResult:
    shape: tuple[int, int]
    n_duplicates: int
    duplicate_rate: float
    memory_mb: float
    object_columns: list[str]
    missing_top: pd.Series
    label_counts: Optional[pd.Series]


def basic_audit(df: pd.DataFrame, label_col: str = "Label", missing_top_k: int = 15) -> AuditResult:
    """
    A compact first-pass audit:
    - shape
    - duplicates
    - memory
    - object columns
    - missingness (top-k)
    - label distribution (if present)
    """
    # duplicates
    n_dup = int(df.duplicated().sum())
    dup_rate = float(n_dup / len(df)) if len(df) else 0.0

    # memory
    mem_mb = float(df.memory_usage(deep=True).sum() / (1024**2))

    # object cols
    obj_cols = df.select_dtypes(include=["object"]).columns.tolist()

    # missingness
    missing_pct = (df.isna().mean() * 100).sort_values(ascending=False)
    missing_top = missing_pct.head(missing_top_k)

    # label counts
    label_counts = None
    if label_col in df.columns:
        label_counts = df[label_col].value_counts()

    return AuditResult(
        shape=df.shape,
        n_duplicates=n_dup,
        duplicate_rate=dup_rate,
        memory_mb=mem_mb,
        object_columns=obj_cols,
        missing_top=missing_top,
        label_counts=label_counts,
    )


def numeric_summary(df: pd.DataFrame, max_cols: int = 25) -> pd.DataFrame:
    """
    Numeric describe with a few percentiles for sanity checking.
    Limits columns returned so it stays readable in presentation.
    """
    num_df = df.select_dtypes(include=[np.number])
    if num_df.empty:
        return pd.DataFrame()

    summary = num_df.describe(percentiles=[0.01, 0.5, 0.99]).T
    return summary.head(max_cols)


def clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """
    Strip whitespace and remove problematic BOM or hidden characters in column names.
    """
    df = df.copy()
    df.columns = (
        df.columns
        .astype(str)
        .str.replace("\ufeff", "", regex=False)
        .str.strip()
    )
    return df


def find_suspicious_columns(df: pd.DataFrame) -> dict:
    cols = df.columns.tolist()
    unnamed = [c for c in cols if str(c).lower().startswith("unnamed")]
    dup_cols = df.columns[df.columns.duplicated()].tolist()

    # whitespace / hidden char checks
    leading_trailing_ws = [c for c in cols if isinstance(c, str) and (c != c.strip())]
    bom_cols = [c for c in cols if isinstance(c, str) and "\ufeff" in c]

    return {
        "unnamed_columns": unnamed,
        "duplicate_columns": dup_cols,
        "whitespace_columns": leading_trailing_ws,
        "bom_columns": bom_cols,
    }
