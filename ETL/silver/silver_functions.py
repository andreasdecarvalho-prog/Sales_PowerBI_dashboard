from pathlib import Path
import pandas as pd
import sqlite3
import logging

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

COLUMNS = ["title", "category", "price", "rating"]
COLUMN_MAPPING = {"title": "product"}

DB_PATH = Path.cwd() / "data" / "silver" / "products.db"

def get_csv_path(filename: str) -> Path:
    csv = Path.cwd() / "data" / "bronze"
    return csv / f"{filename}.csv"


def csv_to_df(csv_path: Path) -> pd.DataFrame:
    if not csv_path.exists():
        raise FileNotFoundError(f"CSV file not found: {csv_path}")
    
    try:
        df = pd.read_csv(csv_path, usecols=COLUMNS)
        df = df.rename(columns=COLUMN_MAPPING)
        return df
    except KeyError as e:
        raise ValueError(f"Missing required column: {e}") from e
    except pd.errors.ParserError as e:
        raise ValueError(f"CSV parsing error: {e}") from e

def get_df(file_name: str) -> pd.DataFrame:
    csv_path = get_csv_path(file_name)
    return csv_to_df(csv_path)

def df_to_table(df: pd.DataFrame, table_name: str) -> None:
    if df.empty:
        raise ValueError("DataFrame is empty, nothing to write")
    
    try:
        DB_PATH.parent.mkdir(parents=True, exist_ok=True)  # Ensure directory exists


        with sqlite3.connect(DB_PATH) as conn:
            df.to_sql(table_name, conn, if_exists="replace", index=False)

        return table_name


    except sqlite3.Error as e:
        raise RuntimeError(f"Database error: {e}") from e


