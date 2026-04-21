import random
import pandas as pd
from datetime import datetime, timedelta
import sqlite3
from core.logger import logger
from core.config import SILVER_DB


def generate_fake_sales(products_table: pd.DataFrame, n_sales: int = 1000) -> pd.DataFrame:
    """
    Generate a DataFrame of fake sales based on products_table.
    Each sale includes product_id, quantity, sale_date, and gross_profit.
    """
    if products_table.empty:
        raise ValueError("Products table is empty, cannot generate sales")

    sales = []
    start_date = datetime(2026, 1, 1)
    end_date = datetime.today()
    days_range = (end_date - start_date).days

    for sale_id in range(1, n_sales + 1):
        product = products_table.sample(1).iloc[0]
        quantity = random.randint(1, 5)
        sale_date = start_date + timedelta(days=random.randint(0, days_range))
        gross_profit = round(product["price"] * quantity, 2)

        sales.append({
            "id": sale_id,
            "product_id": product.get("id"),
            "quantity": quantity,
            "sale_date": sale_date.strftime("%Y-%m-%d"),
            "gross_profit": gross_profit
        })

    logger.info("Generated %d fake sales records", n_sales)
    return pd.DataFrame(sales)


def insert_sales_into_db(sales_df: pd.DataFrame, table_name: str = "sales") -> None:
    """
    Insert the fake sales DataFrame into SQLite.
    Replaces the table if it already exists.
    """
    if sales_df.empty:
        logger.warning("Sales DataFrame is empty, nothing to insert")
        return

    try:
        with sqlite3.connect(SILVER_DB) as conn:
            sales_df.to_sql(table_name, conn, if_exists="replace", index=False)
        logger.info("Inserted %d records into table '%s'", len(sales_df), table_name)
    except sqlite3.Error as e:
        logger.error("Database error inserting sales: %s", e, exc_info=True)
        raise


def fake_sales(n_sales: int = 1000) -> None:
    """
    Generate and insert fake sales into the Silver DB.
    """
    try:
        with sqlite3.connect(SILVER_DB) as conn:
            products_table = pd.read_sql_query("SELECT * FROM products;", conn)

        fake_sales_df = generate_fake_sales(products_table, n_sales)
        insert_sales_into_db(fake_sales_df, "sales")
        logger.info("Fake sales pipeline complete")

    except sqlite3.Error as e:
        logger.error("Failed to read products table: %s", e, exc_info=True)
    except ValueError as e:
        logger.error("Sales generation failed: %s", e, exc_info=True)
