from pathlib import Path

# Base directories
BASE_DIR = Path.cwd()
DATA_DIR = BASE_DIR / "data"
BRONZE_DIR = DATA_DIR / "bronze"
GOLD_DIR = DATA_DIR / "gold"


# Ensure directories exist
for d in [DATA_DIR, BRONZE_DIR, GOLD_DIR]:
    d.mkdir(parents=True, exist_ok=True)

# API endpoints
APIS = {
    "dummyjson": {"url": "https://dummyjson.com/products", "key": "products"},
    "fakestore": {"url": "https://fakestoreapi.com/products", "key": None},
}

# Database
GOLD_DB = GOLD_DIR / "products.db"

# Settings
REQUEST_TIMEOUT = 10
CSV_ENCODING = "utf-8"

