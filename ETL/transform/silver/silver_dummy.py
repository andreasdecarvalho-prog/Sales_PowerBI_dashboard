import helper_functions as hf

FILE_NAME = "dummy"
CSV_PATH, DB_PATH = hf.get_csv_and_db_path(FILE_NAME)
COLUMNS = hf.COLUMNS
COLUMN_MAPPING = hf.COLUMN_MAPPING


def main():
    hf.silver_store_logic(CSV_PATH, DB_PATH, FILE_NAME)


if __name__ == "__main__":
    main()