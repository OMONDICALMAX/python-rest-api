import argparse
import requests


BASE_URL = "http://127.0.0.1:5000"


def list_items():
    """Display all inventory items."""

    try:
        response = requests.get(
            f"{BASE_URL}/inventory",
            timeout=10
        )

        response.raise_for_status()

    except requests.RequestException as error:
        print(f"Error connecting to API: {error}")
        return

    items = response.json()

    if not items:
        print("Inventory is empty.")
        return

    for item in items:
        print(
            f"ID: {item['id']} | "
            f"Product: {item['product_name']} | "
            f"Brand: {item['brands']} | "
            f"Price: {item['price']} | "
            f"Stock: {item['stock']}"
        )


def get_item(item_id):
    """Display one inventory item."""

    try:
        response = requests.get(
            f"{BASE_URL}/inventory/{item_id}",
            timeout=10
        )

    except requests.RequestException as error:
        print(f"Error connecting to API: {error}")
        return

    if response.status_code == 404:
        print(f"Inventory item {item_id} was not found.")
        return

    try:
        response.raise_for_status()

    except requests.RequestException as error:
        print(f"API error: {error}")
        return

    item = response.json()

    print(f"ID: {item['id']}")
    print(f"Product: {item['product_name']}")
    print(f"Brand: {item['brands']}")
    print(f"Ingredients: {item['ingredients_text']}")
    print(f"Barcode: {item['barcode']}")
    print(f"Categories: {item['categories']}")
    print(f"Quantity: {item['quantity']}")
    print(f"Price: {item['price']}")
    print(f"Stock: {item['stock']}")


def add_item(product_name, brands, barcode, price, stock,
             ingredients_text="", categories="", quantity=""):
    """Add a new inventory item through the API."""

    payload = {
        "product_name": product_name,
        "brands": brands,
        "ingredients_text": ingredients_text,
        "barcode": barcode,
        "categories": categories,
        "quantity": quantity,
        "price": price,
        "stock": stock
    }

    try:
        response = requests.post(
            f"{BASE_URL}/inventory",
            json=payload,
            timeout=10
        )

        response.raise_for_status()

    except requests.RequestException as error:
        print(f"API error: {error}")

        if hasattr(error, "response") and error.response is not None:
            try:
                print(error.response.json())
            except ValueError:
                pass

        return

    item = response.json()

    print("Inventory item added successfully.")
    print(f"ID: {item['id']}")
    print(f"Product: {item['product_name']}")
    print(f"Price: {item['price']}")
    print(f"Stock: {item['stock']}")

def update_item(item_id, price=None, stock=None):
    """Update an inventory item's price or stock."""

    payload = {}

    if price is not None:
        payload["price"] = price

    if stock is not None:
        payload["stock"] = stock

    if not payload:
        print("Please provide either --price or --stock.")
        return

    try:
        response = requests.patch(
            f"{BASE_URL}/inventory/{item_id}",
            json=payload,
            timeout=10
        )

    except requests.RequestException as error:
        print(f"Error connecting to API: {error}")
        return

    if response.status_code == 404:
        print(f"Inventory item {item_id} was not found.")
        return

    if response.status_code == 400:
        try:
            error_data = response.json()
            print(f"Error: {error_data.get('error', 'Invalid data.')}")
        except ValueError:
            print("Error: Invalid data.")
        return

    try:
        response.raise_for_status()

    except requests.RequestException as error:
        print(f"API error: {error}")
        return

    item = response.json()

    print("Inventory item updated successfully.")
    print(f"ID: {item['id']}")
    print(f"Product: {item['product_name']}")
    print(f"Price: {item['price']}")
    print(f"Stock: {item['stock']}")

def delete_item(item_id):
    """Delete an inventory item through the API."""

    try:
        response = requests.delete(
            f"{BASE_URL}/inventory/{item_id}",
            timeout=10
        )

    except requests.RequestException as error:
        print(f"Error connecting to API: {error}")
        return

    if response.status_code == 404:
        print(f"Inventory item {item_id} was not found.")
        return

    try:
        response.raise_for_status()

    except requests.RequestException as error:
        print(f"API error: {error}")
        return

    print(f"Inventory item {item_id} deleted successfully.")

