import pandas as pd
from core.logger import logger
from core.config import GOLD_DIR, CSV_ENCODING, BASE_DIR

def df_to_gold_csv(df: pd.DataFrame, file_name: str) -> str:
    """
    Save a DataFrame as a CSV file in the bronze directory.

    Args:
        df (pd.DataFrame): The DataFrame to save.
        file_name (str): The base name (without extension) for the CSV file.

    Returns:
        str: Path to the saved CSV file.
    """
    file_path = GOLD_DIR / f"{file_name}_gold.csv"
    

    try:
        df.to_csv(file_path, index=False, encoding=CSV_ENCODING)
        logger.debug("Saved DataFrame to CSV: %s", file_path)
        return str(file_path.relative_to(BASE_DIR)
)
    except Exception as e:
        logger.error("Failed to save DataFrame to CSV %s: %s", file_path, e)
        raise
