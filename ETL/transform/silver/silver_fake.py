from pathlib import Path
import pandas as pd
import sqlite3

CSV_PATH = Path.cwd() / "data" / "bronze" / "fakestoreapi.csv"
DB_PATH = Path.cwd() / "data" / "silver" / "silver_fakestore.db"

COLUMNS = ["id", "title", "category", "price", "rating"]
COLUMN_MAPPING = {"title": "product"}


def main():
    df = pd.read_csv(CSV_PATH, usecols=COLUMNS)
    df = df.rename(columns=COLUMN_MAPPING)

    with sqlite3.connect(DB_PATH) as conn:
        df.to_sql("silver_fakestore", conn, if_exists="replace", index=False)

    print("- Transformation complete")


if __name__ == "__main__":
    main()