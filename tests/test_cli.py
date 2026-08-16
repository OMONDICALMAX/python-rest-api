from unittest.mock import Mock, patch

import cli


@patch("cli.requests.get")
def test_list_items(mock_get, capsys):
    mock_response = Mock()
    mock_response.status_code = 200

    mock_response.json.return_value = [
        {
            "id": 1,
            "product_name": "Organic Almond Milk",
            "brands": "Silk",
            "price": 450.0,
            "stock": 20
        },
        {
            "id": 2,
            "product_name": "Whole Grain Bread",
            "brands": "Nature's Own",
            "price": 180.0,
            "stock": 15
        }
    ]

    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    cli.list_items()

    captured = capsys.readouterr()

    assert "Organic Almond Milk" in captured.out
    assert "Whole Grain Bread" in captured.out

    mock_get.assert_called_once_with(
        f"{cli.BASE_URL}/inventory",
        timeout=10
    )


@patch("cli.requests.get")
def test_get_item(mock_get, capsys):
    mock_response = Mock()
    mock_response.status_code = 200

    mock_response.json.return_value = {
        "id": 1,
        "product_name": "Organic Almond Milk",
        "brands": "Silk",
        "ingredients_text": "Filtered water, almonds, cane sugar",
        "barcode": "0123456789012",
        "categories": "Plant-based beverages",
        "quantity": "1 L",
        "price": 450.0,
        "stock": 20
    }

    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    cli.get_item(1)

    captured = capsys.readouterr()

    assert "Organic Almond Milk" in captured.out
    assert "Silk" in captured.out
    assert "450.0" in captured.out
    assert "20" in captured.out

    mock_get.assert_called_once_with(
        f"{cli.BASE_URL}/inventory/1",
        timeout=10
    )


@patch("cli.requests.get")
def test_get_item_not_found(mock_get, capsys):
    mock_response = Mock()
    mock_response.status_code = 404

    mock_get.return_value = mock_response

    cli.get_item(999)

    captured = capsys.readouterr()

    assert "Inventory item 999 was not found." in captured.out


@patch("cli.requests.post")
def test_add_item(mock_post, capsys):
    mock_response = Mock()
    mock_response.status_code = 201

    mock_response.json.return_value = {
        "id": 4,
        "product_name": "Chocolate Milk",
        "brands": "Test Brand",
        "barcode": "9999999999999",
        "price": 300.0,
        "stock": 12
    }

    mock_response.raise_for_status.return_value = None
    mock_post.return_value = mock_response

    cli.add_item(
        "Chocolate Milk",
        "Test Brand",
        "9999999999999",
        300,
        12,
        "Milk, cocoa, sugar",
        "Dairy beverages",
        "500 ml"
    )

    captured = capsys.readouterr()

    assert "Inventory item added successfully." in captured.out
    assert "Chocolate Milk" in captured.out
    assert "300.0" in captured.out
    assert "12" in captured.out

    mock_post.assert_called_once_with(
        f"{cli.BASE_URL}/inventory",
        json={
            "product_name": "Chocolate Milk",
            "brands": "Test Brand",
            "ingredients_text": "Milk, cocoa, sugar",
            "barcode": "9999999999999",
            "categories": "Dairy beverages",
            "quantity": "500 ml",
            "price": 300,
            "stock": 12
        },
        timeout=10
    )


@patch("cli.requests.patch")
def test_update_item(mock_patch, capsys):
    mock_response = Mock()
    mock_response.status_code = 200

    mock_response.json.return_value = {
        "id": 1,
        "product_name": "Organic Almond Milk",
        "brands": "Silk",
        "price": 500.0,
        "stock": 25
    }

    mock_response.raise_for_status.return_value = None
    mock_patch.return_value = mock_response

    cli.update_item(
        item_id=1,
        price=500,
        stock=25
    )

    captured = capsys.readouterr()

    assert "Inventory item updated successfully." in captured.out
    assert "500.0" in captured.out
    assert "25" in captured.out

    mock_patch.assert_called_once_with(
        f"{cli.BASE_URL}/inventory/1",
        json={
            "price": 500,
            "stock": 25
        },
        timeout=10
    )


@patch("cli.requests.delete")
def test_delete_item(mock_delete, capsys):
    mock_response = Mock()
    mock_response.status_code = 200

    mock_response.raise_for_status.return_value = None
    mock_delete.return_value = mock_response

    cli.delete_item(4)

    captured = capsys.readouterr()

    assert "Inventory item 4 deleted successfully." in captured.out

    mock_delete.assert_called_once_with(
        f"{cli.BASE_URL}/inventory/4",
        timeout=10
    )


