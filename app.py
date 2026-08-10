from flask import Flask

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


if __name__ == "__main__":
    app.run(debug=True)