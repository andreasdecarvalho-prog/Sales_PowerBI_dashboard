from ETL.extract import extract_to_csv
from ETL.silver.fakestore import transform_fakestore
from ETL.silver.dummy import transform_dummy
from ETL.silver.silver_logic import products_dfs_to_db

def main():

    # get data
    file_names = extract_to_csv()


    # transform data
    dfs = []
    dfs.append(transform_dummy(file_names[0]))
    dfs.append(transform_fakestore(file_names[1]))
    
    
    # create silver_products db with already parsed data that is still dfs
    products_dfs_to_db(file_names, dfs)


    # generate fake sales data into sales table
    ...


    # 















main()