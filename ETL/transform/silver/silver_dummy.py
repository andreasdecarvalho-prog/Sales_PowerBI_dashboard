import pandas as pd
import sqlite3

# reads into dummy csv file, selects wich columns will stay, parse data and writes to new sqlite db
def main():
    cols = ["id", 
        "title", 
        "category", 
        "price", 
        "rating", 
        "stock", 
        "brand", 
        "availabilityStatus",
        ]

    products = pd.read_csv("/Users/camelo/power_bi?/data/bronze/dummyjson.csv", usecols=cols)


    pd.set_option("display.max_columns", None)

    # renaming columns for better readabilty
    products = products.rename(columns={
        "title": "product",
        "availabilityStatus": "availability",
    })

    conn = sqlite3.connect("products.db")
    cur = conn.cursor()



    products.to_sql("products", conn, if_exists="replace", index=False)

  



if __name__ == "__main__":
    main()









