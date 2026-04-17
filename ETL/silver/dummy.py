import ast
import logging
import ETL.silver.silver_functions as hf


logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


def transform_dummy(file_name):
    try:
        df = hf.get_df(file_name)

        cols = list(df.columns)
        cols.remove("price")
        cols.insert(1, "price")
        df = df[cols]


        return df

    except (FileNotFoundError, ValueError, RuntimeError) as e:
        logger.error(f" {file_name} failed: {e}")


    logger.info("- Transformation complete")
    


