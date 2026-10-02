# inventory_manager.py
# Inventory Management System

from fileinput import filename
import json
import os

INVENTORY_FILE = "inventory.json"

DEFAULT_INVENTORY = [
    {"id": "P001", "name": "Laptop", "price": 1200.00, "stock": 15},
    {"id": "P002", "name": "Mouse", "price": 25.50, "stock": 40},
    {"id": "P003", "name": "Keyboard", "price": 45.00, "stock": 25},
]

if __name__ == "__main__":
    print(DEFAULT_INVENTORY)

def load_inventory(filename):
    """Loads inventory from a JSON file.
    If the file exists, loads and returns its contents.
    If it doesn't exist, starts with a default 3-product inventory
    and does not raise an error.
    """
    if os.path.exists(filename):
        print(f"{filename} found.")
        with open(filename, "r") as f:
            inventory = json.load(f)
        print("Inventory loaded successfully.")
        return inventory
    else:
        print(f"{filename} not found. Starting with a default inventory.")
        return [item.copy() for item in DEFAULT_INVENTORY]


if __name__ == "__main__":
    inventory = load_inventory(INVENTORY_FILE)
    print(inventory)

def find_product(inventory, product_id):
    """Helper: returns the product dict matching product_id, or None."""
    for product in inventory:
        if product["id"] == product_id:
            return product
    return None


def add_product(inventory):
    """Prompts for new product details and appends it to inventory."""
    print("\nAdd New Product")
    product_id = input("Product ID: ").strip()

    if find_product(inventory, product_id):
        print(f"Product ID {product_id} already exists. Add cancelled.")
        return

    name = input("Product Name: ").strip()

    try:
        price = float(input("Price: ").strip())
        stock = int(input("Stock Quantity: ").strip())
    except ValueError:
        print("Invalid price or stock quantity. Add cancelled.")
        return

    inventory.append({
        "id": product_id,
        "name": name,
        "price": price,
        "stock": stock,
    })
    print("\nProduct added successfully!")


def update_stock(inventory):
    """Prompts for a product ID and updates its stock quantity."""
    print("\nUpdate Stock")
    product_id = input("Enter Product ID: ").strip()
    product = find_product(inventory, product_id)

    if not product:
        print("\nProduct not found.")
        return

    print("\nProduct Found:")
    print(f"Name: {product['name']}")
    print(f"Current Stock: {product['stock']}")

    try:
        new_stock = int(input("\nNew Stock Quantity: ").strip())
    except ValueError:
        print("Invalid quantity. Update cancelled.")
        return

    product["stock"] = new_stock
    print("\nStock updated successfully!")


def search_product(inventory):
    """Prompts for a product ID and prints its details if found."""
    print("\nSearch Product")
    product_id = input("Enter Product ID: ").strip()
    product = find_product(inventory, product_id)

    if not product:
        print("\nProduct not found.")
        return

    print("\nProduct Found")
    print("-" * 40)
    print(f"ID: {product['id']}")
    print(f"Name: {product['name']}")
    print(f"Price: ${product['price']:.2f}")
    print(f"Stock: {product['stock']}")
    print("-" * 40)


def display_all(inventory):
    """Prints every product in the inventory as a formatted table."""
    print("\nCurrent Inventory")
    print("-" * 40)
    if not inventory:
        print("(No products in inventory.)")
    else:
        for product in inventory:
            print(f"ID: {product['id']} | Name: {product['name']} | "
                  f"Price: ${product['price']:.2f} | Stock: {product['stock']}")
    print("-" * 40)