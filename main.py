from subprocess import run


def main():
    run(["python3", "ETL/silver_logic.py"], check=True)
main()