import logging
import helper_functions as hf
from extract import main as get_file_names
import sqlite3

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

FILE_NAMES = get_file_names()
TABLE_NAMES = []


def main() -> None:
    if not FILE_NAMES:
        logger.warning("No files to process")
        return
    
    for file_name in FILE_NAMES:
        try:
            csv_path = hf.get_csv_path(file_name)
            df = hf.csv_to_df(csv_path)

            TABLE_NAMES.append(hf.df_to_table(df, f"silver_{file_name}"))


        except (FileNotFoundError, ValueError, RuntimeError) as e:
            logger.error(f" {file_name} failed: {e}")
            continue
    
    merge_query = f"""
    CREATE TABLE "products" AS
    SELECT * FROM {TABLE_NAMES[0]}
    UNION ALL
    SELECT * FROM {TABLE_NAMES[1]};
    """

    with sqlite3.connect(hf.DB_PATH) as conn:
        conn.execute("DROP TABLE IF EXISTS products;")  
        conn.execute(merge_query)


    logger.info("- Transformation complete")
    



if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.critical(f"Pipeline crashed: {e}", exc_info=True)
        exit(1)