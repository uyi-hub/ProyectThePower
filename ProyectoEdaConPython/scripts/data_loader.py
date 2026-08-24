"""Utilities to load data for ProyectoEdaConPython
"""
from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DATA_DIR = PROJECT_ROOT / "data"


def load_csv(filename, data_dir: Path = DEFAULT_DATA_DIR, **kwargs):
    """Load a CSV file located in the data directory or given by absolute path.

    Parameters
    - filename: str or Path. If relative, it's resolved against data_dir.
    - data_dir: Path where data files are stored.
    - **kwargs: passed to pd.read_csv
    """
    path = Path(filename)
    if not path.is_absolute():
        path = Path(data_dir) / filename
    return pd.read_csv(path, **kwargs)


def list_data_files(data_dir: Path = DEFAULT_DATA_DIR):
    """Return a list of data file names present in the data directory."""
    d = Path(data_dir)
    if not d.exists():
        return []
    return [p.name for p in d.iterdir() if p.is_file()]


if __name__ == "__main__":
    print("Data files:", list_data_files())
