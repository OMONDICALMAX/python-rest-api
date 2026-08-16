from unittest.mock import Mock, patch

from services.openfoodfacts import (
    get_product_by_barcode,
    search_product_by_name,
)

@patch("services.openfoodfacts.requests.get")
def test_get_product_by_barcode(mock_get):
    mock_response = Mock()

    mock_response.json.return_value = {
        "status": 1,
        "product": {
            "product_name": "Organic Almond Milk",
            "brands": "Silk",
            "ingredients_text": (
                "Filtered water, almonds, cane sugar"
            ),
            "categories": "Plant-based beverages"
        }
    }

    mock_response.raise_for_status.return_value = None

    mock_get.return_value = mock_response

    product = get_product_by_barcode("0123456789012")

    assert product["product_name"] == "Organic Almond Milk"
    assert product["brands"] == "Silk"

    mock_get.assert_called_once()

@patch("services.openfoodfacts.requests.get")
def test_search_product_by_name(mock_get):
    mock_response = Mock()

    mock_response.json.return_value = {
        "products": [
            {
                "product_name": "Organic Almond Milk",
                "brands": "Silk",
                "ingredients_text": (
                    "Filtered water, almonds, cane sugar"
                ),
                "categories": "Plant-based beverages"
            }
        ]
    }

    mock_response.raise_for_status.return_value = None

    mock_get.return_value = mock_response

    product = search_product_by_name("almond milk")

    assert product["product_name"] == "Organic Almond Milk"
    assert product["brands"] == "Silk"

    mock_get.assert_called_once()

@patch("services.openfoodfacts.requests.get")
def test_get_product_by_barcode_not_found(mock_get):
    mock_response = Mock()

    mock_response.json.return_value = {
        "status": 0
    }

    mock_response.raise_for_status.return_value = None

    mock_get.return_value = mock_response

    product = get_product_by_barcode("9999999999999")

    assert product is None

@patch("services.openfoodfacts.requests.get")
def test_search_product_by_name_not_found(mock_get):
    mock_response = Mock()

    mock_response.json.return_value = {
        "products": []
    }

    mock_response.raise_for_status.return_value = None

    mock_get.return_value = mock_response

    product = search_product_by_name("product-that-does-not-exist")

    assert product is None

@patch("services.openfoodfacts.requests.get")
def test_get_product_by_barcode_api_failure(mock_get):
    mock_get.side_effect = Exception("API unavailable")

    try:
        get_product_by_barcode("0123456789012")
    except Exception as error:
        assert str(error) == "API unavailable"

