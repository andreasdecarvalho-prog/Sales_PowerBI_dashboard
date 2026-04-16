from subprocess import run

def main():
    run(["python3", "ETL/extract.py"], check=True)
    run(["python3", "ETL/transform/silver/silver_logic.py"], check=True)

main()