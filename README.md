# Inventory Management System

A Flask-based REST API and command-line inventory management system developed for a small retail business.

The application provides complete CRUD functionality for inventory management and integrates with the OpenFoodFacts API to retrieve real-world product information by barcode or product name. It also includes a CLI client, a web interface, error handling, and an automated test suite.

---

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Project Structure](#project-structure)
- [Installation and Setup](#installation-and-setup)
- [Running the Application](#running-the-application)
- [REST API Documentation](#rest-api-documentation)
- [OpenFoodFacts Integration](#openfoodfacts-integration)
- [CLI Documentation](#cli-documentation)
- [Web Interface](#web-interface)
- [Testing](#testing)
- [Error Handling](#error-handling)
- [Data Storage](#data-storage)
- [Git Workflow](#git-workflow)
- [Project Requirements](#project-requirements)
- [Future Improvements](#future-improvements)
- [Author](#author)

---

## Project Overview

The Inventory Management System is an administrator-focused application designed to help a small retail business manage its products.

The system provides a Flask REST API that allows administrators to:

- View all inventory items
- View individual inventory items
- Add new inventory items
- Update inventory prices and stock levels
- Delete inventory items
- Search for products using OpenFoodFacts
- Import product information from OpenFoodFacts
- Manage inventory through a command-line interface

For this project, a Python list is used as simulated database storage, as required by the assignment.

---

## Features

### Inventory Management

- Create inventory items
- Retrieve all inventory items
- Retrieve individual inventory items
- Update inventory items
- Delete inventory items
- Validate inventory data
- Prevent duplicate product barcodes
- Handle missing inventory items

### OpenFoodFacts Integration

- Search products by barcode
- Search products by product name
- Retrieve product information from OpenFoodFacts
- Import external product information into the inventory
- Handle external API failures
- Handle products that cannot be found

### Command-Line Interface

The CLI provides commands for:

- Listing inventory
- Viewing individual products
- Adding products
- Updating products
- Deleting products
- Searching OpenFoodFacts
- Importing OpenFoodFacts products

### Web Interface

The project also includes a simple web interface that allows users to interact with the inventory system through a browser.

### Testing

The project includes automated tests using:

- `pytest`
- `unittest.mock`

The tests cover:

- Flask API endpoints
- CRUD operations
- CLI commands
- OpenFoodFacts integration
- External API failures
- Invalid requests
- Product import functionality

---

## Technologies Used

| Technology | Purpose |
|---|---|
| Python 3.12 | Programming language |
| Flask 3.1.3 | REST API framework |
| Requests 2.34.2 | HTTP/API requests |
| Pytest 9.1.1 | Automated testing |
| unittest.mock | Mocking external requests |
| HTML | Web interface |
| CSS | Web interface styling |
| JavaScript | Web interface functionality |
| OpenFoodFacts API | External product data |
| Git | Version control |
| GitHub | Repository hosting |

---

## Project Structure

```text
python-rest-api/
│
├── app.py
├── cli.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── services/
│   ├── __init__.py
│   └── openfoodfacts.py
│
├── templates/
│   └── index.html
│
├── static/
│   ├── app.js
│   └── style.css
│
└── tests/
    ├── __init__.py
    ├── conftest.py
    ├── test_cli.py
    ├── test_external_api.py
    └── test_inventory.py
````

### File Responsibilities

#### `app.py`

Contains the Flask application, inventory routes, CRUD operations, OpenFoodFacts integration endpoints, and simulated inventory database.

#### `cli.py`

Contains the command-line client used to interact with the Flask REST API.

#### `services/openfoodfacts.py`

Contains the functions responsible for communicating with the OpenFoodFacts API.

#### `templates/index.html`

Contains the HTML structure for the web interface.

#### `static/app.js`

Contains the JavaScript responsible for interacting with the Flask API from the browser.

#### `static/style.css`

Contains styling for the web interface.

#### `tests/test_inventory.py`

Tests inventory CRUD functionality and inventory import functionality.

#### `tests/test_external_api.py`

Tests OpenFoodFacts API interactions using mocked responses.

#### `tests/test_cli.py`

Tests CLI commands and API interactions performed by the CLI.

#### `tests/conftest.py`

Contains shared pytest configuration and fixtures.

---

# Installation and Setup

## 1. Clone the Repository

Clone the GitHub repository:

```bash
git clone https://github.com/OMONDICALMAX/python-rest-api.git
```

Navigate into the project:

```bash
cd python-rest-api
```

---

## 2. Create a Virtual Environment

Create a Python virtual environment:

```bash
python3 -m venv venv
```

---

## 3. Activate the Virtual Environment

On Linux/WSL:

```bash
source venv/bin/activate
```

On Windows:

```powershell
venv\Scripts\activate
```

---

## 4. Install Dependencies

Install the required packages:

```bash
pip install -r requirements.txt
```

---

# Running the Application

Start the Flask application:

```bash
python app.py
```

The application will run on:

```text
http://127.0.0.1:5000
```

Flask debug mode is enabled during development.

---

# REST API Documentation

The application follows RESTful API conventions.

## Inventory Endpoints

| Method | Endpoint          | Description                  |
| ------ | ----------------- | ---------------------------- |
| GET    | `/inventory`      | Retrieve all inventory items |
| GET    | `/inventory/<id>` | Retrieve one inventory item  |
| POST   | `/inventory`      | Create a new inventory item  |
| PATCH  | `/inventory/<id>` | Update an inventory item     |
| DELETE | `/inventory/<id>` | Delete an inventory item     |

---

## GET `/inventory`

Returns all inventory items.

### Request

```bash
curl http://127.0.0.1:5000/inventory
```

### Response

```json
[
  {
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
]
```

---

## GET `/inventory/<id>`

Returns a single inventory item.

### Example

```bash
curl http://127.0.0.1:5000/inventory/1
```

---

## POST `/inventory`

Creates a new inventory item.

### Example

```bash
curl -X POST http://127.0.0.1:5000/inventory \
-H "Content-Type: application/json" \
-d '{
    "product_name": "Chocolate Milk",
    "brands": "Test Brand",
    "barcode": "9999999999999",
    "price": 300,
    "stock": 10
}'
```

Optional product information can also be provided:

```json
{
  "product_name": "Chocolate Milk",
  "brands": "Test Brand",
  "ingredients_text": "Milk, cocoa, sugar",
  "barcode": "9999999999999",
  "categories": "Dairy beverages",
  "quantity": "500 ml",
  "price": 300,
  "stock": 10
}
```

---

## PATCH `/inventory/<id>`

Updates an existing inventory item.

For example, to update price and stock:

```bash
curl -X PATCH http://127.0.0.1:5000/inventory/1 \
-H "Content-Type: application/json" \
-d '{
    "price": 500,
    "stock": 25
}'
```

The PATCH operation allows partial updates.

---

## DELETE `/inventory/<id>`

Deletes an inventory item.

### Example

```bash
curl -X DELETE http://127.0.0.1:5000/inventory/1
```

---

# OpenFoodFacts Integration

The application integrates with the OpenFoodFacts API to retrieve product information.

The external product information can be searched using:

* Barcode
* Product name

---

## Find Product by Barcode

### Endpoint

```text
GET /products/barcode/<barcode>
```

### Example

```bash
curl http://127.0.0.1:5000/products/barcode/<BARCODE>
```

The application retrieves product information and returns relevant fields such as:

* Product name
* Brand
* Ingredients
* Categories
* Quantity
* Barcode

---

## Find Product by Name

### Endpoint

```text
GET /products/search?name=<product-name>
```

### Example

```bash
curl "http://127.0.0.1:5000/products/search?name=almond%20milk"
```

---

## Import Product into Inventory

The application can retrieve product information from OpenFoodFacts and add it to the simulated inventory database.

### Endpoint

```text
POST /inventory/import
```

### Example

```bash
curl -X POST http://127.0.0.1:5000/inventory/import \
-H "Content-Type: application/json" \
-d '{
    "barcode": "<BARCODE>",
    "price": 500,
    "stock": 10
}'
```

The application:

1. Receives the barcode or product name.
2. Queries OpenFoodFacts.
3. Retrieves the product information.
4. Creates an inventory item.
5. Assigns a unique inventory ID.
6. Adds the item to the simulated inventory array.

---

# CLI Documentation

The CLI communicates with the Flask REST API using HTTP requests.

Make sure the Flask server is running before using the CLI.

---

## List Inventory

```bash
python cli.py list-items
```

Example output:

```text
ID: 1 | Product: Organic Almond Milk | Brand: Silk | Price: 450.0 | Stock: 20
ID: 2 | Product: Whole Grain Bread | Brand: Nature's Own | Price: 180.0 | Stock: 15
```

---

## Get One Inventory Item

```bash
python cli.py get-item --id 1
```

Example output:

```text
ID: 1
Product: Organic Almond Milk
Brand: Silk
Ingredients: Filtered water, almonds, cane sugar
Barcode: 0123456789012
Categories: Plant-based beverages
Quantity: 1 L
Price: 450.0
Stock: 20
```

---

## Add an Inventory Item

```bash
python cli.py add-item \
--product-name "Chocolate Milk" \
--brands "Test Brand" \
--barcode "9999999999999" \
--price 300 \
--stock 10
```

Optional information can also be supplied:

```bash
python cli.py add-item \
--product-name "Chocolate Milk" \
--brands "Test Brand" \
--barcode "9999999999999" \
--price 300 \
--stock 10 \
--ingredients "Milk, cocoa, sugar" \
--categories "Dairy beverages" \
--quantity "500 ml"
```

---

## Update an Inventory Item

Update price:

```bash
python cli.py update-item \
--id 1 \
--price 500
```

Update stock:

```bash
python cli.py update-item \
--id 1 \
--stock 25
```

Update both:

```bash
python cli.py update-item \
--id 1 \
--price 500 \
--stock 25
```

---

## Delete an Inventory Item

```bash
python cli.py delete-item --id 1
```

---

## Find Product by Barcode

```bash
python cli.py find-item \
--barcode "<BARCODE>"
```

---

## Find Product by Name

```bash
python cli.py find-item \
--name "almond milk"
```

---

## Import Product by Barcode

```bash
python cli.py import-item \
--barcode "<BARCODE>" \
--price 500 \
--stock 10
```

---

## Import Product by Name

```bash
python cli.py import-item \
--name "almond milk" \
--price 500 \
--stock 10
```

The import command retrieves product information from OpenFoodFacts and adds the product to the inventory.

---

# Web Interface

The project includes a simple browser-based interface.

Start Flask:

```bash
python app.py
```

Then open:

```text
http://127.0.0.1:5000
```

The interface provides a graphical way to interact with the inventory system.

The frontend communicates with the Flask API using JavaScript.

---

# Testing

The project uses `pytest` for automated testing.

External HTTP requests are mocked using `unittest.mock` so that tests do not depend on the availability of the OpenFoodFacts service.

## Run All Tests

```bash
pytest -v
```

The current test suite contains:

```text
33 passed
```

### Test Breakdown

| Test File              | Purpose                   |  Tests |
| ---------------------- | ------------------------- | -----: |
| `test_cli.py`          | CLI functionality         |     13 |
| `test_external_api.py` | OpenFoodFacts integration |      5 |
| `test_inventory.py`    | Inventory API and CRUD    |     15 |
| **Total**              |                           | **33** |

---

## Testing Coverage

### Inventory API

Tests cover:

* GET all inventory
* GET individual item
* GET nonexistent item
* POST inventory item
* POST with missing fields
* Duplicate barcode validation
* PATCH price
* PATCH stock
* PATCH nonexistent item
* Invalid price
* DELETE item
* DELETE nonexistent item

### CLI

Tests cover:

* List inventory
* Get inventory item
* Handle nonexistent item
* Add inventory item
* Update inventory item
* Delete inventory item
* Find product by barcode
* Find product by name
* External API failure
* Import product by barcode
* Import product by name
* Product not found
* Import API failure

### External API

Tests cover:

* Barcode lookup
* Product-name search
* Product not found
* API failure

---

# Error Handling

The application provides error handling for common problems.

Examples include:

* `400 Bad Request` for invalid input
* `404 Not Found` when an inventory item does not exist
* `404 Not Found` when a product cannot be found
* `409 Conflict` for duplicate barcodes
* `502 Bad Gateway` when OpenFoodFacts is unavailable
* Connection errors between the CLI and Flask API
* Invalid price values
* Invalid stock values
* Missing required fields

The CLI displays user-friendly error messages rather than exposing raw exceptions to users.

---

# Data Storage

For this summative lab, the application uses a Python list as simulated database storage.

Example:

```python
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
    }
]
```

Each inventory item contains a unique ID.

The structure resembles product information returned by OpenFoodFacts while also storing inventory-specific information such as:

* Price
* Stock
* Inventory ID

---

# API Architecture

The application follows a simple client-server architecture.

```text
                    ┌─────────────────────┐
                    │   Web Interface     │
                    │ HTML/CSS/JavaScript │
                    └──────────┬──────────┘
                               │
                               │ HTTP
                               ▼
┌─────────────────┐     ┌─────────────────────┐
│   CLI Client    │────▶│    Flask REST API   │
│    cli.py       │ HTTP│      app.py         │
└─────────────────┘     └──────────┬──────────┘
                                   │
                         ┌─────────┴─────────┐
                         │                   │
                         ▼                   ▼
                  Inventory Array     OpenFoodFacts
                  Simulated DB           API
```

---

# Git Workflow

Git is used for version control throughout development.

Feature development is performed on dedicated branches before being merged into the main branch.

Example workflow:

```bash
git checkout -b feature/flask-crud
```

Make changes and commit:

```bash
git add .
git commit -m "Implement inventory CRUD operations"
```

Push the feature branch:

```bash
git push origin feature/flask-crud
```

A pull request can then be created on GitHub and merged into `main` after testing.

Before merging, the test suite should pass:

```bash
pytest -v
```

---

# Project Requirements

This project was developed to satisfy the following requirements.

## Flask REST API

Implemented:

* GET `/inventory`
* GET `/inventory/<id>`
* POST `/inventory`
* PATCH `/inventory/<id>`
* DELETE `/inventory/<id>`

## External API

Implemented:

* OpenFoodFacts barcode lookup
* OpenFoodFacts product-name search
* Product import into inventory
* External API error handling

## CLI

Implemented:

* Add inventory item
* View inventory
* Update inventory
* Delete inventory
* Find product on OpenFoodFacts
* Import product from OpenFoodFacts

## Testing

Implemented:

* API endpoint tests
* CLI tests
* External API tests
* Mocked API responses
* Error-condition tests

## Documentation

Implemented:

* Installation instructions
* API documentation
* CLI documentation
* Project structure
* Testing instructions
* Error handling documentation

## Git Management

Implemented:

* Git repository
* Feature branch development
* Version-controlled changes
* Pull-request-based workflow

---

# Future Improvements

Although the current project satisfies the summative lab requirements, the following improvements could be added in a production environment:

* Replace the simulated array with a real database such as PostgreSQL or SQLite.
* Add authentication and administrator authorization.
* Add pagination for large inventories.
* Add inventory categories and filtering.
* Add low-stock notifications.
* Add product images from OpenFoodFacts.
* Add logging.
* Add environment-based configuration.
* Deploy the Flask API to a production server.
* Add API documentation using Swagger/OpenAPI.
* Add integration and end-to-end tests.
* Containerize the application using Docker.

---

# Author

**Calmax Omondi**

Python REST API — Inventory Management System


---

## License

This project was developed for educational purposes.

````