from pathlib import Path
import pandas as pd
import sqlite3
from core.logger import logger
from core.config import BRONZE_DIR, GOLD_DB, BASE_DIR

# Column definitions
COLUMNS = ["title", "category", "price", "rating"]
COLUMN_MAPPING = {"title": "product"}

TABLE_NAMES: list[str] = []


def get_csv_path(filename: str) -> Path:
    """Return the path to a CSV file in the bronze layer."""
    return BRONZE_DIR / f"{filename}.csv"


def csv_to_df(csv_path: Path) -> pd.DataFrame:
    """Load a CSV into a DataFrame with selected columns and renamed headers."""
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
    """Convenience wrapper to load a DataFrame from a bronze CSV by file name."""
    csv_path = get_csv_path(file_name)
    return csv_to_df(csv_path)


def df_to_table(df: pd.DataFrame, table_name: str) -> str:
    """Write a DataFrame to a SQLite table, replacing if it exists."""
    if df.empty:
        raise ValueError("DataFrame is empty, nothing to write")

    try:
        GOLD_DB.parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(GOLD_DB) as conn:
            df.to_sql(table_name, conn, if_exists="replace", index=False)
        return table_name
    except sqlite3.Error as e:
        raise RuntimeError(f"Database error: {e}") from e


def products_dfs_to_db(file_names: list[str], dfs: list[pd.DataFrame]) -> None:
    """
    Write multiple product DataFrames to the Gold DB and merge them into a unified 'products' table.
    """
    if not file_names:
        logger.warning("No files to process")
        return

    for file_name, df in zip(file_names, dfs):
        try:
            table_name = df_to_table(df, f"silver_{file_name}")
            TABLE_NAMES.append(table_name)
            logger.debug("Table %s created successfully", table_name)
        except (FileNotFoundError, ValueError, RuntimeError) as e:
            logger.error("%s failed: %s", file_name, e, exc_info=True)
            continue

    if len(TABLE_NAMES) < 2:
        logger.warning("Not enough tables to merge into 'products'")
        return

    merge_query = f"""
        CREATE TABLE products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product TEXT,
            category TEXT,
            price REAL,
            rating REAL
        );

        INSERT INTO products (product, category, price, rating)
        SELECT product, category, price, rating FROM {TABLE_NAMES[0]}
        UNION ALL
        SELECT product, category, price, rating FROM {TABLE_NAMES[1]};
    """

    try:
        with sqlite3.connect(GOLD_DB) as conn:
            conn.executescript("DROP TABLE IF EXISTS products;")
            conn.executescript(merge_query)
        logger.info("Merged tables into 'products'")
        return str(GOLD_DB.relative_to(BASE_DIR))
    except sqlite3.Error as e:
        logger.error("Failed to merge tables into 'products': %s", e, exc_info=True)

    logger.info("Silver transformation complete")
