import logging
import helper_functions as hf
from ETL.transform.silver.extract import FILE_NAMES

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

FILE_NAMES = FILE_NAMES  # Get file names from extract module


def main() -> None:
    if not FILE_NAMES:
        logger.warning("No files to process")
        return
    
    for file_name in FILE_NAMES:
        try:
            logger.info(f"Processing {file_name}...")
            csv_path, db_path = hf.get_csv_and_db_path(file_name)
            df = hf.csv_to_df(csv_path)
            hf.df_to_db(df, db_path, f"silver_{file_name}")
            logger.info(f"✓ {file_name} completed")
        except (FileNotFoundError, ValueError, RuntimeError) as e:
            logger.error(f"✗ {file_name} failed: {e}")
            continue
    
    logger.info("✓ All transformations complete")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.critical(f"Pipeline crashed: {e}", exc_info=True)
        exit(1)