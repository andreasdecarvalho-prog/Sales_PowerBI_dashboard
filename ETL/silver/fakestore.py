import ast
import logging
import ETL.silver.silver_functions as hf


logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


def transform_fakestore(file_name):
    try:
        df = hf.get_df(file_name)


        df["rating"] = df["rating"].apply(lambda x: ast.literal_eval(x)["rate"])

        return df


    except (FileNotFoundError, ValueError, RuntimeError) as e:
        logger.error(f" {file_name} failed: {e}")


    logger.info("- Transformation complete")
    


