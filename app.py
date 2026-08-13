from flask import Flask, jsonify, request

app = Flask(__name__)


# Simulated inventory database
inventory = [
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

def find_inventory_item(item_id):
    """Find an inventory item by its ID."""
    for item in inventory:
        if item["id"] == item_id:
            return item

    return None


@app.route("/inventory", methods=["GET"])
def get_inventory():
    return inventory


@app.route("/inventory/<int:item_id>", methods=["GET"])
def get_inventory_item(item_id):
    item = find_inventory_item(item_id)

    if item is None:
        return jsonify({
            "error": "Inventory item not found"
        }), 404

    return jsonify(item), 200

@app.route("/inventory", methods=["POST"])
def create_inventory_item():
    data = request.get_json(silent=True)

    if not data:
        return jsonify({
            "error": "Request body must contain JSON data"
        }), 400

    required_fields = [
        "product_name",
        "brands",
        "ingredients_text",
        "barcode",
        "categories",
        "quantity",
        "price",
        "stock"
    ]

    missing_fields = [
        field for field in required_fields
        if field not in data
    ]

    if missing_fields:
        return jsonify({
            "error": "Missing required fields",
            "fields": missing_fields
        }), 400

    try:
        price = float(data["price"])
        stock = int(data["stock"])
    except (ValueError, TypeError):
        return jsonify({
            "error": "Price must be a number and stock must be an integer"
        }), 400

    if price < 0:
        return jsonify({
            "error": "Price cannot be negative"
        }), 400

    if stock < 0:
        return jsonify({
            "error": "Stock cannot be negative"
        }), 400

    for item in inventory:
        if item["barcode"] == data["barcode"]:
            return jsonify({
                "error": "An inventory item with this barcode already exists"
            }), 409

    new_id = max(
        [item["id"] for item in inventory],
        default=0
    ) + 1

    new_item = {
        "id": new_id,
        "product_name": data["product_name"],
        "brands": data["brands"],
        "ingredients_text": data["ingredients_text"],
        "barcode": data["barcode"],
        "categories": data["categories"],
        "quantity": data["quantity"],
        "price": price,
        "stock": stock
    }

    inventory.append(new_item)

    return jsonify(new_item), 201

    return jsonify(new_item), 201

@app.route("/inventory/<int:item_id>", methods=["PATCH"])
def update_inventory_item(item_id):
    data = request.get_json(silent=True)

    if not data:
        return jsonify({
            "error": "Request body must contain JSON data"
        }), 400

    allowed_fields = [
        "product_name",
        "brands",
        "ingredients_text",
        "barcode",
        "categories",
        "quantity",
        "price",
        "stock"
    ]

    invalid_fields = [
        field for field in data
        if field not in allowed_fields
    ]

    if invalid_fields:
        return jsonify({
            "error": "Invalid fields",
            "fields": invalid_fields
        }), 400

    item = find_inventory_item(item_id)

    if item is None:
        return jsonify({
            "error": "Inventory item not found"
        }), 404

    updated_values = {}

    if "price" in data:
        try:
            price = float(data["price"])
        except (ValueError, TypeError):
            return jsonify({
                "error": "Price must be a number"
            }), 400

        if price < 0:
            return jsonify({
                "error": "Price cannot be negative"
            }), 400

        updated_values["price"] = price

    if "stock" in data:
        try:
            stock = int(data["stock"])
        except (ValueError, TypeError):
            return jsonify({
                "error": "Stock must be an integer"
            }), 400

        if stock < 0:
            return jsonify({
                "error": "Stock cannot be negative"
            }), 400

        updated_values["stock"] = stock

    if "barcode" in data:
        for existing_item in inventory:
            if (
                existing_item["id"] != item_id
                and existing_item["barcode"] == data["barcode"]
            ):
                return jsonify({
                    "error": "An inventory item with this barcode already exists"
                }), 409

    for field in allowed_fields:
        if field in data and field not in ["price", "stock"]:
            updated_values[field] = data[field]

    item.update(updated_values)

    return jsonify(item), 200

@app.route("/inventory/<int:item_id>", methods=["DELETE"])
def delete_inventory_item(item_id):
    item = find_inventory_item(item_id)

    if item is None:
        return jsonify({
            "error": "Inventory item not found"
        }), 404

    inventory.remove(item)

    return jsonify({
        "message": "Inventory item deleted successfully",
        "item": item
    }), 200

if __name__ == "__main__":
    app.run(debug=True)