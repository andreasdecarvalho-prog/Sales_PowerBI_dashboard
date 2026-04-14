import csv
from pathlib import Path
from requests import get

# Config
RAW_DATA_DIR = Path(__file__).parent.parent / "data" / "raw"
APIs = {
    "dummyjson": {"url": "https://dummyjson.com/products", "key": "products"},
    "fakestore": {"url": "https://fakestoreapi.com/products", "key": None},
}


def main():
    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)  # Create dir if missing

    for api_name, config in APIs.items():
        try:
            url = config["url"]
            data = extract(url)

            # Handle both API response structures
            if config["key"]:
                data = data[config["key"]]

            file_name = get_file_name_from_url(url)
            response_to_csv(data, file_name)
            print(f"Data extracted from {url}")

        except Exception as e:
            print(f"Error processing {api_name}: {e}")


def extract(url: str) -> dict | list:
    """Fetch JSON data from URL."""
    response = get(url, timeout=10)
    response.raise_for_status()  # Raises HTTPError for bad status
    return response.json()


def response_to_csv(data: list[dict], file_name: str) -> None:
    """Write list of dicts to CSV file."""
    if not data:
        print(f"Warning: No data to write for {file_name}")
        return

    file_path = RAW_DATA_DIR / f"{file_name}.csv"

    try:
        with open(file_path, "w", newline="", encoding="utf-8") as f:
            fieldnames = data[0].keys()
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
        print(f"Saved to {file_path}")
    except IOError as e:
        print(f"Failed to write CSV: {e}")
        raise


def get_file_name_from_url(url: str) -> str:
    """Extract domain name from URL."""
    return url.split("//")[1].split(".")[0]


if __name__ == "__main__":
    main()
