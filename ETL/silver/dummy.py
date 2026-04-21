import pandas as pd
from core.logger import logger
from ETL.silver import silver_functions as hf


def transform_dummy(file_name: str) -> pd.DataFrame | None:
    """
    Transform the dummy dataset:
    - Ensures 'price' column is moved to index 1.
    - Returns a cleaned DataFrame or None if errors occur.
    """
    try:
        df = hf.get_df(file_name)

        if "price" not in df.columns:
            logger.error("Column 'price' not found in %s", file_name)
            return None

        cols = list(df.columns)
        cols.remove("price")
        cols.insert(1, "price")
        df = df[cols]

        logger.info("Transformation complete for %s", file_name)
        return df

    except (FileNotFoundError, ValueError, RuntimeError) as e:
        logger.error("%s failed: %s", file_name, e, exc_info=True)
        return None