def find_item_by_barcode(barcode):
    """Find a product on OpenFoodFacts using its barcode."""

    try:
        response = requests.get(
            f"{BASE_URL}/products/barcode/{barcode}",
            timeout=10
        )

    except requests.RequestException as error:
        print(f"Error connecting to API: {error}")
        return

    if response.status_code == 404:
        print("Product was not found on OpenFoodFacts.")
        return

    if response.status_code == 502:
        print("OpenFoodFacts is currently unavailable.")
        return

    try:
        response.raise_for_status()

    except requests.RequestException as error:
        print(f"API error: {error}")
        return

    product = response.json()

    print("Product found on OpenFoodFacts.")
    print(f"Product: {product.get('product_name', 'N/A')}")
    print(f"Brand: {product.get('brands', 'N/A')}")
    print(
        f"Ingredients: "
        f"{product.get('ingredients_text', 'N/A')}"
    )
    print(f"Barcode: {barcode}")
    print(f"Categories: {product.get('categories', 'N/A')}")
    print(f"Quantity: {product.get('quantity', 'N/A')}")

def find_item_by_name(product_name):
    """Find a product on OpenFoodFacts using its name."""

    try:
        response = requests.get(
            f"{BASE_URL}/products/search",
            params={"name": product_name},
            timeout=10
        )

    except requests.RequestException as error:
        print(f"Error connecting to API: {error}")
        return

    if response.status_code == 404:
        print("Product was not found on OpenFoodFacts.")
        return

    if response.status_code == 502:
        print("OpenFoodFacts is currently unavailable.")
        return

    try:
        response.raise_for_status()

    except requests.RequestException as error:
        print(f"API error: {error}")
        return

    product = response.json()

    print("Product found on OpenFoodFacts.")
    print(f"Product: {product.get('product_name', 'N/A')}")
    print(f"Brand: {product.get('brands', 'N/A')}")
    print(
        f"Ingredients: "
        f"{product.get('ingredients_text', 'N/A')}"
    )
    print(f"Barcode: {product.get('code', 'N/A')}")
    print(f"Categories: {product.get('categories', 'N/A')}")
    print(f"Quantity: {product.get('quantity', 'N/A')}")

def import_item(barcode=None, product_name=None,
                price=None, stock=None):
    """Import an OpenFoodFacts product into inventory."""

    payload = {
        "price": price,
        "stock": stock
    }

    if barcode:
        payload["barcode"] = barcode
    elif product_name:
        payload["product_name"] = product_name
    else:
        print("Provide either --barcode or --name.")
        return

    try:
        response = requests.post(
            f"{BASE_URL}/inventory/import",
            json=payload,
            timeout=15
        )

    except requests.RequestException as error:
        print(f"Error connecting to API: {error}")
        return

    if response.status_code == 404:
        print("Product was not found on OpenFoodFacts.")
        return

    if response.status_code == 409:
        print("Product already exists in inventory.")
        return

    if response.status_code == 502:
        print("OpenFoodFacts is currently unavailable.")
        return

    if response.status_code == 400:
        try:
            error_data = response.json()
            print(
                f"Error: "
                f"{error_data.get('error', 'Invalid request.')}"
            )
        except ValueError:
            print("Error: Invalid request.")

        return

    try:
        response.raise_for_status()

    except requests.RequestException as error:
        print(f"API error: {error}")
        return

    data = response.json()
    item = data["item"]

    print("Product imported successfully.")
    print(f"ID: {item['id']}")
    print(f"Product: {item['product_name']}")
    print(f"Brand: {item['brands']}")
    print(f"Barcode: {item['barcode']}")
    print(f"Price: {item['price']}")
    print(f"Stock: {item['stock']}")

