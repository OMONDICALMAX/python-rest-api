import requests


BASE_URL = "https://world.openfoodfacts.org"

HEADERS = {
    "User-Agent": "InventoryManagementSystem/1.0 (Educational Project)"
}


class OpenFoodFactsAPIError(Exception):
    """Raised when the OpenFoodFacts API cannot be reached."""
    pass


def get_product_by_barcode(barcode):
    """Fetch product information using a barcode."""

    url = f"{BASE_URL}/api/v3/product/{barcode}"

    try:
        response = requests.get(
            url,
            headers=HEADERS,
            timeout=10
        )
        response.raise_for_status()

    except requests.RequestException as error:
        raise OpenFoodFactsAPIError(
            f"OpenFoodFacts API request failed: {error}"
        ) from error

    data = response.json()

    if data.get("status") != 1:
        return None

    return data.get("product")


def search_product_by_name(product_name):
    """Search OpenFoodFacts using a product name."""

    url = f"{BASE_URL}/cgi/search.pl"

    params = {
        "search_terms": product_name,
        "search_simple": 1,
        "action": "process",
        "json": 1,
        "page_size": 10
    }

    try:
        response = requests.get(
            url,
            params=params,
            headers=HEADERS,
            timeout=10
        )
        response.raise_for_status()

    except requests.RequestException as error:
        raise OpenFoodFactsAPIError(
            f"OpenFoodFacts API request failed: {error}"
        ) from error

    data = response.json()

    products = data.get("products", [])

    if not products:
        return None

    return products[0]