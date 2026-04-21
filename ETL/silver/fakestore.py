import ast
import pandas as pd
from core.logger import logger
from ETL.silver import silver_functions as hf


def transform_fakestore(file_name: str) -> pd.DataFrame | None:
    """
    Transform the fakestore dataset:
    - Loads a DataFrame from bronze CSV.
    - Converts 'rating' column from JSON-like string to numeric 'rate'.
    - Returns a cleaned DataFrame or None if errors occur.
    """
    try:
        df = hf.get_df(file_name)

        if "rating" not in df.columns:
            logger.error("Column 'rating' not found in %s", file_name)
            return None

        # Safely parse rating values
        df["rating"] = df["rating"].apply(
            lambda x: ast.literal_eval(x)["rate"] if isinstance(x, str) else x
        )

        logger.info("Transformation complete for %s", file_name)
        return df

    except (FileNotFoundError, ValueError, RuntimeError, SyntaxError) as e:
        logger.error("%s failed: %s", file_name, e, exc_info=True)
        return None
