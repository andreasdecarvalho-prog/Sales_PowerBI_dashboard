import csv
from requests import get, RequestException
from core.logger import logger
from core.config import BRONZE_DIR, APIS, REQUEST_TIMEOUT, CSV_ENCODING

FILE_NAMES: list[str] = []


def extract_to_csv() -> list[str]:
    """
    Extract raw data from APIs and save to CSV files.
    Returns a list of generated file names.
    """
    BRONZE_DIR.mkdir(parents=True, exist_ok=True)

    for api_name, config in APIS.items():
        url = config["url"]
        try:
            data = fetch_data(url)

            if config["key"]:
                data = data.get(config["key"], [])
                if not data:
                    logger.warning("No data found under key '%s' for %s", config["key"], api_name)

            file_name = get_file_name_from_url(url)
            FILE_NAMES.append(file_name)

            response_to_csv(data, file_name)
            logger.debug("Successfully processed %s → %s.csv", api_name, file_name)

        except Exception as e:
            logger.error("Error processing %s: %s", api_name, e, exc_info=True)

    logger.info("Extraction complete")
    return FILE_NAMES


def fetch_data(url: str) -> dict | list:
    """Fetch JSON data from URL with error handling."""
    try:
        response = get(url, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        return response.json()
    except RequestException as e:
        logger.error("Failed to fetch data from %s: %s", url, e)
        raise


def response_to_csv(data: list[dict], file_name: str) -> None:
    """Write list of dicts to CSV file."""
    if not data:
        logger.warning("No data to write for %s", file_name)
        return

    file_path = BRONZE_DIR / f"{file_name}.csv"

    try:
        with open(file_path, "w", newline="", encoding=CSV_ENCODING) as f:
            fieldnames = data[0].keys()
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
    except IOError as e:
        logger.error("Failed to write CSV %s: %s", file_path, e)
        raise


def get_file_name_from_url(url: str) -> str:
    """Extract domain name from URL."""
    try:
        return url.split("//")[1].split(".")[0]
    except IndexError:
        logger.warning("Could not parse file name from URL: %s", url)
        return "unknown"


