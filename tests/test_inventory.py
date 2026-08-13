import pytest

from app import app, inventory


@pytest.fixture
def client():
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client


@pytest.fixture(autouse=True)
def reset_inventory():
    original_inventory = [
        {
            "id": 1,
            "product_name": "Organic Almond Milk",
            "brands": "Silk",
            "ingredients_text": "Filtered water, almonds, cane sugar",
            "barcode": "0123456789012",
            "categories": "Plant-based beverages",
            "quantity": "1 L",
            "price": 450.00,
            "stock": 20
        },
        {
            "id": 2,
            "product_name": "Whole Grain Bread",
            "brands": "Nature's Own",
            "ingredients_text": "Whole wheat flour, water, yeast, salt",
            "barcode": "0123456789013",
            "categories": "Bakery products",
            "quantity": "600 g",
            "price": 180.00,
            "stock": 15
        },
        {
            "id": 3,
            "product_name": "Organic Peanut Butter",
            "brands": "Kirkland",
            "ingredients_text": "Roasted peanuts, salt",
            "barcode": "0123456789014",
            "categories": "Spreads",
            "quantity": "500 g",
            "price": 650.00,
            "stock": 8
        }
    ]

    inventory.clear()
    inventory.extend(original_inventory)

    yield

    inventory.clear()
    inventory.extend(original_inventory)


def test_get_inventory(client):
    response = client.get("/inventory")

    assert response.status_code == 200

    data = response.get_json()

    assert isinstance(data, list)
    assert len(data) == 3


def test_get_inventory_item(client):
    response = client.get("/inventory/1")

    assert response.status_code == 200

    data = response.get_json()

    assert data["id"] == 1
    assert data["product_name"] == "Organic Almond Milk"


def test_get_inventory_item_not_found(client):
    response = client.get("/inventory/999")

    assert response.status_code == 404

    data = response.get_json()

    assert data["error"] == "Inventory item not found"


def test_create_inventory_item(client):
    new_item = {
        "product_name": "Oat Milk",
        "brands": "Oatly",
        "ingredients_text": "Water, oats, rapeseed oil, salt",
        "barcode": "0123456789015",
        "categories": "Plant-based beverages",
        "quantity": "1 L",
        "price": 520.00,
        "stock": 12
    }

    response = client.post("/inventory", json=new_item)

    assert response.status_code == 201

    data = response.get_json()

    assert data["id"] == 4
    assert data["product_name"] == "Oat Milk"
    assert data["price"] == 520.00
    assert data["stock"] == 12


def test_create_inventory_item_missing_fields(client):
    response = client.post(
        "/inventory",
        json={
            "product_name": "Incomplete Product"
        }
    )

    assert response.status_code == 400

    data = response.get_json()

    assert data["error"] == "Missing required fields"
    assert "price" in data["fields"]
    assert "stock" in data["fields"]


def test_create_inventory_item_duplicate_barcode(client):
    duplicate_item = {
        "product_name": "Duplicate Almond Milk",
        "brands": "Test Brand",
        "ingredients_text": "Water, almonds",
        "barcode": "0123456789012",
        "categories": "Beverages",
        "quantity": "1 L",
        "price": 500,
        "stock": 10
    }

    response = client.post(
        "/inventory",
        json=duplicate_item
    )

    assert response.status_code == 409

    data = response.get_json()

    assert data["error"] == (
        "An inventory item with this barcode already exists"
    )


def test_update_inventory_price(client):
    response = client.patch(
        "/inventory/1",
        json={
            "price": 500
        }
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["id"] == 1
    assert data["price"] == 500.0
    assert data["stock"] == 20


def test_update_inventory_stock(client):
    response = client.patch(
        "/inventory/1",
        json={
            "stock": 35
        }
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["stock"] == 35
    assert data["price"] == 450.0


def test_update_inventory_item_not_found(client):
    response = client.patch(
        "/inventory/999",
        json={
            "price": 500
        }
    )

    assert response.status_code == 404

    data = response.get_json()

    assert data["error"] == "Inventory item not found"


def test_update_inventory_invalid_price(client):
    response = client.patch(
        "/inventory/1",
        json={
            "price": -100
        }
    )

    assert response.status_code == 400

    data = response.get_json()

    assert data["error"] == "Price cannot be negative"


def test_delete_inventory_item(client):
    response = client.delete("/inventory/3")

    assert response.status_code == 200

    data = response.get_json()

    assert data["message"] == "Inventory item deleted successfully"
    assert data["item"]["id"] == 3

    get_response = client.get("/inventory/3")

    assert get_response.status_code == 404


def test_delete_inventory_item_not_found(client):
    response = client.delete("/inventory/999")

    assert response.status_code == 404

    data = response.get_json()

    assert data["error"] == "Inventory item not found"