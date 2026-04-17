import logging
import ETL.silver.silver_functions as hf
import sqlite3

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


TABLE_NAMES = []


def products_dfs_to_db(FILE_NAMES, dfs) -> None:
    if not FILE_NAMES:
        logger.warning("No files to process")
        return
    
    for file_name, df in zip(FILE_NAMES, dfs):
        try:
            table_name = hf.df_to_table(df, f"silver_{file_name}")
            TABLE_NAMES.append(table_name)


        except (FileNotFoundError, ValueError, RuntimeError) as e:
            logger.error(f" {file_name} failed: {e}")
            continue
    
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

    with sqlite3.connect(hf.DB_PATH) as conn:
        conn.executescript("DROP TABLE IF EXISTS products;")  
        conn.executescript(merge_query)



    logger.info("- Transformation complete")
    


