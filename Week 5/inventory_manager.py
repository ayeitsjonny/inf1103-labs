# inventory_manager.py
# Inventory Management System
#
# Data representation:
#   inventory = [ {"id": "P001", "name": "Laptop", "price": 1200.00, "stock": 15}, ... ]
#   A list of dictionaries, one dictionary per product.
#
# Functions:
#   load_inventory(filename)              -> list (loaded or empty/default)
#   save_inventory(inventory, filename)   -> None (writes to disk)
#   add_product(inventory)                -> None (appends new product in place)
#   update_stock(inventory)               -> None (updates stock in place)
#   search_product(inventory)             -> None (prints matching product)
#   display_all(inventory)                -> None (prints full inventory table)

import json
import os

INVENTORY_FILE = "inventory.json"

DEFAULT_INVENTORY = [
    {"id": "P001", "name": "Laptop", "price": 1200.00, "stock": 15},
    {"id": "P002", "name": "Mouse", "price": 25.50, "stock": 40},
    {"id": "P003", "name": "Keyboard", "price": 45.00, "stock": 25},
]


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


def save_inventory(inventory, filename):
    """Saves the current inventory list to a JSON file."""
    print("Saving inventory...")
    with open(filename, "w") as f:
        json.dump(inventory, f, indent=4)
    print(f"Inventory saved successfully to {filename}.")


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


def print_menu():
    print("\n----------- MENU -----------")
    print("1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Save Inventory")
    print("6. Exit")
    print("-" * 28)


def main():
    print("=" * 50)
    print("INVENTORY MANAGEMENT SYSTEM")
    print("=" * 50)

    inventory = load_inventory(INVENTORY_FILE)

    while True:
        print_menu()
        choice = input("\nEnter option: ").strip()

        if choice == "1":
            display_all(inventory)
        elif choice == "2":
            add_product(inventory)
        elif choice == "3":
            update_stock(inventory)
        elif choice == "4":
            search_product(inventory)
        elif choice == "5":
            save_inventory(inventory, INVENTORY_FILE)
        elif choice == "6":
            print("\nSaving inventory before exit...")
            save_inventory(inventory, INVENTORY_FILE)
            print("\nThank you for using Inventory Management System.")
            print("Program terminated.")
            break
        else:
            print("\nInvalid option. Please choose 1-6.")


if __name__ == "__main__":
    main()