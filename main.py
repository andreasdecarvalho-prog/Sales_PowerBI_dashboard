from ETL.bronze.extract import extract_to_csv
from ETL.silver.fakestore import transform_fakestore
from ETL.silver.dummy import transform_dummy
from ETL.gold.gold_csv import df_to_gold_csv
from ETL.silver.silver_functions import products_dfs_to_db
from ETL.gen_fake_sales import fake_sales
from ETL.deliver import send_data_email

def main():
    # get data
    raw_files = extract_to_csv()
    gold_files = []


    # transform data
    dfs = []
    dfs.append(transform_dummy(raw_files[0]))
    dfs.append(transform_fakestore(raw_files[1]))
    

    # create csv files with parsed data
    for file_name, df in zip(raw_files, dfs):
        gold_files.append(df_to_gold_csv(df, file_name))


    # create silver_products db with already parsed data that is still dfs
    gold_files.append(products_dfs_to_db(raw_files, dfs))


    # generate fake sales data into sales table
    gold_files.append(fake_sales())

    # send email with csv files and db file
    send_data_email(gold_files)


if __name__ == "__main__":
    main()