@patch("cli.requests.get")
def test_find_item_by_barcode(mock_get, capsys):
    mock_response = Mock()
    mock_response.status_code = 200

    mock_response.json.return_value = {
        "product_name": "Organic Almond Milk",
        "brands": "Silk",
        "ingredients_text": "Filtered water, almonds, cane sugar",
        "categories": "Plant-based beverages",
        "quantity": "1 L"
    }

    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    cli.find_item_by_barcode("0123456789012")

    captured = capsys.readouterr()

    assert "Product found on OpenFoodFacts." in captured.out
    assert "Organic Almond Milk" in captured.out
    assert "Silk" in captured.out

    mock_get.assert_called_once_with(
        f"{cli.BASE_URL}/products/barcode/0123456789012",
        timeout=10
    )


@patch("cli.requests.get")
def test_find_item_by_name(mock_get, capsys):
    mock_response = Mock()
    mock_response.status_code = 200

    mock_response.json.return_value = {
        "product_name": "Organic Almond Milk",
        "brands": "Silk",
        "ingredients_text": "Filtered water, almonds, cane sugar",
        "categories": "Plant-based beverages",
        "quantity": "1 L",
        "code": "0123456789012"
    }

    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    cli.find_item_by_name("almond milk")

    captured = capsys.readouterr()

    assert "Product found on OpenFoodFacts." in captured.out
    assert "Organic Almond Milk" in captured.out

    mock_get.assert_called_once_with(
        f"{cli.BASE_URL}/products/search",
        params={"name": "almond milk"},
        timeout=10
    )


@patch("cli.requests.get")
def test_find_item_by_barcode_api_failure(mock_get, capsys):
    mock_response = Mock()
    mock_response.status_code = 502

    mock_get.return_value = mock_response

    cli.find_item_by_barcode("0123456789012")

    captured = capsys.readouterr()

    assert "OpenFoodFacts is currently unavailable." in captured.out

@patch("cli.requests.post")
def test_import_item_by_barcode(mock_post, capsys):
    mock_response = Mock()
    mock_response.status_code = 201

    mock_response.json.return_value = {
        "item": {
            "id": 4,
            "product_name": "Organic Almond Milk",
            "brands": "Silk",
            "barcode": "0123456789012",
            "price": 500.0,
            "stock": 10
        }
    }

    mock_response.raise_for_status.return_value = None
    mock_post.return_value = mock_response

    cli.import_item(
        barcode="0123456789012",
        price=500,
        stock=10
    )

    captured = capsys.readouterr()

    assert "Product imported successfully." in captured.out
    assert "Organic Almond Milk" in captured.out
    assert "Silk" in captured.out
    assert "500.0" in captured.out
    assert "10" in captured.out

    mock_post.assert_called_once_with(
        f"{cli.BASE_URL}/inventory/import",
        json={
            "barcode": "0123456789012",
            "price": 500,
            "stock": 10
        },
        timeout=15
    )

@patch("cli.requests.post")
def test_import_item_by_name(mock_post, capsys):
    mock_response = Mock()
    mock_response.status_code = 201

    mock_response.json.return_value = {
        "item": {
            "id": 5,
            "product_name": "Organic Almond Milk",
            "brands": "Silk",
            "barcode": "0123456789012",
            "price": 550.0,
            "stock": 15
        }
    }

    mock_response.raise_for_status.return_value = None
    mock_post.return_value = mock_response

    cli.import_item(
        product_name="almond milk",
        price=550,
        stock=15
    )

    captured = capsys.readouterr()

    assert "Product imported successfully." in captured.out
    assert "Organic Almond Milk" in captured.out
    assert "550.0" in captured.out
    assert "15" in captured.out

    mock_post.assert_called_once_with(
        f"{cli.BASE_URL}/inventory/import",
        json={
            "product_name": "almond milk",
            "price": 550,
            "stock": 15
        },
        timeout=15
    )

@patch("cli.requests.post")
def test_import_item_not_found(mock_post, capsys):
    mock_response = Mock()
    mock_response.status_code = 404

    mock_post.return_value = mock_response

    cli.import_item(
        barcode="0000000000000",
        price=500,
        stock=10
    )

    captured = capsys.readouterr()

    assert "Product was not found on OpenFoodFacts." in captured.out

@patch("cli.requests.post")
def test_import_item_api_failure(mock_post, capsys):
    mock_response = Mock()
    mock_response.status_code = 502

    mock_post.return_value = mock_response

    cli.import_item(
        barcode="0123456789012",
        price=500,
        stock=10
    )

    captured = capsys.readouterr()

    assert "OpenFoodFacts is currently unavailable." in captured.out