def main():
    parser = argparse.ArgumentParser(
        description="Inventory Management CLI"
    )

    subparsers = parser.add_subparsers(
        dest="command"
    )

    # List items
    subparsers.add_parser(
        "list-items",
        help="Display all inventory items"
    )

    # Get one item
    get_parser = subparsers.add_parser(
        "get-item",
        help="Display one inventory item"
    )

    get_parser.add_argument(
        "--id",
        type=int,
        required=True,
        help="Inventory item ID"
    )

    # Add item
    add_parser = subparsers.add_parser(
        "add-item",
        help="Add a new inventory item"
    )

    add_parser.add_argument(
        "--product-name",
        required=True,
        help="Product name"
    )

    add_parser.add_argument(
        "--brands",
        required=True,
        help="Product brand"
    )

    add_parser.add_argument(
        "--barcode",
        required=True,
        help="Product barcode"
    )

    add_parser.add_argument(
        "--price",
        type=float,
        required=True,
        help="Product price"
    )

    add_parser.add_argument(
        "--stock",
        type=int,
        required=True,
        help="Available stock"
    )

    add_parser.add_argument(
        "--ingredients",
        default="",
        help="Product ingredients"
    )

    add_parser.add_argument(
        "--categories",
        default="",
        help="Product categories"
    )

    add_parser.add_argument(
        "--quantity",
        default="",
        help="Product quantity"
    )
        # Update item
    update_parser = subparsers.add_parser(
        "update-item",
        help="Update an inventory item's price or stock"
    )

    update_parser.add_argument(
        "--id",
        type=int,
        required=True,
        help="Inventory item ID"
    )

    update_parser.add_argument(
        "--price",
        type=float,
        help="New product price"
    )

    update_parser.add_argument(
        "--stock",
        type=int,
        help="New stock level"
    )
        # Delete item
    delete_parser = subparsers.add_parser(
        "delete-item",
        help="Delete an inventory item"
    )

    delete_parser.add_argument(
        "--id",
        type=int,
        required=True,
        help="Inventory item ID"
    )
        # Find product on OpenFoodFacts
    find_parser = subparsers.add_parser(
        "find-item",
        help="Find a product on OpenFoodFacts"
    )

    search_group = find_parser.add_mutually_exclusive_group(
        required=True
    )

    search_group.add_argument(
        "--barcode",
        help="Search using a product barcode"
    )

    search_group.add_argument(
        "--name",
        help="Search using a product name"
    )
        # Import product from OpenFoodFacts
    import_parser = subparsers.add_parser(
        "import-item",
        help="Import a product from OpenFoodFacts"
    )

    import_group = import_parser.add_mutually_exclusive_group(
        required=True
    )

    import_group.add_argument(
        "--barcode",
        help="OpenFoodFacts product barcode"
    )

    import_group.add_argument(
        "--name",
        help="OpenFoodFacts product name"
    )

    import_parser.add_argument(
        "--price",
        type=float,
        required=True,
        help="Inventory price"
    )

    import_parser.add_argument(
        "--stock",
        type=int,
        required=True,
        help="Inventory stock"
    )

    args = parser.parse_args()

    if args.command == "list-items":
        list_items()

    elif args.command == "get-item":
        get_item(args.id)

    elif args.command == "add-item":
        add_item(
            args.product_name,
            args.brands,
            args.barcode,
            args.price,
            args.stock,
            args.ingredients,
            args.categories,
            args.quantity
        )

    elif args.command == "add-item":
        add_item(
            args.product_name,
            args.brands,
            args.barcode,
            args.price,
            args.stock,
            args.ingredients,
            args.categories,
            args.quantity
        )

    elif args.command == "update-item":
        update_item(
            args.id,
            args.price,
            args.stock
        )
    elif args.command == "find-item":
        if args.barcode:
            find_item_by_barcode(args.barcode)

        elif args.name:
            find_item_by_name(args.name)

    elif args.command == "delete-item":
        delete_item(args.id)
    elif args.command == "import-item":
        import_item(
            barcode=args.barcode,
            product_name=args.name,
            price=args.price,
            stock=args.stock
        )

if __name__ == "__main__":
    main()