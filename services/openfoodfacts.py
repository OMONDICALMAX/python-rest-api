import requests


BASE_URL = "https://world.openfoodfacts.org"


def get_product_by_barcode(barcode):
    """Fetch product information from OpenFoodFacts using a barcode."""

    url = f"{BASE_URL}/api/v2/product/{barcode}.json"

    response = requests.get(url, timeout=10)

    response.raise_for_status()

    data = response.json()

    if data.get("status") != 1:
        return None

    return data.get("product")