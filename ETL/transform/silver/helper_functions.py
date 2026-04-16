from pathlib import Path
import pandas as pd
import sqlite3
import logging

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

COLUMNS = ["id", "title", "category", "price", "rating"]
COLUMN_MAPPING = {"title": "product"}


def get_csv_and_db_path(filename: str) -> tuple[Path, Path]:
    csv = Path.cwd() / "data" / "bronze"
    db = Path.cwd() / "data" / "silver"
    return csv / f"{filename}.csv", db / f"silver_{filename}.db"


def csv_to_df(csv_path: Path) -> pd.DataFrame:
    if not csv_path.exists():
        raise FileNotFoundError(f"CSV file not found: {csv_path}")
    
    try:
        df = pd.read_csv(csv_path, usecols=COLUMNS)
        df = df.rename(columns=COLUMN_MAPPING)
        logger.info(f"✓ Loaded {len(df)} rows from {csv_path.name}")
        return df
    except KeyError as e:
        raise ValueError(f"Missing required column: {e}") from e
    except pd.errors.ParserError as e:
        raise ValueError(f"CSV parsing error: {e}") from e


def df_to_db(df: pd.DataFrame, db_path: Path, table_name: str) -> None:
    if df.empty:
        raise ValueError("DataFrame is empty, nothing to write")
    
    try:
        db_path.parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(db_path) as conn:
            df.to_sql(table_name, conn, if_exists="replace", index=False)
        logger.info(f"✓ Written to {db_path.name} (table: {table_name})")
    except sqlite3.Error as e:
        raise RuntimeError(f"Database error: {e}") from e


def main(filename: str) -> None:
    try:
        csv_path, db_path = get_csv_and_db_path(filename)
        df = csv_to_df(csv_path)
        df_to_db(df, db_path, f"silver_{filename}")
        logger.info("✓ Transformation complete")
    except (FileNotFoundError, ValueError, RuntimeError) as e:
        logger.error(f"Transformation failed: {e}")
        raise


if __name__ == "__main__":
    main("dummyjson")